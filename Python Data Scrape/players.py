import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import re
import itertools

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
            r = requests.get(current_url)
            raw_html = r.content
            soup = BeautifulSoup(raw_html, 'html.parser')
            tables = soup.findAll('table')
            max_len = 0
            index = 0

            for i in range(len(tables)):
                tags = tables[i].findAll('a')
                if len(tags) > 0:
                    url = tags[0].get('href', None)
                    if "/boxscores/20" in url and len(tables[i]) > max_len:
                        index = i
                        max_len = len(tables[i])

            table = tables[index]

            tags = table.findAll('a')
            for tag in tags:
                url = re.sub("\.\.", original_url + year, tag.get('href', None))
                url += '?view=teamstats'
                href_list.append(url)

    print("done getting links")
    return href_list

def vsplayers_scrape(url):
    vslist = {}
    homelist = {}
    for j in range(len(url)):
        print(url[j])
        r = requests.get(url[j])
        raw_html = r.content
        soup = BeautifulSoup(raw_html, 'html.parser')
        soup[url[j]] = BeautifulSoup(raw_html, 'html.parser')

        boxscore = soup[url[j]].find_all('article', {'class': 'game-boxscore bkb clearfix'})

        players = boxscore[0].find_all('div', {'class': 'player-stats'})
        team1 = players[0].find_all('div', {'class': 'stats-wrap clearfix'})
        visitorteam = team1[0].find_all('div', {'class': 'stats-box full lineup visitor clearfix'})

        team2 = players[0].find_all('div', {'class': 'stats-wrap clearfix'})[1]
        hometeam = team2.find_all('div', {'class': 'stats-box full lineup home clearfix'})
        hometbody = hometeam[0].find_all('tbody')
        hometr = hometbody[1].find_all('tr')


        visitortbody = visitorteam[0].find_all('tbody')
        visitortr = visitorteam[0].find_all('tr')
        vslist[url[j]] = {}

        for k in range(len(visitorteam[0].find_all('tbody'))):
            if visitorteam[0].find_all('tbody')[k].tr.text.strip() == str('STARTERS'):
                starters = visitorteam[0].find_all('tbody')[k]
                starterstr = starters.find_all('tr')
            elif visitorteam[0].find_all('tbody')[k].tr.text.strip() == str('RESERVES'):
                reserves = visitorteam[0].find_all('tbody')[k]
                reservestr = reserves.find_all('tr')


        if len(starterstr) > 4:
            for i in range((len(starters.find_all('th'))) - 1):
                vslist[url[j],i] = {
                    'Away' : visitorteam[0].caption.text.strip(),
                    visitorteam[0].thead.th.text.strip() : starters.find_all('th')[i+1].text.strip(),
                    visitorteam[0].find_all('th')[1].text.strip() : starterstr[i+1].td.text.strip(),
                    visitorteam[0].find_all('th')[2].text.strip() : starterstr[i+1].find_all('td')[1].text.strip(),
                    visitorteam[0].find_all('th')[3].text.strip() : starterstr[i+1].find_all('td')[2].text.strip(),
                    visitorteam[0].find_all('th')[4].text.strip() : starterstr[i+1].find_all('td')[3].text.strip(),
                    visitorteam[0].find_all('th')[5].text.strip() : starterstr[i+1].find_all('td')[4].text.strip(),
                    visitorteam[0].find_all('th')[6].text.strip() : starterstr[i+1].find_all('td')[5].text.strip(),
                    visitorteam[0].find_all('th')[7].text.strip(): starterstr[i+1].find_all('td')[6].text.strip(),
                    visitorteam[0].find_all('th')[8].text.strip(): starterstr[i+1].find_all('td')[7].text.strip(),
                    visitorteam[0].find_all('th')[9].text.strip(): starterstr[i+1].find_all('td')[8].text.strip(),
                    visitorteam[0].find_all('th')[10].text.strip(): starterstr[i+1].find_all('td')[9].text.strip(),
                    visitorteam[0].find_all('th')[11].text.strip(): starterstr[i+1].find_all('td')[10].text.strip(),
                    visitorteam[0].find_all('th')[12].text.strip(): starterstr[i+1].find_all('td')[11].text.strip(),
                    visitorteam[0].find_all('th')[13].text.strip(): starterstr[i+1].find_all('td')[12].text.strip(),
                }

    return vslist

