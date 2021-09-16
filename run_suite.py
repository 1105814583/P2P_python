import time
import app
from lib.HTMLTestRunner import HTMLTestRunner
import unittest
from script.openAccountTest import openAccountTest
from script.loginTest import loginTest
from script.authenticationTest import authenticationTest
from script.payTest import payTest
from utils import clear_data

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(loginTest))
# suite.addTest(unittest.makeSuite(openAccountTest))
# suite.addTest(unittest.makeSuite(authenticationTest))
# suite.addTest(unittest.makeSuite(payTest))
#清除数据
clear_data()



report_file =app.BASE_DIR+"/report/report-{}.html".format(time.strftime("%Y%m%d-%H%M%S"))

with open(report_file, "wb")as f:
    runner = HTMLTestRunner(f, title="P2P金融接口测试报告")
    runner.run(suite)

