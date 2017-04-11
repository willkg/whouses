# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import csv
import os
import string

from github3 import GitHub, login


def get_auth():
    path = os.path.expanduser('~/.githubauth')
    if os.path.exists(path):
        return open(path, 'r').read().strip().split(':')
    return None


def two_factor_callback():
    code = ''
    while not code:
        code = input('Enter 2fa: ')
    return code


def get_github_stats_as_csv(python_module):
    auth = get_auth()
    if auth:
        gh = login(auth[0], auth[1], two_factor_callback=two_factor_callback)
    else:
        gh = GitHub()

    query = '%s language:python' % python_module
    print('Searching github for "%s"' % query)
    res = gh.search_code(
        query=query,
        per_page=100
    )

    filename = 'uses_%s.csv' % ''.join(
        [c for c in python_module if c in (string.ascii_letters + string.digits)]
    )

    all_repos = set()

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'full_name',
            'url',
            'stars',
            'last_event',
        ])

        for i, item in enumerate(res):
            repo = item.repository

            # We get duplicate entries, so throw them in a set so we don't add
            # them all to our csv which isn't helpful.
            if repo.full_name in all_repos:
                continue
            all_repos.add(repo.full_name)

            print((i, item, item.repository))

            # FIXME(willkg): grab the date of the last commit and use the most
            # recent of the two. Seems like GitHub doesn't keep event history
            # older than 3 months.
            events = list(repo.events(10))
            if events:
                last_event_at = events[0].created_at
            else:
                last_event_at = ''

            writer.writerow([
                repo.full_name,
                repo.html_url,
                len(list(repo.stargazers())),
                last_event_at,
            ])

    for repo in all_repos:
        print(repo)

    print('Wrote %s' % filename)
    print('Done!')


def get_github_stats(name):
    print('Github stats')
    auth = get_auth()
    if auth:
        gh = login(auth[0], auth[1], two_factor_callback=two_factor_callback)
    else:
        gh = GitHub()

    query = '"import %(name)s" OR "from %(name)s" language:python' % {'name': name}
    print('    Searching github for "%s"' % query)
    res = gh.search_code(
        query=query,
        per_page=100
    )

    # Map of repo.full_name -> data
    repo_data = {}

    for i, item in enumerate(res):
        repo = item.repository

        if repo.full_name in repo_data:
            continue

        # FIXME(willkg): grab the date of the last commit and use the most
        # recent of the two. Seems like GitHub doesn't keep event history
        # older than 3 months.
        events = list(repo.events(10))
        if events:
            last_event_at = events[0].created_at
        else:
            last_event_at = ''

        repo_data[repo.full_name] = {
            'full_name': repo.full_name,
            'url': repo.html_url,
            'stars': len(list(repo.stargazers())),
            'last_event': last_event_at,
        }

    # Map of project name -> list of users
    project_names = {}
    for repo in repo_data:
        user, project = repo.split('/')
        project_names.setdefault(project, []).append(user)

    # Print 10 top stars
    print('    By stars:')
    for repo_data in sorted(repo_data.values(), key=lambda x: x['stars'], reverse=True)[:20]:
        print('        %s: %s  (%s)' % (repo_data['full_name'], repo_data['stars'], repo_data['url']))
    print('')

    # Print by repeats
    print('    By user repeats:')
    for project, users in sorted(project_names.items(), key=lambda x: len(x[1]), reverse=True):
        print('        %s: %s' % (project, ', '.join(users)))
    print('')
