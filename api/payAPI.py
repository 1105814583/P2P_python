import app


class payAPI:
    def __init__(self):
        self.payCode_url = app.BASE_URL + "/common/public/verifycode/"
        self.pay_url = app.BASE_URL + "/trust/trust/recharge"

    def payCode(self, session, r):
        url = self.payCode_url + str(r)
        response = session.get(url)
        return response

    def pay(self, session, amount="10000", code="8888"):
        data = {"paymentType": "chinapnrTrust",
                "formStr": "reForm",
                "amount": amount,
                "valicode": code}
        response = session.post(self.pay_url, data=data)
        return response
