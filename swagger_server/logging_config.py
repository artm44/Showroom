# import logging
# import logging_loki

# class MyFilt(logging.Filter):
#     def filter(self, record):
#         record.tags['func'] = record.funcName
#         record.tags['fname'] = record.fileName
#         return True

# logger_conf = {
#     "version": 1,
#     "formatters": {
#        "console_msg": {
#            "format": "{asctime} {levelname} {module} {funcName} {message}",
#            "style": "{"
#        }
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "level": "INFO",
#             "formatter": "console_msg",
#             'filters': ['my_filt']
#         },
#         'loki_handler': {
#             "class": "logging_loki.LokiHandler",
#             "level": "DEBUG",
#             'url':"http://loki:3100/loki/api/v1/push", 
#             'tags':{"application": "Showroom"},
#             'formatter': 'console_msg',
#             'filters': ['my_filt'],
#             "version": '1',
#         }
#     },
#     'filters': {
#         'my_filt' : {
#             '()': MyFilt
#         },
#     },
#     "loggers": {"my_python_logger":
#         {
#          "handlers": ['loki_handler', "console"], 
#          "level": "DEBUG"
#         }
#     }
# }