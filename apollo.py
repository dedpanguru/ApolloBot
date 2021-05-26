# Author: Gurveer Singh
# Time of Creation: 01:08, May 26, 2021
# Edits: Added file writing feature -> Program no longer outputs to terminal and instead saves to a file in the same directory
#       Added command-line interface involving programming command-line flags while retaining basic argument processing

# import selenium webdriver
from selenium import webdriver
# import webdriverwait - used to wait for changes to the page after an interaction
from selenium.webdriver.support.ui import WebDriverWait
# import opera driver - can be changed if wished, requires Opera browser and its driver manager
from webdriver_manager.opera import OperaDriverManager
# import argparse to create CLI
import argparse


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
                                     usage='%(prog)s.py course [course department] [course number] [options]',
                                     description="Scrape SJSU course information by providing the course's department and number",
                                     epilog='I hope you get a good use out of it')
# This version of the project is 2.0
cmd_parser.version = 'Apollo 2.0'
# add positional flag: "course", which will guarantee that user will enter a course department and number
cmd_parser.add_argument('course',
                        action='append',
                        nargs=3,
                        help='course department and course number, e.g. CS 122')
# add positional flag: "-f" and "--file", which will define the name of the file to send output to
cmd_parser.add_argument('-f', '--file',
                        dest='file',
                        action='append',
                        nargs=1,
                        help='write to a txt file with a specified name; by default, this program will write to course_info.txt in appending mode ')
# add positional flag: "-w" and "--write-over", set file writing mode to truncate (wipe the file and start anew)
cmd_parser.add_argument('-w', '--write-over',
                        dest='w',
                        action='store_true',
                        help='write over file with course information')
# add positional flag: "-w" and "--write-over", set file writing mode to truncate (wipe the file and start anew)
cmd_parser.add_argument('-v', '--version',
                        action='version',
                        help='version of this program')

# collect all command-line arguments
args = cmd_parser.parse_args()

# set filename if it needs to be set
filename = args.file[0][1] if len(args.file[0]) == 2 else "course_info.txt"

# set file writing type if it needs to be set
writing_type = 'w' if args.w else 'a'

# open file
file = open(filename, writing_type)

# extact tokens from command-line arguments
inits = args.course[0][1]
num = args.course[0][2]

# ensure that tokens are provided
if not inits or not num:
    print("You did not supply necessary inputs!")
    exit(0)

# create url with tokens
url = "https://catalog.sjsu.edu/content.php?filter%5B27%5D={dept}&filter%5B29%5D={number}&filter%5Bcourse_type%5D=-1&" \
      "filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=2&expand=&navoid=95&search_database=Filter&" \
      "filter%5Bexact_match%5D=1#acalog_template_course_filter".format(dept=inits, number=num)

# initialize webdriver
driver = webdriver.Opera(executable_path=OperaDriverManager().install())

# run the url on the driver
driver.get(url)

# find the course on the page
elem = driver.find_elements_by_xpath("//*[contains(text(), '{}')]".format(inits.upper() + " " + num))

# if the course exists, click on it, otherwise, throw an exception
if elem:
    elem[0].click()
else:
    driver.quit()
    file.close()
    raise Exception("Course Not Found! Please make sure you entered it correctly!\n Run \'python apollo.py --help\' for help")

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
        file.write(line + "\n")

# new line space between entries on the file        
file.write('\n')

# close the file once done
file.close()

# print finishing message
print("Thank you for using Apollo! \nCheck", filename, "for the information!\n")
