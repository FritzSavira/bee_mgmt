class Hive:
    def __init__(self, stocknummer, standort, beutentyp, zargen_anzahl, colony_strength=None, temperament=None, swarming_tendency=None, comb_settling=None, honey_yield_rating=None, id=None):
        self.id = id
        self.stocknummer = stocknummer
        self.standort = standort
        self.beutentyp = beutentyp
        self.zargen_anzahl = zargen_anzahl
        self.colony_strength = colony_strength
        self.temperament = temperament
        self.swarming_tendency = swarming_tendency
        self.comb_settling = comb_settling
        self.honey_yield_rating = honey_yield_rating

    def to_dict(self):
        return {
            "id": self.id,
            "stocknummer": self.stocknummer,
            "standort": self.standort,
            "beutentyp": self.beutentyp,
            "zargen_anzahl": self.zargen_anzahl,
            "colony_strength": self.colony_strength,
            "temperament": self.temperament,
            "swarming_tendency": self.swarming_tendency,
            "comb_settling": self.comb_settling,
            "honey_yield_rating": self.honey_yield_rating
        }

    @staticmethod
    def from_dict(data):
        return Hive(
            id=data.get('id'),
            stocknummer=data.get('stocknummer'),
            standort=data.get('standort'),
            beutentyp=data.get('beutentyp'),
            zargen_anzahl=data.get('zargen_anzahl'),
            colony_strength=data.get('colony_strength'),
            temperament=data.get('temperament'),
            swarming_tendency=data.get('swarming_tendency'),
            comb_settling=data.get('comb_settling'),
            honey_yield_rating=data.get('honey_yield_rating')
        )