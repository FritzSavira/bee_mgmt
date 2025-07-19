import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data')

class DataManager:
    def __init__(self, entity_name):
        self.entity_name = entity_name
        self.filepath = os.path.join(DATA_DIR, f'{entity_name}.json')

    def _load_raw_data(self):
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_raw_data(self, data):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_all(self):
        from app.models.hive import Hive
        from app.models.queen import Queen
        from app.models.inspection import Inspection
        from app.models.treatment import Treatment
        from app.models.feeding import Feeding
        from app.models.harvest import Harvest
        from app.models.varroa_control import VarroaControl
        from app.models.split import Split

        model_map = {
            'hives': Hive,
            'queens': Queen,
            'inspections': Inspection,
            'treatments': Treatment,
            'feeding': Feeding,
            'harvests': Harvest,
            'varroa_controls': VarroaControl,
            'splits': Split
        }
        raw_data = self._load_raw_data()
        model_class = model_map.get(self.entity_name)
        if model_class:
            return [model_class.from_dict(item) for item in raw_data]
        return raw_data

    def load(self, item_id):
        all_items = self.load_all()
        for item in all_items:
            if item.id == item_id:
                return item
        return None

    def save(self, item):
        all_items = self.load_all()
        all_items.append(item)
        self._save_raw_data([i.to_dict() for i in all_items])

    def update(self, updated_item):
        all_items = self.load_all()
        updated = False
        for i, item in enumerate(all_items):
            if item.id == updated_item.id:
                all_items[i] = updated_item
                updated = True
                break
        if updated:
            self._save_raw_data([i.to_dict() for i in all_items])
        return updated

    def delete(self, item_id):
        all_items = self.load_all()
        initial_len = len(all_items)
        all_items = [item for item in all_items if item.id != item_id]
        if len(all_items) < initial_len:
            self._save_raw_data([i.to_dict() for i in all_items])
            return True
        return False

    def get_all_for_hive(self, hive_id):
        all_items = self.load_all()
        return [item for item in all_items if hasattr(item, 'hive_id') and item.hive_id == hive_id]