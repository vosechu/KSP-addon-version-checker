#coding: utf8
"""
The versionComparator class uses 2
provided *.version files and
allows comparing of the contents.
"""
# Copyright 2014 Dimitri "Tyrope" Molenaars

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json, os
from urllib2 import urlopen

class VersionComparator(object):
    """ Initialize the comparator. """
    def __init__(self, localVersion, remoteVersion):
        with open(localVersion, 'r') as f:
            self.local = json.load(f)
        f = urlopen(remoteVersion)
        self.remote = json.load(f)
        f.close()

    """ Compare two modules. Returns a printable string if there is a version difference """
    def compare(self):
        if not self.__compareName():
            raise Exception("Remote version file is for %s" % self.remote['NAME'])
        if not self.__compareURL():
            raise Exception("Remote version file reports different URL.")
        if not self.__compareVersion():
            return "  [UPDATE] A new version(%s) of %s is available. (You have %s)" % \
            (self.__getVersion('r'), self.local['NAME'], self.__getVersion('l'))

    def __compareVersion(self):
        return self.__compareMajor and self.__compareMinor

    def __compareMajor(self):
        return self.local['VERSION']['MAJOR'] == self.remote['VERSION']['MAJOR']

    def __compareMinor(self):
        return self.local['VERSION']['MINOR'] == self.remote['VERSION']['MINOR']

    # TODO: Add __comparePatch to be inline with semantic versioning http://semver.org/

    def __getVersion(self, side):
        if side in ('l','local'):
            v = self.local
        elif side in ('r', 'remote'):
            v = self.remote
        else:
            return '0.0'
        return '%s.%s' % (v['VERSION']['MAJOR'], v['VERSION']['MINOR'])

    def __compareURL(self):
        return self.local['URL'] == self.remote['URL']

    def __compareName(self):
        return self.local['NAME'] == self.remote['NAME']

""" Discover whether AVC itself needs to be updated """
def compareAVCVersions():
    localVersion = os.path.join(os.path.expanduser('.'), 'KSP-AVC.version')
    remoteVersion = __getRemote(localVersion)
    vc = VersionComparator(localVersion, remoteVersion)
    return vc.compare()

""" Discover whether a mod needs to be updated """
def compareMod(local):
    remoteVersion = verComp.__getRemote(local['URL'])
    vc = VersionComparator(localVersion, remoteVersion)
    return vc.compare()

def __getRemote(fle):
    if not os.path.exists(fle):
        raise OSError("File not found.")

    with open(fle,'r') as f:
        json_dec = json.load(f)
    return json_dec['URL']

if __name__ == '__main__':
    print __doc__