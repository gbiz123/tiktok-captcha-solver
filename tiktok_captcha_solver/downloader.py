import requests
import base64

def download_image_b64(url: str) -> str:
    """Download an image from URL and return as base64 encoded string"""
    r = requests.get(url)
    return base64.b64encode(r.content).decode()
