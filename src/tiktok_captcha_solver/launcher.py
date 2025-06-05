import logging
import tempfile
from typing import Any
import io
import os
import zipfile
import requests

from selenium.webdriver import ChromeOptions
from selenium import webdriver
import undetected_chromedriver as uc
import nodriver

from playwright import sync_api
from playwright import async_api

LOGGER = logging.getLogger(__name__)

async def make_nodriver_solver(
    api_key: str,
    **nodriver_start_kwargs
) -> nodriver.Browser:
    """Create a nodriver Browser patched with SadCaptcha.
    
    Args:
        api_key (str): SadCaptcha API key
        nodriver_start_args: Keyword arguments for nodriver.start()
    """
    ext_dir = download_extension_to_unpacked()
    _patch_extension_file_with_key(ext_dir.name, api_key)
    load_extension_argument = f'--load-extension={ext_dir.name}'
    disable_extensions_except_argument = f'--disable-extensions-except-{ext_dir.name}'
    browser_args = nodriver_start_kwargs.get("browser_args")
    if isinstance(browser_args, list):
        nodriver_start_kwargs["browser_args"].append(load_extension_argument)
        nodriver_start_kwargs["browser_args"].append(disable_extensions_except_argument)
        LOGGER.debug("Appended add extension argument to browser args: " + load_extension_argument)
        LOGGER.debug("Appended add extension argument to browser args: " + disable_extensions_except_argument)
    else:
        nodriver_start_kwargs["browser_args"] = [load_extension_argument, disable_extensions_except_argument]
        LOGGER.debug("Set browser arg to " + load_extension_argument)
    chrome = await nodriver.start(**nodriver_start_kwargs)
    LOGGER.debug("created new nodriver Browser patched with sadcaptcha")
    return chrome

def make_selenium_solver(
    api_key: str,
    options: ChromeOptions | None = None,
    no_warn: bool = False,
    **webdriver_chrome_kwargs
) -> uc.Chrome:
    """Create an selenium chromedriver patched with SadCaptcha.
    
    Args:
        api_key (str): SadCaptcha API key
        options (ChromeOptions | None): Options to launch webdriver.Chrome with
        webdriver_chrome_kwargs: keyword arguments for call to webdriver.Chrome
    """
    if not no_warn:
        LOGGER.warning("Selenium, playwright, and undetected chromedriver are no longer recommended for scraping. A better option is to use nodriver. To use nodriver, use the command 'make_nodriver_solver()' instead. To disable this warning, set the kwarg no_warn=True.")
    if options is None:
        options = ChromeOptions()
    ext_dir = download_extension_to_unpacked()
    _patch_extension_file_with_key(ext_dir.name, api_key)
    options.add_argument(f'--load-extension={ext_dir.name}')
    chrome = webdriver.Chrome(options=options, **webdriver_chrome_kwargs)
    LOGGER.debug("created new undetected chromedriver patched with sadcaptcha")
    return chrome

def make_undetected_chromedriver_solver(
    api_key: str,
    options: ChromeOptions | None = None,
    no_warn: bool = False,
    **uc_chrome_kwargs
) -> uc.Chrome:
    """Create an undetected chromedriver patched with SadCaptcha.
    
    Args:
        api_key (str): SadCaptcha API key
        options (ChromeOptions | None): Options to launch uc.Chrome with
        uc_chrome_kwargs: keyword arguments for call to uc.Chrome
    """
    if not no_warn:
        LOGGER.warning("Selenium, playwright, and undetected chromedriver are no longer recommended for scraping. A better option is to use nodriver. To use nodriver, use the command 'make_nodriver_solver()' instead. To disable this warning, set the kwarg no_warn=True.")
    if options is None:
        options = ChromeOptions()
    ext_dir = download_extension_to_unpacked()
    _patch_extension_file_with_key(ext_dir.name, api_key)
    verify_api_key_injection(ext_dir.name, api_key)
    options.add_argument(f'--load-extension={ext_dir.name}')
    chrome = uc.Chrome(options=options, **uc_chrome_kwargs)
    # keep the temp dir alive for the lifetime of the driver
    chrome._sadcaptcha_tmpdir = ext_dir      # ← prevents garbage collection
    LOGGER.debug("created new undetected chromedriver patched with sadcaptcha")
    return chrome

def make_playwright_solver_context(
    playwright: sync_api.Playwright,
    api_key: str,
    user_data_dir: str | None = None,
    no_warn: bool = False,
    **playwright_context_kwargs
) -> sync_api.BrowserContext:
    """Create a playwright context patched with SadCaptcha.
    
    Args:
        playwright (playwright.sync_api.playwright) - Playwright instance
        api_key (str): SadCaptcha API key
        user_data_dir (str | None): User data dir that is passed to playwright.chromium.launch_persistent_context. If None, a temporary directory will be used.
        **playwright_context_kwargs: Keyword args which will be passed to playwright.chromium.launch_persistent_context()
    """
    if not no_warn:
        LOGGER.warning("Selenium, playwright, and undetected chromedriver are no longer recommended for scraping. A better option is to use nodriver. To use nodriver, use the command 'make_nodriver_solver()' instead. To disable this warning, set the kwarg no_warn=True.")
    ext_dir = download_extension_to_unpacked()
    if user_data_dir is None:
        user_data_dir_tempdir = tempfile.TemporaryDirectory()
        user_data_dir = user_data_dir_tempdir.name
    _patch_extension_file_with_key(ext_dir.name, api_key)
    playwright_context_kwargs = _prepare_pw_context_args(playwright_context_kwargs, ext_dir.name)
    ctx = playwright.chromium.launch_persistent_context(
        user_data_dir,
        **playwright_context_kwargs
    )
    ctx._sadcaptcha_tmpdir = ext_dir          # keep reference
    LOGGER.debug("created patched playwright context")
    return ctx

