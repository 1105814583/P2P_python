import logging
import unittest
import requests
from api.authenticationAPI import authenticationAPI
from api.loginAPI import loginAPI
from utils import assert_pubilc


class authenticationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.login_api = loginAPI()
        cls.authentication_api = authenticationAPI()

    def setUp(self) -> None:
        self.session = requests.session()

    def tearDown(self) -> None:
        self.session.close()

    def test01_authentication_success(self):
        # 成功登陆
        response = self.session.post(self.login_api.login_url, data={"keywords": "13710733710", "password": "a123456"})

        logging.info("login{}".format(response.json()))

        response = self.authentication_api.authentication(self.session, "张三", "111111111111111111")
        logging.info("authentication_success{}".format(response.json()))
        assert_pubilc(self, response, 200, 200, "提交成功!")

    def test02_authentication_fail_null_name(self):
        # 成功登陆
        response = self.session.post(self.login_api.login_url, data={"keywords": "13710733711", "password": "a123456"})

        logging.info("login{}".format(response.json()))
        # 认证失败
        response = self.authentication_api.authentication(self.session, "", "211111111111111111")
        logging.info("authentication_success{}".format(response.json()))
        assert_pubilc(self, response, 200, 100, "姓名不能为空")

    def test03_authentication_fail_null_cardID(self):
        # 成功登陆
        response = self.session.post(self.login_api.login_url, data={"keywords": "13710733711", "password": "a123456"})

        logging.info("login{}".format(response.json()))
        # 认证失败
        response = self.authentication_api.authentication(self.session, "张三", "")
        logging.info("authentication_success{}".format(response.json()))
        assert_pubilc(self, response, 200, 100, "身份证号不能为空")

    def test03_authentication_fail_exist_cardID(self):
        # 成功登陆
        response = self.session.post(self.login_api.login_url, data={"keywords": "13710733711", "password": "a123456"})
        logging.info("login{}".format(response.json()))
        # 认证失败
        response = self.authentication_api.authentication(self.session, "张三", "11111111111")
        logging.info("authentication_success{}".format(response.json()))
        assert_pubilc(self, response, 200, 100, "身份证号已存在")

    def test03_authentication_fail_error_cardID(self):
        # 成功登陆
        response = self.session.post(self.login_api.login_url, data={"keywords": "13710733711", "password": "a123456"})
        logging.info("login{}".format(response.json()))
        # 认证失败
        response = self.authentication_api.authentication(self.session, "张三", "abcd")
        logging.info("authentication_success{}".format(response.json()))
        assert_pubilc(self, response, 200, 100, "身份证号格式不正确")

    def test05_authentication_is_verified(self):
        # 成功登陆已认证账号
        response = self.session.post(self.login_api.login_url, data={"keywords": "13710733710", "password": "a123456"})

        logging.info("login{}".format(response.json()))
        # 认证失败
        response = self.authentication_api.queryAuthentication(self.session)
        logging.info("query_authentication{}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual("张**",response.json().get("realname"))

    def test06_authentication_unverified(self):
        # 成功登陆已认证账号
        response = self.session.post(self.login_api.login_url, data={"keywords": "13710733712", "password": "a123456"})

        logging.info("login{}".format(response.json()))
        # 认证失败
        response = self.authentication_api.queryAuthentication(self.session)
        logging.info("query_authentication{}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(100,response.json().get("status"))
