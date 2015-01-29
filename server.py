# -*- coding: utf-8 -*-
import BaseHTTPServer


# def gen_html(ping_stats, page_refr_time):
#     html = '<!DOCTYPE html>\n' \
#            '<html lang="ru"><head>\n'
#     if page_refr_time:# refresh equal zero for debug
#         html += '<meta http-equiv="refresh" content="%s">\n' % page_refr_time
#     html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' \
#             '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' \
#             '<link href="css/bootstrap.min.css" rel="stylesheet" media="screen">\n' \
#             '<link rel="stylesheet" href="css/bootstrap-theme.min.css">\n' \
#             '</head><body>\n' \
#             '<div class="container"><div class="row"><div class="col-xs-6">\n' \
#             '<h4>Локальные хосты</h4>' \
#             '<table class="table table-bordered"><thead>\n' \
#             '<tr><th>Hostname</th><th>IP Address</th><th>Status</th></tr>\n' \
#             '</thead><tbody>\n'
#     for server in ping_stats:
#         if server[2] == 'l':
#             if server[3] == 'offline':
#                 html += '<tr class="danger">'
#             else:
#                 html += '<tr>'
#             html += '<td>%s</td><td>%s</td><td>%s</td>\n' %(server[0], server[1], server[3])
#     html += '</tbody>\n' \
#             '</table></div><div class="col-xs-6">\n' \
#             '<h4>VPN хосты</h4>' \
#             '<table class="table table-bordered">\n' \
#             '<thead>\n' \
#             '<tr><th>Hostname</th><th>IP Address</th><th>Status</th></tr>\n' \
#             '</thead>\n' \
#             '<tbody>\n'
#     for server in ping_stats:
#         if server[2] == 'r':
#             if server[3] == 'offline':
#                 html += '<tr class="danger">'
#             else:
#                 html += '<tr>'
#             html += '<td>%s</td><td>%s</td><td>%s</td>\n' %(server[0], server[1], server[3])
#     html += '</tbody></table>\n' \
#             '</div></div></div>\n' \
#             '<script src="js/jquery.min.js"></script>\n' \
#             '<script src="js/bootstrap.min.js"></script>\n' \
#             '</body>\n' \
#             '</html>\n'
#     return html
#
#
# class PingMonHttpReqHandler(BaseHTTPServer.BaseHTTPRequestHandler):
#     def do_HEAD(s):
#         s.send_response(200)
#         s.send_header("Content-type", "text/html")
#         s.end_headers()
#     def do_GET(s):
#         if s.path.endswith('.js'):
#             f = open(s.path[1::])
#             s.send_response(200)
#             s.send_header("Content-type", "application/javascript")
#             s.end_headers()
#             s.wfile.write(f.read())
#         elif s.path.endswith('.css'):
#             f = open(s.path[1::])
#             s.send_response(200)
#             s.send_header("Content-type", "text/css")
#             s.end_headers()
#             s.wfile.write(f.read())
#         else:
#             s.send_response(200)
#             s.send_header("Content-type", "text/html")
#             s.end_headers()
#             #s.wfile.write(s.path)
#             s.wfile.write(gen_html(stats,3))
#
# class PingMonHttpServer(object)
#
# server_class = BaseHTTPServer.HTTPServer
# httpd = server_class((SRV_HOSTNAME, SRV_PORT), MyHandler)
# try:
#         httpd.serve_forever()
# except KeyboardInterrupt:
#         pass
# httpd.server_close()
