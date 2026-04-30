import logging
import os
import sys

from celery.schedules import crontab
from flask_caching.backends.filesystemcache import FileSystemCache

logger = logging.getLogger()

DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")

EXAMPLES_USER = os.getenv("EXAMPLES_USER")
EXAMPLES_PASSWORD = os.getenv("EXAMPLES_PASSWORD")
EXAMPLES_HOST = os.getenv("EXAMPLES_HOST")
EXAMPLES_PORT = os.getenv("EXAMPLES_PORT")
EXAMPLES_DB = os.getenv("EXAMPLES_DB")

SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_DIALECT}://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = os.getenv("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 24 * 3600,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG

FILTER_STATE_CACHE_CONFIG = {
    **CACHE_CONFIG,
    'CACHE_KEY_PREFIX': 'superset_filter_cache',
    'CACHE_DEFAULT_TIMEOUT': 7776000,
}

EXPLORE_FORM_DATA_CACHE_CONFIG = {
    **CACHE_CONFIG,
    'CACHE_KEY_PREFIX': 'superset_explore_form_data_cache',
    'CACHE_DEFAULT_TIMEOUT': 604800,
}

THUMBNAIL_CACHE_CONFIG = {
    **CACHE_CONFIG,
    'CACHE_KEY_PREFIX': 'superset_thumb_',
    'CACHE_DEFAULT_TIMEOUT': 604800,
    'CACHE_NO_NULL_WARNING': True,
}


class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = (
        "superset.sql_lab",
        "superset.tasks.scheduler",
        "superset.tasks.thumbnails",
        "superset.tasks.cache",
    )
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
        'cache-warmup-hourly': {
            'task': 'cache-warmup',
            'schedule': crontab(minute=1, hour='*'),
            'kwargs': {
                'strategy_name': 'top_n_dashboards',
                'top_n': 10,
                'since': '7 days ago',
            },
        },
    }


CELERY_CONFIG = CeleryConfig

ALERT_REPORTS_NOTIFICATION_DRY_RUN = False #True

WEBDRIVER_BASEURL = "http://superset:8088/"
WEBDRIVER_BASEURL_USER_FRIENDLY = (
    f"http://localhost:8888/{os.environ.get('SUPERSET_APP_ROOT', '/')}/"
)

WEBDRIVER_TYPE = "chromium"

SQLLAB_CTAS_NO_LIMIT = True

log_level_text = os.getenv("SUPERSET_LOG_LEVEL", "INFO")
LOG_LEVEL = getattr(logging, log_level_text.upper(), logging.INFO)

if os.getenv("CYPRESS_CONFIG") == "true":
    base_dir = os.path.dirname(__file__)
    module_folder = os.path.abspath(
        os.path.join(base_dir, "../../tests/integration_tests/")
    )
    sys.path.insert(0, module_folder)
    from superset_test_config import *  # noqa

    sys.path.pop(0)

try:
    import superset_config_docker
    from superset_config_docker import *  # noqa: F403

    logger.info(
        "Loaded your Docker configuration at [%s]", superset_config_docker.__file__
    )
except ImportError:
    logger.info("Using default Docker config...")

LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "pt_BR": {"flag": "br", "name": "Brazilian Portuguese"},
}

BABEL_DEFAULT_LOCALE = "pt_BR"

D3_FORMAT = {
    "decimal": ",",        
    "thousands": ".",      
    "grouping": [3],       
    "currency": ["R$ ", ""]
}

D3_TIME_FORMAT = {
    "dateTime": "%d/%m/%Y, %H:%M:%S",
    "date": "%d/%m/%Y",
    "time": "%H:%M:%S",
    "periods": ["AM", "PM"],
    "days": ["domingo", "segunda", "terça", "quarta", "quinta", "sexta", "sábado"],
    "shortDays": ["dom", "seg", "ter", "qua", "qui", "sex", "sab"],
    "months": ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
               "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"],
    "shortMonths": ["jan", "fev", "mar", "abr", "mai", "jun",
                    "jul", "ago", "set", "out", "nov", "dez"]
}

CURRENCIES = ["BRL","USD", "EUR"]

SMTP_HOST=os.getenv("SMTP_HOST")
SMTP_PORT=os.getenv("SMTP_PORT")
SMTP_STARTTLS = os.getenv("SMTP_STARTTLS", "false").lower() == "true"
SMTP_SSL_SERVER_AUTH = os.getenv("SMTP_SSL_SERVER_AUTH", "false").lower() == "true"
SMTP_SSL = os.getenv("SMTP_SSL", "false").lower() == "true"
SMTP_USER=os.getenv("SMTP_USER") 
SMTP_PASSWORD=os.getenv("SMTP_PASSWORD") 
SMTP_MAIL_FROM=os.getenv("SMTP_MAIL_FROM")

ENABLE_UI_THEME_ADMINISTRATION = True

BUILD_TRANSLATIONS = True

ENABLE_CORS = True
CORS_OPTIONS = {
    "origins": "*",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
}

FEATURE_FLAGS = {
    'ALERT_REPORTS': True,
    'DATASET_FOLDERS': True,
    'THUMBNAILS': True,
    'PLAYWRIGHT_REPORTS_AND_THUMBNAILS': True,
    'DASHBOARD_RBAC': True,
    'EMBEDDED_SUPERSET': True,
    'DISABLE_EMBEDDED_SUPERSET_LOGOUT': True,
    'GUEST_TOKEN': True,
}

#SESSION_COOKIE_SAMESITE = None
#SESSION_COOKIE_SECURE = True

GUEST_TOKEN_HEADER_NAME = "X-GuestToken"
GUEST_TOKEN_JWT_EXP_SECONDS = 300
ENABLE_GUEST_TOKEN = True
HTTP_HEADERS={"X-Frame-Options":"ALLOWALL"}

TALISMAN_ENABLED = False
TALISMAN_CONFIG = {
        "content_security_policy": {
            "frame-ancestors": ["'self'", 
                                "http://localhost",
                                "http://localhost:8088",
                                ".jacomar.com.br"],
            },
        "force_https": False,
        "session_cookie_secure": False,
        }

PUBLIC_ROLE_LIKE = "Gamma"

APP_ICON = "/static/assets/images/superset-logo-horiz.png"
