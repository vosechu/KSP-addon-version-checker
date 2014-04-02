#!/usr/bin/env python2.7
#coding: utf8

"""
KSP Add-on Version Checker.
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

import config
import os, sys
import versionComparator as verComp
import modFinder

def main():
    # Find config folder.
    cfg_dir = os.path.join(os.path.expanduser('~'), '.KSP-AVC')
    # Create it if needed.
    if not os.path.exists(cfg_dir):
        os.makedirs(cfg_dir)

    # Create config object.
    #TODO Don't hardcode the file name.
    cfg = config.Config(os.path.join(cfg_dir, 'default.cfg'))

    print "+----------------------------------------------+"
    print "| Kerbal Space Program Add-on Version Checker  |"
    print "| This program is not made by Squad, nor is it |"
    print "|        Officially recognized by them.        |"
    print "+----------------------------------------------+"

    try:
        print verComp.compareAVCVersions()
    except Exception as e:
        print "[ERROR] Couldn't update KSP-AVC. %s" % e
        cfg.save()
        sys.exit(1)

    print "Starting add-on checks."
    toUpdate = set()
    mods = modFinder.find(cfg)
    for mod in mods:
        try:
            modname = mod['NAME']
            print "[ADD-ON] %s" % modname

            updateRequired = verComp.compareMod(mod)
            if updateRequired:
                print "  [UPDATE] Latest version: %s, Installed version: %s" % \
                    (comp.getVersion('r'), comp.getVersion('l'))
                toUpdate.add(modname)
        except Exception as e:
            print "[ERROR] Couldn't update module %s because %s" % modname, e

    # End for
    if len(toUpdate):
        print ""
        print "You should update the following add-ons:"
        print "    "+', '.join(toUpdate)
    else:
        print "%s add-ons found, and none require an update!" % len(mods)

    #Shutdown procedure
    cfg.save()
    sys.exit(0)

# Startup sequence
if __name__ == '__main__':
    main()

