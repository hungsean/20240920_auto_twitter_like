# Selenium Image Downloader

A Python-based automation tool using Selenium to download images from a specified website. The tool saves session cookies, manages downloaded media data in a SQLite database, and logs all activities for easy monitoring.

## Table of Contents

- [Selenium Image Downloader](#selenium-image-downloader)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Set Up Virtual Environment](#2-set-up-virtual-environment)
    - [3. Install Dependencies](#3-install-dependencies)
    - [4. Install ChromeDriver](#4-install-chromedriver)
  - [Configuration](#configuration)
    - [Environment Variables](#environment-variables)
      - [`.env` File](#env-file)
  - [Usage](#usage)
    - [1. Save Cookies](#1-save-cookies)
    - [2. Run the Main Script](#2-run-the-main-script)
  - [Troubleshooting](#troubleshooting)
  - [License](#license)

## Features

- **Session Management**: Save and load session cookies to maintain authenticated sessions.
- **Automated Image Downloads**: Scrape and download images based on specific criteria.
- **Database Integration**: Store metadata of downloaded images in a SQLite database to avoid duplicates.
- **Comprehensive Logging**: Logs all activities to both console and log files for easy monitoring and debugging.
- **Configurable Settings**: Easily adjust paths and settings via environment variables to suit different environments.

## Prerequisites

- **Operating System**: Windows
- **Python**: Version 3.7 or higher
- **Google Chrome**: Installed on your system

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/hungsean/20240920_auto_twitter_like.git .
```

### 2. Set Up Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv .venv
```

Activate the virtual environment:

- **Command Prompt:**

  ```bash
  .venv\Scripts\activate
  ```

- **PowerShell:**

  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

### 3. Install Dependencies

Ensure you have `pip` installed and up to date.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install ChromeDriver

please download from [here](https://googlechromelabs.github.io/chrome-for-testing/)

---

## Configuration

### Environment Variables

All configurable paths and settings are managed via environment variables. You can set these variables in a `.env` file located in the project's root directory.

#### `.env` File

Create a `.env` file and add the following configurations:

```dotenv
# Path to the ChromeDriver executable
CHROMEDRIVER_PATH=chromedriver-win64/chromedriver.exe

# URL of the target website
TARGET_URL=https://x.com/home

# Path to save cookies
COOKIES_FILE=cookies.pkl

# Path to the SQLite database
MEDIA_DB_PATH=databases/media_data.db

# Directory to save downloaded images
IMAGES_DIR=images_png

# URL of the likes page
LIKES_URL=https://x.com/youname/likes

# Directory for logs
LOGS_DIR=logs
```

**Note:** Adjust the values according to your setup.

---

## Usage

### 1. Save Cookies

Before running the main automation script, you need to save your session cookies.

```bash
python save_cookies.py
```

**Steps:**

1. The script will open the target website specified in the `.env` file.
2. Perform any manual login or actions required.
3. Once completed, return to the terminal and press **Enter** to save the cookies.
4. Cookies will be saved to the file specified by `COOKIES_FILE` in the `.env` file.

### 2. Run the Main Script

After saving the cookies, run the main automation script to start downloading images.

```bash
python main_withlog.py
```

**Functionality:**

- Loads the saved cookies to maintain the session.
- Navigates to the specified likes page.
- Continuously scrapes and downloads images based on defined criteria.
- Logs all activities to both console and log files.

---
<!--
## Automating Initialization

To streamline the setup process, you can create a Windows batch script (`setup.bat`) that automates the activation of the virtual environment and runs the necessary scripts.

**Example `setup.bat`:**

```batch
@echo off
REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

REM Run the save_cookies script
python save_cookies.py

REM Run the main automation script
python main_withlog.py

REM Pause the script to keep the window open
pause
```

**Usage:**

1. Double-click `setup.bat` or run it via Command Prompt.
2. The script will activate the virtual environment, install dependencies, prompt you to save cookies, and then start the main automation process.

-->

---

## Troubleshooting

- **ChromeDriver Version Mismatch:**
  Ensure that the ChromeDriver version matches your installed Google Chrome version. Mismatched versions can lead to errors.

- **Environment Variables Not Loaded:**
  Make sure the `.env` file is correctly formatted and located in the project's root directory.

- **Permissions Issues:**
  Run your Command Prompt or PowerShell as an administrator to avoid permission-related issues.

- **Missing Dependencies:**
  Ensure all dependencies are installed by verifying the `requirements.txt` installation step.

---

## License

[MIT](LICENSE)
