import uuid
from app.utils.data_manager import DataManager
from app.models.queen import Queen

class QueensController:
    def __init__(self):
        self.data_manager = DataManager('queens')

    def get_all_queens(self, hive_id=None):
        queens = self.data_manager.load_all()
        if hive_id:
            queens = [q for q in queens if q.hive_id == hive_id]
        return queens

    def get_queen_by_id(self, queen_id):
        return self.data_manager.load(queen_id)

    def create_queen(self, queen_data):
        new_queen = Queen(
            id=str(uuid.uuid4()),
            hive_id=queen_data['hive_id'],
            origin=queen_data['origin'],
            birth_date=queen_data['birth_date'],
            color_mark=queen_data['color_mark'],
            breed=queen_data['breed'],
            introduction_date=queen_data['introduction_date'],
            marked=queen_data['marked'],
            clipped=queen_data['clipped']
        )
        self.data_manager.save(new_queen)
        return new_queen

    def update_queen(self, queen_id, updated_data):
        queen = self.data_manager.load(queen_id)
        if queen:
            queen.origin = updated_data.get('origin', queen.origin)
            queen.birth_date = updated_data.get('birth_date', queen.birth_date)
            queen.color_mark = updated_data.get('color_mark', queen.color_mark)
            queen.breed = updated_data.get('breed', queen.breed)
            queen.introduction_date = updated_data.get('introduction_date', queen.introduction_date)
            queen.marked = updated_data.get('marked', queen.marked)
            queen.clipped = updated_data.get('clipped', queen.clipped)
            self.data_manager.update(queen)
            return queen
        return None

    def delete_queen(self, queen_id):
        return self.data_manager.delete(queen_id)
