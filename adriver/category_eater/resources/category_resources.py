import logging

from adriver.category_eater.lib.exceptions import *
from adriver.category_eater.lib.handler import CategoryHandler

logger = logging.getLogger(__name__)
requests_log = logging.getLogger("adriver.category_eater.requests")


class CategoryResource:
    BLANK_RESPONSE = []

    def __init__(self, servers, config):
        self.servers = servers
        self.config = config
        self.cats = CategoryHandler(self.servers, self.config)
        self.res = []

    def on_get(self, req, resp):
        user_agent = req.user_agent
        ip_address = req.remote_addr
        referer = req.referer
	#print(user_agent,ip_address,referer)
        try:
            site_id = req.get_param("siteId")
        except InvalidRequest:
            logger.exception("Param doesn't exists in query string")
            resp.media = []
            return resp.media
	
	if site_id:
	    try:
                site_id = int(site_id)	
	    except ValueError:
		resp.media = []
	        return resp.media, "Invalid site id"
        try:
            url = req.get_param("url")
	    print(url)
        except InvalidRequest:
            logger.exception("Param doesn't exists in query string")
            resp.media = []
            return resp.media

        try:
            self.res = self.cats.get_result(req, site_id, url)
        except CategoryException as e:
            logger.exception("Category error " + str(e))
            resp.media = []
            return resp.media, "Category error"
        except Exception as e:
            logger.error("Unknown error happens " + str(e))
            return "Unknown error " + str(e)
        else:
	    if self.res:
            	resp.media = {"results": self.res}
		requests_log.info("url: {}, siteId: {}, IP: {}, User-Agent: {},Referer {}, Categories: {}".format(url,
                                                                                                   site_id,
                                                                                                   ip_address,
                                                                                                   user_agent,
                                                                                                   referer,
                                                                                                   self.res))

	    else:
 		resp.media = {"results": []}
            return resp.media
#        finally:
#            requests_log.info("url: {}, siteId: {}, IP: {}, User-Agent: {},Referer {}, Categories: {}".format(url,
#                                                                                                   site_id,
#                                                                                                   ip_address,
#                                                                                                   user_agent,
#                                                                                                   referer,
#                                                                                                   self.res))
