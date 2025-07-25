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
        return Feeding(
            id=data.get("id"),
            hive_id=data["hive_id"],
            feeding_date=data["feeding_date"],
            food_type=data["food_type"],
            amount=data["amount"],
            concentration=data["concentration"]
        )