async def make_async_playwright_solver_context(
    async_playwright: async_api.Playwright,
    api_key: str,
    user_data_dir: str | None = None,
    **playwright_context_kwargs
) -> async_api.BrowserContext:
    """Create a async playwright context patched with SadCaptcha.
    
    Args:
        playwright (playwright.async_api.playwright) - Playwright instance
        api_key (str): SadCaptcha API key
        user_data_dir (str | None): User data dir that is passed to playwright.chromium.launch_persistent_context. If None, a temporary directory will be used.
        **playwright_context_kwargs: Keyword args which will be passed to playwright.chromium.launch_persistent_context()
    """
    ext_dir = download_extension_to_unpacked()
    if user_data_dir is None:
        user_data_dir_tempdir = tempfile.TemporaryDirectory()
        user_data_dir = user_data_dir_tempdir.name
    _patch_extension_file_with_key(ext_dir.name, api_key)
    playwright_context_kwargs = _prepare_pw_context_args(playwright_context_kwargs, ext_dir.name)
    ctx = await async_playwright.chromium.launch_persistent_context(
        user_data_dir,
        **playwright_context_kwargs
    )
    ctx._sadcaptcha_tmpdir = ext_dir          # keep reference
    LOGGER.debug("created patched async playwright context")
    return ctx

def _prepare_pw_context_args(
        playwright_context_kwargs: dict[str, Any],
        ext: str
) -> dict[str, Any]:
    if "args" in playwright_context_kwargs.keys():
        playwright_context_kwargs["args"] = playwright_context_kwargs["args"] + [
            f"--disable-extensions-except={ext}",
            f"--load-extension={ext}",
        ]
    else:
        playwright_context_kwargs["args"] = [
            f"--disable-extensions-except={ext}",
            f"--load-extension={ext}",
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',         
            '--disable-web-security',
            '--disable-infobars',  
            '--start-maximized',  
        ]
    if playwright_context_kwargs.get("headless") == True:
        if "--headless=new" not in playwright_context_kwargs["args"]:
            _ = playwright_context_kwargs["args"].append("--headless=new")
        playwright_context_kwargs["headless"] = None
        LOGGER.debug("Removed headless=True and added --headless=new launch arg")
    LOGGER.debug("prepared playwright context kwargs")
    return playwright_context_kwargs

def download_extension_to_unpacked() -> tempfile.TemporaryDirectory:
    """
    Download the SadCaptcha Chrome extension from GitHub and return an unpacked
    TemporaryDirectory that can be passed to Playwright / Chrome.
    """
    repo_zip_url = (
        "https://codeload.github.com/gbiz123/sadcaptcha-chrome-extensino/zip/refs/heads/master"
    )

    LOGGER.debug("Downloading SadCaptcha extension from %s", repo_zip_url)
    resp = requests.get(repo_zip_url, timeout=30)
    resp.raise_for_status()

    tmp_dir = tempfile.TemporaryDirectory(prefix="sadcaptcha_ext_")
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        # GitHub zips have a single top‑level folder → strip it
        root_prefix = zf.namelist()[0].split("/")[0] + "/"
        for member in zf.namelist():
            if member.endswith("/"):
                continue
            rel_path = member[len(root_prefix) :]
            if not rel_path:
                continue
            dest_file = os.path.join(tmp_dir.name, rel_path)
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            with zf.open(member) as src, open(dest_file, "wb") as dst:
                dst.write(src.read())

    LOGGER.debug("Extension unpacked to %s", tmp_dir.name)
    return tmp_dir

def _patch_extension_file_with_key(extension_dir: str, api_key: str) -> None:
    script_path = os.path.join(extension_dir, "script.js")
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            script = f.read()
        
        original_script = script
        script = patch_extension_script_with_key(script, api_key)
        
        # Verify replacement happened
        if script == original_script:
            LOGGER.warning("API key pattern not found in script.js")
        
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script)
            
        LOGGER.debug("Successfully patched extension file with API key")
    except Exception as e:
        LOGGER.error(f"Failed to patch extension with API key: {e}")
        raise

def patch_extension_script_with_key(script: str, api_key: str) -> str:
    script = script.replace('localStorage.getItem("sadCaptchaKey")', f"\"{api_key}\";")
    LOGGER.debug("patched extension script with api key")
    return script

def verify_api_key_injection(extension_dir, api_key):
    script_path = os.path.join(extension_dir, "script.js")
    
    # Check if file exists and contains your API key
    if os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        if f'"{api_key}";' in content:
            LOGGER.info(f"SUCCESS: API key found in script.js")
            return True
        else:
            LOGGER.warning(f"FAILURE: API key not found in script.js")
    else:
        LOGGER.error(f"FAILURE: script.js not found at {script_path}")
    return False
