# G2G Account Scraper

A Selenium-based web scraper designed to extract account information from G2G marketplace.

## 🚀 Features

- Automated login to G2G
- Scraping of account details
- Configurable target URLs
- Headless mode support
- Data export to JSON/CSV
- Screenshot capture on error
- Proxy support (optional)

## 🛠️ Prerequisites

- Python 3.8+
- Google Chrome browser installed
- ChromeDriver (automatically handled by webdriver-manager)
- G2G Seller Account with valid credentials
- 2FA disabled (recommended) or configured for automation
- Stable internet connection
- Sufficient permissions to install Python packages

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd g2g-scraper
   ```

2. Create and activate a virtual environment:
   ```bash
   uv venv
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   uv sync
   # or
   uv pip install -r requirements.txt
   ```

4. You have to login before using the script with your G2G credentials:
   ```
   G2G_EMAIL=your_email@example.com
   G2G_PASSWORD=your_secure_password
   G2G_2FA=your_2fa_code
   ```

   ⚠️ **Security Note**: Add `.env` to your `.gitignore` to prevent committing sensitive information.
   

## 📁 Project Structure

```
g2g-scraper/
├── config/
│   ├── __init__.py
│   └── settings.py        # Configuration settings
├── data/
│   ├── input/            # Input files (CSV/JSON if needed)
│   ├── output/           # Scraped data output
│   └── screenshots/      # Screenshots of errors
├── src/
│   ├── pages/           # Page object classes
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   └── account_page.py
│   ├── utils/            # Helper functions
│   │   ├── browser.py    # Browser setup
│   │   ├── logger.py     # Logging configuration
│   │   └── helpers.py    # Common utilities
│   └── main.py           # Main script
├── .env.example          # Example environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## 🏗️ Project Overview

### Key Features
- **Automated Login**: Handles G2G login with session management
- **Configurable Scraping**: Easily modify target URLs and selectors
- **Error Handling**: Robust error handling with retry mechanism
- **Headless Mode**: Run without GUI for server deployment
- **Data Export**: Save scraped data in multiple formats

### Important Notes
- Respect G2G's Terms of Service and rate limits
- Use appropriate delays between requests
- Consider using proxies for large-scale scraping
- The script includes random delays to mimic human behavior

## 🚀 Running the Scraper

1. **Basic Usage**:
   ```bash
   python src/main.py
   ```

2. **With Custom URL**:
   ```bash
   python src/main.py --url "https://www.g2g.com/your-target-url"
   ```

3. **Headless Mode** (no browser UI):
   ```bash
   python src/main.py --headless
   ```

4. **Using a Proxy**:
   ```bash
   python src/main.py --proxy "http://user:pass@ip:port"
   ```

5. **View Help**:
   ```bash
   python src/main.py --help
   ```

## ⚙️ Configuration

1. **Environment Variables** (`.env`):
   ```
   G2G_EMAIL=your_email@example.com
   G2G_PASSWORD=your_secure_password
   HEADLESS=False  # Set to True for server use
   DELAY=2         # Delay between actions (seconds)
   ```

2. **Settings** (`config/settings.py`):
   ```python
   # Browser settings
   BROWSER = "chrome"
   WINDOW_SIZE = "1920,1080"
   
   # Scraping settings
   MAX_RETRIES = 3
   TIMEOUT = 30  # seconds
   
   # Output settings
   OUTPUT_FORMAT = "json"  # or 'csv'
   SAVE_SCREENSHOTS = True
   ```

## 📊 Output

Scraped data is saved in the `data/output/` directory with timestamps:
```
data/output/
├── accounts_20230515_123456.json
├── accounts_20230515_123456.csv
└── screenshots/
    └── error_20230515_123456.png
```

Logs are stored in the root directory:
- `scraper.log` - Detailed execution logs
- `errors.log` - Error-specific logs

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Selenium WebDriver](https://www.selenium.dev/)
- [Pytest](https://docs.pytest.org/) for test framework
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) for browser driver management
