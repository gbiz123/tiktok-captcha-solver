import logging
import tempfile
import os
import requests
from typing import Any

from selenium.webdriver import ChromeOptions
import undetected_chromedriver as uc
from playwright import sync_api
from playwright import async_api

LOGGER = logging.getLogger(__name__)
SCRIPT_JS_URL = "https://raw.githubusercontent.com/gbiz123/sadcaptcha-chrome-extensino/refs/heads/master/script.js"

def download_script_js() -> str:
    """Download the latest script.js file from GitHub and return its content."""
    response = requests.get(SCRIPT_JS_URL)
    response.raise_for_status()  # Raise exception if download fails
    LOGGER.debug("Downloaded script.js from GitHub")
    return response.text

def make_undetected_chromedriver_solver(
    api_key: str,
    options: ChromeOptions | None = None,
    **uc_chrome_kwargs
) -> uc.Chrome:
    """Create an undetected chromedriver with SadCaptcha script injected."""
    if options is None:
        options = ChromeOptions()
    
    # Download and patch the script
    script_content = download_script_js()
    patched_script = patch_extension_script_with_key(script_content, api_key)
    
    # Launch Chrome
    chrome = uc.Chrome(options=options, **uc_chrome_kwargs)
    
    # Set up a listener to inject the script on each page load
    chrome.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': patched_script
    })
    
    LOGGER.debug("Created undetected chromedriver with SadCaptcha script")
    return chrome

def make_playwright_solver_context(
    playwright: sync_api.Playwright,
    api_key: str,
    user_data_dir: str | None = None,
    **playwright_context_kwargs
) -> sync_api.BrowserContext:
    """Create a playwright context with SadCaptcha script injected on each page."""
    if user_data_dir is None:
        user_data_dir_tempdir = tempfile.TemporaryDirectory()
        user_data_dir = user_data_dir_tempdir.name
    
    # Add common browser arguments
    if "args" not in playwright_context_kwargs:
        playwright_context_kwargs["args"] = [
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',         
            '--disable-web-security',
            '--disable-infobars',  
            '--start-maximized',  
        ]
    
    # Launch browser context
    ctx = playwright.chromium.launch_persistent_context(
        user_data_dir,
        **playwright_context_kwargs
    )
    
    # Download and patch the script
    script_content = download_script_js()
    patched_script = patch_extension_script_with_key(script_content, api_key)
    
    # Set up event listener to inject the script on each new page
    ctx.on("page", lambda page: _inject_script_to_page(page, patched_script))
    
    LOGGER.debug("Created patched playwright context")
    return ctx

async def make_async_playwright_solver_context(
    async_playwright: async_api.Playwright,
    api_key: str,
    user_data_dir: str | None = None,
    **playwright_context_kwargs
) -> async_api.BrowserContext:
    """Create an async playwright context with SadCaptcha script injected on each page."""
    if user_data_dir is None:
        user_data_dir_tempdir = tempfile.TemporaryDirectory()
        user_data_dir = user_data_dir_tempdir.name
    
    # Add common browser arguments
    if "args" not in playwright_context_kwargs:
        playwright_context_kwargs["args"] = [
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',         
            '--disable-web-security',
            '--disable-infobars',  
            '--start-maximized',  
        ]
    
    # Launch browser context
    ctx = await async_playwright.chromium.launch_persistent_context(
        user_data_dir,
        **playwright_context_kwargs
    )
    
    # Download and patch the script
    script_content = download_script_js()
    patched_script = patch_extension_script_with_key(script_content, api_key)
    
    # Set up event listener to inject the script on each new page
    ctx.on("page", lambda page: _inject_async_script_to_page(page, patched_script))
    
    LOGGER.debug("Created patched async playwright context")
    return ctx

def _inject_script_to_page(page: sync_api.Page, script: str) -> None:
    """Inject script to a Playwright page."""
    page.on("load", lambda: page.evaluate(script))
    LOGGER.debug("Set up script injection for page")

async def _inject_async_script_to_page(page: async_api.Page, script: str) -> None:
    """Inject script to an async Playwright page."""
    page.on("load", lambda: page.evaluate(script))
    LOGGER.debug("Set up async script injection for page")

def patch_extension_script_with_key(script: str, api_key: str) -> str:
    """Patch the script with the user's API key."""
    script = script.replace("localStorage.getItem(\"sadCaptchaKey\");", f"\"{api_key}\";")
    LOGGER.debug("Patched script with API key")
    return script
