import logging
import time
import os

from playwright.sync_api import Page, sync_playwright, expect
from playwright_stealth import stealth_sync, StealthConfig

from ..playwrightsolver import PlaywrightSolver


def open_tiktkok_login(page: Page) -> None:
    page.goto("https://www.tiktok.com/login/phone-or-email/email")
    time.sleep(10)
    write_username = page.locator('xpath=//input[contains(@name,"username")]')
    write_username.type(os.environ["TIKTOK_USERNAME"]);
    time.sleep(2);
    # write_password = page.locator('xpath=//input[contains(@type,"password")]')
    write_password = page.get_by_placeholder('Password')
    write_password.type(os.environ["TIKTOK_PASSWORD"]);
    time.sleep(2)
    login_btn = page.locator('//button[contains(@data-e2e,"login-button")]').click();
    time.sleep(8)

def open_tiktok_search(page: Page) -> None:
    search_query = "davidteather"
    page.goto(f"https://www.tiktok.com/search/user?q={search_query}&t=1715558822399")

def test_does_not_false_positive(caplog):
    caplog.set_level(logging.DEBUG)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
        stealth_sync(page, config)
        page.goto("https://www.tiktok.com/login/phone-or-email/email")
        sadcaptcha = PlaywrightSolver(page, os.environ["API_KEY"])
        assert sadcaptcha.captcha_is_present(timeout=5) == False

def test_solve_captcha_at_login(caplog):
    caplog.set_level(logging.DEBUG)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
        stealth_sync(page, config)
        open_tiktkok_login(page)
        sadcaptcha = PlaywrightSolver(page, os.environ["API_KEY"])
        sadcaptcha.solve_captcha_if_present()
        page.locator("css=#header-more-menu-icon").is_visible()
        expect(page.locator("css=#header-more-menu-icon")).to_be_visible(timeout=30000)

# def test_solve_captcha_at_login_with_proxy(caplog):
#     caplog.set_level(logging.DEBUG)
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
#         stealth_sync(page, config)
#         open_tiktkok_login(page)
#         sadcaptcha = PlaywrightSolver(page, os.environ["API_KEY"], proxy=os.environ["PROXY"])
#         sadcaptcha.solve_captcha_if_present()
#         page.locator("css=#header-more-menu-icon").is_visible()
#         expect(page.locator("css=#header-more-menu-icon")).to_be_visible(timeout=30000)
#
# def test_solve_captcha_at_search(caplog):
#     caplog.set_level(logging.DEBUG)
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         open_tiktok_search(page) 
#         sadcaptcha = PlaywrightSolver(page, os.environ["API_KEY"])
#         sadcaptcha.solve_captcha_if_present()

def test_detect_douyin(caplog):
    caplog.set_level(logging.DEBUG)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.douyin.com")
        sadcaptcha = PlaywrightSolver(page, os.environ["API_KEY"])
        assert sadcaptcha.page_is_douyin()

def test_solve_douyin_puzzle(caplog):
    caplog.set_level(logging.DEBUG)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.douyin.com")
        page.goto("https://www.douyin.com/discover")
        sadcaptcha = PlaywrightSolver(page, os.environ["API_KEY"])
        sadcaptcha.solve_captcha_if_present()
