#!/usr/bin/env python

# Copyright - 2013 - Rich Somerfield (rs@richsomerfield.com)
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import time
import re
import sys

##################################################################
class TermColor:
    pc = u'\033[95m'
    bc = u'\033[94m'
    gc = u'\033[92m'
    yc = u'\033[93m'
    rc = u'\033[91m'
    nc = u'\033[0m'

    def p(self, message):
        return u"" + self.pc + message + self.nc    
    def g(self, message):
        return u"" + self.gc + message + self.nc
    def b(self, message):
        return u"" + self.bc + message + self.nc
    def y(self, message):
        return u"" + self.yc + message + self.nc
    def r(self, message):
        return u"" + self.rc + message + self.nc

    def disable(self):
        self.pc = u''
        self.bc = u''
        self.gc = u''
        self.yc = u''
        self.rc = u''
        self.nc = u''

gColor = TermColor();

##################################################################
def follow(thefile):
    thefile.seek(0,2)      # Go to the end of the file
    sleep = 0.00001
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(sleep)    # Sleep briefly
            if sleep < 1.0:
                sleep += 0.00001
            continue
        sleep = 0.00001
        yield line

##################################################################
logfile = open("/var/log/system.log")
loglines = follow(logfile)

color = True
multiline = u""
for line in loglines:
    # Detect a non-tab line
    if re.search( u'^[^\t]', line): 
        if 0 < len(multiline):
            printline = True
            if ( 1 < len(sys.argv) ):
                if not re.search( sys.argv[1], multiline, re.IGNORECASE):
                    printline = False

            if printline:
                color = not color
                try:
                    if color:
                        print (gColor.y(multiline.strip(u'\n')))
                    else:
                        print (gColor.g(multiline.strip(u'\n')))
                except:
                    print (multiline)

        multiline = line
    elif 0 < len(multiline):
        multiline = multiline + line