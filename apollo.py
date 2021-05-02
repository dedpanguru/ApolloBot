#import selenium webdriver
from selenium import webdriver
#import wait function
from selenium.webdriver.support.ui import WebDriverWait 
#import Opera Webdriver
from webdriver_manager.opera import OperaDriverManager
#import sys library for command-line processing
import sys

#Extract specific course info after finding the course on the page
def inner_table(driver):
    """finds inner table element of the current element the global driver is on"""
    element = driver.find_elements_by_xpath(".//table[@class='td_dark']")
    if element:
        return element
    else:
        return False

#Command-line Processing
#Arguments must be in XX-XXX format, otherwise Timeout error ocurrs
course = sys.argv[1]
tokens = course.split('-')
url = "https://catalog.sjsu.edu/preview_entity.php?catoid=2&ent_oid=130"
if tokens[0] == "SE":
    url = "https://catalog.sjsu.edu/preview_entity.php?catoid=1&ent_oid=18&p=2#courses"
elif tokens[0] == "CMPE":
    url = "https://catalog.sjsu.edu/preview_entity.php?catoid=1&ent_oid=18"
course = course.replace("-", " ", 1)

#Open webdriver
driver = webdriver.Opera(executable_path=OperaDriverManager().install())
#Enter webpage
driver.get(url)
#Find course on the webpage
elem = driver.find_elements_by_xpath("//*[contains(text(), '{}')]".format(course))
#Course information is available only after clicking on the title, so click the title
elem[0].click()
#wait for the webpage to change, otherwise get a StaleElementException
#Then, extract the inner information
table = WebDriverWait(driver, 3).until(inner_table)
#Format information
lines = table[0].text.split('\n')
#No need to keep driver open anymore, so close it
driver.quit()
#no need for last line of information
lines.remove(lines[len(lines)-1])
#print information
for line in lines:
    print(line)
