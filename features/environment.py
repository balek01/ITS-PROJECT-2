from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

BASE_URL = "http://opencart:8080/"

def get_driver():
    '''Get Chrome/Firefox driver from Selenium Hub'''
    try:
        driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                options=webdriver.ChromeOptions())
    except WebDriverException:
        print("trying firefox")
        driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                options=webdriver.FirefoxOptions())
    driver.implicitly_wait(15)

    # Web stranku ziskate nasledujicim:
    # (jedno nebo druhe, zalezi na nastaveni prostedi)
    # driver.get("http://opencart:8080/")
    # driver.get("http://localhost:8080/")

    return driver


def before_all(context):
    context.driver = get_driver()
    context.base_url = BASE_URL

def after_all(context):
    context.driver.quit()

