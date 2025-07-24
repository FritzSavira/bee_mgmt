import uuid

class Treatment:
    FORM_LABELS = {
        'treatment_date': 'Treatment Date',
        'treatment_type': 'Treatment Type',
        'used_agent': 'Used Agent',
        'dosage': 'Dosage',
        'duration': 'Duration of Treatment',
        'efficacy_observation': 'Efficacy Observation',
        'images': 'Images'
    }

    def __init__(self, hive_id, treatment_date, treatment_type, used_agent, dosage, duration, efficacy_observation, images=None, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.hive_id = hive_id
        self.treatment_date = treatment_date
        self.treatment_type = treatment_type
        self.used_agent = used_agent
        self.dosage = dosage
        self.duration = duration
        self.efficacy_observation = efficacy_observation
        self.images = images if images is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "hive_id": self.hive_id,
            "treatment_date": self.treatment_date,
            "treatment_type": self.treatment_type,
            "used_agent": self.used_agent,
            "dosage": self.dosage,
            "duration": self.duration,
            "efficacy_observation": self.efficacy_observation,
            "images": self.images
        }

    @staticmethod
    def from_dict(data):
        from datetime import datetime
        treatment_date = data.get("treatment_date")
        try:
            datetime.strptime(treatment_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            treatment_date = None

        return Treatment(
            id=data.get("id"),
            hive_id=data.get("hive_id"),
            treatment_date=treatment_date,
            treatment_type=data.get("treatment_type"),
            used_agent=data.get("used_agent"),
            dosage=data.get("dosage"),
            duration=data.get("duration"),
            efficacy_observation=data.get("efficacy_observation"),
            images=data.get("images", [])
        )