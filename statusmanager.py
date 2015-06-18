from dbmanager import PMDbManager
import threading
import re
import time
import os


class PMPingThread:
    def __init__(self, server):
        self.server = server
        self.status = "Pending"
        self.cycle_pause = 2
        self.stopped = False
        self.thread = threading.Thread(target=self.ping_loop)
        self.thread.start()

    def ping_loop(self):
        while True:
            if self.stopped:
                break
            ping_output = os.popen('ping -W 2 -c 1 ' + self.server).read()
            host_state = re.search('time=(\d+\.*\d+\s)ms', ping_output)
            if host_state is not None:
                time.sleep(self.cycle_pause)
                self.status = '{} ms'.format(host_state.group(1))
            else:
                self.status = 'offline'

    def stop(self):
        self.cycle_pause = 0
        self.stopped = True


class PMStatusManager:
    def __init__(self, db_manager: PMDbManager):
        self.db = db_manager
        self.storage = {}
        self.start_all()

    def start_all(self):
        for i in self.db.get_servers():
            if i[2] not in self.storage:
                self.storage[i[2]] = {i[0]:PMPingThread(i[1])}
            else:
                self.storage[i[2]][i[0]] = PMPingThread(i[1])

    def get_group(self, group_id):
        return  self.storage[int(group_id)]


    def stop_all(self):
        for group in self.storage:
            for server in self.storage[group]:
                self.storage[group][server].stop()
        self.storage = {}

    def restart(self):
        self.stop_all()
        self.start_all()
