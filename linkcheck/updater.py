# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2010 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
Function to check for updates.
"""

import os
from .configuration import Version
from .url import get_content
from distutils.version import StrictVersion

# Use the Freshmeat submit file as source since that file gets updated
# only when releasing a new version.
UPDATE_URL = "http://linkchecker.git.sourceforge.net/git/gitweb.cgi?p=linkchecker/linkchecker;a=blob_plain;f=linkchecker.freshmeat;hb=HEAD"
VERSION_TAG = 'Version:'
if os.name == 'nt':
    URL_TAG = 'Windows-installer-URL:'
else:
    URL_TAG = 'Source-Package-URL:'


def check_update ():
    """Return URL of new version, None if there is no update, or
    an error message if there was an error."""
    version, url = get_current_version()
    print "XXX", version, url
    if version is None:
        return False, url
    if is_newer_version(version):
        return True, url
    return True, None


def get_current_version ():
    """Download update info and parse it."""
    info, content = get_content(UPDATE_URL)
    if info is None:
        None, _('Could not check for updates.')
    version, url = None, None
    for line in content.splitlines():
        if line.startswith(VERSION_TAG):
            version = line.split(':', 1)[1].strip()
        elif line.startswith(URL_TAG):
            url = line.split(':', 1)[1].strip()
    return version, url


def is_newer_version (version):
    """Check if given version is newer than current version."""
    return StrictVersion(version) > StrictVersion(Version)