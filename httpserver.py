import http.server as http
from mako.template import Template
from urllib.parse import parse_qs, unquote

tpl_path = lambda req_path: "templates{}".format(req_path)
str_to_byte = lambda unicode_string: bytes(unicode_string, 'UTF-8')


class PMHTTPServer(http.HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, config, db, status):
        self.config = config
        self.status = status
        self.db = db
        super().__init__(server_address, RequestHandlerClass)


class PMHTTPRequestHandler(http.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.config = server.config
        self.status = server.status
        self.db = server.db
        super().__init__(request, client_address, server)

    # GET requests router
    def do_GET(self):
        if self.path == '/favicon.ico':
            file = open(tpl_path(self.path), 'rb')
            self.response_headers(200, "image/x-icon")
            self.wfile.write(file.read())
            file.close()
        elif self.path.endswith('.js'):
            file = open(tpl_path("/js" + self.path), 'rb')
            self.response_headers(200, "application/javascript")
            self.wfile.write(file.read())
            file.close()
        elif self.path.endswith('.css'):
            file = open(tpl_path("/css" + self.path), 'rb')
            self.response_headers(200, "text/css")
            self.wfile.write(file.read())
            file.close()
        else:
            if self.path == '/':
                self.path = '/index'
            # Status page
            if self.path == '/index':
                data = {'groups': self.db.get_grouped_servers()}
            # Groups page
            elif self.path == '/admin':
                data = {'groups': self.db.get_group_list()}
            # Servers page
            elif self.path.startswith('/admin/'):
                group_id = int(self.path[7::])
                print(group_id)
                if group_id in self.db.get_group_list(id_list=True):
                    data = {'servers': self.db.get_servers(group_id),
                            'name': self.db.get_group_name(group_id),
                            'group_id': group_id}
                    self.path = "/admin_group"
                else:
                    data = {'requested_url': self.path}
                    self.path = '/404'
            else:
                data = {'requested_url': self.path}
                self.path = '/404'
            template = Template(filename='templates{}.html'.format(self.path))
            html = template.render(**data)
            self.response_headers(200, "text/html")
            self.wfile.write(str_to_byte(html))

    # POST requests router
    def do_POST(self):
        print(self.path)
        print(self.headers['content-type'].lower())
        #
        # If received from the AJAX
        if self.path == '/index':
            if self.headers['content-type'].lower().startswith('application/x-www-form-urlencoded'):
                length = int(self.headers['content-length'])
                params = parse_qs(self.rfile.read(length).decode(), keep_blank_values=True)
                if 'group' in params:
                    group_id = params['group'][0]
                    data = {'group': self.server.status.get_group(group_id)}
                    template = Template(filename='templates/ajax_status.html')
                    html = template.render(**data)
                    self.response_headers(200, "text/html")
                    self.wfile.write(str_to_byte(html))
        # If  received from the admin form
        elif self.path == '/admin':
            if self.headers['content-type'].lower().startswith('application/x-www-form-urlencoded'):
                length = int(self.headers['content-length'])
                params = parse_qs(self.rfile.read(length).decode(), keep_blank_values=True)
                print(params)
                if 'delete' in params:
                    for group_id in params['delete']:
                        self.db.del_group(int(group_id))
                    self.status.restart()
                    self.redirect('/admin')
                elif 'add' in params:
                    self.db.add_group(params['add'][0].capitalize())
                    self.status.restart()
                    self.redirect('/admin')
                elif 'edit' in params:
                    group_id = params['group_id'][0]
                    new_name = params['edit'][0]
                    self.db.edit_group(group_id, new_name)
                    self.status.restart()
                    self.redirect('/admin')
                else:
                    self.response_headers(404, "text/html")
        # If received from the server form
        elif self.path.startswith('/admin/'):
            group_id = int(self.path[7::])
            if group_id in self.db.get_group_list(id_list=True):
                if self.headers['content-type'].lower().startswith('application/x-www-form-urlencoded'):
                    length = int(self.headers['content-length'])
                    params = parse_qs(self.rfile.read(length).decode(), keep_blank_values=True)
                    if 'delete' in params:
                        for server_id in params['delete']:
                            self.db.del_server(server_id)
                        self.status.restart()
                        self.redirect('/admin/{}'.format(group_id))
                    elif 'add' in params:
                        name = params['add'][0].capitalize()
                        address = params['address'][0]
                        self.db.add_server(group_id, name, address)
                        self.status.restart()
                        self.redirect('/admin/{}'.format(group_id))
                    elif 'edit' in params:
                        desc = params['edit'][0]
                        addr = params['address'][0]
                        server_id = params['server_id'][0]
                        self.db.edit_server(server_id, desc, addr)
                        self.status.restart()
                        self.redirect('/admin/{}'.format(group_id))
        # If received params are unknown
        else:
            self.response_headers(404, "text/html")
            self.wfile.write(str_to_byte('Invalid request!'))

    # HTTP headers
    def response_headers(self, resp_code, content_type):
        self.send_response(resp_code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def redirect(self, location):
        self.send_response(301,message='Moved permanently')
        self.send_header('Location', '{}'.format(location))
        self.end_headers()
