from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC

def drowpdown_select(el_id, option_value, driver):
    xpath = '//*[@id="'+el_id+'"]/option[. ="'+option_value+'"]'
    # print('xpath', xpath)
    option = driver.find_element(By.XPATH, xpath)
    option.click()
    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.ID, el_id)))    