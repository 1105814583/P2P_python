import os
import logging
from logging import handlers

# 当前路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 项目域名
BASE_URL = "http://user-p2p-test.itheima.net"
# 数据库信息
MYSQL_USER = "root"
MYSQL_PASSWORD = "Itcast_p2p_20191228"
MYSQL_HOST = "121.43.169.97"
MYSQL_MENBER = "czbk_member"
MYSQL_FINANCE = "czbk_finance"
MYSQL_PORT = 3306


# 初始化日志配置
def init_logger():
    # 1、初始化日志对象
    logger = logging.getLogger()
    # 2、设置日志级别
    logger.setLevel(logging.INFO)
    # 3、创建控制台日志处理器和文件日志处理器
    sf = logging.StreamHandler()
    log_path = BASE_DIR + "/log/p2p.log"
    fh = logging.handlers.TimedRotatingFileHandler(log_path, when="m", interval=3, backupCount=5, encoding="UTF-8")
    # 4、设置日志格式，创建格式化器
    fmt = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
    formatter = logging.Formatter(fmt)
    # 5、将格式化器设置到日志器中
    sf.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 6、将日志处理器添加到日志对象
    logger.addHandler(sf)
    logger.addHandler(fh)
