# -*- coding: utf-8 -*-
import logging
import settings
import tornado.log
from logging.handlers import RotatingFileHandler

tornado.log.enable_pretty_logging()


for logger_name, path in settings.log['log_path'].iteritems():
    name = logger_name if logger_name != 'logger' else None
    logger = locals()[logger_name] = logging.getLogger(name)
    logger.setLevel(logging.NOTSET)
    file_handler = RotatingFileHandler(
        path,
        maxBytes=settings.log['log_max_bytes'],
        backupCount=settings.log['backup_count']
    )
    file_handler.setFormatter(tornado.log.LogFormatter(color=False))
    logger.addHandler(file_handler)
