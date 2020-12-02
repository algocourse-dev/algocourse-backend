import os

from django.conf import settings
import logging.config

log = None


def _log_record_exception(func):
    def _func(self):
        try:
            return func(self)
        except Exception:
            log.exception('log_exception|thread=%s:%s,file=%s:%s,func=%s:%s,log=%s',
                          self.process, self.thread, self.filename, self.lineno, self.module, self.funcName, self.msg)
            raise
    return _func


def init_logger():
    log_dir = settings.LOG_DIR
    if log_dir is None:
        log_dir = './log'

    if log_dir != '@stdout':
        log_dir = os.path.abspath(log_dir)
        if log_dir and not os.path.exists(log_dir):
            os.mkdir(log_dir)

    module_path = ".".join(__name__.split(".")[:-1] + ["loggingmp"])

    logger_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s.%(msecs)03d|%(levelname)s|%(process)d:%(thread)d|%(filename)s:%(lineno)d|'
                          '%(module)s.%(funcName)s|%(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'short': {
                'format': '%(asctime)s.%(msecs)03d|%(levelname)s|%(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'data': {
                'format': '%(asctime)s.%(msecs)03d|%(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'file_fatal': {
                'level': 'CRITICAL',
                'filename': os.path.join(log_dir, 'fatal.log').replace('\\', '/'),
                'formatter': 'standard',
                'class': '%s.MPTimedRotatingFileHandler' % module_path,
                'when': 'MIDNIGHT',
            },
            'file_error': {
                'level': 'WARNING',
                'filename': os.path.join(log_dir, 'error.log').replace('\\', '/'),
                'formatter': 'standard',
                'class': '%s.MPTimedRotatingFileHandler' % module_path,
                'when': 'MIDNIGHT',
            },
            'file_info': {
                'level': 'INFO',
                'filename': os.path.join(log_dir, 'info.log').replace('\\', '/'),
                'formatter': 'short',
                'class': '%s.MPTimedRotatingFileHandler' % module_path,
                'when': 'MIDNIGHT',
            },
            'file_data': {
                'level': 'INFO',
                'filename': os.path.join(log_dir, 'data.log').replace('\\', '/'),
                'formatter': 'data',
                'class': '%s.MPTimedRotatingFileHandler' % module_path,
                'when': 'MIDNIGHT',
            }
        },
        'loggers': {
            'main': {
                'handlers': ['file_fatal', 'file_error', 'file_info'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'data': {
                'handlers': ['file_data'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

    logging.config.dictConfig(logger_config)

    global log  # pylint: disable=global-statement
    log = logging.getLogger('main')
    log.assertion = log.critical
    log.data = logging.getLogger('data').info
    logging.LogRecord.getMessage = _log_record_exception(logging.LogRecord.getMessage)


if log is None:
    init_logger()
