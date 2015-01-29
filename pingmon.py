# -*- coding: utf-8 -*-
import re
import time
import os




# def ping_print(index):
#     while 1:
#         ping_output = os.popen('ping -c 1 ' + stats[index][1]).read()
#         host_state = re.search('time=(\d+\.*\d+\ )ms', ping_output)
#         if host_state is not None:
#             stats[index][3] = host_state.group(1) + ' ms'
#             time.sleep(2)
#         else:
#             stats[index][3] = 'offline'
#             time.sleep(1)