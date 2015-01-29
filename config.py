# -*- coding: utf-8 -*-
import os


class PMConf (object):
    stats = {}  # Statistics data

    def __init__(self, hosts_file_path, hostname='localhost', port=8080):
        self.hostname = hostname
        self.port = port
        if os.path.exists(hosts_file_path):
            self.h_file = open(hosts_file_path, 'r')
        else:
            raise Exception('Can\'t open hosts file!')
        self.load_host_list()

    def get_stats(self):
        return self.stats

    def load_host_list(self):
        lines = self.h_file.readlines()
        for line in lines:
            if line.strip() != '':
                a = line.split(":")
                a_group = a[0]
                a_host_desc = a[1]
                a_host_addr = a[2].strip()
                if a_group not in self.stats:
                    self.stats[a_group] = [{a_host_desc: a_host_addr}]
                else:
                    self.stats[a_group].append({a_host_desc: a_host_addr})