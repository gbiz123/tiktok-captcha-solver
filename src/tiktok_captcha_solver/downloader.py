import requests
import base64

from undetected_chromedriver import logging

def download_image_b64(url: str) -> str:
    """Download an image from URL and return as base64 encoded string"""
    r = requests.get(url)
    image = base64.b64encode(r.content).decode()
    logging.debug(f"Got image from {url} as B64: {image[0:20]}...")
    return image
