
import uuid

class VarroaControl:
    FORM_LABELS = {
        'control_date': 'Control Date',
        'mite_count': 'Mite Count',
        'method': 'Method',
        'infestation_level': 'Infestation Level',
        'images': 'Images'
    }

    def __init__(self, hive_id, control_date, mite_count, method, infestation_level, images=None, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.hive_id = hive_id
        self.control_date = control_date
        self.mite_count = mite_count
        self.method = method
        self.infestation_level = infestation_level
        self.images = images if images is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "hive_id": self.hive_id,
            "control_date": self.control_date,
            "mite_count": self.mite_count,
            "method": self.method,
            "infestation_level": self.infestation_level,
            "images": self.images
        }

    @staticmethod
    def from_dict(data):
        from datetime import datetime
        control_date = data.get("control_date")
        try:
            datetime.strptime(control_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            control_date = None

        return VarroaControl(
            id=data.get("id"),
            hive_id=data.get("hive_id"),
            control_date=control_date,
            mite_count=data.get("mite_count"),
            method=data.get("method"),
            infestation_level=data.get("infestation_level"),
            images=data.get("images", [])
        )
