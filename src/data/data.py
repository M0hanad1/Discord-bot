from os import getenv
from src.data.database import Database
from dotenv import load_dotenv


class Data:
    load_dotenv()
    def __init__(self) -> None:
        self.data = Database(getenv('HOST'), 'discord-bot')
        self.data.add_collection('servers', 'users')
        self.servers = 'servers'
        self.users = 'users'

    def add_user(self, *values: dict):
        self.data.add_post(self.users, values)

    def remove_user(self, value: dict):
        self.data.remove_post(self.users, value)

    def update_user(self, value: dict, new_value: dict):
        self.data.update_post(self.users, value, new_value)

    def check_user(self, value: dict):
        return self.data.check_post(self.users, value)

    def get_user(self, value: dict):
        return self.data.find_post(self.users, value)

    def add_server(self, *values: dict):
        self.data.add_post(self.servers, values)

    def remove_server(self, value: dict):
        self.data.remove_post(self.servers, value)

    def update_server(self, value: dict, new_value: dict):
        self.data.update_post(self.servers, value, new_value)

    def check_server(self, value: dict):
        self.data.check_post(self.servers, value)

    def get_server(self, value: dict):
        return self.data.find_post(self.servers, value)