def vrplayers_scrape(url):
    vrlist = {}
    homelist = {}
    for j in range(len(url)):
        print(url[j])
        r = requests.get(url[j])
        raw_html = r.content
        soup = BeautifulSoup(raw_html, 'html.parser')
        soup[url[j]] = BeautifulSoup(raw_html, 'html.parser')

        boxscore = soup[url[j]].find_all('article', {'class': 'game-boxscore bkb clearfix'})

        players = boxscore[0].find_all('div', {'class': 'player-stats'})
        team1 = players[0].find_all('div', {'class': 'stats-wrap clearfix'})
        visitorteam = team1[0].find_all('div', {'class': 'stats-box full lineup visitor clearfix'})

        team2 = players[0].find_all('div', {'class': 'stats-wrap clearfix'})[1]
        hometeam = team2.find_all('div', {'class': 'stats-box full lineup home clearfix'})
        hometbody = hometeam[0].find_all('tbody')
        hometr = hometbody[1].find_all('tr')


        visitortbody = visitorteam[0].find_all('tbody')
        visitortr = visitorteam[0].find_all('tr')
        vrlist[url[j]] = {}

        for k in range(len(visitorteam[0].find_all('tbody'))):
            if visitorteam[0].find_all('tbody')[k].tr.text.strip() == str('STARTERS'):
                starters = visitorteam[0].find_all('tbody')[k]
                starterstr = starters.find_all('tr')
            elif visitorteam[0].find_all('tbody')[k].tr.text.strip() == str('RESERVES'):
                reserves = visitorteam[0].find_all('tbody')[k]
                reservestr = reserves.find_all('tr')


        if len(reservestr) > 0:
            for i in range((len(reserves.find_all('th'))) - 1):
                vrlist[url[j],i] = {
                    'Away' : visitorteam[0].caption.text.strip(),
                    visitorteam[0].thead.th.text.strip() : reserves.find_all('th')[i+1].text.strip(),
                    visitorteam[0].find_all('th')[1].text.strip() : reservestr[i+1].td.text.strip(),
                    visitorteam[0].find_all('th')[2].text.strip() : reservestr[i+1].find_all('td')[1].text.strip(),
                    visitorteam[0].find_all('th')[3].text.strip() : reservestr[i+1].find_all('td')[2].text.strip(),
                    visitorteam[0].find_all('th')[4].text.strip() : reservestr[i+1].find_all('td')[3].text.strip(),
                    visitorteam[0].find_all('th')[5].text.strip() : reservestr[i+1].find_all('td')[4].text.strip(),
                    visitorteam[0].find_all('th')[6].text.strip() : reservestr[i+1].find_all('td')[5].text.strip(),
                    visitorteam[0].find_all('th')[7].text.strip(): reservestr[i+1].find_all('td')[6].text.strip(),
                    visitorteam[0].find_all('th')[8].text.strip(): reservestr[i+1].find_all('td')[7].text.strip(),
                    visitorteam[0].find_all('th')[9].text.strip(): reservestr[i+1].find_all('td')[8].text.strip(),
                    visitorteam[0].find_all('th')[10].text.strip(): reservestr[i+1].find_all('td')[9].text.strip(),
                    visitorteam[0].find_all('th')[11].text.strip(): reservestr[i+1].find_all('td')[10].text.strip(),
                    visitorteam[0].find_all('th')[12].text.strip(): reservestr[i+1].find_all('td')[11].text.strip(),
                    visitorteam[0].find_all('th')[13].text.strip(): reservestr[i+1].find_all('td')[12].text.strip(),
                }

    return vrlist





