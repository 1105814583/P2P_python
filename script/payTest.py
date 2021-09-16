import logging
import random
import unittest

import requests

from api.loginAPI import loginAPI
from api.payAPI import payAPI
from utils import assert_pubilc, third_openAccoun_interface


class payTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pay_api = payAPI()
        cls.login_api = loginAPI()

    def setUp(self) -> None:
        self.session = requests.session()

    def tearDown(self) -> None:
        self.session.close()

    def test01_payCode_success_decimal(self):
        # 前置登陆
        response = self.session.post(self.login_api.login_url, {"keywords": "13710733710", "password": "a123456"})
        logging.info("login response{}".format(response.json()))

        r = random.random()
        response = self.pay_api.payCode(self.session, r)
        logging.info("pay_success_decimal response -{}".format(response.content))
        self.assertEqual(200, response.status_code)

    def test02_payCode_success_integer(self):
        # 前置登陆
        response = self.session.post(self.login_api.login_url, {"keywords": "13710733710", "password": "a123456"})
        logging.info("login response{}".format(response.json()))

        r = random.randint(1, 99999)
        response = self.pay_api.payCode(self.session, r)
        logging.info("pay_success_integer response -{}".format(response.content))
        self.assertEqual(200, response.status_code)

    def test03_payCode_fail_null_parameter(self):
        # 前置登陆
        response = self.session.post(self.login_api.login_url, {"keywords": "13710733710", "password": "a123456"})
        logging.info("login response {}".format(response.json()))

        r = ""
        response = self.pay_api.payCode(self.session, r)
        logging.info("pay_fail_null_parameter response -{}".format(response.content))
        self.assertEqual(404, response.status_code)

    def test04_payCode_fail_error_parameter(self):
        # 前置登陆
        response = self.session.post(self.login_api.login_url, {"keywords": "13710733710", "password": "a123456"})
        logging.info("login response{}".format(response.json()))

        r = "a！你"
        response = self.pay_api.payCode(self.session, r)
        logging.info("pay_fail_error_parameter response -{}".format(response.content))
        self.assertEqual(400, response.status_code)

    def test05_pay_success(self):
        # 前置登陆
        response = self.session.post(self.login_api.login_url, {"keywords": "a123456", "password": "a123456"})
        logging.info("login response{}".format(response.json()))

        # 获取充值验证码成功
        r = random.random()
        response = self.pay_api.payCode(self.session, r)
        logging.info("pay_success_decimal response -{}".format(response.content))
        self.assertEqual(200, response.status_code)

        response = self.pay_api.pay(self.session)
        logging.info("pay_success response-{}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))

    def test06_pay_fail_error_payCode(self):
        # 前置登陆
        response = self.session.post(self.login_api.login_url, {"keywords": "a123456", "password": "a123456"})
        logging.info("login response{}".format(response.json()))

        # 获取充值验证码成功
        r = random.random()
        response = self.pay_api.payCode(self.session, r)
        logging.info("pay_success_decimal response -{}".format(response.content))
        self.assertEqual(200, response.status_code)
        # 填写错误验证码
        response = self.pay_api.pay(self.session, code="7777")
        logging.info("pay_fail_error_payCode response-{}".format(response.json()))
        assert_pubilc(self, response, 200, 100, "验证码错误")

    def test07_third_pay(self):
        # 前置登陆
        response = self.session.post(self.login_api.login_url, {"keywords": "a123456", "password": "a123456"})
        logging.info("login response{}".format(response.json()))

        # 获取充值验证码成功
        r = random.random()
        response = self.pay_api.payCode(self.session, r)
        logging.info("pay_success_decimal response -{}".format(response.content))
        self.assertEqual(200, response.status_code)

        response = self.pay_api.pay(self.session)
        logging.info("third_pay response-{}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))

        # 调用提取html方法
        response = third_openAccoun_interface(response, self.session)
        logging.info("third_openAccoun_interface response{}".format(response))
        self.assertEqual(200, response.status_code)
        self.assertEqual("Netsave OK", response.text)
