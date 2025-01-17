

BOT_NAME = "houzz"

SPIDER_MODULES = ["houzz.spiders"]
NEWSPIDER_MODULE = "houzz.spiders"

# USER_AGENT='Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36'


FEED_FORMAT = 'json'  # Set the output format to JSON
FEED_URI = 'output.json'  # Set the output file name (you can change 'output.json' to your preferred filename)



REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# ----------- OWN_SETTINGS --------------


# Manejo de downloaders con Playwright
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}


PLAYWRIGHT_BROWSER_TYPE = "chromium"  # O "firefox" o "webkit" o "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": False,
}

PLAYWRIGHT_CONTEXTS = {
    "default": {
        "viewport": {"width": 720, "height": 720},
    }
}


ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True

DEFAULT_REQUEST_HEADERS = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81",
                'Upgrade-Insecure-Requests': '1',
                'Connection': 'keep-alive'
            }

DOWNLOAD_DELAY = 5
# settings.py

LOG_FILE = 'scrapy_output.txt'
""" 
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 60
"""