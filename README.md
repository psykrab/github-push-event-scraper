# GitHub Push Events Scraper

[![Apify Actor](https://badgen.net/badge/Apify%20Store/View%20Actor/ffdd00?icon=apify)](https://apify.com/krab/github-push-event-scraper)

Extracts detailed GitHub push events and their associated commit data for any public repository. This Actor allows you to monitor repository activity, track user contributions, or gather data for analysis by specifying a date range.

The scraper is designed for performance and a great user experience:

- **⚡️ Direct & Fresh**: Your stream begins in about a minute, fetching data directly from the source.
- **📡 Continuous Live Feed**: Progressively fetches data as the stream runs, ideal for continuous monitoring.
- **🔧 Customizable Output**: Select only the fields you need in the output.

## Input Parameters

The Actor requires the following input:

| Field        | Type           | Description                                                                                                                |
| ------------ | -------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `start_date` | Date           | **Required.** The first date to scrape data from, in `YYYY-MM-DD` format.                                                  |
| `end_date`   | Date           | **Optional.** The last date to scrape data from. If left blank, data will be scraped up to the most recent available hour. |
| `fields`     | Checkbox Group | **Optional.** Select the fields you want to include in the output. By default, all fields are selected.                    |

## Output Data

The Actor returns a dataset of GitHub push events. Each item in the dataset is a JSON object containing the fields you selected.

Here is an example of a single output record with all fields selected:

```json
{
  "PushId": 1234567890,
  "PushTimeStamp": "2025-07-28T10:30:00Z",
  "CommitMessage": "feat: Implement new user authentication flow",
  "WebCommitUrl": "https://github.com/user/repo/commit/a1b2c3d4e5f6",
  "CommitAuthorName": "Jane Doe",
  "CommitEmail": "jane.doe@example.com",
  "UserLogin": "janedoe",
  "UserEmail": "jane.doe@users.noreply.github.com",
  "WebUserUrl": "https://github.com/janedoe",
  "WebRepoUrl": "https://github.com/user/repo"
}
```

## Support

Find a bug or have a suggestion? Let me know!

API call for caffeine -> <a href="https://buymeacoffee.com/krab" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Fuel the dev" width="108" height="30"></a>
