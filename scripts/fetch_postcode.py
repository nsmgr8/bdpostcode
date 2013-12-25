#!/usr/bin/env python

import json
from datetime import datetime
from collections import defaultdict

import requests
from BeautifulSoup import BeautifulSoup


SOURCE = 'http://www.bangladeshpost.gov.bd/PostCode.asp'
LIST_PAGE = 'http://www.bangladeshpost.gov.bd/PostCodeList.asp?DivID={}'


def get_codes():
    """
    Fetch all available Bangladesh post codes

    :returns: a nested dictionary of
        {division: district: thana: (suboffice, postcode)}
    """
    codes = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for i in range(10):
        response = requests.get(LIST_PAGE.format(i))
        if response.status_code != 200:
            raise Exception('Cannot download page')
        soup = BeautifulSoup(response.content)

        code_table = soup.findAll('table')[-1]
        # last table lists all codes
        rows = code_table.findAll('tr')[1:]
        # ignore header row

        # find the parent table that holds division name
        div_table = code_table.parent
        for j in range(5):
            div_table = div_table.parent
        division = div_table.tr.text.splitlines()[1].strip()
        # second line has the division name
        if not division:
            continue

        division = codes[division]
        for row in rows:
            data = [col.text for col in row.findAll('td')]
            # columns: district, thana, suboffice, postcode
            division[data[0]][data[1]].append((data[2], data[3]))

    return codes


if __name__ == '__main__':
    codes = {
        'data': get_codes(),
        'meta': {
            'updated_at': datetime.utcnow().isoformat(),
            'source': SOURCE,
        },
    }
    print(json.dumps(codes))
