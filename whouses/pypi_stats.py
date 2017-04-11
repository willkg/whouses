# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests


PYPI_URL = 'https://pypi.python.org'


def fix_name(name):
    url = PYPI_URL + '/pypi/' + name

    resp = requests.head(url)
    if resp.status_code == 200:
        return name
    elif resp.status_code == 301:
        loc = resp.headers['Location']
        return loc.split('/')[-1]
    else:
        raise Exception('Do not know what to do with %s' % resp.status_code)


def get_json_data(name):
    url = PYPI_URL + '/pypi/' + name + '/json'

    resp = requests.get(url)
    data = resp.json()
    return data


def get_pypi_stats(name):
    name = fix_name(name)

    data = get_json_data(name)

    print('PyPI stats')
    print('    Overall downloads:')
    print('        last month: %5d' % data['info']['downloads']['last_month'])
    print('        last week:  %5d' % data['info']['downloads']['last_week'])
    print('        last day:   %5d' % data['info']['downloads']['last_day'])
    print('')

    print('    Latest release:')
    for item in data['urls']:
        print('        %-36s  %6d %s' % (item['filename'], item['downloads'], item['upload_time']))
    print('')

    total_downloads = 0
    for name, item in data['releases'].items():
        for file_item in item:
            total_downloads += file_item['downloads']

    print('    Total downloads: %d' % total_downloads)
