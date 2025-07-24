from datetime import date
import datetime

class Queen:
    FORM_LABELS = {
        'origin': 'Origin',
        'birth_date': 'Birth Year/Hatching Date',
        'color_mark': 'Color Mark',
        'breed': 'Breed/Genetics',
        'introduction_date': 'Introduction Date',
        'marked': 'Marked',
        'clipped': 'Clipped/Unclipped'
    }

    def __init__(self, hive_id, origin, birth_date, color_mark, breed, introduction_date, marked, clipped, id=None, name=None):
        self.id = id
        self.hive_id = hive_id
        self.name = name
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

    def to_dict(self):
        return {
            "id": self.id,
            "hive_id": self.hive_id,
            "name": self.name,
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
        from datetime import datetime
        birth_date = data.get('birth_date')
        introduction_date = data.get('introduction_date')

        try:
            datetime.strptime(birth_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            birth_date = None

        try:
            datetime.strptime(introduction_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            introduction_date = None

        return Queen(
            id=data.get('id'),
            hive_id=data.get('hive_id'),
            name=data.get('name'),
            origin=data.get('origin'),
            birth_date=birth_date,
            color_mark=data.get('color_mark'),
            breed=data.get('breed'),
            introduction_date=introduction_date,
            marked=data.get('marked'),
            clipped=data.get('clipped')
        )
