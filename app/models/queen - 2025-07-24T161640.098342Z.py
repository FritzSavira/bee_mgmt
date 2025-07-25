from datetime import date
import datetime

class Queen:
    def __init__(self, hive_id, origin, birth_date, color_mark, breed, introduction_date, marked, clipped, id=None):
        self.id = id
        self.hive_id = hive_id
        self.origin = origin
        self.birth_date = birth_date # YYYY-MM-DD string
        self.color_mark = color_mark
        self.breed = breed
        self.introduction_date = introduction_date # YYYY-MM-DD string
        self.marked = marked
        self.clipped = clipped

    def get_age(self):
        if not self.birth_date:
            return "N/A"
        today = date.today()
        birth_date_obj = datetime.datetime.strptime(self.birth_date, '%Y-%m-%d').date()
        age = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
        return age
        self.id = id
        self.hive_id = hive_id
        self.origin = origin
        self.birth_date = birth_date # YYYY-MM-DD string
        self.color_mark = color_mark
        self.breed = breed
        self.introduction_date = introduction_date # YYYY-MM-DD string
        self.marked = marked
        self.clipped = clipped

    def to_dict(self):
        return {
            "id": self.id,
            "hive_id": self.hive_id,
            "origin": self.origin,
            "birth_date": self.birth_date,
            "color_mark": self.color_mark,
            "breed": self.breed,
            "introduction_date": self.introduction_date,
            "marked": self.marked,
            "clipped": self.clipped
        }

    @staticmethod
    def from_dict(data):
        return Queen(
            id=data.get('id'),
            hive_id=data.get('hive_id'),
            origin=data.get('origin'),
            birth_date=data.get('birth_date'),
            color_mark=data.get('color_mark'),
            breed=data.get('breed'),
            introduction_date=data.get('introduction_date'),
            marked=data.get('marked'),
            clipped=data.get('clipped')
        )
