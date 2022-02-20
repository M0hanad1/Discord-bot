from src.data.data import Data


class AutoRole(Data):
    def __init__(self) -> None:
        super().__init__()

    def get_roles(self, server_id):
        for i in self.get_server({'_id': server_id, 'autoroles': {'$exists': True}}):
            return i['autoroles']

        return []

    def add_role(self, server_id, role_id):
        self.update_server({'_id': server_id}, {'$push': {'autoroles': role_id}})

    def remove_role(self, server_id, role_id):
        for i in self.get_server({'_id': server_id, f'autoroles': {'$in': [role_id]}}):
            self.update_server({'_id': server_id}, {'$pull': {'autoroles': role_id}})
            i['autoroles'].remove(role_id)

            if len(i['autoroles']) == 0:
                self.update_server({'_id': server_id}, {'$unset': {'autoroles': ''}})
                self.check_server_len(server_id)

    def remove_all_roles(self, server_id):
        for _ in self.get_server({'_id': server_id, f'autoroles': {'$exists': True}}):
            self.update_server({'_id': server_id}, {'$unset': {'autoroles': ''}})
            self.check_server_len(server_id)
