import uuid

class Inspection:
    FORM_LABELS = {
        'inspection_date': 'Inspection Date',
        'brood_status': 'Brood Status',
        'queen_sighted': 'Queen Sighted',
        'swarm_cells': 'Swarm Cells',
        'food_supply': 'Food Supply',
        'measures_taken': 'Measures Taken',
        'observations': 'Observations',
        'images': 'Images'
    }

    def __init__(self, hive_id, inspection_date, brood_status, queen_sighted, swarm_cells, food_supply, measures_taken, observations, images=None, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.hive_id = hive_id
        self.inspection_date = inspection_date
        self.brood_status = brood_status
        self.queen_sighted = queen_sighted
        self.swarm_cells = swarm_cells
        self.food_supply = food_supply
        self.measures_taken = measures_taken
        self.observations = observations
        self.images = images if images is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "hive_id": self.hive_id,
            "inspection_date": self.inspection_date,
            "brood_status": self.brood_status,
            "queen_sighted": self.queen_sighted,
            "swarm_cells": self.swarm_cells,
            "food_supply": self.food_supply,
            "measures_taken": self.measures_taken,
            "observations": self.observations,
            "images": self.images
        }

    @staticmethod
    def from_dict(data):
        from datetime import datetime
        inspection_date = data.get("inspection_date")
        try:
            datetime.strptime(inspection_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            inspection_date = None

        return Inspection(
            id=data.get("id"),
            hive_id=data.get("hive_id"),
            inspection_date=inspection_date,
            brood_status=data.get("brood_status"),
            queen_sighted=data.get("queen_sighted"),
            swarm_cells=data.get("swarm_cells"),
            food_supply=data.get("food_supply"),
            measures_taken=data.get("measures_taken"),
            observations=data.get("observations"),
            images=data.get("images", [])
        )