import uuid
from datetime import date, timedelta, datetime
from app.utils.data_manager import DataManager
from app.models.hive import Hive
from app.models.inspection import Inspection
from app.models.treatment import Treatment

class HivesController:
    def __init__(self):
        self.data_manager = DataManager('hives')
        self.inspections_data_manager = DataManager('inspections')
        self.treatments_data_manager = DataManager('treatments')
        self.queens_data_manager = DataManager('queens')

    def get_all_hives(self):
        hives = self.data_manager.load_all()
        queens = self.queens_data_manager.load_all()

        queens_by_hive = {}
        for queen in queens:
            if not hasattr(queen, 'hive_id') or not queen.hive_id:
                continue
            if queen.hive_id not in queens_by_hive:
                queens_by_hive[queen.hive_id] = []
            queens_by_hive[queen.hive_id].append(queen)

        for hive in hives:
            hive.queen = None
            if hive.id in queens_by_hive:
                hive_queens = queens_by_hive[hive.id]
                
                valid_queens = []
                for q in hive_queens:
                    if hasattr(q, 'birth_date') and q.birth_date:
                        try:
                            q.birth_date_obj = datetime.strptime(q.birth_date, '%Y-%m-%d')
                            valid_queens.append(q)
                        except (ValueError, TypeError):
                            continue
                
                if valid_queens:
                    valid_queens.sort(key=lambda x: x.birth_date_obj, reverse=True)
                    hive.queen = valid_queens[0]
        
        return hives

    def get_hive_by_id(self, hive_id):
        hive = self.data_manager.load(hive_id)
        if not hive:
            return None

        queens = self.queens_data_manager.get_all_for_hive(hive.id)
        
        hive.queen = None
        if queens:
            valid_queens = []
            for q in queens:
                if hasattr(q, 'birth_date') and q.birth_date:
                    try:
                        q.birth_date_obj = datetime.strptime(q.birth_date, '%Y-%m-%d')
                        valid_queens.append(q)
                    except (ValueError, TypeError):
                        continue
            
            if valid_queens:
                valid_queens.sort(key=lambda x: x.birth_date_obj, reverse=True)
                hive.queen = valid_queens[0]

        return hive

    def create_hive(self, hive_data):
        new_hive = Hive(
            id=str(uuid.uuid4()),
            stocknummer=hive_data['stocknummer'],
            standort=hive_data['standort'],
            beutentyp=hive_data['beutentyp'],
            zargen_anzahl=hive_data['zargen_anzahl'],
            colony_strength=hive_data.get('colony_strength'),
            temperament=hive_data.get('temperament'),
            swarming_tendency=hive_data.get('swarming_tendency'),
            comb_settling=hive_data.get('comb_settling'),
            honey_yield_rating=hive_data.get('honey_yield_rating')
        )
        self.data_manager.save(new_hive)
        return new_hive

    def update_hive(self, hive_id, updated_data):
        hive = self.data_manager.load(hive_id)
        if hive:
            hive.stocknummer = updated_data.get('stocknummer', hive.stocknummer)
            hive.standort = updated_data.get('standort', hive.standort)
            hive.beutentyp = updated_data.get('beutentyp', hive.beutentyp)
            hive.zargen_anzahl = updated_data.get('zargen_anzahl', hive.zargen_anzahl)
            hive.colony_strength = updated_data.get('colony_strength', hive.colony_strength)
            hive.temperament = updated_data.get('temperament', hive.temperament)
            hive.swarming_tendency = updated_data.get('swarming_tendency', hive.swarming_tendency)
            hive.comb_settling = updated_data.get('comb_settling', hive.comb_settling)
            hive.honey_yield_rating = updated_data.get('honey_yield_rating', hive.honey_yield_rating)
            self.data_manager.update(hive)
            return hive
        return None

    def delete_hive(self, hive_id):
        return self.data_manager.delete(hive_id)

    def get_overdue_inspections(self):
        overdue_hives = []
        all_hives = self.get_all_hives()
        today = date.today()

        for hive in all_hives:
            hive_inspections = self.inspections_data_manager.get_all_for_hive(hive.id)
            if not hive_inspections:
                overdue_hives.append({'hive': hive, 'reason': 'No inspections recorded'})
                continue

            latest_inspection_date = None
            for inspection in hive_inspections:
                try:
                    inspection_date = datetime.strptime(inspection.inspection_date, '%Y-%m-%d').date()
                    if latest_inspection_date is None or inspection_date > latest_inspection_date:
                        latest_inspection_date = inspection_date
                except (ValueError, TypeError):
                    # Handle cases where date format might be incorrect or date is None
                    continue

            if latest_inspection_date and (today - latest_inspection_date) > timedelta(days=30): # Example: overdue if no inspection in 30 days
                overdue_hives.append({'hive': hive, 'reason': f'Last inspection on {latest_inspection_date.strftime("%Y-%m-%d")} is over 30 days old'})
        return overdue_hives

    def get_overdue_treatments(self):
        overdue_hives = []
        all_hives = self.get_all_hives()
        today = date.today()

        for hive in all_hives:
            hive_treatments = self.treatments_data_manager.get_all_for_hive(hive.id)
            if not hive_treatments:
                overdue_hives.append({'hive': hive, 'reason': 'No treatments recorded'})
                continue

            latest_treatment_date = None
            for treatment in hive_treatments:
                try:
                    treatment_date = datetime.strptime(treatment.treatment_date, '%Y-%m-%d').date()
                    if latest_treatment_date is None or treatment_date > latest_treatment_date:
                        latest_treatment_date = treatment_date
                except (ValueError, TypeError):
                    # Handle cases where date format might be incorrect or date is None
                    continue

            # Example: overdue if last treatment was more than 90 days ago (adjust as needed)
            if latest_treatment_date and (today - latest_treatment_date) > timedelta(days=90):
                overdue_hives.append({'hive': hive, 'reason': f'Last treatment on {latest_treatment_date.strftime("%Y-%m-%d")} is over 90 days old'})
        return overdue_hives
