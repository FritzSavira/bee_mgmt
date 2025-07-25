
import uuid

class Harvest:
    def __init__(self, hive_id, harvest_date, amount_kg, honey_type, water_content, notes, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.hive_id = hive_id
        self.harvest_date = harvest_date
        self.amount_kg = amount_kg
        self.honey_type = honey_type
        self.water_content = water_content
        self.notes = notes

    def to_dict(self):
        return {
            "id": self.id,
            "hive_id": self.hive_id,
            "harvest_date": self.harvest_date,
            "amount_kg": self.amount_kg,
            "honey_type": self.honey_type,
            "water_content": self.water_content,
            "notes": self.notes
        }

    @staticmethod
    def from_dict(data):
        return Harvest(
            id=data.get("id"),
            hive_id=data["hive_id"],
            harvest_date=data["harvest_date"],
            amount_kg=data["amount_kg"],
            honey_type=data["honey_type"],
            water_content=data["water_content"],
            notes=data["notes"]
        )
