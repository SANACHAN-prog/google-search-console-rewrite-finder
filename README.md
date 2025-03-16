# google-search-console-rewrite-finder

A Python tool that analyzes Google Search Console data to identify content requiring rewrites based on search performance metrics. It helps content managers efficiently identify pages that rank well but have low CTR.

## Features

- Bulk retrieval of `page` and `query` relationships from Google Search Console
- Automatic identification of rewrite candidates based on:
  - Search position (top 10 rankings)
  - Impressions (100+ views)
  - CTR (below 3%)
- Excel report generation with:
  - Easy-to-read formatting
  - Japanese text support
  - Rewrite recommendation markers

## Prerequisites

- Python 3.8+
- Google Cloud Platform account
- Google Search Console access
- Required Python packages:
  ```
  pandas
  openpyxl
  google-api-python-client
  oauth2client
  ```

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/SANACHAN-prog/google-search-console-rewrite-finder.git
   cd google-search-console-rewrite-finder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Cloud Platform:
   - Create a project
   - Enable Google Search Console API
   - Create a service account
   - Download the key file as key_file.json

4. Configure Search Console:
   - Add your service account to your Search Console property
   - Grant necessary permissions

For setup of GCP and Search Console, please also refer to: [https://progzakki.sanachan.com/develop-software/environment/setup-gcp-for-search-console-api/](https://progzakki.sanachan.com/develop-software/environment/setup-gcp-for-search-console-api/)

## Usage

1. Place your `key_file.json` in the project root directory

2. Update the configuration in `main.py`:
   ````python
   API_MAX_ROWS = 1000
   (snip)
   SITE_URL = 'https://your-site.com/'
   PERIOD_DAYS = 90
   ```

3. Run the script:
   ```bash
   python main.py
   ```

The script will generate an Excel file with:
- URL and query relationships
- Performance metrics
- Rewrite recommendations

## Output Format

The Excel report includes:
- Query
- URL
- Clicks
- Impressions
- CTR
- Position
- Rewrite recommendation marker (*)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
