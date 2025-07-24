import uuid
from app.utils.data_manager import DataManager
from app.models.queen import Queen
from flask import render_template, request, redirect, url_for, Blueprint
from app.controllers.hives_controller import HivesController
from datetime import datetime

class QueensController:
    def __init__(self):
        self.data_manager = DataManager('queens')
        self.hives_controller = HivesController()

    def _generate_queen_name(self, queen_data):
        breed = queen_data.get('breed', 'Unknown')
        origin = queen_data.get('origin', 'Unknown')
        birth_year = 'Unknown'
        if queen_data.get('birth_date'):
            try:
                birth_year = datetime.strptime(queen_data['birth_date'], '%Y-%m-%d').year
            except (ValueError, TypeError):
                birth_year = 'InvalidYear'
        return f"{breed}-{origin}-{birth_year}"

    def get_all_queens(self, hive_id=None):
        queens = self.data_manager.load_all()
        if hive_id:
            queens = [q for q in queens if q.hive_id == hive_id]
        return queens

    def get_queen_by_id(self, queen_id):
        return self.data_manager.load(queen_id)

    def create_queen(self, hive_id, queen_data):
        queen_data['name'] = self._generate_queen_name(queen_data)
        new_queen = Queen(
            id=str(uuid.uuid4()),
            hive_id=hive_id,
            name=queen_data['name'],
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
            
            # Regenerate name based on potentially updated fields
            queen.name = self._generate_queen_name(queen.__dict__)
            
            self.data_manager.update(queen)
            return queen
        return None

    def delete_queen(self, queen_id):
        return self.data_manager.delete(queen_id)

queens_bp = Blueprint('queens_controller', __name__)
queens_instance = QueensController()

@queens_bp.route('/hives/<hive_id>/queens')
def list_queens(hive_id):
    hive = queens_instance.hives_controller.get_hive_by_id(hive_id)
    queens = queens_instance.get_all_queens(hive_id=hive_id)
    return render_template('queens_list.html', hive=hive, queens=queens)

@queens_bp.route('/hives/<hive_id>/queens/new', methods=['GET', 'POST'])
def new_queen(hive_id):
    hive = queens_instance.hives_controller.get_hive_by_id(hive_id)
    if request.method == 'POST':
        queen_data = {
            'hive_id': hive_id,
            'origin': request.form['origin'],
            'birth_date': request.form['birth_date'],
            'color_mark': request.form['color_mark'],
            'breed': request.form['breed'],
            'introduction_date': request.form['introduction_date'],
            'marked': 'marked' in request.form,
            'clipped': 'clipped' in request.form
        }
        queens_instance.create_queen(hive_id, queen_data)
        return redirect(url_for('main.queens_controller.list_queens', hive_id=hive_id))
    return render_template('new_queen.html', hive=hive, form_labels=Queen.FORM_LABELS)

@queens_bp.route('/hives/<hive_id>/queens/<queen_id>/edit', methods=['GET', 'POST'])
def edit_queen(hive_id, queen_id):
    hive = queens_instance.hives_controller.get_hive_by_id(hive_id)
    queen = queens_instance.get_queen_by_id(queen_id)
    if request.method == 'POST':
        updated_data = {
            'origin': request.form['origin'],
            'birth_date': request.form['birth_date'],
            'color_mark': request.form['color_mark'],
            'breed': request.form['breed'],
            'introduction_date': request.form['introduction_date'],
            'marked': 'marked' in request.form,
            'clipped': 'clipped' in request.form
        }
        queens_instance.update_queen(queen_id, updated_data)
        return redirect(url_for('main.queens_controller.list_queens', hive_id=hive_id))
    return render_template('edit_queen.html', hive=hive, queen=queen, form_labels=Queen.FORM_LABELS)

@queens_bp.route('/hives/<hive_id>/queens/<queen_id>/delete', methods=['POST'])
def delete_queen(hive_id, queen_id):
    queens_instance.delete_queen(queen_id)
    return redirect(url_for('main.queens_controller.list_queens', hive_id=hive_id))