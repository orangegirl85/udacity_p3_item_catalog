mport sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/udacity_p3_item_catalog")
from app import app as application
application.secret_key = 'catalog_secret'
