#coding: utf8
"""
The modFinder class hunts through the system looking for mods to compare
"""
# Copyright 2014 Dimitri "Tyrope" Molenaars, Chuck Lauer Vose (@vosechu)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

class ModFinder(object):
    def __init__(self, config):
        self.config = config

    def findMods(self):
        mods = set()
        for path, folders, files in os.walk(self.config.get('gamedata_dir')):
            for f in files:
                if f.lower().endswith(".version"):
                    mods.add(os.path.join(path, f))
        return mods

def find(config):
    mf = ModFinder(config)
    return mf.findMods()
