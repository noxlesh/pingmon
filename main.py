#!/usr/bin/python2
# -*- coding: utf-8 -*-

from config import PMConf
import pingmon
import server

conf = PMConf('server')
stats = conf.get_stats()

print stats

# stats = load_host_list(file)
#
# for host in stats:
#     #print host
#     thread.start_new_thread(ping_print, (stats.index(host),)
