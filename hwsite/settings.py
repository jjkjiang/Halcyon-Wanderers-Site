try:
    from .prod_settings import *
except:
    from .dev_settings import *
