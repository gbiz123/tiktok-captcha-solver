import time
import logging
import os

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

from ..seleniumsolver import SeleniumSolver

options = webdriver.ChromeOptions()
options.add_argument("--headless=0")
options.binary_location = "/usr/bin/google-chrome-stable"


def make_driver() -> uc.Chrome:
    return uc.Chrome(service=ChromeDriverManager().install(), headless=False, use_subprocess=False, browser_executable_path="/usr/bin/google-chrome-stable")


def open_tiktkok_login(driver: uc.Chrome) -> None:
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    time.sleep(10)
    write_username = driver.find_element(By.XPATH, '//input[contains(@name,"username")]');
    write_username.send_keys(os.environ["TIKTOK_USERNAME"]);
    time.sleep(2);
    write_password = driver.find_element(By.XPATH, '//input[contains(@type,"password")]');
    write_password.send_keys(os.environ["TIKTOK_PASSWORD"]);
    time.sleep(2)
    login_btn = driver.find_element(By.XPATH, '//button[contains(@data-e2e,"login-button")]').click();
    time.sleep(8)

def open_tiktkok_search(driver: uc.Chrome) -> None:
    search_query = "davidteather"
    driver.get(f"https://www.tiktok.com/@therock")

def test_does_not_false_positive():
    driver = make_driver()
    try:
        driver.get("https://www.tiktok.com/login/phone-or-email/email")
        sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
        assert sadcaptcha.captcha_is_present(timeout=5) == False
    finally:
        driver.quit()

def test_solve_captcha_at_login(caplog):
    caplog.set_level(logging.DEBUG)
    driver = make_driver()
    try:
        open_tiktkok_login(driver)
        sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
        sadcaptcha.solve_captcha_if_present()
    finally:
        driver.quit()

# def test_solve_captcha_at_login_with_proxy(caplog):
#     caplog.set_level(logging.DEBUG)
#     driver = make_driver()
#     try:
#         open_tiktkok_login(driver)
#         sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"], proxy=os.environ["PROXY"])
#         sadcaptcha.solve_captcha_if_present()
#     finally:
#         driver.quit()

def test_solve_captcha_at_search(caplog):
    caplog.set_level(logging.DEBUG)
    driver = make_driver()
    open_tiktkok_search(driver)
    sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
    sadcaptcha.solve_captcha_if_present()
    driver.quit()

def test_detect_douyin(caplog):
    caplog.set_level(logging.DEBUG)
    driver = make_driver()
    try:
        driver.get("https://www.douyin.com")
        sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
        assert sadcaptcha.page_is_douyin()
    finally:
        driver.quit()

def test_solve_douyin_puzzle(caplog):
    caplog.set_level(logging.DEBUG)
    driver = webdriver.Chrome(options)
    try:
        driver.get("https://www.douyin.com/discover")
        time.sleep(5)
        sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
        sadcaptcha.solve_captcha_if_present()
    finally:
        driver.quit()
