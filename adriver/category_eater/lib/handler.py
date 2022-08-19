from exceptions import *
from utils import parse_domain
import logging


logger = logging.getLogger(__name__)

class CategoryHandler:

    def __init__(self, category_collector, clients_conf):
        self.collector = category_collector
        self._clients_conf = clients_conf
	
       # try:
       #     self.collector.connect()
	#    print("Connected")
      #  except Exception as e:
	
       #     logger.exception("Couldn't connect to server because of error: " + str(e))
        #    raise

    def get_result(self, req, site_id, url):
	self.collector.connect()
        if site_id and url:
            client_conf = self._clients_conf[site_id]
            if client_conf.enabled:
                referer = req.referer
                domain = parse_domain(url)

                if client_conf.referers_access.check(domain):

                    if parse_domain(url) != parse_domain(referer):
			logger.exception("Domain and referer doesn't match")
                        raise InvalidRequest("Domain and referer doesn't match")
                    else:
		        print("Inside of categories")
                        categories = self.collector.get_categories_id_from_url(url)

                        allowed_categories = client_conf.categories_access.filter(categories)

                    return allowed_categories
