from typing import Any
import requests
import base64

from undetected_chromedriver import logging

def fetch_image_b64(url: str, headers: dict[str, Any] | None = None, proxy: str | None = None) -> str:
    """Fetch an image from URL and return as base64 encoded string"""
    if proxy:
        proxies = {"http": proxy, "https": proxy}
    else:
        proxies = None
    r = requests.get(url, headers=headers, proxies=proxies)
    image = base64.b64encode(r.content).decode()
    logging.debug(f"Got image from {url} as B64: {image[0:20]}...")
    return image
