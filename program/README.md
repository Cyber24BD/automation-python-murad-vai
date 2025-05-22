# G2G Account Scraper

A Selenium-based web automation tool for G2G marketplace.

## ⚠️ Important Warning
**DISCLAIMER**: This script is for educational purposes only. The creator is not responsible for any account bans or other consequences resulting from the use of this script. Use at your own risk. If the website bans your account, the creator will not be held responsible.

## 🚀 Features

- Manual login to G2G
- Automated interactions with G2G marketplace
- Configurable settings
- Headless mode support
- Screenshot capture on error

## 🛠️ Prerequisites

- Python 3.8+
- Google Chrome browser installed
- ChromeDriver (automatically handled by webdriver-manager)
- G2G Account with valid credentials
- Stable internet connection

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd selenium
   ```

2. Create and activate a virtual environment:
   ```bash
   uv venv
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies using uv:
   ```bash
   uv pip install -r requirements.txt
   ```

## 📁 Project Structure

```
selenium/
├── .venv/              # Virtual environment
├── data/               # Data directory
│   ├── output/         # Output files
│   └── screenshots/    # Screenshots of errors
├── main.py             # Main script
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## 🚀 Running the Script

1. **Run the script**:
   ```bash
   uv run main.py
   ```

2. **Headless Mode** (no browser UI):
   ```bash
   uv run main.py --headless
   ```

## ⚙️ Configuration

1. **Manual Login**:
   - The script will open a browser window where you need to manually log in to your G2G account
   - After successful login, the script will continue with the automation

2. **Environment Variables** (optional, in `.env` file):
   ```
   HEADLESS=False  # Set to True to run in headless mode
   DELAY=2         # Delay between actions (seconds)
   ```

## 📄 License

**PRIVATE LICENSE**

This software is the private property of Cyber24BD. Unauthorized copying, distribution, modification, public display, or public performance of this software is strictly prohibited.

All rights reserved. No part of this software may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the copyright holder.

## 📧 Contact

- **Creator**: Abid Shariar Sakib
- **Company**: Cyber24BD
- **Support Email**: abidsakib28@gmail.com

## 🙏 Acknowledgments

- Built with [Selenium WebDriver](https://www.selenium.dev/)
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) for browser driver management
