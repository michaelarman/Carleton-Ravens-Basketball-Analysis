import re
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import csv
from collections import defaultdict

def get_links():
    print("getting links...")
    teams = ['algoma', 'brock', 'carleton', 'guelph', 'lakehead', 'laurentian',
             'laurier', 'mcmaster', 'nipissing', 'ottawa', 'queens', 'ryerson',
             'toronto', 'waterloo', 'western', 'windsor', 'york']
    years = ['2014-15', '2015-16', '2016-17', '2017-18', '2018-19']
    original_url = 'http://oua.ca/sports/mbkb/'
    end_url = '?view=gamelog'
    href_list = []
    for year in years:
        for team in teams:
            current_url = original_url + year + '/teams/' + team + end_url
            # r = requests.get(current_url)
            # raw_html = r.content
            #soup = BeautifulSoup(raw_html, 'html.parser')
            #tab1 = soup.findAll('div', {'class': 'tab-panel clearfix'})[5]
            href_list.append(current_url)


    print("done getting links")
    return href_list


def scrape(url):
    """ This function is used to create data dictionaries for any url of team stats in the oua website. It
    takes an array of urls but for some games there are extra fields to look out for. This function is for those that
    do not have those extra fields in the table"""

    # create dictionary for links with less fields in table
    dictlist = {}
    for i in range(len(url)):

        print(url[i])
        r = requests.get(url[i])
        raw_html = r.content
        soup = BeautifulSoup(raw_html, 'html.parser')
        soup[url[i]] = BeautifulSoup(raw_html, 'html.parser')
        tabs = soup.findAll('div', {'class': 'tab-panel clearfix'})
        tab1 = tabs[4]
        for tab in range(len(tabs)):
            if str(soup.findAll('div', {'class': 'tab-panel clearfix'})[tab].tr.th) == '<th class="text">Date</th>':
                tab1 = soup.findAll('div', {'class': 'tab-panel clearfix'})[tab]

        # dates = tab1.div.div.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['text'])
        # opponents = tab1.div.div.findAll('td', {'class': 'text pinned-col'})
        # score = tab1.table.findAll('a')

        # d[url[i]] = {}

        # some links have different amounts of tables and sometimes the team stats table is different
        dictlist[url[i]] = {}
        for j in range(len(tab1.table.findAll('a'))):
            # dates = tab1.div.div.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['text'])
            # opponents = tab1.div.div.findAll('td', {'class': 'text pinned-col'})
            # score = tab1.table.findAll('a')

            dictlist[url[i]][j+1] = {
                'Dates': tab1.div.div.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['text'])[j].text.strip(),
                'Opponent': re.sub('\n(\s*)', '', tab1.div.div.findAll('td', {'class': 'text pinned-col'})[j].text.strip()),
                'Score': tab1.table.findAll('a')[j].contents
                }
            dictlist
            #dictlist[url[i]].append(dict)
    return dictlist









if __name__ == '__main__':
    # q = ['http://oua.ca/sports/mbkb/2014-15/boxscores/20141107_ekyz.xml?view=teamstats','http://oua.ca/sports/mbkb/2014-15/boxscores/20141108_zc1e.xml?view=teamstats',
    # 'http://oua.ca/sports/mbkb/2014-15/boxscores/20141114_jyud.xml?view=teamstats','http://oua.ca/sports/mbkb/2014-15/boxscores/20141121_5m0y.xml?view=teamstats',
    # 'http://oua.ca/sports/mbkb/2014-15/boxscores/20141122_kkin.xml?view=teamstats','http://oua.ca/sports/mbkb/2014-15/boxscores/20141128_q4pf.xml?view=teamstats']
    q = get_links()
    a = scrape(q)
    df = pd.DataFrame(a)
    df = df.T
    df = pd.DataFrame.from_dict(j, orient='index')



    df.to_csv('smd.csv', header=True)

    import pdb; pdb.set_trace()
