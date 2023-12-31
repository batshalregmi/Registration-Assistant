from time import sleep

from selenium import webdriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import os
import datetime
from selenium.common.exceptions import NoSuchElementException

directory = os.path.dirname(os.path.realpath(__file__))

if os.name == "nt":
    PATH = "chromedriver.exe"
else:
    PATH = "./chromedriver"

BASE_URL = URLHERE
with open("config.json", "r") as f:
    config = json.load(f)

print("Starting...")
chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={directory}\selenium")
driver = uc.Chrome(PATH, chrome_options=chrome_options)
driver.get(BASE_URL)
print(driver.title)


def get_time():
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")


def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


if config["firstRun"] == "True":
    print("First run detected, please login and then close the browser.")
    while True:
        if check_exists_by_xpath(
            "/html/body/div/main/div/div/div/div[1]/form/div[3]/input[1]"
        ):
            print("Login detected, continuing...")
            break
        else:
            sleep(1)
    config["firstRun"] = False
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

try:
    if check_exists_by_xpath(
        "/html/body/div/main/div/div/div/div[1]/form/div[3]/input[1]"
    ):
        WebDriverWait(driver, 5).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "/html/body/app-root/app-login/iframe")
            )
        )
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm:username"]'))
        ).send_keys(config["username"])
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm:password"]'))
        ).send_keys(config["password"])
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm:loginButton"]'))
        ).click()
except Exception as e:
    print(e)

def startRegistration():
    driver.find_element(By.ID, "registerLink").click()
    driver.implicitly_wait(3)
    driver.find_element(By.CLASS_NAME, "select2-arrow").click()
    driver.implicitly_wait(3)
    driver.find_element(By.ID, config["termHTMLCode"]).click()
    driver.find_element(By.ID, "term-go").click()
    driver.implicitly_wait(2)
    driver.find_element(By.ID, "enterCRNs-tab").click()

    for each in range(config["numberOfClasses"]):
        driver.implicitly_wait(1)
        driver.find_element(By.ID, "addAnotherCRN").click()
        driver.find_element(By.ID, "txt_crn" + str(each + 1)).send_keys(
            config["CRN_" + str(each + 1)]
        )

    if config["ENV"] == "PROD":
        driver.find_element(By.ID, "addCRNbutton").click()
        driver.find_element(By.ID, "saveButton").click()
    sleep(9999)


startRegistration()
