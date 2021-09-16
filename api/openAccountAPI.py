import app


class openAccountAPI:
    def __init__(self):
        self.open_account_url = app.BASE_URL + "/trust/trust/register"

    def openAccount(self, session):
        response = session.post(self.open_account_url)
        return response
