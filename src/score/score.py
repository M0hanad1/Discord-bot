from src.data.data import Data


class ScoreData(Data):
    def __init__(self) -> None:
        super().__init__()

    def add_score(self, id_, score):
        self.update_user({'_id': id_}, {'$set': {'score': score}})

    def get_score(self, id_):
        if self.check_user_score(id_) is False:
            return 0

        for i in self.get_user({'_id': id_}):
            return i['score']

    def get_all_score(self):
        return {i['_id']: i['score'] for i in self.get_user({'score': {'$exists': True}})}

    def check_user_score(self, id_):
        return self.check_user({'_id': id_, 'score': {'$exists': True}})
