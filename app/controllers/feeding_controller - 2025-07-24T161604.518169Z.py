from flask import render_template, request, redirect, url_for, Blueprint
from app.models.feeding import Feeding
from app.utils.data_manager import DataManager

class FeedingController:
    def __init__(self):
        self.data_manager = DataManager('feeding')

    def get_all_feedings(self, hive_id=None):
        feedings = self.data_manager.load_all()
        if hive_id:
            return [f for f in feedings if f.hive_id == hive_id]
        return feedings

    def get_feeding_by_id(self, feeding_id):
        return self.data_manager.load(feeding_id)

    def create_feeding(self, hive_id, feeding_data):
        feeding = Feeding(
            hive_id=hive_id,
            feeding_date=feeding_data['feeding_date'],
            food_type=feeding_data['food_type'],
            amount=feeding_data['amount'],
            concentration=feeding_data['concentration']
        )
        self.data_manager.save(feeding)
        return feeding

    def update_feeding(self, feeding_id, updated_data):
        feeding = self.data_manager.load(feeding_id)
        if feeding:
            feeding.feeding_date = updated_data.get('feeding_date', feeding.feeding_date)
            feeding.food_type = updated_data.get('food_type', feeding.food_type)
            feeding.amount = updated_data.get('amount', feeding.amount)
            feeding.concentration = updated_data.get('concentration', feeding.concentration)
            self.data_manager.update(feeding)
            return feeding
        return None

    def delete_feeding(self, feeding_id):
        return self.data_manager.delete(feeding_id)

feeding_bp = Blueprint('feeding_controller', __name__)
feeding_instance = FeedingController()

@feeding_bp.route('/hives/<hive_id>/feeding')
def feeding_list(hive_id):
    hive_feedings = feeding_instance.get_all_feedings(hive_id=hive_id)
    return render_template('feeding_list.html', hive_id=hive_id, feedings=hive_feedings)

@feeding_bp.route('/hives/<hive_id>/feeding/new', methods=['GET', 'POST'])
def new_feeding(hive_id):
    if request.method == 'POST':
        feeding_data = {
            'feeding_date': request.form['feeding_date'],
            'food_type': request.form['food_type'],
            'amount': request.form['amount'],
            'concentration': request.form['concentration']
        }
        feeding_instance.create_feeding(hive_id, feeding_data)
        return redirect(url_for('feeding_controller.feeding_list', hive_id=hive_id))
    return render_template('new_feeding.html', hive_id=hive_id)

@feeding_bp.route('/hives/<hive_id>/feeding/<feeding_id>/edit', methods=['GET', 'POST'])
def edit_feeding(hive_id, feeding_id):
    feeding = feeding_instance.get_feeding_by_id(feeding_id)
    if request.method == 'POST':
        updated_data = {
            'feeding_date': request.form['feeding_date'],
            'food_type': request.form['food_type'],
            'amount': request.form['amount'],
            'concentration': request.form['concentration']
        }
        feeding_instance.update_feeding(feeding_id, updated_data)
        return redirect(url_for('feeding_controller.feeding_list', hive_id=hive_id))
    return render_template('edit_feeding.html', hive_id=hive_id, feeding=feeding)

@feeding_bp.route('/hives/<hive_id>/feeding/<feeding_id>/delete', methods=['POST'])
def delete_feeding(hive_id, feeding_id):
    feeding_instance.delete_feeding(feeding_id)
    return redirect(url_for('feeding_controller.feeding_list', hive_id=hive_id))