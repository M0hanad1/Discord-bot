import json
from os import path
from pathlib import Path


class Data:
    instances = []

    def __init__(self) -> None:
        Data.instances.append(self)
        self.folder = './api/'
        self.servers_path = self.folder + 'servers.json'
        self.users_path = self.folder + 'users.json'
        self.servers_data = self.create_data(self.servers_path)
        self.users_data = self.create_data(self.users_path)

    def create_data(self, data_path):
        if path.exists(self.folder) is False or path.isfile(data_path) is False or path.getsize(data_path) == 0:
            Path.mkdir(self.folder, exist_ok=True)

            with open(data_path, 'w') as f:
                json.dump({}, f, indent=4)

        with open(data_path) as f:
            return json.load(f)

    def update_data(self):
        for i in self.instances:
            i.users_data, i.servers_data = self.users_data, self.servers_data

        with open(self.users_path, 'w') as f:
            json.dump(self.users_data, f, indent=4)

        with open(self.servers_path, 'w') as d:
            json.dump(self.servers_data, d, indent=4)

    def change_score(self, id, new_score):
        self.users_data[id]['score'] = new_score
        self.update_data()

    def get_score(self, id):
        if (id not in self.users_data) or ('score' not in self.users_data[id]):
            return -1

        return self.users_data[id]['score']

    def add_user(self, id):
        self.users_data[id] = {}

    def data_check(self, id, mood):
        if (mood == 'user' and (id not in self.users_data  or 'words' not in self.users_data[id])) or (mood == 'server' and (id not in self.servers_data  or 'words' not in self.servers_data[id])):
            return -1

    def add_key(self, id, key, value, mood):
        if self.data_check(id, mood) == -1:
            return -1

        if (mood == 'user' and key in self.users_data[id]['words']) or (mood == 'server' and key in self.servers_data[id]['words']):
            return -2

        if mood == 'user':
            self.users_data[id]['words'][key] = value

        else:
            self.servers_data[id]['words'][key] = value

        self.update_data()

    def remove_key(self, id, key, mood):
        if self.data_check(id, mood) == -1:
            return -1

        if (mood == 'user' and key not in self.users_data[id]['words']) or (mood == 'server' and key not in self.servers_data[id]['words']):
            return -2

        if mood == 'user':
            del self.users_data[id]['words'][key]

        else:
            del self.servers_data[id]['words'][key]

        self.update_data()

    def edit_key(self, id, old_key, new_key, mood):
        if self.data_check(id, mood) == -1:
            return -1

        if (mood == 'user' and old_key not in self.users_data[id]['words']) or (mood == 'server' and old_key not in self.servers_data[id]['words']):
            return -2

        if (mood == 'user' and new_key in self.users_data[id]['words']) or (mood == 'server' and new_key in self.servers_data[id]['words']):
            return -3

        if mood == 'user':
            self.users_data[id]['words'][new_key] = self.users_data[id]['words'][old_key]
            del self.users_data[id]['words'][old_key]

        else:
            self.servers_data[id]['words'][new_key] = self.servers_data[id]['words'][old_key]
            del self.servers_data[id]['words'][old_key]

        self.update_data()

    def edit_value(self, id, key, new_value, mood):
        if self.data_check(id, mood) == -1:
            return -1

        if (mood == 'user' and key not in self.users_data[id]['words']) or (mood == 'server' and key not in self.servers_data[id]['words']):
            return -2

        if mood == 'user':
            self.users_data[id]['words'][key] = new_value

        else:
            self.servers_data[id]['words'][key] = new_value

        self.update_data()

    def leave_data(self, id, mood):
        if self.data_check(id, mood) == -1:
            return -1

        if mood == 'user':
            if self.get_score(id) == -1:
                del self.users_data[id]

            else:
                del self.users_data[id]['words']

        else:
            del self.servers_data[id]

        self.update_data()

    def join_data(self, id, mood):
        if self.data_check(id, mood) != -1:
            return -1

        if mood == 'user':
            if id not in self.users_data or 'score' not in self.users_data[id]:
                self.users_data[id] = {'words': {}}

            else:
                self.users_data[id]['words'] = {}

        else:
            self.servers_data[id] = {'words': {}}

        self.update_data()

    def data_search(self, id, key, mood):
        if (self.data_check(id, mood) == -1) or ((mood == 'user' and key not in self.users_data[id]['words']) or (mood == 'server' and key not in self.servers_data[id]['words'])):
            return -1

        if mood == 'user':
            return self.users_data[id]['words'][key]

        return self.servers_data[id]['words'][key]
