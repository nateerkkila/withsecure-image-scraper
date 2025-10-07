# Image Scraper

A Python command-line tool to fetch and download all static images from a given webpage.

## Features

- Fetches all `<img>` and `<source>` URLs from a webpage via src and srcset attributes.
- Handles both relative and absolute image paths.
- Downloads images to a local directory.
- Creates a log file (`image_log.txt`) of all successfully fetched URLs.
- Includes a test suite using `pytest`.

## Assumptions

1.  **Image Sources:** The scraper only targets `<img>` and `<source>` tags. It does not parse CSS or JavaScript or Lazy Loaded images.
2.  **URL Handling:** The tool resolves relative URLs but ignores non-downloadable `data:` URIs.
3.  **Output:** Downloads are saved to a `./downloaded_images/` directory by default, which is created if it does not exist.
4.  **Error Handling:** The tool skips images that fail to download due to network or file system errors and continues processing the rest.
5.  **Environment:** This tool has been developed and tested on a Linux-based environment. While the code uses cross-platform libraries, its behavior is only guaranteed on Linux.

## Setup & Installation

**Prerequisites:**
- Python 3.13+
- `pipenv`

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/withsecure-image-scraper.git
    cd withsecure-image-scraper
    ```

2.  **Install dependencies:**
    Use `pipenv` to create a virtual environment and install all packages.
    ```bash
    pipenv install --dev
    ```

3.  **Activate the virtual environment:**
    ```bash
    pipenv shell
    ```

## Usage

Run the tool from the project's root directory. A URL is a required argument.

#### **Basic Usage**

Downloads images to the default `./downloaded_images/` directory.

```bash
python -m image_scraper.main https://www.python.org/
```

#### **Specify an Output Directory**

Use the `-o` or `--output` flag to set a custom download location.

```bash
python -m image_scraper.main https://www.google.com/ -o google_images
```

## Testing

The project uses `pytest` for unit testing. The tests mock all network and file system interactions to ensure reliability and speed.

To run the full test suite, execute the following command from the project's root directory:

```bash
pytest
```