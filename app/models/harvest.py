
import uuid

class Harvest:
    FORM_LABELS = {
        'harvest_date': 'Harvest Date',
        'amount_kg': 'Amount (kg)',
        'honey_type': 'Honey Type',
        'water_content': 'form_label_water_content',
        'notes': 'Notes',
        'images': 'Images'
    }

    def __init__(self, hive_id, harvest_date, amount_kg, honey_type, water_content, notes, images=None, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.hive_id = hive_id
        self.harvest_date = harvest_date
        self.amount_kg = amount_kg
        self.honey_type = honey_type
        self.water_content = water_content
        self.notes = notes
        self.images = images if images is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "hive_id": self.hive_id,
            "harvest_date": self.harvest_date,
            "amount_kg": self.amount_kg,
            "honey_type": self.honey_type,
            "water_content": self.water_content,
            "notes": self.notes,
            "images": self.images
        }

    @staticmethod
    def from_dict(data):
        from datetime import datetime
        harvest_date = data.get("harvest_date")
        try:
            datetime.strptime(harvest_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            harvest_date = None

        return Harvest(
            id=data.get("id"),
            hive_id=data.get("hive_id"),
            harvest_date=harvest_date,
            amount_kg=data.get("amount_kg"),
            honey_type=data.get("honey_type"),
            water_content=data.get("water_content"),
            notes=data.get("notes"),
            images=data.get("images", [])
        )
