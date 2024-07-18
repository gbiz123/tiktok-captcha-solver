import asyncio
import logging
import os

from playwright.async_api import Page, async_playwright, expect
from playwright_stealth import stealth_async
import pytest

from ..asyncplaywrightsolver import AsyncPlaywrightSolver


async def open_tiktkok_login(page: Page) -> None:
    await page.goto("https://www.tiktok.com/login/phone-or-email/email")
    await asyncio.sleep(10)
    write_username = page.locator('xpath=//input[contains(@name,"username")]')
    await write_username.type(os.environ["TIKTOK_USERNAME"]);
    await asyncio.sleep(2);
    write_password = page.locator('xpath=//input[contains(@type,"password")]')
    await write_password.type(os.environ["TIKTOK_PASSWORD"]);
    await asyncio.sleep(2)
    login_btn = await page.locator('//button[contains(@data-e2e,"login-button")]').click();
    await asyncio.sleep(8)

async def open_tiktok_search(page: Page) -> None:
    search_query = "davidteather"
    await page.goto(f"https://www.tiktok.com/search/user?q={search_query}&t=1715558822399")

@pytest.mark.asyncio
async def test_solve_captcha_at_login(caplog):
    caplog.set_level(logging.DEBUG)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await stealth_async(page)
        await open_tiktkok_login(page)
        sadcaptcha = AsyncPlaywrightSolver(page, os.environ["API_KEY"])
        await sadcaptcha.solve_captcha_if_present()
        await expect(page.locator("css=#header-more-menu-icon")).to_be_visible(timeout=30000)

@pytest.mark.asyncio
async def test_solve_captcha_at_search(caplog):
    caplog.set_level(logging.DEBUG)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await open_tiktok_search(page) 
        sadcaptcha = AsyncPlaywrightSolver(page, os.environ["API_KEY"])
        await sadcaptcha.solve_captcha_if_present()
