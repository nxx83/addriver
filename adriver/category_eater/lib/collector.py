# coding: utf-8
import sys 
sys.path.append('/usr/local/rle/lib/python') 
import ReClients 
from ReClients import Vector_ReUrlCategoryGetInfo 
import logging

logger = logging.getLogger(__name__)


class CategoryIdCollector:

    def __init__(self, servers):

        self._client = ReClients.ReClients()
        self._servers = servers
        self._vector = Vector_ReUrlCategoryGetInfo()

    def connect(self):
        try:
            for server in self._servers:
                self._client.addServer(str(server), 1)
        except Exception:
            logging.exception("")

    def get_categories_id_from_url(self, url):
        categories_id = []

        ref = self._client.preprocessReferrer(url)
        url_id = self._client.getUrlId(ref)
        categories = self._client.getUrlCategories(url_id, self._vector)
        for index in range(categories):
            categories_id.append(self._vector[index].categoryId)

        return categories_id
