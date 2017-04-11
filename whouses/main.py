# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys


from whouses.github_stats import get_github_stats
from whouses.pypi_stats import get_pypi_stats


def main(args):
    name = args[0]

    get_pypi_stats(name)
    print('')
    get_github_stats(name)


def cmdline():
    sys.exit(main(sys.argv[1:]))
