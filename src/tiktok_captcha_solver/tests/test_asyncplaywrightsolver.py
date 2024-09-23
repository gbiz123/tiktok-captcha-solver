import asyncio
import logging
import os

from playwright.async_api import Page, async_playwright, expect
from playwright_stealth import stealth_async, StealthConfig
import pytest

from ..asyncplaywrightsolver import AsyncPlaywrightSolver

async def open_tiktkok_login(page: Page) -> None:
    await page.goto("https://www.tiktok.com/login/phone-or-email/email")
    await asyncio.sleep(10)
    write_username = page.locator('xpath=//input[contains(@name,"username")]')
    await write_username.type(os.environ["TIKTOK_USERNAME"]);
    await asyncio.sleep(2);
    write_password = page.get_by_placeholder('Password')
    await write_password.type(os.environ["TIKTOK_PASSWORD"]);
    await asyncio.sleep(2)
    login_btn = await page.locator('//button[contains(@data-e2e,"login-button")]').click();
    await asyncio.sleep(8)

async def open_tiktok_search(page: Page) -> None:
    search_query = "davidteather"
    await page.goto(f"https://www.tiktok.com/@therock")

@pytest.mark.asyncio
async def test_does_not_false_positive(caplog):
    caplog.set_level(logging.DEBUG)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
        await stealth_async(page, config)
        await page.goto("https://www.tiktok.com/login/phone-or-email/email")
        sadcaptcha = AsyncPlaywrightSolver(page, os.environ["API_KEY"])
        assert await sadcaptcha.captcha_is_present(timeout=5) == False

@pytest.mark.asyncio
async def test_solve_captcha_at_login(caplog):
    proxy = {
        "server": "pr.oxylabs.io:7777",
        "username": "customer-toughdata-cc-br",
        "password": "toughproxies"
    }
    caplog.set_level(logging.DEBUG)
    async with async_playwright() as p:
        #browser = await p.chromium.launch(headless=False, proxy=proxy)
        browser = await p.chromium.launch(headless=False, proxy=proxy)
        page = await browser.new_page()
        config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
        await stealth_async(page, config)
        await open_tiktkok_login(page)
        sadcaptcha = AsyncPlaywrightSolver(page, os.environ["API_KEY"])
        await sadcaptcha.solve_captcha_if_present()
        await expect(page.locator("css=#header-more-menu-icon")).to_be_visible(timeout=30000)

# @pytest.mark.asyncio
# async def test_solve_captcha_at_login_with_proxy(caplog):
#     caplog.set_level(logging.DEBUG)
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()
#         config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
#         await stealth_async(page, config)
#         await open_tiktkok_login(page)
#         sadcaptcha = AsyncPlaywrightSolver(page, os.environ["API_KEY"], proxy=os.environ["PROXY"])
#         await sadcaptcha.solve_captcha_if_present()
#         await expect(page.locator("css=#header-more-menu-icon")).to_be_visible(timeout=30000)

@pytest.mark.asyncio
async def test_solve_captcha_at_search(caplog):
    caplog.set_level(logging.DEBUG)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
        await stealth_async(page, config)
        await open_tiktok_search(page) 
        sadcaptcha = AsyncPlaywrightSolver(page, os.environ["API_KEY"])
        await sadcaptcha.solve_captcha_if_present()

@pytest.mark.asyncio
async def test_detect_douyin(caplog):
    caplog.set_level(logging.DEBUG)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.douyin.com")
        sadcaptcha = AsyncPlaywrightSolver(page, os.environ["API_KEY"])
        assert sadcaptcha.page_is_douyin()

@pytest.mark.asyncio
async def test_solve_douyin_puzzle(caplog):
    caplog.set_level(logging.DEBUG)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.douyin.com")
        await page.goto("https://www.douyin.com/discover")
        sadcaptcha = AsyncPlaywrightSolver(page, os.environ["API_KEY"])
        await sadcaptcha.solve_captcha_if_present()
