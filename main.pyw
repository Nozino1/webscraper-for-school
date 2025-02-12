import time
import PySimpleGUI as pg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

############################################### your information
schoolName = "<name of your school>"
userName = "<your web-untis username>"
password = "<your web-untis password>"
###############################################

listTestsThisWeek = []
listTestsNextWeek = []

url = "https://klio.webuntis.com" # setting up webdriver
path = "C:\Program Files (x86)/chromedriver.exe"
options = Options()
options.add_argument("headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)
time.sleep(2.0)

schoolParent = driver.find_element(By.CLASS_NAME, "Select-input") # selects school
schoolInput = schoolParent.find_elements(By.XPATH, "*")[0]
schoolInput.send_keys(schoolName)
time.sleep(1.0)
schoolInput.send_keys(Keys.RETURN)
time.sleep(1.0)

userInputs = driver.find_elements(By.CLASS_NAME, "un-input-group__input") # logs in
for element in userInputs:
    if element.get_attribute("type") == "text":
        element.send_keys(userName)
    elif element.get_attribute("type") == "password":
        element.send_keys(password)
        element.send_keys(Keys.RETURN)
time.sleep(2.0)

buttons = driver.find_elements(By.CLASS_NAME, "item-container") # goes to timetable(You probably will have to change the'Mein Stundenplan' to the english version if you want to use this program)
time.sleep(1.0)
for element in buttons:
    if element.text == "Mein Stundenplan":
        element.click()
        time.sleep(2.0)

WebDriverWait(driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"embedded-webuntis"))) # switch to iframe
time.sleep(1.5)

legend = driver.find_elements(By.CLASS_NAME, "un-timetable-legend__cell") # find legend and gets the rgb value for a test(Again, change it from 'Prüfung' to test or something)
for element in legend:
    if element.text == "Prüfung":
        testColor = element.value_of_css_property("background-color")[:16]

lessons = driver.find_elements(By.CLASS_NAME, "renderedEntry") # gets all lessons
for element in lessons:                                        # iterates through the list and finds tests
    if element.value_of_css_property("background-color")[:16] == testColor:
        listTestsThisWeek.append(element.find_element(By.XPATH, "./div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[1]/span").get_attribute("innerHTML"))

buttons = driver.find_elements(By.CSS_SELECTOR, "button[type=button]") # gets all buttons
for element in buttons:                                                # iterates through all buttons and finds the button to change the timetable
    if element.get_attribute("class") == "btn btn-default":
        if element.find_element(By.XPATH, "./*").get_attribute("class") == "un-icon fa fa-arrow-right":
            element.click()
time.sleep(1.5)

lessons = driver.find_elements(By.CLASS_NAME, "renderedEntry") # gets all lessons(of the next week because the program pressed the button earlier)
for element in lessons:                                        # iterates through all lessons and finds tests
    if element.value_of_css_property("background-color")[:16] == testColor:
        listTestsNextWeek.append(element.find_element(By.XPATH, "./div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[1]/span").get_attribute("innerHTML"))

testsThisWeek = "" # declares variable
for element in listTestsThisWeek: # gets all tests and puts them in a human-readable string
    testsThisWeek = testsThisWeek + element + ", "
testsThisWeek = testsThisWeek[:-2] # removes the las ', '

testsNextWeek = "" # declares variable
for element in listTestsNextWeek: # gets all tests and puts them in a human-readable string
    testsNextWeek = testsNextWeek + element + ", "
testsNextWeek = testsNextWeek[:-2] # removes the las ', '

pg.theme("DarkBlue14")

layout = [                                  # creates layout
    [pg.Text("Tests in dieser Woche:")],
    [pg.Text(str(testsThisWeek))],
    [pg.Text("Tests in der nächsten Woche:")],
    [pg.Text(str(testsNextWeek))],
    [pg.Button("exit", size=(20, 2))]
]

window = pg.Window("pop-up", layout, size=(250, int(layout.__len__()) * 35), element_justification="l") # creates window
while True:                         # 'main' loop
    event , values = window.read()
    match event:
        case "exit":
            window.close()
            driver.quit()
            break