#import selenium webdriver
from selenium import webdriver
#import wait function from selenium webdriver support
from selenium.webdriver.support.ui import WebDriverWait
#import Opera Webdriver
from webdriver_manager.opera import OperaDriverManager
#import sys library for command-line processing
import sys

#Extract specific course info after finding the course on the page
def inner_table(driver):
    element = driver.find_elements_by_xpath(".//table[@class='td_dark']")
    if element:
        return element
    else:
        return False

#Intake Command-line input 
if len(sys.argv) > 3:
    raise Exception("Invalid Argument!\n Format = <course department initials> <course number>")
dept = sys.argv[1]
number = sys.argv[2]

#Generate new url to webscrape from
url = "https://catalog.sjsu.edu/content.php?filter%5B27%5D={dept}&filter%5B29%5D={number}&filter%5Bcourse_type%5D=-1&" \
"filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=2&expand=&navoid=95&search_database=Filter&" \
"filter%5Bexact_match%5D=1#acalog_template_course_filter".format(dept=dept, number=number)

#Spin up new Opera window
driver = webdriver.Opera(executable_path=OperaDriverManager().install())

#Go to the webpage
driver.get(url)

#Find course title
elem = driver.find_elements_by_xpath("//*[contains(text(), '{}')]".format(tokens[0]+" "+tokens[1]))

#Click on the course title element to access the course information
if elem[0]:
    elem[0].click()
else:
    try:
        raise Exception()
    except Exception:
        print("Course not found!")
        raise

table = WebDriverWait(driver, 3).until(inner_table)
lines = table[0].text.split('\n')
driver.quit()
lines.remove(lines[len(lines) - 1])
for line in lines:
      print(line)
