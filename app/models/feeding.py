import uuid

class Feeding:
    FORM_LABELS = {
        'feeding_date': 'Feeding Date',
        'food_type': 'Food Type',
        'amount': 'Amount',
        'concentration': 'Concentration',
        'images': 'Images'
    }

    def __init__(self, hive_id, feeding_date, food_type, amount, concentration, images=None, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.hive_id = hive_id
        self.feeding_date = feeding_date
        self.food_type = food_type
        self.amount = amount
        self.concentration = concentration
        self.images = images if images is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "hive_id": self.hive_id,
            "feeding_date": self.feeding_date,
            "food_type": self.food_type,
            "amount": self.amount,
            "concentration": self.concentration,
            "images": self.images
        }

    @staticmethod
    def from_dict(data):
        from datetime import datetime
        feeding_date = data.get("feeding_date")
        try:
            datetime.strptime(feeding_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            feeding_date = None

        return Feeding(
            id=data.get("id"),
            hive_id=data.get("hive_id"),
            feeding_date=feeding_date,
            food_type=data.get("food_type"),
            amount=data.get("amount"),
            concentration=data.get("concentration"),
            images=data.get("images", [])
        )