#!/usr/bin/python2
# -*- coding: utf-8 -*-

import re
import time
import os
import thread
import BaseHTTPServer

__author__ = 'noxlesh'
SRV_HOSTNAME = 'pingmon'
SRV_PORT = 8080
HOSTS_LIST_FILE = 'servers'
stats = []


def load_host_list(filename):
    stats = []
    f = open(filename, 'r')
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
            stats.append(stats_data)
        else:
            is_remote = True
    return stats


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        if s.path.endswith('.js'):
            f = open(s.path[1::])
            s.send_response(200)
            s.send_header("Content-type", "application/javascript")
            s.end_headers()
            s.wfile.write(f.read())
        elif s.path.endswith('.css'):
            f = open(s.path[1::])
            s.send_response(200)
            s.send_header("Content-type", "text/css")
            s.end_headers()
            s.wfile.write(f.read())
        else:
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            #s.wfile.write(s.path)
            s.wfile.write(gen_html(stats,3))


def gen_html(ping_stats, page_refr_time):
    html = '<!DOCTYPE html>\n' \
           '<html lang="ru"><head>\n'
    if page_refr_time:# refresh equal zero for debug
        html += '<meta http-equiv="refresh" content="%s">\n' % page_refr_time
    html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' \
            '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' \
            '<link href="css/bootstrap.min.css" rel="stylesheet" media="screen">\n' \
            '<link rel="stylesheet" href="css/bootstrap-theme.min.css">\n' \
            '</head><body>\n' \
            '<div class="container"><div class="row"><div class="col-xs-6">\n' \
            '<h4>Локальные хосты</h4>' \
            '<table class="table table-bordered"><thead>\n' \
            '<tr><th>Hostname</th><th>IP Address</th><th>Status</th></tr>\n' \
            '</thead><tbody>\n'
    for server in ping_stats:
        if server[2] == 'l':
            if server[3] == 'offline':
                html += '<tr class="danger">'
            else:
                html += '<tr>'
            html += '<td>%s</td><td>%s</td><td>%s</td>\n' %(server[0], server[1], server[3])
    html += '</tbody>\n' \
            '</table></div><div class="col-xs-6">\n' \
            '<h4>VPN хосты</h4>' \
            '<table class="table table-bordered">\n' \
            '<thead>\n' \
            '<tr><th>Hostname</th><th>IP Address</th><th>Status</th></tr>\n' \
            '</thead>\n' \
            '<tbody>\n'
    for server in ping_stats:
        if server[2] == 'r':
            if server[3] == 'offline':
                html += '<tr class="danger">'
            else:
                html += '<tr>'
            html += '<td>%s</td><td>%s</td><td>%s</td>\n' %(server[0], server[1], server[3])
    html += '</tbody></table>\n' \
            '</div></div></div>\n' \
            '<script src="js/jquery.min.js"></script>\n' \
            '<script src="js/bootstrap.min.js"></script>\n' \
            '</body>\n' \
            '</html>\n'
    return html


def ping_print(index):
    while 1:
        ping_output = os.popen('ping -c 1 ' + stats[index][1]).read()
        host_state = re.search('time=(\d+\.*\d+\ )ms', ping_output)
        if host_state is not None:
            stats[index][3] = host_state.group(1) + ' ms'
            time.sleep(2)
        else:
            stats[index][3] = 'offline'
            time.sleep(1)

stats = load_host_list(HOSTS_LIST_FILE)

for host in stats:
    #print host
    thread.start_new_thread(ping_print, (stats.index(host),))

server_class = BaseHTTPServer.HTTPServer
httpd = server_class((SRV_HOSTNAME, SRV_PORT), MyHandler)
try:
        httpd.serve_forever()
except KeyboardInterrupt:
        pass
httpd.server_close()

