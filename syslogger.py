import logging

# 创建一个日志记录器
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# 创建一个文件处理程序，将日志写入文件
# file_handler = logging.FileHandler('run.log')
# file_handler.setLevel(logging.DEBUG)

# 创建一个控制台处理程序，将日志显示在终端
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建日志格式器
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(log_formatter)
console_handler.setFormatter(log_formatter)

# 将处理程序添加到记录器
# logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 记录一条错误日志
# logger.error('这是一条错误信息')
