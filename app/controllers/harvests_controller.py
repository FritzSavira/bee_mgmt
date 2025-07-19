from flask import render_template, request, redirect, url_for, Blueprint
from app.models.harvest import Harvest
from app.utils.data_manager import DataManager
from app.controllers.hives_controller import HivesController

class HarvestsController:
    def __init__(self):
        self.data_manager = DataManager('harvests')
        self.hives_controller = HivesController()

    def get_all_harvests(self, hive_id=None):
        harvests = self.data_manager.load_all()
        if hive_id:
            return [h for h in harvests if h.hive_id == hive_id]
        return harvests

    def get_harvest_by_id(self, harvest_id):
        return self.data_manager.load(harvest_id)

    def create_harvest(self, hive_id, harvest_data):
        harvest = Harvest(
            hive_id=hive_id,
            harvest_date=harvest_data['harvest_date'],
            amount_kg=harvest_data['amount_kg'],
            honey_type=harvest_data['honey_type'],
            water_content=harvest_data['water_content'],
            notes=harvest_data['notes']
        )
        self.data_manager.save(harvest)
        return harvest

    def update_harvest(self, harvest_id, updated_data):
        harvest = self.data_manager.load(harvest_id)
        if harvest:
            harvest.harvest_date = updated_data.get('harvest_date', harvest.harvest_date)
            harvest.amount_kg = updated_data.get('amount_kg', harvest.amount_kg)
            harvest.honey_type = updated_data.get('honey_type', harvest.honey_type)
            harvest.water_content = updated_data.get('water_content', harvest.water_content)
            harvest.notes = updated_data.get('notes', harvest.notes)
            self.data_manager.update(harvest)
            return harvest
        return None

    def delete_harvest(self, harvest_id):
        return self.data_manager.delete(harvest_id)

    def get_total_honey_yield(self):
        all_harvests = self.data_manager.load_all()
        total_yield = sum(float(h.amount_kg) for h in all_harvests)
        return total_yield

harvests_bp = Blueprint('harvests_controller', __name__)
harvests_instance = HarvestsController()

@harvests_bp.route('/hives/<hive_id>/harvests')
def harvests_list(hive_id):
    hive = harvests_instance.hives_controller.get_hive_by_id(hive_id) # Get hive object
    if not hive:
        return "Hive not found", 404 # Handle case where hive is not found
    hive_harvests = harvests_instance.get_all_harvests(hive_id=hive_id)
    return render_template('harvests_list.html', hive=hive, harvests=hive_harvests) # Pass hive object

@harvests_bp.route('/hives/<hive_id>/harvests/new', methods=['GET', 'POST'])
def new_harvest(hive_id):
    hive = harvests_instance.hives_controller.get_hive_by_id(hive_id)
    if request.method == 'POST':
        harvest_data = {
            'harvest_date': request.form['harvest_date'],
            'amount_kg': request.form['amount_kg'],
            'honey_type': request.form['honey_type'],
            'water_content': request.form['water_content'],
            'notes': request.form['notes']
        }
        harvests_instance.create_harvest(hive_id, harvest_data)
        return redirect(url_for('main.harvests_controller.harvests_list', hive_id=hive_id))
    return render_template('new_harvest.html', hive_id=hive_id, hive=hive)

@harvests_bp.route('/hives/<hive_id>/harvests/<harvest_id>/edit', methods=['GET', 'POST'])
def edit_harvest(hive_id, harvest_id):
    hive = harvests_instance.hives_controller.get_hive_by_id(hive_id)
    harvest = harvests_instance.get_harvest_by_id(harvest_id)
    if request.method == 'POST':
        updated_data = {
            'harvest_date': request.form['harvest_date'],
            'amount_kg': request.form['amount_kg'],
            'honey_type': request.form['honey_type'],
            'water_content': request.form['water_content'],
            'notes': request.form['notes']
        }
        harvests_instance.update_harvest(harvest_id, updated_data)
        return redirect(url_for('main.harvests_controller.harvests_list', hive_id=hive_id))
    return render_template('edit_harvest.html', hive=hive, harvest=harvest)

@harvests_bp.route('/hives/<hive_id>/harvests/<harvest_id>/delete', methods=['POST'])
def delete_harvest(hive_id, harvest_id):
    harvests_instance.delete_harvest(harvest_id)
    return redirect(url_for('main.harvests_controller.harvests_list', hive_id=hive_id))

