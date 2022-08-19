#from urllib.parse import urlparse 
from six.moves.urllib.parse import urlparse

def parse_domain(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    scheme = parsed.scheme
    full_domain_name = scheme + "://" + domain

    return full_domain_name
