
import uuid

class Split:
    FORM_LABELS = {
        'split_date': 'Split Date',
        'method': 'Method',
        'new_hive_id': 'New Hive ID (optional)',
        'images': 'Images'
    }

    def __init__(self, hive_id, split_date, method, new_hive_id, images=None, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.hive_id = hive_id
        self.split_date = split_date
        self.method = method
        self.new_hive_id = new_hive_id
        self.images = images if images is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "hive_id": self.hive_id,
            "split_date": self.split_date,
            "method": self.method,
            "new_hive_id": self.new_hive_id,
            "images": self.images
        }

    @staticmethod
    def from_dict(data):
        from datetime import datetime
        split_date = data.get("split_date")
        try:
            datetime.strptime(split_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            split_date = None

        return Split(
            id=data.get("id"),
            hive_id=data.get("hive_id"),
            split_date=split_date,
            method=data.get("method"),
            new_hive_id=data.get("new_hive_id"),
            images=data.get("images", [])
        )
