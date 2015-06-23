from configmanager import PMConfig
from statusmanager import PMStatusManager
import httpserver
from dbmanager import PMDbManager

config = PMConfig()
db = PMDbManager(config.get_db_config())
status = PMStatusManager(db)

http_server = httpserver.PMHTTPServer(config.get_pm_address(),
                                      httpserver.PMHTTPRequestHandler,
                                      config, db, status)
try:
    http_server.serve_forever()
except KeyboardInterrupt:
    status.stop()
