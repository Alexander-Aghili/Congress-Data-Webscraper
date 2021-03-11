from bs4 import BeautifulSoup
import requests
import json

senate_URL = " https://www.senate.gov/senators/index.htm"
senate_page = requests.get(senate_URL).text
senateSoup = BeautifulSoup(senate_page, 'html.parser')
senate = []


def get_info(tr, house):
    info = tr.find('a')
    name = info.text.split(",")
    realname = name[1].strip() + ' ' + name[0].strip()
    url = str(str(info).split("\"")[1]).strip()
    if house:
        temp = tr.find_all("td")[1].text.strip() + " Congressional District"
        if len(temp.split(",")) < 2:
            district = temp
        state = district.split()[0]
        if state == "South" or state == "North" or state == "New":
            state = state + " " + district.split[1]

        partyShort = tr.find_all("td")[2].text.strip()
        party = ""

        if partyShort == "R":
            party = "Republican"
        else:
            party = "Democratic"

        current = [realname, state, party, district, url]
    else:
        state = tr.find_all("td")[1].text
        party = tr.find_all("td")[2].text
        current = [realname, state, party, url]
    return current


header = True
for tr in senateSoup.findAll('table')[0].findAll('tr'):
    if header:
        header = False
    else:
        senate.append(get_info(tr, False))

house_URL = "https://www.house.gov/representatives"
house_page = requests.get(house_URL).text
houseSoup = BeautifulSoup(house_page, 'html.parser')
house = []

for table in houseSoup.findAll('table'):
    for tr in table.findAll('tr'):
        try:
            house.append(get_info(tr, True))
        except:
            pass
senators = " \"senators\": ["
reps = " \"representatives\": ["

for senator in senate:
    senators = senators + json.dumps({"name": senator[0], "state": senator[1], "party": senator[2], "website": senator[3]},
                              sort_keys=True, indent = 4) + ", "
senators = senators[:-2]
senators = senators + "], "
for rep in house:
    reps = reps + json.dumps({"name": rep[0], "state": rep[1], "party": rep[2], "district": rep[3], "website": rep[4]},
                              sort_keys=True, indent = 4) + ", "
reps = reps[:-2]
reps = reps + "]"
congress = "{ " + senators + reps + " }"
with open("info.json", "w") as info:
    info.write(congress)
info.close()
