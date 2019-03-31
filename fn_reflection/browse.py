# pylint: disable=missing-docstring,invalid-name
# %%
import os
import selenium.webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def make_firefox():
    if os.name == 'nt':
        return wd.Firefox(executable_path='browser_engines/geckodriver.exe')
    if os.name == 'posix':
        return wd.Firefox(executable_path='browser_engines/geckodriver')


def make_chrome(savedir=None, headless=True):
    opts = wd.ChromeOptions()
    if savedir is not None:
        opts.add_experimental_option(
            "prefs", {"download.default_directory": savedir})
    if headless:
        opts.add_argument('--headless')
    arglist = ['--disable-gpu', '--ignore-certificate-errors',
               '--allow-running-insecure-content',
               '--disable-web-security', '--disable-desktop-notifications',
               "--disable-extensions", '--lang=ja',
               '--blink-settings=imagesEnabled=false']
    for optionarg in arglist:
        opts.add_argument(optionarg)
    if os.name == 'posix':
        return wd.Chrome(executable_path='browser_engines/chromedriver', chrome_options=opts)
    if os.name == 'nt':
        return wd.Chrome(executable_path='browser_engines/chromedriver.exe', chrome_options=opts)

def wait_visible_bycss(brz, selector):
    return WebDriverWait(brz, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
