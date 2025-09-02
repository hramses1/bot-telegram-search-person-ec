


class User:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.firstname = None
        self.lastname = None
        self.quota = {"date": None, "count": 0}

    def set_firstname(self, firstname: str):
        self.firstname = firstname

    def set_lastname(self, lastname: str):
        self.lastname = lastname

    def set_quota(self, date, count):
        self.quota = {"date": date, "count": count}
