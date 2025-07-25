
import uuid

class VarroaControl:
    def __init__(self, hive_id, control_date, mite_count, method, infestation_level, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.hive_id = hive_id
        self.control_date = control_date
        self.mite_count = mite_count
        self.method = method
        self.infestation_level = infestation_level

    def to_dict(self):
        return {
            "id": self.id,
            "hive_id": self.hive_id,
            "control_date": self.control_date,
            "mite_count": self.mite_count,
            "method": self.method,
            "infestation_level": self.infestation_level
        }

    @staticmethod
    def from_dict(data):
        return VarroaControl(
            id=data.get("id"),
            hive_id=data["hive_id"],
            control_date=data["control_date"],
            mite_count=data["mite_count"],
            method=data["method"],
            infestation_level=data["infestation_level"]
        )
