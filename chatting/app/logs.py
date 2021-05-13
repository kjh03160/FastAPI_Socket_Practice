import logging
import logging.handlers
FILE_MAX_BYTE = 1024 * 1024 * 100

formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

sql_logger = logging.getLogger('sqlalchemy.engine')
sql_file_handler = logging.handlers.RotatingFileHandler('./sql.log', maxBytes=FILE_MAX_BYTE, backupCount=10)
sql_stream = logging.StreamHandler()
sql_file_handler.setFormatter(formatter)
sql_stream.setFormatter(formatter)
sql_logger.handlers = [sql_file_handler, sql_stream]
sql_logger.setLevel(logging.INFO)
    
server_logger = logging.getLogger()
server_file_handler = logging.handlers.RotatingFileHandler('./server.log', maxBytes=FILE_MAX_BYTE, backupCount=10)
server_file_handler.setFormatter(formatter)
server_logger.handlers = [server_file_handler]
server_logger.setLevel(logging.DEBUG)
