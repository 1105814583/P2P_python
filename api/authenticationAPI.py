import app


class authenticationAPI:
    def __init__(self):
        self.headers = {"Content-Type": "multipart/form-data"}
        self.authentication_url = app.BASE_URL + "/member/realname/approverealname"
        self.query_authentication_url = app.BASE_URL + "/member/member/getapprove"


    def authentication(self, session, name, card_id):
        data = {"realname": name, "card_id": card_id}
        response = session.post(self.authentication_url, data=data, files={"x": "y"})
        return response

    def queryAuthentication(self, session):
        response = session.post(self.query_authentication_url)
        return response
