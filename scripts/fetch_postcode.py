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

    counts = {
        'divisions': 0,
        'districts': 0,
        'thanas': 0,
        'offices': 0,
    }
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

        counts['divisions'] += 1
        division = codes[division]
        pdist, pthana = '', ''
        for row in rows:
            district, thana, po, code = [col.text for col in row.findAll('td')]
            if district == 'IBH WAs Here':
                district = 'Bagerhat'

            if pdist != district:
                pdist = district
                counts['districts'] += 1
            if pthana != thana:
                pthana = thana
                counts['thanas'] += 1
            counts['offices'] += 1

            division[district][thana].append((po, code))

    return codes, counts


if __name__ == '__main__':
    data, counts = get_codes()
    codes = {
        'data': data,
        'meta': {
            'updated_at': datetime.utcnow().isoformat(),
            'source': SOURCE,
            'counts': counts,
        },
    }
    print(json.dumps(codes))
