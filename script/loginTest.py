import json
import unittest
from time import sleep

import requests
from parameterized import parameterized

import app
from api.loginAPI import loginAPI
import random
import logging

from utils import assert_pubilc, read_data_parameter


class loginTest(unittest.TestCase):
    phone1 = "13710733777"
    imgVerifyCode = "8888"

    @classmethod
    def setUpClass(cls) -> None:
        cls.login_api = loginAPI()

    def setUp(self) -> None:
        self.session = requests.session()

    def tearDown(self) -> None:
        self.session.close()

    # # 读取数据文件
    # data_file = app.BASE_DIR + "/data/imgCode_data.json"
    # with open(data_file, encoding="UTF-8") as f:
    #     data_list = json.load(f)
    #
    # parameter_data = []
    # # 循环获取参数
    # for i in data_list:
    #     type = i["type"]
    #     status_code = i["status_code"]
    #
    #     # type1 = i.get("type")
    #     # status_code = i.get("status_code")
    #
    #     parameter_data.append((type, status_code))
    # print(parameter_data)
    #
    # @parameterized.expand(parameter_data)

    @parameterized.expand(read_data_parameter("imgCode_data.json", ["type", "status_code"]))
    def test01_getImgCode_parameterized(self, type, status_code):
        r = None
        if type == "decimal":
            r = random.random()
        elif type == "integer":
            r = random.randint(1, 99999)
        elif type == "null":
            r = ""
        elif type == "letter":
            sample = random.sample("abcdefasdgdg", 4)
            r = "".join(sample)
        elif type == "symbol":
            sample = random.sample("!@#$%^&**()", 4)
            r = "".join(sample)
        elif type == "char":
            sample = random.sample("你我他", 1)
            r = "".join(sample)

        response = self.login_api.getImgCode(r)
        logging.info("getImgCode_parameter ——{}".format(response))
        self.assertEqual(status_code, response.status_code)

    @parameterized.expand(read_data_parameter("getMsgCode_data.json", ["phone", "imgVerifyCode","status_code","status","description"]))
    def test02_getMsgCode_parameterized(self, phone, imgVerifyCode,status_code,status,description):
        #获取图片验证码
        r = random.random()
        url = self.login_api.getImgCode_url + str(r)
        response = self.session.get(url)
        logging.info("login_response —{}".format(response))
        self.assertEqual(200, response.status_code)

        # 获取短信验证码
        response = self.login_api.getMsgCode(self.session,phone,imgVerifyCode)
        logging.info("getMsgCode_parameter response -{}".format(response.json()))
        assert_pubilc(self,response,status_code,status,description)

    def test03_getMsgCode_no_imgCode_request(self):
        response = self.login_api.getMsgCode(self.session, self.phone1, self.imgVerifyCode)
        logging.info("getMsgCode_no_imgCode_request —{}".format(response.json()))
        assert_pubilc(self,response,200,100,"图片验证码错误")

    @parameterized.expand(read_data_parameter("register_data.json",["phone","password","imgVerifyCode","phone_code","dy_server","invite_phone","status_code","status","description"]))
    def test04_register_parameterized(self,phone,password,imgVerifyCode,phone_code,dy_server,invite_phone,status_code,status,description):
        # 获取图片验证码
        r = random.random()
        url = self.login_api.getImgCode_url + str(r)
        response = self.session.get(url)
        logging.info("login_response —{}".format(response))
        self.assertEqual(200, response.status_code)


        # 获取短信验证码
        response = self.login_api.getMsgCode(self.session,phone,self.imgVerifyCode)
        logging.info("getMsgCode_parameter response -{}".format(response.json()))
        assert_pubilc(self,response,200,200,"短信发送成功")

        #申请注册
        response = self.login_api.register(self.session,phone,password,imgVerifyCode,phone_code,dy_server,invite_phone)
        logging.info("register_parameterized —{}".format(response.json()))
        assert_pubilc(self,response,status_code,status,description)



    # def test01_getImgCode_decimal(self):
    #     r = random.random()
    #     response = self.login_api.getImgCode(r)
    #     self.assertEqual(200, response.status_code)
    #     self.cookies = response.cookies
    #     logging.info("cookies{}".format(self.cookies))
    #     logging.info("response{}".format(response.content))

    # def test02_getImgCode_integer(self):
    #     r = random.randint(1, 99999)
    #     response = self.login_api.getImgCode(r)
    #     self.assertEqual(200, response.status_code)
    #     logging.info("response{}".format(response.content))
    #
    # def test03_getImgCode_fail_parameter_null(self):
    #     r = ""
    #     response = self.login_api.getImgCode(r)
    #     self.assertEqual(404, response.status_code)
    #     logging.info("response{}".format(response.text))
    #
    # def test04_getImgCode_fail_parameter_not_number(self):
    #     r = "你!c"
    #     response = self.login_api.getImgCode(r)
    #     self.assertEqual(400, response.status_code)
    #     logging.info("response{}".format(response.text))
    #
    # def test05_getMsgCode_success(self):
    #     r = random.random()
    #     response = self.login_api.getImgCode(r)
    #     self.cookies = response.cookies
    #
    #     response = self.login_api.getMsgCode(self.phone1, self.imgVerifyCode, cookies=self.cookies)
    #     assert_pubilc(self, response, 200, 200, "短信发送成功")
    #     logging.info("response{}".format(response.json()))
    #
    # def test06_getMsgCode_error_imgcode(self):
    #     r = random.random()
    #     response = self.login_api.getImgCode(r)
    #     self.cookies = response.cookies
    #     response = self.login_api.getMsgCode(self.phone1, "8889", cookies=self.cookies)
    #     assert_pubilc(self, response, 200, 100, "图片验证码错误")
    #     logging.info("response{}".format(response.json()))
    #
    # def test07_getMsgCode_null_imgcode(self):
    #     r = random.random()
    #     response = self.login_api.getImgCode(r)
    #     self.cookies = response.cookies
    #     response = self.login_api.getMsgCode(self.phone1, "", cookies=None)
    #     assert_pubilc(self, response, 200, 100, "图片验证码错误")
    #     logging.info("response{}".format(response.json()))
    #
    # def test08_getMsgCode_null_phone(self):
    #     r = random.random()
    #     response = self.login_api.getImgCode(r)
    #     self.cookies = response.cookies
    #     response = self.login_api.getMsgCode("", self.imgVerifyCode, cookies=None)
    #     logging.info("response{}".format(response.json()))
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(100, response.json().get("status"))
    #
    # def test09_getMsgCode_no_imgcode(self):
    #     response = self.login_api.getMsgCode(self.phone1, self.imgVerifyCode, cookies=None)
    #     assert_pubilc(self, response, 200, 100, "图片验证码错误")
    #     logging.info("gtt MsgCode response{}".format(response.json()))
    #
    # def test10_register_success_all_parameter(self):
    #     # 获取图片验证码
    #     r = random.random()
    #     response = self.login_api.getImgCode(r)
    #     self.cookies = response.cookies
    #     logging.info("cookies{}".format(self.cookies))
    #     logging.info("response{}".format(response.content))
    #     # 获取短信验证码
    #     response = self.login_api.getMsgCode(self.phone1, self.imgVerifyCode, cookies=self.cookies)
    #     assert_pubilc(self, response, 200, 200, "短信发送成功")
    #     logging.info("gtt MsgCode response{}".format(response.json()))
    #
    #     response = self.login_api.register(self.cookies, self.phone1, self.password, invite_phone="13710733791")
    #     logging.info("register{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 200, "注册成功")
    #
    # def test11_register_success_must_parameter(self):
    #     # 获取图片验证码
    #     r = random.random()
    #     response = self.login_api.getImgCode(r)
    #     self.cookies = response.cookies
    #     logging.info("cookies{}".format(self.cookies))
    #     logging.info("response{}".format(response.content))
    #     # 获取短信验证码
    #     response = self.login_api.getMsgCode(self.phone2, self.imgVerifyCode, cookies=self.cookies)
    #     assert_pubilc(self, response, 200, 200, "短信发送成功")
    #     logging.info("gtt MsgCode response{}".format(response.json()))
    #
    #     response = self.login_api.register(self.cookies, self.phone2, self.password)
    #     assert_pubilc(self, response, 200, 200, "注册成功")
    #     logging.info("register{}".format(response.json()))
    #
    # def test12_register_fail_error_imgcoed(self):
    #     # 获取图片验证码
    #     r = random.random()
    #     response = self.login_api.getImgCode(r)
    #     self.cookies = response.cookies
    #     logging.info("cookies{}".format(self.cookies))
    #     logging.info("response{}".format(response.content))
    #     # 获取短信验证码
    #     response = self.login_api.getMsgCode(self.phone3, self.imgVerifyCode, cookies=self.cookies)
    #     assert_pubilc(self, response, 200, 200, "短信发送成功")
    #     logging.info("gtt MsgCode response{}".format(response.json()))
    #
    #     response = self.login_api.register(self.cookies, self.phone3, self.password, "6666")
    #     logging.info("register{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 100, "验证码错误!")
    #
    # def test13_register_fail_error_phone_code(self):
    #     # 获取图片验证码
    #     r = random.random()
    #     response = self.login_api.getImgCode(r)
    #     self.cookies = response.cookies
    #     logging.info("cookies{}".format(self.cookies))
    #     logging.info("response{}".format(response.content))
    #     # 获取短信验证码
    #     response = self.login_api.getMsgCode(self.phone3, self.imgVerifyCode, cookies=self.cookies)
    #     assert_pubilc(self, response, 200, 200, "短信发送成功")
    #     logging.info("gtt MsgCode response{}".format(response.json()))
    #
    #     response = self.login_api.register(self.cookies, self.phone3, self.password, phone_code="123456")
    #     logging.info("register{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 100, "验证码错误")
    #
    # def test14_register_fail_error_phone_code(self):
    #     # 获取图片验证码
    #     r = random.random()
    #     response = self.login_api.getImgCode(r)
    #     self.cookies = response.cookies
    #     logging.info("cookies{}".format(self.cookies))
    #     logging.info("response{}".format(response.content))
    #     # 获取短信验证码
    #     response = self.login_api.getMsgCode(self.phone2, self.imgVerifyCode, cookies=self.cookies)
    #     assert_pubilc(self, response, 200, 200, "短信发送成功")
    #     logging.info("gtt MsgCode response{}".format(response.json()))
    #
    #     response = self.login_api.register(self.cookies, self.phone2, self.password)
    #     logging.info("register{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 100, "手机已存在!")
    #
    # def test15_register_fail_null_password(self):
    #     # 获取图片验证码
    #     r = random.random()
    #     response = self.login_api.getImgCode(r)
    #     self.cookies = response.cookies
    #     logging.info("cookies{}".format(self.cookies))
    #     logging.info("response{}".format(response.content))
    #     # 获取短信验证码
    #     response = self.login_api.getMsgCode(self.phone3, self.imgVerifyCode, cookies=self.cookies)
    #     assert_pubilc(self, response, 200, 200, "短信发送成功")
    #     logging.info("gtt MsgCode response{}".format(response.json()))
    #
    #     response = self.login_api.register(self.cookies, self.phone3, password="")
    #     logging.info("register{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 100, "密码不能为空")
    #
    # def test16_register_fail_not_agreed(self):
    #     # 获取图片验证码
    #     r = random.random()
    #     response = self.login_api.getImgCode(r)
    #     self.cookies = response.cookies
    #     logging.info("cookies{}".format(self.cookies))
    #     logging.info("response{}".format(response.content))
    #     # 获取短信验证码
    #     response = self.login_api.getMsgCode(self.phone4, self.imgVerifyCode, cookies=self.cookies)
    #     assert_pubilc(self, response, 200, 200, "短信发送成功")
    #     logging.info("gtt MsgCode response{}".format(response.json()))
    #
    #     response = self.login_api.register(self.cookies, self.phone4, self.password, dy_server="off")
    #     logging.info("register{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 100, "请同意我们的条款")
    #
    # def test17_login_success(self):
    #     response = self.login_api.login(self.phone1, self.password)
    #     logging.info("login{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 200, "登录成功")
    #
    # def test18_login_fail_phone_not_exist(self):
    #     response = self.login_api.login("12345678910", self.password)
    #     logging.info("login{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 100, "用户不存在")
    #
    # def test19_login_fail_null_password(self):
    #     response = self.login_api.login(self.phone1, "")
    #     logging.info("login{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 100, "密码不能为空")
    #
    # def test20_login_fail_continue_login_error(self):
    #     #错误一次
    #     response = self.login_api.login(self.phone1, "error")
    #     self.cookies=response.cookies
    #     logging.info("login{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")
    #
    #     # 错误两次
    #     response = self.login_api.login(self.phone1, "error",self.cookies)
    #     logging.info("login{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")
    #     #错误三次
    #     response = self.login_api.login(self.phone1, "error",self.cookies)
    #     logging.info("login{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
    #     #输入正确账号密码，提示被锁定
    #     response = self.login_api.login(self.phone1, "error",self.cookies)
    #     logging.info("login{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
    #     #等待一分钟后输入正确账号密码登录成功
    #     sleep(60)
    #     response = self.login_api.login(self.phone1, self.password,self.cookies)
    #     logging.info("login{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 200, "登录成功")
    #
    #
    # def test21_querying_login_status_is_login(self):
    #     #成功登录
    #     response = self.login_api.login(self.phone1, self.password)
    #     logging.info("login{}".format(response.json()))
    #     self.cookies = response.cookies
    #     assert_pubilc(self, response, 200, 200, "登录成功")
    #
    #     response = self.login_api.querying_login_status(self.cookies)
    #     logging.info("querying_login_status{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 200, "OK")
    #
    # def test22_querying_login_status_not_login(self):
    #     response = self.login_api.querying_login_status()
    #     logging.info("querying_login_status{}".format(response.json()))
    #     assert_pubilc(self, response, 200, 250, "您未登陆！")
    #
