from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import os
import sys

"""Since Synergy uses a lot of javascript, a normal html scraper like beautifulsoup would not do the trick so we'd have to
use selenium and a webdriver to interact with the javascript and finally we can use beautifulsoup to interact with the innerhtml"""
browser = webdriver.Chrome(os.path.join(sys.path[0], 'chromedriver'))

def login():
    
    login_url = 'https://www.synergysportstech.com/Synergy/Default.aspx'
    browser.get(login_url)
    username1 = browser.find_element_by_css_selector('#txtUserName')
    username = "************"
    username1.send_keys(username)
    password1 = browser.find_element_by_css_selector('#txtPassword')
    password = "************"
    password1.send_keys(password)

    browser.find_element_by_css_selector('#btnLogin').click()


def get_links():
    browser.get('https://www.synergysportstech.com/Synergy/Sport/Basketball/web/teamsst/Video/SelectGame2.aspx')

    el5 = browser.find_element_by_css_selector('#ctl00_MainContent_lstSeason')
    for option in el5.find_elements_by_tag_name('option'):
        if option.text == '2017 - 2018':
            option.click() # select() in earlier versions of webdriver
            break

    time.sleep(3)
    el2 = browser.find_element_by_css_selector('#ctl00_MainContent_lstDivisionGroup')
    for option in el2.find_elements_by_tag_name('option'):
        if option.text == 'U Sports':
            option.click() # select() in earlier versions of webdriver
            break

    el4 = browser.find_element_by_css_selector('#ctl00_MainContent_lstViewMax')
    for option in el4.find_elements_by_tag_name('option'):
        if option.text == '1600':
            option.click() # select() in earlier versions of webdriver
            break

    el = browser.find_element_by_css_selector('#ctl00_MainContent_lstSubType')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == 'Regular Season':
            option.click() # select() in earlier versions of webdriver
            break

    time.sleep(5)

    el3 = browser.find_element_by_css_selector('#ctl00_MainContent_lstDivisions')
    for option in el3.find_elements_by_tag_name('option'):
        if option.text == 'Ontario University Athletics':
            option.click() # select() in earlier versions of webdriver
            break


    time.sleep(5)


    links = browser.find_elements_by_tag_name('table')
    html = links[2].get_attribute('innerHTML')
    soup1 = BeautifulSoup(html, 'html.parser')
    href_list1 = soup1.find_all('a')
    i = 0
    url_list = []
    root_url = 'https://www.synergysportstech.com/Synergy/Sport/Basketball/web/teamsst/Video/'
    for link in href_list1:
        if "GameGrid2" in link['href']:
            url_list.append(root_url + link['href'])

    return url_list

def scrape(url_list):
    dict = {}
    for url in url_list:
        dict[url] = {}
        browser.get(url)
        browser.find_element_by_link_text('Team Play Types').click()
        time.sleep(5)

        table = browser.find_elements_by_class_name('Tier')
        raw_html = table[2].get_attribute('innerHTML')
        soup = BeautifulSoup(raw_html, 'html.parser')
        raw_html2 = table[0].get_attribute('innerHTML')
        soup2 = BeautifulSoup(raw_html2, 'html.parser')
        print(soup.tr)
        tr = soup2.find_all('tr')
        Away_Team = tr[1].td.text.strip()
        Away_Total_Score = tr[1].find_all('td')[1].text.strip()
        Home_Team = tr[2].td.text.strip()
        Home_Total_Score = tr[2].find_all('td')[1].text.strip()
        # team1 = soup.find_all('td')[7].text.strip()
        # team2 = soup.find_all('td')[8].text.strip()

        tierrow = soup.find_all('tr', {'class': 'TierRow'})

        dict[url][Home_Team] = {}
        dict[url][Away_Team] = {}
        for i in range(len(tierrow)):
            row = soup.find_all('tr', {'class': 'TierRow'})[i]
            rowname = row.find_all('td')[0].text.strip()
            dict[url][Home_Team][rowname] = row.find_all('td')[1].text.strip()
            dict[url][Home_Team]['Total Points'] = Home_Total_Score
            dict[url][Away_Team][rowname] = row.find_all('td')[2].text.strip()
            dict[url][Away_Team]['Total Points'] = Away_Total_Score
            if int(Home_Total_Score) > int(Away_Total_Score):
                dict[url][Home_Team]['Winner'] = 1
            elif Away_Total_Score > Home_Total_Score:
                dict[url][Away_Team]['Winner'] = 1



    return dict

if __name__ == '__main__':
    login()
    urls = get_links()
    dict = scrape(urls)

    df = pd.DataFrame.from_dict({(i,j): dict[i][j]
                           for i in dict.keys()
                           for j in dict[i].keys()})
    df = df.T
    df.to_csv('PlayTypes2017-18.csv')
    df.fillna(0)
