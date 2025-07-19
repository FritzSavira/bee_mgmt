import uuid

class Feeding:
    def __init__(self, hive_id, feeding_date, food_type, amount, concentration, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.hive_id = hive_id
        self.feeding_date = feeding_date
        self.food_type = food_type
        self.amount = amount
        self.concentration = concentration

    def to_dict(self):
        return {
            "id": self.id,
            "hive_id": self.hive_id,
            "feeding_date": self.feeding_date,
            "food_type": self.food_type,
            "amount": self.amount,
            "concentration": self.concentration
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
            concentration=data.get("concentration")
        )