import logging
from typing import Any
from playwright.sync_api import Page as SyncPage
from playwright.async_api import Page as AsyncPage
import requests
import base64

from selenium.webdriver.chrome.webdriver import WebDriver


def fetch_image_b64(
        url: str,
        driver: WebDriver | None = None,
        sync_page: SyncPage | None = None,
        headers: dict[str, Any] | None = None,
        proxy: str | None = None
    ) -> str:
    """Fetch an image from URL and return as base64 encoded string

    If just the URL is passed, it will be feched with python requests.
    If driver is passed, chromedriver will be used to evaluate javascript to download from blob
    If sync_page is passed, sync playwright will be used to evaluate javascript to download from blob
    """
    if not any([sync_page, driver]):
        logging.debug(f"fetching {url} with requests")
        if proxy:
            proxies = {"http": proxy, "https": proxy}
        else:
            proxies = None
        r = requests.get(url, headers=headers, proxies=proxies)
        image = base64.b64encode(r.content).decode()
        logging.debug(f"Got image from {url} as B64: {image[0:20]}...")
        return image
    if driver:
        logging.debug(f"fetching {url} with selenium script execute")
        return driver.execute_script(_make_selenium_fetch_image_code(url))
    if sync_page: 
        logging.debug(f"fetching {url} with sync playwright javascript evaluate")
        return sync_page.evaluate(_make_playwright_fetch_image_code(url))

async def fetch_image_b64_async_page(url: str, async_page: AsyncPage) -> str:
    logging.debug(f"fetching {url} with async playwright javascript evaluate")
    return await async_page.evaluate(_make_playwright_fetch_image_code(url))

def _make_playwright_fetch_image_code(image_source: str) -> str:
        """prepare javascript on page to fetch image from blob url.
        This is necessary because you can't fetch a blob with requests."""
        return """async () => {
                function getBase64StringFromDataURL(dataUrl){
                    return dataUrl.replace('data:', '').replace(/^.+,/, '')
                }
                async function fetchImageBase64(imageSource) {
                    let res = await fetch(imageSource)
                    let img = await res.blob()
                    let reader = new FileReader()
                    reader.readAsDataURL(img)
                    return new Promise(resolve => {
                        reader.onloadend = () => {
                            resolve(getBase64StringFromDataURL(reader.result))
                        }
                    })
                }
                let imgB64 = await fetchImageBase64([IMAGE_SOURCE]);
                return getBase64StringFromDataURL(imgB64);
            }
        """.replace("[IMAGE_SOURCE]", f"\"{image_source}\"")

def _make_selenium_fetch_image_code(image_source: str) -> str:
        """prepare javascript on page to fetch image from blob url.
        This is necessary because you can't fetch a blob with requests."""
        return """function getBase64StringFromDataURL(dataUrl){
                return dataUrl.replace('data:', '').replace(/^.+,/, '')
            }
            async function fetchImageBase64(imageSource) {
                let res = await fetch(imageSource)
                let img = await res.blob()
                let reader = new FileReader()
                reader.readAsDataURL(img)
                return new Promise(resolve => {
                    reader.onloadend = () => {
                        resolve(getBase64StringFromDataURL(reader.result))
                    }
                })
            }
            let imgB64 = await fetchImageBase64([IMAGE_SOURCE]);
            return getBase64StringFromDataURL(imgB64);
        """.replace("[IMAGE_SOURCE]", f"\"{image_source}\"")
