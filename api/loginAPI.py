import app
import requests

import random


class loginAPI:
    def __init__(self):
        self.getImgCode_url = app.BASE_URL + "/common/public/verifycode1/"
        self.getMsgCode_url = app.BASE_URL + "/member/public/sendSms"
        self.register_url = app.BASE_URL + "/member/public/reg"
        self.login_url = app.BASE_URL+"/member/public/login"
        self.querying_login_status_url = app.BASE_URL+"/member/public/islogin"

    def getImgCode(self, r):
        url = self.getImgCode_url + str(r)
        response = requests.get(url)
        return response

    def getMsgCode(self, session,phone, imgVerifyCode):
        data = {"phone": phone,
                "imgVerifyCode": imgVerifyCode,
                "type": "reg"}
        response = session.post(self.getMsgCode_url, data=data)
        return response

    def register(self, session, phone, password, imgVerifyCode, phone_code, dy_server,
                 invite_phone):
        data = {"phone": phone,
                "password": password,
                "verifycode": imgVerifyCode,
                "phone_code": phone_code,
                "dy_server": dy_server,
                "invite_phone": invite_phone}
        response = session.post(self.register_url, data=data)
        return response

    def login(self,keywords,password,cookies=""):
        data = {"keywords":keywords,"password":password}
        response = requests.post(self.login_url,data,cookies=cookies)
        return response
    #查询登录状态接口
    def querying_login_status(self,cookies=""):
        response = requests.post(self.querying_login_status_url,cookies=cookies)
        return response
