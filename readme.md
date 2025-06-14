# Selenium Automation Project

This project automates various web interactions using Selenium WebDriver. It includes functionalities for handling dropdowns, media items, forms, and pagination. The project is designed to be modular and easily extendable.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Changelog](#changelog)

## Features

- **Dropdown Handling**: Open, close, and select values from dropdowns.
- **Media Handling**: Add media items based on a provided dictionary.
- **Form Handling**: Set title, description, price, and other form fields.
- **Pagination**: Loop through pages and perform operations on each page.
- **Deletion**: Select and delete rows based on specific criteria.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Cyber24BD/automation-python-murad-vai
    cd automation-python-murad-vai
    ```

2. Install the required dependencies:
    ```sh
    uv pip install -r requirements.txt
    ```

3. Ensure you have the ChromeDriver installed and accessible in your PATH.

## Usage

1. Configure the necessary settings in `config.py`.

2. Run the main script:
    ```sh
    uv run main.py
    ```

## Configuration

Update the `config.py` file with your specific settings:

```python
# config.py
selenium_web_driver_path = "path_to_your_webdriver"
after_post_sleep_timer = 10
after_per_post_sleep_timer = 5
account_url = "your_account_url"
delete_url = "your_delete_url"
chrome_user_data_dir = r"your_chrome_user_data_dir"