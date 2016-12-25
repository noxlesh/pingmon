import http.server as http
import socket
from mako.template import Template
from urllib.parse import parse_qs

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
        self.tpl_path = "{}/templates".format(self.config.working_dir)
        self.timeout = 10
        super().__init__(request, client_address, server)
        
    # GET request router
    def do_GET(self):
        # Favicon file req.
        if self.path == '/favicon.ico':
            self.response_headers(200, "image/x-icon")
            with open(self.tpl_path + self.path, 'rb') as ico_file:
                self.wfile.write(ico_file.read())
        # Javascript file req.
        elif self.path.endswith('.js'):
            self.response_headers(200, "application/javascript")
            with open("{}/js{}".format(self.tpl_path, self.path), 'rb') as js_file:
                self.wfile.write(js_file.read())
        # CSS file req.
        elif self.path.endswith('.css'):
            self.response_headers(200, "text/css")
            with open("{}/css{}".format(self.tpl_path, self.path), 'rb') as css_file:
                self.wfile.write(css_file.read())
        # Dynamic content response
        else:
            tpl_file = '404.html'                       # If request is invalid
            tpl_data = {'requested_url': self.path}     #
            # Site root alias to status page
            if self.path == '/':
                self.path = '/index'
            # Status page req.
            if self.path == '/index':
                tpl_data = {'groups': self.db.get_grouped_servers()}
                tpl_file = 'index.html'
            # Groups page req.
            elif self.path == '/admin':
                tpl_data = {'groups': self.db.get_group_list()}
                tpl_file = 'admin.html'
            # Servers page req.
            elif self.path.startswith('/admin/'):
                group_id = int(self.path[7::])
                print(group_id)
                if group_id in self.db.get_group_list(id_list=True):
                    tpl_data = {'servers': self.db.get_servers(group_id),
                                'name': self.db.get_group_name(group_id),
                                'group_id': group_id}
                    tpl_file = 'admin_group.html'
            # Generate html and respond
            template = Template(filename='{}/{}'.format(self.tpl_path, tpl_file))
            html = template.render(**tpl_data)
            self.response_headers(200 if tpl_file != '404.html' else 404, "text/html")
            self.wfile.write(str_to_byte(html))

    # POST request router
    def do_POST(self):
        # Status page req.
        if self.path == '/index':
            if self.headers['content-type'].lower().startswith('application/x-www-form-urlencoded'):
                length = int(self.headers['content-length'])
                params = parse_qs(self.rfile.read(length).decode(), keep_blank_values=True)
                if 'group' in params:
                    group_id = params['group'][0]
                    data = {'group': self.server.status.get_group(group_id)}
                    template = Template(filename='{}/ajax_status.html'.format(self.tpl_path))
                    html = template.render(**data)
                    self.response_headers(200, "text/html")
                    self.wfile.write(str_to_byte(html))
        # Admin form req.
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
        # Server form req.
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
        # Invalid req.
        else:
            self.response_headers(404, "text/html")
            self.wfile.write(str_to_byte('Invalid request!'))

    # HTTP headers
    def response_headers(self, resp_code, content_type):
        self.send_response(resp_code)
        self.send_header("Content-type", content_type)
        self.end_headers()
    # HTTP redirect
    def redirect(self, location):
        self.send_response(301, message='Moved permanently')
        self.send_header('Location', '{}'.format(location))
        self.end_headers()
