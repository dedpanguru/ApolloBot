#!/bin/python3
import argparse
import platform
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
if platform.system() == 'Linux':
    from webdriver_manager.firefox import GeckoDriverManager
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
elif platform.system() == "Windows":
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    driver = webdriver.Edge(EdgeChromiumDriverManager.install())
elif platform.system() == "Darwin":
    driver = webdriver.Safari(executable_path='/usr/bin/safaridriver')
    
# scrape newly formed table
def inner_table(driver):
    """finds inner table element of the current element the global driver is on"""
    element = driver.find_elements_by_xpath(".//table[@class='td_dark']")
    if element:
        return element
    else:
        return None    
    
# initialize argument parser
cmd_parser = argparse.ArgumentParser(prog='apollo',
                                     usage='%(prog)s.py -c/--course [course department] [course number] ',
                                     description="Scrape SJSU course information by providing the course's department and number",
                                     epilog='I hope you get a good use out of it')
cmd_parser.add_argument('-c', '--course',
                        action='append',
                        nargs='*',
                        dest ='courses',
                        help='course department and course number, e.g. CS 122',
                        required=True)
args = cmd_parser.parse_args()
def scrape(inits,num):
    """scrapes SJSU course catalog for all available course information"""
    # create url with tokens
    url = "https://catalog.sjsu.edu/content.php?filter%5B27%5D={dept}&filter%5B29%5D={number}&filter%5Bcourse_type%5D=-1&" \
          "filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=2&expand=&navoid=95&search_database=Filter&" \
          "filter%5Bexact_match%5D=1#acalog_template_course_filter".format(dept=inits, number=num)
    if driver:
        driver.get(url)
        # find the course on the page
        elem = driver.find_elements_by_xpath("//*[contains(text(), '{}')]".format(inits.upper() + " " + num))

        # if the course exists, click on it, otherwise, throw an exception
        if elem:
            elem[0].click()
        else:
            driver.quit()
            raise Exception(inits, num,"- Course Not Found! Please make sure you entered it correctly!\n Run \'python apollo.py --help\' for help")

        # wait until page changes after the click and the inner table is present before extracting the inner table
        table = WebDriverWait(driver, 1).until(inner_table)

        # split the table's text into a list of strings
        lines = table[0].text.split('\n')

        # no need for driver anymore, so close it
        driver.quit()

        # last line is useless, so remove it
        lines.remove(lines[len(lines) - 1])

        # write all remaining significant lines into the file
        for line in lines:
            if len(line) > 1:
                print(line)
    else:
        raise Exception("OS not identified, dm Dedpan#3039 on discord for support")
    
def main():
    # initialize argument parser
    cmd_parser = argparse.ArgumentParser(prog='apollo',
                                     usage='%(prog)s.py -c/--course [course department] [course number] ',
                                     description="Scrape SJSU course information by providing the course's department and number",
                                     epilog='I hope you get a good use out of it')
    cmd_parser.add_argument('-c', '--course',
                        action='append',
                        nargs='*',
                        dest ='courses',
                        help='course department and course number, e.g. CS 122',
                        required=True)
    courses = cmd_parser.parse_args()
    for index, element in enumerate(courses):
        if index % 2 == 0:
            if type(element) != str or len(element) != 2:
                raise Exception(element, '- Invalid input!')
            else:
                inits = element
        else:
            if type(element) != str and len(element) >= 1 and len(element) <= 4:
               num = element
            else:
                raise Exception(element, '- Invalid input!')
        if inits and num :
            try:
                scrape(inits, num)
            except Exception as e:
                raise(e)
        else:
            raise Exception("input not found")
                              
if '__name__' == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting Apollobot")
        exit(0)
    except Exception as e:
        print(e)
        exit(1)
    else:
        print("Thanks for using ApolloBot!")
        exit(0)