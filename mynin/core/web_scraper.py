import requests
import pandas as pd

from bs4 import BeautifulSoup
from datetime import date
from dateutil.relativedelta import relativedelta

today = date.today().strftime('%d-%m-%Y')
lastYear = (date.today() - relativedelta(years=1)).strftime('%d-%m-%Y')
def balanceScraper(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='table')
    df = pd.DataFrame(
        columns=[f'Stav k: {today}', f'Stav k: {lastYear}', 'Suma príjmov', 'Suma výdavkov', 'Suma celkom',
                 'Bežný zostatok'])

    # Collecting Ddata
    for row in table.tbody.find_all('tr'):
        # Find all data for each column
        columns = row.find_all('td')
        if columns != []:
            stavA = columns[0].text.strip()
            stavB = columns[1].text.strip()
            sumaPrijmov = columns[2].text.strip()
            sumaVydavkov = columns[3].text.strip()
            sumaCelkom = columns[4].text.strip()
            beznyZostatok = columns[5].text.strip()

            df = df.append(
                {f'Stav k: {today}': stavA, f'Stav k: {lastYear}': stavB, 'Suma príjmov': sumaPrijmov,
                 'Suma výdavkov': sumaVydavkov, 'Suma celkom': sumaCelkom,
                 'Bežný zostatok': beznyZostatok}, ignore_index=True)

    return df
def accountNumberScraper(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    accountNumber = soup.find()
