"""
Author: Anurag Rana
Site: https://www.pythoncircle.com
"""

import requests
from bs4 import BeautifulSoup
import json
from lxml import html
import time

NOT_FOUND = 404
states = ["U0" + str(u) for u in range(1, 8)] + ["S0" + str(s) if s < 10 else "S" + str(s) for s in range(1, 30)]

# base_url = "http://results.eci.gov.in/pc/en/constituencywise/ConstituencywiseS2910.htm?ac=10"
base_url = "http://results.eci.gov.in/pc/en/constituencywise/Constituencywise"

results = list()

for state in states:
    for constituency_code in range(1, 99):
        url = base_url + state + str(constituency_code) + ".htm?ac=" + str(constituency_code)
        # print("URL", url)
        response = requests.get(url)

        # if some state and constituency combination do not exists, 404, continue for next state
        if NOT_FOUND == response.status_code:
            break

        response_text = response.text

        soup = BeautifulSoup(response_text, 'lxml')
        tbodies = list(soup.find_all("tbody"))
        # 11the tbody from top is the table we need to parse
        tbody = tbodies[10]
        trs = list(tbody.find_all('tr'))

        # all data for a constituency seat is stored in this dictionary
        seat = dict()
        seat["candidates"] = list()
        for tr_index, tr in enumerate(trs):
            # row at index 0 contains name of constituency
            if tr_index == 0:
                state_and_constituency = tr.find('th').text.strip().split("-")
                seat["state"] = state_and_constituency[0].strip().lower()
                seat["constituency"] = state_and_constituency[1].strip().lower()
                continue

            # first and second rows contains headers, ignore
            if tr_index in [1, 2]:
                continue

            # for rest of the rows, get data
            tds = list(tr.find_all('td'))

            candidate = dict()

            # if this is last row get total votes for this seat
            if tds[1].text.strip().lower() == "total":
                seat["evm_total"] = int(tds[3].text.strip())
                if "jammu & kashmir" == seat["state"]:
                    seat["migrant_total"] = int(tds[4].text.strip())
                    seat["post_total"] = int(tds[5].text.strip())
                    seat["total"] = int(tds[6].text.strip())
                else:
                    seat["post_total"] = int(tds[4].text.strip())
                    seat["total"] = int(tds[5].text.strip())
                continue
            else:
                candidate["candidate_name"] = tds[1].text.strip().lower()
                candidate["party_name"] = tds[2].text.strip().lower()
                candidate["evm_votes"] = int(tds[3].text.strip().lower())
                if "jammu & kashmir" == seat["state"]:
                    candidate["migrant_votes"] = int(tds[4].text.strip().lower())
                    candidate["post_votes"] = int(tds[5].text.strip().lower())
                    candidate["total_votes"] = int(tds[6].text.strip().lower())
                    candidate["share"] = float(tds[7].text.strip().lower())
                else:
                    candidate["post_votes"] = int(tds[4].text.strip().lower())
                    candidate["total_votes"] = int(tds[5].text.strip().lower())
                    candidate["share"] = float(tds[6].text.strip().lower())

        seat["candidates"].append(candidate)

    # print(json.dumps(seat, indent=2))
    results.append(seat)
    print("Collected data for", seat["state"], state, seat["constituency"], constituency_code, len(results))
    # Do not send too many hits to server. be gentle. wait.
    time.sleep(0.5)

# write data to file
with open("election_data.json", "a+") as f:
    f.write(json.dumps(results, indent=2))
