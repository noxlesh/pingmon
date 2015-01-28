# -*- coding: utf-8 -*-
import os


class PMConf (object):
    tables = {}  # Categories of hosts
    stats = {}  # Statistics data

    def __init__(self, hosts_file_path, hostname='localhost', port=8080):
        self.hostname = hostname
        self.port = port
        if os.path.exists(hosts_file_path):
            self.h_file = open(hosts_file_path, 'r')
        else:
            raise Exception('Can\'t open hosts file!')

    def get_stats(self):
        return self.stats

    def load_host_list(self):
        f = open(self.h_file, 'r')
        lines = f.readlines()
        is_remote = False
        for line in lines:
            if line != '\r\n':
                stats_data = line.split(":")
                stats_data[1] = stats_data[1][:-2:]
                if not is_remote:
                    stats_data.append('l')
                else:
                    stats_data.append('r')
                stats_data.append('pending')
                self.stats.append(stats_data)
            else:
                is_remote = True