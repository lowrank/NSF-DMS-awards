
import os
import time
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
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome()
    print(generate_query_url(program_name, year))
    driver.get(generate_query_url(program_name, year))
    time.sleep(10)
    driver.get('https://www.nsf.gov/awardsearch/ExportResultServlet?exportType=csv')
    time.sleep(10)
    driver.close()


    cur_dir = os.path.dirname(__file__)
    prog_dir = program_name.replace(" ", "-")
    
    if not os.path.isdir(os.path.join(cur_dir, prog_dir)):
        os.mkdir(os.path.join(cur_dir, prog_dir))

    os.rename("Awards.csv",  os.path.join(os.path.join(cur_dir, prog_dir), "Awards-" + program_name.replace(" ", "-") +"-" + str(year) + ".csv"))