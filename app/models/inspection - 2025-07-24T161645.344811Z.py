import uuid

class Inspection:
    def __init__(self, hive_id, inspection_date, brood_status, queen_sighted, swarm_cells, food_supply, measures_taken, observations, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.hive_id = hive_id
        self.inspection_date = inspection_date
        self.brood_status = brood_status
        self.queen_sighted = queen_sighted
        self.swarm_cells = swarm_cells
        self.food_supply = food_supply
        self.measures_taken = measures_taken
        self.observations = observations

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
            "observations": self.observations
        }

    @staticmethod
    def from_dict(data):
        return Inspection(
            id=data.get("id"),
            hive_id=data["hive_id"],
            inspection_date=data["inspection_date"],
            brood_status=data["brood_status"],
            queen_sighted=data["queen_sighted"],
            swarm_cells=data["swarm_cells"],
            food_supply=data["food_supply"],
            measures_taken=data["measures_taken"],
            observations=data["observations"]
        )