from .base import *

DEBUG = True


WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'INDEX': 'flowpatrol'
    }
}


INSTALLED_APPS+= (
    'djcelery',
    'kombu.transport.django',
    'gunicorn',    
)


CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'KEY_PREFIX': 'flowpatrol',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        }
    }
}

# Use the cached template loader
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# CELERY SETTINGS
import djcelery
djcelery.setup_loader()

BROKER_URL = 'redis://'
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERYD_LOG_COLOR = False


try:
	from .local import *
except ImportError:
	pass

MANDRILL_API_KEY = 'Z7vKU6m7pINJuxiUMco9Yw'
