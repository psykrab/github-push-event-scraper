# src/main.py

import os
import json
import requests
from apify import Actor

async def main():
    """
    Main function for the Apify Actor.
    Connects to the backend API and streams GitHub data into the Actor's dataset.
    """
    async with Actor:
        Actor.log.info("Actor run started.")

        # 1. Get and validate user input from the INPUT_SCHEMA
        actor_input = await Actor.get_input() or {}
        start_date = actor_input.get("start_date")
        end_date = actor_input.get("end_date")  # Can be None

        # Get the list of selected fields directly from the input
        fields = actor_input.get("output_fields", [])

        if not start_date:
            await Actor.fail(status_message="Input error: 'start_date' is a required field.")
            return

        # 2. Get API configuration and metadata from environment variables
        # These must be set in the Actor's secret environment variables on the Apify platform.
        api_host = os.getenv("API_HOST")
        api_key = os.getenv("API_KEY")

        if not api_host or not api_key:
            message = "Configuration error: API_HOST or API_KEY is not set in the Actor's environment variables."
            await Actor.fail(status_message=message)
            return

        # 3. Prepare the request to the backend API
        stream_url = f"{api_host}/scripts/stream-gharchive"

        params = {
            "start_date": start_date,
            "end_date": end_date,
            "fields": fields,
            # Pass Apify metadata to the backend for logging and session management
            "actor_run_id": os.getenv("APIFY_ACTOR_RUN_ID"),
            "user_id": os.getenv("APIFY_USER_ID"),
            "actor_id": os.getenv("APIFY_ACTOR_ID"),
        }
        # Filter out None or empty values from params to keep the URL clean
        params = {k: v for k, v in params.items() if v}

        headers = {
            "X-API-Key": api_key
        }

        Actor.log.info(f"Connecting to data stream for dates: {start_date} to {end_date or 'latest'}...")

        # 4. Connect to the stream and process the data
        record_count = 0
        try:
            # Set a long timeout for potentially long-running streams
            with requests.get(stream_url, params=params, headers=headers, stream=True, timeout=7200) as response:
                response.raise_for_status()  # Will raise an exception for HTTP errors (4xx, 5xx)

                for line in response.iter_lines(decode_unicode=True):
                    if not line.strip():
                        continue

                    try:
                        data = json.loads(line)

                        # Handle status messages from the backend
                        if data.get("status") in ["info", "waiting", "error"]:
                            message = f"[API Status] {data.get('message')}"
                            if data.get("status") == "error":
                                Actor.log.error(message)
                                # If the backend reports a fatal error, fail the Actor run
                                await Actor.fail(status_message=f"Backend error: {data.get('message')}")
                                return
                            else:
                                # For "info" and "waiting" statuses
                                Actor.log.info(message)
                        else:
                            # This is a data record, push it to the dataset
                            await Actor.push_data(data)
                            record_count += 1
                            if record_count % 200 == 0:
                                Actor.log.info(f"Successfully pushed {record_count} records...")

                    except json.JSONDecodeError:
                        Actor.log.warning(f"Received a non-JSON line from stream: {line}")

            Actor.log.info(f"Stream finished. Total records pushed: {record_count}")

        except requests.exceptions.RequestException as e:
            error_message = f"Failed to connect or stream from the API: {e}"
            Actor.log.exception(error_message)
            await Actor.fail(status_message=error_message)
        except Exception as e:
            error_message = f"An unexpected error occurred during streaming: {e}"
            Actor.log.exception(error_message)
            await Actor.fail(status_message=error_message)