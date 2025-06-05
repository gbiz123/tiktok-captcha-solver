import random
import time
import os
from playwright.sync_api import Page, sync_playwright
from playwright.async_api import async_playwright
from playwright_stealth import stealth_sync, stealth_async, StealthConfig

import pytest
from selenium.webdriver import ChromeOptions
from tiktok_captcha_solver import make_async_playwright_solver_context, make_playwright_solver_context, make_undetected_chromedriver_solver
from tiktok_captcha_solver.launcher import make_nodriver_solver, make_selenium_solver
from tiktok_captcha_solver.playwrightsolver import PlaywrightSolver

proxy = {
    # "server": "216.173.104.197:6334",
    # "server": "185.216.106.238:6315",
    # "server": "23.27.75.226:6306"
    # "server": "206.232.75.209:6779"
    # "server": "206.232.75.84:6654"
    "server": "185.216.106.238:6315"
    # "server": "185.15.178.3:5687"
    # "server": "2.57.30.223:7299"
    # "server": "2.57.30.49:7125"
}

# proxy = None
def test_launch_uc_solver():
    options = ChromeOptions()
    # _ = options.add_argument("--proxy-server=2.57.30.49:7125")
    #options.add_argument("--headless=")
    solver = make_selenium_solver(
        os.environ["API_KEY"],
        options=options
    )
    # solver.get("https://affiliate-us.tiktok.com/connection/creator?shop_region=US")
    solver.get("https://www.tiktok.com")
    input("waiting for enter")
    solver.close()

def open_tiktkok_login(page: Page) -> None:
    _ = page.goto("https://www.tiktok.com/login/phone-or-email/email")
    print("opened tiktok login")
    # time.sleep(10)
    write_username = page.locator('xpath=//input[contains(@name,"username")]')
    write_username.type(os.environ["TIKTOK_USERNAME"]);
    time.sleep(2);
    # write_password = page.locator('xpath=//input[contains(@type,"password")]')
    write_password = page.get_by_placeholder('Password')
    write_password.type(os.environ["TIKTOK_PASSWORD"]);
    print("typed credentials")
    time.sleep(2)
    page.locator('//button[contains(@data-e2e,"login-button")]').click();
    print("pressed login button")
    # time.sleep(5)
    _ = page.screenshot(path="post_login_click.png")
    time.sleep(15)
#
# def test_launch_browser_with_crx_headless():
#     with sync_playwright() as p:
#         ctx = make_playwright_solver_context(
#             p,
#             os.environ["API_KEY"],
#             headless=True,
#             proxy=proxy,
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
#             args=["--headless=chrome"],
#             record_video_dir="videos/"
#         )
#         page = ctx.new_page()
#         stealth_config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
#         stealth_sync(page, stealth_config)
#         open_tiktkok_login(page)
#         assert not PlaywrightSolver(page, os.environ["API_KEY"]).captcha_is_present()
#         ctx.close()
#
# def test_launch_browser_with_crx():
#     with sync_playwright() as p:
#         ctx = make_playwright_solver_context(
#             p,
#             os.environ["API_KEY"],
#             headless=False,
#             proxy=proxy,
#             # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
#         )
#         page = ctx.new_page()
#         stealth_config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
#         stealth_sync(page, stealth_config)
#         _ = page.goto("https://tiktok.com")
#         time.sleep(2)
#         _ = page.locator("div[data-e2e=\"explore-item\"]").first.click()
#         input("waiting for enter")
#
# @pytest.mark.asyncio
# async def test_launch_browser_with_asyncpw():
#     async with async_playwright() as p:
#         ctx = await make_async_playwright_solver_context(
#             p,
#             os.environ["API_KEY"],
#             headless=False,
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
#             proxy=proxy
#         )
#         page = await ctx.new_page()
#         stealth_config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
#         await stealth_async(page, stealth_config)
#         _ = await page.goto("https://tiktok.com")
#         x, y = random.randint(0, 50), random.randint(0, 50)
#         a, b = random.randint(1, 50), random.randint(100, 200)
#
#         await page.mouse.move(x, y)
#         await page.wait_for_load_state("networkidle")
#         await page.mouse.move(a, b)
#
#         time.sleep(2)
#         _ = await page.locator("div[data-e2e=\"explore-item\"]").first.click()
#         input("waiting for enter")

@pytest.mark.asyncio
async def test_launch_browser_with_nodriver():
    ctx = await make_nodriver_solver(
        os.environ["API_KEY"],
        headless=False,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        proxy=proxy["server"]
    )
    page = await ctx.get("https://tiktok.com")
    input("waiting for enter")
