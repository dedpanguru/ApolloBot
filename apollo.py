from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.opera import OperaDriverManager
import sys

def inner_table(driver):
    """finds inner table element of the current element the global driver is on"""
    element = driver.find_elements_by_xpath(".//table[@class='td_dark']")
    if element:
        return element
    else:
        return False

course = sys.argv[1]
tokens = course.split('-')
url = "https://catalog.sjsu.edu/preview_entity.php?catoid=2&ent_oid=130"
if tokens[0] == "SE":
    url = "https://catalog.sjsu.edu/preview_entity.php?catoid=1&ent_oid=18&p=2#courses"
elif tokens[0] == "CMPE":
    url = "https://catalog.sjsu.edu/preview_entity.php?catoid=1&ent_oid=18"
course = course.replace("-", " ", 1)
driver = webdriver.Opera(executable_path=OperaDriverManager().install())
driver.get(url)
elem = driver.find_elements_by_xpath("//*[contains(text(), '{}')]".format(course))
elem[0].click()
table = WebDriverWait(driver, 3).until(inner_table)
lines = table[0].text.split('\n')
driver.quit()
lines.remove(lines[len(lines)-1])

for line in lines:
    print(line)
