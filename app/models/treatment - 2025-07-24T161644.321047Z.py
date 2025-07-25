import uuid

class Treatment:
    def __init__(self, hive_id, treatment_date, treatment_type, used_agent, dosage, duration, efficacy_observation, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.hive_id = hive_id
        self.treatment_date = treatment_date
        self.treatment_type = treatment_type
        self.used_agent = used_agent
        self.dosage = dosage
        self.duration = duration
        self.efficacy_observation = efficacy_observation

    def to_dict(self):
        return {
            "id": self.id,
            "hive_id": self.hive_id,
            "treatment_date": self.treatment_date,
            "treatment_type": self.treatment_type,
            "used_agent": self.used_agent,
            "dosage": self.dosage,
            "duration": self.duration,
            "efficacy_observation": self.efficacy_observation
        }

    @staticmethod
    def from_dict(data):
        return Treatment(
            id=data.get("id"),
            hive_id=data["hive_id"],
            treatment_date=data["treatment_date"],
            treatment_type=data["treatment_type"],
            used_agent=data["used_agent"],
            dosage=data["dosage"],
            duration=data["duration"],
            efficacy_observation=data["efficacy_observation"]
        )