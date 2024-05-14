import time
import logging
import os

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

from ..seleniumsolver import SeleniumSolver

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("start-maximized")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument("--accept-lang=en-US,en;q=0.5")
options.add_argument("--dom-automation=disabled")



def make_driver() -> uc.Chrome:
    return uc.Chrome(service=ChromeDriverManager().install(), headless=False, use_subprocess=False)


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
    driver.get(f"https://www.tiktok.com/search/user?q={search_query}&t=1715558822399")

def test_solve_captcha_at_login(caplog):
    caplog.set_level(logging.DEBUG)
    driver = make_driver()
    open_tiktkok_login(driver)
    sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
    sadcaptcha.solve_captcha_if_present()

def test_solve_captcha_at_search(caplog):
    caplog.set_level(logging.DEBUG)
    driver = make_driver()
    open_tiktkok_search(driver)
    sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"])
    sadcaptcha.solve_captcha_if_present()
