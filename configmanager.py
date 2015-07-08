import os
import json


class PMConfig(object):
    def __init__(self, config_filename="config.json"):
        self.working_dir = os.path.dirname(os.path.abspath(__file__))
        self.conf_file_path = '{}/{}'.format(self.working_dir, config_filename)
        if os.path.exists(self.conf_file_path):
            with open(self.conf_file_path, 'r') as config_file:
                self.props = json.load(config_file)
        else:
            raise Exception('Can\'t open config file!')

    def save(self):

        with open(self.conf_file_path, 'w') as config_file:
            config = json.dumps(self.props,
                                ensure_ascii=False,  # It makes human readable a non-ascii str of the config
                                indent=2,
                                sort_keys=True)
            config_file.write(config)

    def get_pm_address(self):
        return self.props['address'], self.props['port']

    def get_db_config(self):
        return self.props['db']
