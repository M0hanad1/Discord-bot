from src.data.data import Data


class TempVoice(Data):
    def __init__(self) -> None:
        super().__init__()

    def get_voice(self, server_id):
        for i in self.get_server({'_id': server_id, 'voice': {'$exists': True}}):
            return i['voice']

        return 0

    def add_voice(self, server_id, voice_channel_id):
        self.update_server({'_id': server_id}, {'$set': {'voice': voice_channel_id}})

    def remove_voice(self, server_id):
        self.update_server({'_id': server_id}, {'$unset': {'voice': ''}})
        self.check_server_len(server_id)
