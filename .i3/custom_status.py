#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script is a simple wrapper which prefixes each i3status line with custom
# information. It is a python reimplementation of:
# http://code.stapelberg.de/git/i3status/tree/contrib/wrapper.pl
#
# To use it, ensure your ~/.i3status.conf contains this line:
#     output_format = "i3bar"
# in the 'general' section.
# Then, in your ~/.i3/config, use:
#     status_command i3status | ~/i3status/contrib/wrapper.py
# In the 'bar' section.
#
# In its current version it will display the cpu frequency governor, but you
# are free to change it to display whatever you like, see the comment in the source code below.
#
# © 2012 Valentin Haenel <valentin.haenel@gmx.de>
#
# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law. You can redistribute it and/or modify it under
# the terms of the Do What The Fuck You Want To Public License (WTFPL), Version
# 2, as published by Sam Hocevar. See http://sam.zoy.org/wtfpl/COPYING for more
# details.

import sys
import json
import re
import subprocess
import os

id_re = re.compile(r"_NET_ACTIVE_WINDOW\(WINDOW\): window id # (.*?)\n")
name_re = re.compile(r"_NET_WM_NAME\(UTF8_STRING\) = \"(.*?)\"\n")

def get_name():
    curr_name = ""
    try:
        output = subprocess.check_output(["xprop", "-root"])
        curr_id = id_re.search(output).group(1)
        output = subprocess.check_output(["xprop", "-id", curr_id])
        curr_name = name_re.search(output).group(1)
    except:
        curr_name = ""

    if len(curr_name) > 48:
        curr_name = curr_name[:22] + " ... " + curr_name[-21:]
    else:
        pad = (48 - len(curr_name))/2
        curr_name = " " * pad + curr_name + " " * pad

    return curr_name

def eva():
    return u"\u25e2\u25a0\u25e4"

def eva_flip():
    return u"\u25e5\u25a0\u25e3"

def get_governor():
    """ Get the current governor for cpu0, assuming all CPUs use the same. """
    with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor') as fp:
        return fp.readlines()[0].strip()

def print_line(message):
    """ Non-buffered printing to stdout. """
    sys.stdout.write(message + '\n')
    sys.stdout.flush()

def read_line():
    """ Interrupted respecting reader for stdin. """
    # try reading a line, removing any extra whitespace
    try:
        line = sys.stdin.readline().strip()
        # i3status sends EOF, or an empty line
        if not line:
            sys.exit(3)
        return line
    # exit on ctrl-c
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    # Skip the first line which contains the version header.
    print_line(read_line())

    # The second line contains the start of the infinite array.
    print_line(read_line())

    color1 = '#6600cc'
    color2 = '#000000'
    color3 = '#afd700'

    try:
        while True:
            line, prefix = read_line(), ''
            # ignore comma at start of lines
            if line.startswith(','):
                line, prefix = line[1:], ','

            j = json.loads(line)
            # insert information into the start of the json, but could be anywhere
            # CHANGE THIS LINE TO INSERT SOMETHING ELSE
            j.insert(0, {'full_text' : '%s' % eva(), 'name' : 'eva0', 'color' : color3})
            j.insert(1, {'full_text' : '%s' % eva(), 'name' : 'eva1', 'color' : color2})
            j.insert(2, {'full_text' : '%s' % eva(), 'name' : 'eva2', 'color' : color1})
            j.insert(3, {'full_text' : '%48s' % get_name(), 'name' : 'win_name', 'color' : '#88ff00'})
            j.insert(4, {'full_text' : '%s' % eva_flip(), 'name' : 'eva3', 'color' : color1})
            j.insert(5, {'full_text' : '%s' % eva_flip(), 'name' : 'eva4', 'color' : color2})
            j.insert(6, {'full_text' : '%s' % eva_flip(), 'name' : 'eva5', 'color' : color3})
            # and echo back new encoded json
            print_line(prefix+json.dumps(j))
            # retarded animation
            # color1, color2, color3 = color3, color1, color2
    except BaseException as e:
        f = open("/home/jarsp/.i3/log", "rw+")
        f.write(e)
        f.close()
