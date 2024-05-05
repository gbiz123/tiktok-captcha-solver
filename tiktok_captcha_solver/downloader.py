import requests
import base64
import tempfile

def download_image_b64(url: str) -> str:
    """Download an image from URL and return as base64 encoded string"""
    with tempfile.SpooledTemporaryFile(max_size=int(10e9), mode="wb") as tmp:
        tmp.write(requests.get(url).content)
        return base64.b64encode(tmp.read()).decode()
