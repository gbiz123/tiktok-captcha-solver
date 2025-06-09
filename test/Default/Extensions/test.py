import os
from os.path import isdir
import shutil
from playwright.sync_api import ProxySettings, sync_playwright, Playwright
from playwright_stealth import stealth_sync, StealthConfig

path_to_extension = "./"
user_data_dir = "/tmp/test-user-data-dir"

if os.path.isdir(user_data_dir):
    shutil.rmtree(user_data_dir)

def run(playwright: Playwright):

    proxy = ProxySettings(server="216.173.104.197:6334")
    proxy = None

    context = playwright.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        proxy=proxy,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/131.0.2903.86",
        args=[
            f"--disable-extensions-except={path_to_extension}",
            f"--load-extension={path_to_extension}",
        ],
    )

    page = context.new_page()
    config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
    stealth_sync(page, config=config)

    input("trigger the captcha")

    # Test the background page as you would any other page.
    context.close()


with sync_playwright() as playwright:
    run(playwright)
