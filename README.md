# Instagram Image/Text Crawler

This tool allows you to crawl an Instagram account (e.g., your own) to download photos and captions, and organizes them into a structure that is easy to reuse.

## Features

- Downloads posts (images and metadata) from a public Instagram profile.
- Organizes downloads into a structured directory.
- Generates an `index.json` file containing captions, timestamps, and paths to images.

## Prerequisites

- Python 3.6+
- Internet connection

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the crawler script with the target username:

```bash
python src/crawler.py <username>
```

Optional arguments:
- `--count <number>`: Number of posts to download (default: 10).
- `--output <dir>`: Root directory for downloads (default: `downloads`).

Example:

```bash
python src/crawler.py my_username --count 50
```

## Output Structure

The crawler creates a directory structure as follows:

```
downloads/
  <username>/
    2023-10-27_12-00-00_UTC.jpg
    2023-10-27_12-00-00_UTC.json
    ...
    index.json
```

### index.json Structure

The `index.json` file contains a list of objects, each representing a post:

```json
[
    {
        "shortcode": "Cy123...",
        "timestamp": 1698408000,
        "date_str": "2023-10-27_12-00-00",
        "caption": "My awesome post caption...",
        "image_path": "downloads/username/2023-10-27_12-00-00_UTC.jpg"
    },
    ...
]
```

You can use this JSON file to easily load your content into other applications.

## Notes

- Accessing private profiles or downloading a large number of posts may require logging in. `instaloader` supports login, but this script is currently configured for public access or cached session usage.
- If you need to login, run `instaloader -l YOUR_USERNAME` from the command line once to create a session file.