def hsplayers_scrape(url):
    rlist = {}
    slist = {}
    for j in range(len(url)):
        print(url[j])
        r = requests.get(url[j])
        raw_html = r.content
        soup = BeautifulSoup(raw_html, 'html.parser')
        soup[url[j]] = BeautifulSoup(raw_html, 'html.parser')

        boxscore = soup[url[j]].find_all('article', {'class': 'game-boxscore bkb clearfix'})

        players = boxscore[0].find_all('div', {'class': 'player-stats'})
        team1 = players[0].find_all('div', {'class': 'stats-wrap clearfix'})
        visitorteam = team1[0].find_all('div', {'class': 'stats-box full lineup visitor clearfix'})

        team2 = players[0].find_all('div', {'class': 'stats-wrap clearfix'})[1]
        hometeam = team2.find_all('div', {'class': 'stats-box full lineup home clearfix'})
        hometbody = hometeam[0].find_all('tbody')
        hometr = hometbody[1].find_all('tr')


        for k in range(len(hometeam[0].find_all('tbody'))):
            if hometeam[0].find_all('tbody')[k].tr.text.strip() == str('STARTERS'):
                starters = hometeam[0].find_all('tbody')[k]
                starterstr = starters.find_all('tr')
            elif hometeam[0].find_all('tbody')[k].tr.text.strip() == str('RESERVES'):
                reserves = hometeam[0].find_all('tbody')[k]
                reservestr = reserves.find_all('tr')

        slist[url[j]] = {}
        if len(starterstr) > 4:
            for i in range((len(starters.find_all('th'))) - 1):
                slist[url[j],i] = {
                    'Home': hometeam[0].caption.text.strip(),
                    hometeam[0].thead.th.text.strip(): starters.find_all('th')[i + 1].text.strip(),
                    hometeam[0].find_all('th')[1].text.strip(): starterstr[i + 1].td.text.strip(),
                    hometeam[0].find_all('th')[2].text.strip(): starterstr[i + 1].find_all('td')[1].text.strip(),
                    hometeam[0].find_all('th')[3].text.strip(): starterstr[i + 1].find_all('td')[2].text.strip(),
                    hometeam[0].find_all('th')[4].text.strip(): starterstr[i + 1].find_all('td')[3].text.strip(),
                    hometeam[0].find_all('th')[5].text.strip(): starterstr[i + 1].find_all('td')[4].text.strip(),
                    hometeam[0].find_all('th')[6].text.strip(): starterstr[i + 1].find_all('td')[5].text.strip(),
                    hometeam[0].find_all('th')[7].text.strip(): starterstr[i + 1].find_all('td')[6].text.strip(),
                    hometeam[0].find_all('th')[8].text.strip(): starterstr[i + 1].find_all('td')[7].text.strip(),
                    hometeam[0].find_all('th')[9].text.strip(): starterstr[i + 1].find_all('td')[8].text.strip(),
                    hometeam[0].find_all('th')[10].text.strip(): starterstr[i + 1].find_all('td')[9].text.strip(),
                    hometeam[0].find_all('th')[11].text.strip(): starterstr[i + 1].find_all('td')[10].text.strip(),
                    hometeam[0].find_all('th')[12].text.strip(): starterstr[i + 1].find_all('td')[11].text.strip(),
                    hometeam[0].find_all('th')[13].text.strip(): starterstr[i + 1].find_all('td')[12].text.strip(),
                }

    return slist
        # a = pd.DataFrame(slist)
        # df1 = pd.DataFrame(a)
        # df1 = df1.T
        # df1 = df1.replace('\-', ' -- ', regex=True).astype(object)
        # df1 = df1.replace('\\n', '', regex=True).astype(object)



