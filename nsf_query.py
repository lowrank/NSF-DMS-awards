
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


program_elements_codes = {
    "Algebra and Number Theory": "1264",
    "Analysis": "1281",
    "Applied Mathematics": "1266",
    "Combinatorics": "7970",
    "Computational Mathematics": "1271",
    "Foundations": "1268",
    "Geometric Analysis": "1265",
    "Mathematical Biology": "7334",
    "Probability": "1263",
    "Statistics": "1269",
    "Topology": "1267"
}

def generate_query_url(program_name, start_year, expired='true'):
    URL = 'https://www.nsf.gov/awardsearch/advancedSearchResult?'
    Query = {
        'PIId': '',
        'PIFirstName': '',
        'PILastName': '',
        'PIOrganization': '',
        'PIState': '',
        'PIZip': '',
        'PICountry': '',
        'ProgOrganization':'03040000',
        'ProgEleCode': program_elements_codes[program_name],
        'BooleanElement': 'All',
        'ProgRefCode': '',
        'BooleanRef': 'All',
        'Program': '',
        'ProgOfficer': '',
        'Keyword': '',
        'AwardNumberOperator': '',
        'AwardAmount': '',
        'AwardInstrument': '',
        'ActiveAwards': 'true',
        'ExpiredAwards': expired,
        'OriginalAwardDateOperator': '',
        'OriginalAwardDateFrom': '',
        'OriginalAwardDateTo': '',
        'StartDateOperator': 'Range',
        'StartDateFrom': '01%2F01%2F' + str(start_year),
        'StartDateTo': '12%2F31%2F' + str(start_year),
        'ExpDateOperator': ''
    }

    for q in Query:
        URL += q + '=' + Query[q] + '&'

    return URL[:-1]


def get_awards_csv(program_name, year, headless=True):

    if headless:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('--user-data-dir=.config/google-chrome')
        path = os.path.dirname(os.path.abspath(__file__))
        prefs = {"download.default_directory":path}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=chrome_options)
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--user-data-dir=.config/google-chrome')
        path = os.path.dirname(os.path.abspath(__file__))
        prefs = {"download.default_directory":path}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=chrome_options)

    print(generate_query_url(program_name, year))

    driver.get(generate_query_url(program_name, year))
    time.sleep(10)
    driver.get('https://www.nsf.gov/awardsearch/ExportResultServlet?exportType=csv')
    time.sleep(10)

    trials = 0

    while not os.path.exists("Awards.csv") and trials < 3:
        driver.get(driver.current_url)
        time.sleep(10)
        trials += 1
        print('retrying at ', trials, ' time')


    cur_dir = os.path.dirname(__file__)
    prog_dir = program_name.replace(" ", "-")
    
    if not os.path.isdir(os.path.join(cur_dir, prog_dir)):
        os.mkdir(os.path.join(cur_dir, prog_dir))


    target_file = os.path.join(os.path.join(cur_dir, prog_dir), "Awards-" + program_name.replace(" ", "-") +"-" + str(year) + ".csv")
    if os.path.exists(target_file) and os.path.exists("Awards.csv"):
        # check rows in csv
        old_num_of_rows = len(pd.read_csv(target_file,  encoding='latin-1'))
        new_num_of_rows = len(pd.read_csv("Awards.csv", encoding='latin-1'))
        
        if old_num_of_rows != new_num_of_rows:
            os.remove(target_file)
            os.rename("Awards.csv",  target_file)
            return 0
        else:
            os.remove("Awards.csv")
            return 1
    elif os.path.exists("Awards.csv"):
        os.rename("Awards.csv",  target_file)
        return 2
    else:
        return 3
