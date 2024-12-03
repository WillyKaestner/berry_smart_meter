from settings import SETTINGS

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "ch_formatter": {
            "format": "%(asctime)s - %(levelname)s - %(message)s - %(name)s"
        },
        "ph_formatter": {
            "format": "%(levelname)s - %(message)s - %(name)s - line number:%(lineno)s - luz_energy_meter"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "ch_formatter",
        },
        "papertrail": {
            "class": "logging.handlers.SysLogHandler",
            "level": "DEBUG",
            "address": (SETTINGS.papertrail_host, SETTINGS.papertrail_port),
            "formatter": "ph_formatter",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console",
            "papertrail"
        ]
    }
}


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'simple': {
#             'format': '%(asctime)s %(hostname)s YOUR_APP: [%(levelname)s] %(message)s',
#             'datefmt': '%b %d %H:%M:%S',
#         },
#     },
#     'handlers': {
#         'SysLog': {
#             'level': 'INFO',
#             'class': 'logging.handlers.SysLogHandler',
#             'formatter': 'simple',
#             'address': ('logsN.papertrailapp.com', 30000),
#             'filters': ['require_hostname']
#         }
#     },
#     'loggers': {
#         'papertrail_logger': {
#             'handlers': ['SysLog'],
#             'level': 'INFO',
#             'propagate': True,
#         }
#     }
# }