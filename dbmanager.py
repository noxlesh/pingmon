from mysql import connector


class PMDbManager:
    def __init__(self, db_config):
        self.config = db_config
        self.connection = connector.connect(**self.config)
        conn_state_str = "Connected" if self.connection.is_connected() else "Not connected"
        print('{} to {} db'.format(conn_state_str, self.connection.database))

    def connect_if_not(self):
        if not self.connection.is_connected():
            self.connection = connector.connect(**self.config)

    def add_group(self, group):
        self.connect_if_not()
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO groups (name) VALUES('{}')".format(group))
        self.connection.commit()
        cursor.close()

    def add_server(self, group_id, server, address):
        self.connect_if_not()
        cursor = self.connection.cursor()
        add_srv_query = ("INSERT INTO servers (group_id, name, address)"
                         "VALUES ({}, '{}', '{}')".format(group_id, server, address))
        cursor.execute(add_srv_query)
        self.connection.commit()
        cursor.close()

    def del_group(self, group_id):
        self.connect_if_not()
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM groups WHERE id={}".format(group_id))
        self.connection.commit()
        cursor.close()

    def del_server(self, server_id):
        self.connect_if_not()
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM servers WHERE server_id={}".format(server_id))
        self.connection.commit()
        cursor.close()

    def get_group_name(self, group_id):
        self.connect_if_not()
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM groups WHERE id={}".format(group_id))
        row_list = cursor.fetchall()
        cursor.close()
        return  row_list[0][0]

    def get_group_list(self, id_list=False):
        self.connect_if_not()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM groups")
        row_list = cursor.fetchall()
        cursor.close()
        if id_list:
            return [g[0] for g in row_list]
        else:
            return row_list

    def get_grouped_servers(self):
        self.connect_if_not()
        group_list = self.get_group_list()
        output_list = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM servers")
        server_list = cursor.fetchall()
        cursor.close()
        for group in group_list:
            grouped_servers = []
            for server in server_list:
                if group[0] == server[2]:
                    grouped_servers.append((server[1], server[3]))  #  tuple (name, address)

            output_list.append((group[0], group[1], grouped_servers))
        return output_list

    def get_servers(self, group_id=False):
        self.connect_if_not()
        cursor = self.connection.cursor()
        if group_id:
            cursor.execute("SELECT name, address, server_id FROM servers WHERE group_id={}".format(group_id))
        else:
            cursor.execute("SELECT name, address, group_id FROM servers")
        row_list = cursor.fetchall()
        cursor.close()
        return row_list
