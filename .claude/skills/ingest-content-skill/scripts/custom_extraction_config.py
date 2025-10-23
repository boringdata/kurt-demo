"""
Custom Extraction Configuration

Use custom trafilatura settings for extraction timeout, minimum size, etc.

Trafilatura Documentation:
- Extraction Settings: https://trafilatura.readthedocs.io/en/latest/corefunctions.html#extraction-settings
- Configuration Options: https://trafilatura.readthedocs.io/en/latest/corefunctions.html#options
- Settings Module: https://trafilatura.readthedocs.io/en/latest/corefunctions.html#settings
"""

import trafilatura
from trafilatura.settings import use_config

# Configure custom settings
config = use_config()
config.set("DEFAULT", "EXTRACTION_TIMEOUT", "30")
config.set("DEFAULT", "MIN_EXTRACTED_SIZE", "200")

# Download and extract with custom config
url = "https://example.com/page"
downloaded = trafilatura.fetch_url(url)

content = trafilatura.extract(
    downloaded,
    config=config,
    output_format='markdown'
)

print(content)
