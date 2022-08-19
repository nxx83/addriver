from __future__ import unicode_literals, absolute_import, print_function

import os
import falcon
from adriver.category_eater.lib.config_load import ConfigLoader
import logging
from adriver.category_eater.lib.middleware import CORSComponent
from adriver.category_eater.resources.category_resources import CategoryResource
from adriver.category_eater.lib.collector import CategoryIdCollector
from adriver.category_eater.lib.client_config import *
import logging.config
import yaml



logger = logging.getLogger(__name__)
config_loader = ConfigLoader('category_eater')
clients_config_loc = os.path.join(os.environ.get('CONF_PATH'))
#log_conf = os.path.join(os.environ.get('CATEGORY_EATER_LOGGING_CONFIG'))


try:

    config_loader.configure_logging()
except Exception as e:
    logger.exception("Can not start app without config. Error while loading configs")
    raise
try:
    servers = config_loader.load_config().get("servers_config", {})
    clients_from_config = config_loader.load_config().get("clients_path",{})
    cl_cfg = config_loader.load_config(clients_from_config)


except Exception as e:
    logger.exception("Can not start app without config. Error while loading configs")
    raise

app = falcon.API(middleware=[CORSComponent()])
clients_conf = ConfigBuilder()

try:
    # TODO: category_collector = CategoryIdCollector(config.servers)
    # TODO: clients_config =  # Load configs

    clients = ConfigBuilder().build_config(cl_cfg)
    
    collector = CategoryIdCollector(servers)

    app.add_route('/api/v1/categories', CategoryResource(collector, clients))
except Exception as e:
    #print(clients_config)
    logger.exception("Something goes wrong. Can not start app normally")
    raise

