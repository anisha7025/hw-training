import logging
import random
from shopclues.settings import *

logger = logging.getLogger(__name__)


def parse_proxy():

    PROXY = random.choice(PROXY_LIST)
    proxies = {"http": "http://%s" % PROXY, "https": "https://%s" % PROXY}
    logger.debug("Proxy added")
    return {'proxies': proxies}