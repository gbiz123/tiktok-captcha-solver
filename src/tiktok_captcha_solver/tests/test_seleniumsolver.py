import random
import time
import logging
import os

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

from tiktok_captcha_solver.captchatype import CaptchaType

from ..seleniumsolver import SeleniumSolver



def make_driver() -> uc.Chrome:
    options = uc.ChromeOptions()
    # options.add_argument('--proxy-server=http://pr.oxylabs.io:7777')
    options.add_argument('--ignore-certificate-errors')
    options.binary_location = "/usr/bin/google-chrome-stable"
    return uc.Chrome(
        service=ChromeDriverManager().install(),
        headless=False,
        use_subprocess=False,
        options=options,
        browser_executable_path="/usr/bin/google-chrome-stable"
    )

def make_driver_normal() -> WebDriver:
    options = webdriver.ChromeOptions()
    # options.add_argument('--proxy-server=http://pr.oxylabs.io:7777')
    options.add_argument('--ignore-certificate-errors')
    options.binary_location = "/usr/bin/google-chrome-stable"
    options.headless = False
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


### TODO
# Make unit tests for static HTML files.
# TikTok is way too finicky and testing is annoying!

def open_tiktkok_login(driver: uc.Chrome) -> None:
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    time.sleep(10)
    write_username = driver.find_element(By.XPATH, '//input[contains(@name,"username")]');
    write_username.click()
    for char in os.environ["TIKTOK_USERNAME"]:
        write_username.send_keys(char)
        time.sleep(0.001)
        # time.sleep(random.random())

    time.sleep(2);
    write_password = driver.find_element(By.XPATH, '//input[contains(@type,"password")]');
    write_password.click()
    for char in os.environ["TIKTOK_PASSWORD"]:
        write_password.send_keys(char)
        time.sleep(0.001)
        # time.sleep(random.random())
    time.sleep(2)
    login_btn = driver.find_element(By.XPATH, '//button[contains(@data-e2e,"login-button")]').click();
    time.sleep(8)

def open_tiktkok_search(driver: uc.Chrome) -> None:
    search_query = "davidteather"
    driver.get(f"https://www.tiktok.com/@therock")

def test_solve_at_scroll(caplog) -> None:
    caplog.set_level(logging.DEBUG)
    driver = make_driver_normal()
    driver.get("https://www.tiktok.com/")
    input("Trigger a captcha...")
    sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"], mouse_step_size=2)
    with open("src/tiktok_captcha_solver/tests/puzzle_video_search.html", "w") as f:
        f.write(driver.page_source)
    sadcaptcha.solve_captcha_if_present()

# def test_does_not_false_positive():
#     driver = make_driver()
#     try:
#         driver.get("https://www.tiktok.com/login/phone-or-email/email")
#         sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
#         assert sadcaptcha.captcha_is_present(timeout=5) == False
#     finally:
#         driver.quit()
#

# def test_shapes_v2_is_detected():
#     driver = make_driver()
#     try:
#         driver.get("file:///home/gregb/ToughdataLLC/SadCaptcha/tiktok-captcha-solver/src/tiktok_captcha_solver/tests/new_shapes.html")
#         sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
#         assert sadcaptcha.identify_captcha() == CaptchaType.SHAPES_V2
#     finally:
#         driver.quit()
#
#
# def test_rotate_v2_is_detected():
#     driver = make_driver()
#     try:
#         driver.get("file:///home/gregb/ToughdataLLC/SadCaptcha/tiktok-captcha-solver/src/tiktok_captcha_solver/tests/new_rotate.html")
#         sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
#         assert sadcaptcha.identify_captcha() == CaptchaType.ROTATE_V2
#     finally:
#         driver.quit()
#
# def test_puzzle_v2_is_detected():
#     driver = make_driver()
#     try:
#         driver.get("file:///home/gregb/ToughdataLLC/SadCaptcha/tiktok-captcha-solver/src/tiktok_captcha_solver/tests/new_puzzle.html")
#         sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
#         assert sadcaptcha.identify_captcha() == CaptchaType.PUZZLE_V2
#     finally:
#         driver.quit()
#
# def test_solve_captcha_at_login(caplog):
#     caplog.set_level(logging.DEBUG)
#     driver = make_driver()
#     try:
#         open_tiktkok_login(driver)
#         sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
#         sadcaptcha.solve_captcha_if_present()
#         time.sleep(3)
#         assert not sadcaptcha.captcha_is_present()
#     finally:
#         driver.quit()
#
# # def test_solve_captcha_at_login_with_proxy(caplog):
# #     caplog.set_level(logging.DEBUG)
# #     driver = make_driver()
# #     try:
# #         open_tiktkok_login(driver)
# #         sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"], proxy=os.environ["PROXY"])
# #         sadcaptcha.solve_captcha_if_present()
# #     finally:
# #         driver.quit()
#
# def test_solve_captcha_at_search(caplog):
#     caplog.set_level(logging.DEBUG)
#     driver = make_driver_normal()
#     open_tiktkok_search(driver)
#     sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
#     sadcaptcha.solve_captcha_if_present()
#     driver.quit()
#
# def test_detect_douyin(caplog):
#     caplog.set_level(logging.DEBUG)
#     driver = make_driver()
#     try:
#         driver.get("https://www.douyin.com")
#         sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
#         assert sadcaptcha.page_is_douyin()
#     finally:
#         driver.quit()
#
# def test_solve_douyin_puzzle(caplog):
#     caplog.set_level(logging.DEBUG)
#     driver = webdriver.Chrome(options)
#     try:
#         driver.get("https://www.douyin.com/discover")
#         time.sleep(5)
#         sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
#         sadcaptcha.solve_captcha_if_present()
#     finally:
#         driver.quit()
