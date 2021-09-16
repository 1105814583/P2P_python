import unittest
import requests
import logging
from utils import third_openAccoun_interface

from api.loginAPI import loginAPI
from api.openAccountAPI import openAccountAPI


class openAccountTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.login_api = loginAPI()
        cls.open_account_api = openAccountAPI()

    def setUp(self) -> None:
        self.session = requests.session()

    def tearDown(self) -> None:
        self.session.close()

    def test01_openAccount(self):
        # 登陆
        response = self.session.post(self.login_api.login_url, {"keywords": 13710733711, "password": "a123456"})
        logging.info("openAccount longin{}".format(response.json()))

        response = self.open_account_api.openAccount(self.session)
        logging.info("openAccount{}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))

    def test02_openAccount_thirdParty(self):
        # 登录
        response = self.session.post(self.login_api.login_url, {"keywords": 13710733712, "password": "a123456"})
        logging.info("openAccount longin{}".format(response.json()))
        # 开户请求
        response = self.open_account_api.openAccount(self.session)
        logging.info("openAccount{}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # html_data = response.json().get("description").get("form")
        # soup = BeautifulSoup(html_data, "html.parser")

        # # 提取url
        # action_url = soup.form["action"]
        #
        # # 提取input标签数据
        # data = {}
        # for input_data in soup.find_all("input"):
        #     # soup = BeautifulSoup(input_data, "html.parser")
        #     name = input_data["name"]
        #     value = input_data["value"]
        #     data.update({name: value})
        #     # data.setdefault(name, value)
        #
        # response = self.session.post(action_url, data=data)
        # logging.info("openAccount_thirdParty{}".format(response.text))

        response=third_openAccoun_interface(response, self.session)
        logging.info("openAccount_thirdParty{}".format(response.text))

        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)