def hrplayers_scrape(url):
    rlist = {}
    slist = {}
    for j in range(len(url)):
        print(url[j])
        r = requests.get(url[j])
        raw_html = r.content
        soup = BeautifulSoup(raw_html, 'html.parser')
        soup[url[j]] = BeautifulSoup(raw_html, 'html.parser')

        boxscore = soup[url[j]].find_all('article', {'class': 'game-boxscore bkb clearfix'})

        players = boxscore[0].find_all('div', {'class': 'player-stats'})
        team1 = players[0].find_all('div', {'class': 'stats-wrap clearfix'})
        visitorteam = team1[0].find_all('div', {'class': 'stats-box full lineup visitor clearfix'})

        team2 = players[0].find_all('div', {'class': 'stats-wrap clearfix'})[1]
        hometeam = team2.find_all('div', {'class': 'stats-box full lineup home clearfix'})
        hometbody = hometeam[0].find_all('tbody')
        hometr = hometbody[1].find_all('tr')

        for k in range(len(hometeam[0].find_all('tbody'))):
            if hometeam[0].find_all('tbody')[k].tr.text.strip() == str('STARTERS'):
                starters = hometeam[0].find_all('tbody')[k]
                starterstr = starters.find_all('tr')
            elif hometeam[0].find_all('tbody')[k].tr.text.strip() == str('RESERVES'):
                reserves = hometeam[0].find_all('tbody')[k]
                reservestr = reserves.find_all('tr')

        rlist[url[j]] = {}
        if len(reservestr) > 0:
            for i in range((len(reserves.find_all('th'))) - 1):
                rlist[url[j], i] = {
                    'Home': hometeam[0].caption.text.strip(),
                    hometeam[0].thead.th.text.strip(): reserves.find_all('th')[i + 1].text.strip(),
                    hometeam[0].find_all('th')[1].text.strip(): reservestr[i + 1].td.text.strip(),
                    hometeam[0].find_all('th')[2].text.strip(): reservestr[i + 1].find_all('td')[1].text.strip(),
                    hometeam[0].find_all('th')[3].text.strip(): reservestr[i + 1].find_all('td')[2].text.strip(),
                    hometeam[0].find_all('th')[4].text.strip(): reservestr[i + 1].find_all('td')[3].text.strip(),
                    hometeam[0].find_all('th')[5].text.strip(): reservestr[i + 1].find_all('td')[4].text.strip(),
                    hometeam[0].find_all('th')[6].text.strip(): reservestr[i + 1].find_all('td')[5].text.strip(),
                    hometeam[0].find_all('th')[7].text.strip(): reservestr[i + 1].find_all('td')[6].text.strip(),
                    hometeam[0].find_all('th')[8].text.strip(): reservestr[i + 1].find_all('td')[7].text.strip(),
                    hometeam[0].find_all('th')[9].text.strip(): reservestr[i + 1].find_all('td')[8].text.strip(),
                    hometeam[0].find_all('th')[10].text.strip(): reservestr[i + 1].find_all('td')[9].text.strip(),
                    hometeam[0].find_all('th')[11].text.strip(): reservestr[i + 1].find_all('td')[10].text.strip(),
                    hometeam[0].find_all('th')[12].text.strip(): reservestr[i + 1].find_all('td')[11].text.strip(),
                    hometeam[0].find_all('th')[13].text.strip(): reservestr[i + 1].find_all('td')[12].text.strip(),
                }
    return rlist
        # b = pd.DataFrame(rlist)
        # df2 = pd.DataFrame(a)
        # df2 = df2.T
        # df2 = df2.replace('\-', ' -- ', regex=True).astype(object)
        # df2 = df2.replace('\\n', '', regex=True).astype(object)









# for i in range((len(visitortbody[1].find_all('th')))-2):
#     print(visitortr[i+1].find_all('td')[1].text.strip())
#
# dictlist = {}
#
# for j in range(len(visitorteam[0].find_all('th', {'class' : 'col-head'}))) and i in range((len(visitortbody[1].find_all('th'))) - 2):
#     for i in range((len(visitortbody[1].find_all('th'))) - 2):
#         dictlist[i] = {
#         'Away': visitorteam[0].caption.text.strip(),
#         visitorteam[0].find_all('th')[j].text.strip(): visitortr[1].find_all('td')[i].text.strip()
#         }
#
# A = (range((len(visitortbody[1].find_all('th'))) - 2),range(len(visitorteam[0].find_all('th', {'class': 'col-head'}))))
#
# for j,i in itertools.product(*A):
#     dictlist[i,j] = {
#     'Away': visitorteam[0].caption.text.strip(),
#     visitorteam[0].find_all('th')[j].text.strip(): visitortr[1].find_all('td')[i].text.strip()
#     }

url = 'http://www.oua.ca/sports/mbkb/2014-15/boxscores/20141109_qc5c.xml?view=boxscore'

q = get_links()
b = hrplayers_scrape(q)
c = hsplayers_scrape(q)
d = vsplayers_scrape(q)
e = vrplayers_scrape(q)



df1 = pd.DataFrame(b)
df1 = df1.T
df1 = df1.replace('\-', ' -- ', regex=True).astype(object)
df1 = df1.replace('\\n', '', regex=True).astype(object)
df1.to_csv('home reserves.csv',header = True)

df2 = pd.DataFrame(c)
df2 = df2.T
df2 = df2.replace('\-', ' -- ', regex=True).astype(object)
df2 = df2.replace('\\n', '', regex=True).astype(object)
df2.to_csv('home starters.csv',header = True)

df3 = pd.DataFrame(d)
df3 = df3.T
df3 = df3.replace('\-', ' -- ', regex=True).astype(object)
df3 = df3.replace('\\n', '', regex=True).astype(object)
df3.to_csv('visitors starters.csv',header = True)

df4 = pd.DataFrame(e)
df4 = df4.T
df4 = df4.replace('\-', ' -- ', regex=True).astype(object)
df4 = df4.replace('\\n', '', regex=True).astype(object)
df4.to_csv('visitors reserves.csv',header = True)


concat = pd.concat([df2,df3,df1,df4],sort=False)

df1.columns

concat.to_csv('player_data.csv',header=True)