from flask import render_template, request, redirect, url_for, Blueprint
from app.models.inspection import Inspection
from app.utils.data_manager import DataManager

class InspectionsController:
    def __init__(self):
        self.data_manager = DataManager('inspections')

    def get_all_inspections(self, hive_id=None):
        inspections = self.data_manager.load_all()
        if hive_id:
            return [i for i in inspections if i.hive_id == hive_id]
        return inspections

    def get_inspection_by_id(self, inspection_id):
        return self.data_manager.load(inspection_id)

    def create_inspection(self, hive_id, inspection_data):
        inspection = Inspection(
            hive_id=hive_id,
            inspection_date=inspection_data['inspection_date'],
            brood_status=inspection_data['brood_status'],
            queen_sighted=inspection_data['queen_sighted'],
            swarm_cells=inspection_data['swarm_cells'],
            food_supply=inspection_data['food_supply'],
            measures_taken=inspection_data['measures_taken'],
            observations=inspection_data['observations']
        )
        self.data_manager.save(inspection)
        return inspection

    def update_inspection(self, inspection_id, updated_data):
        inspection = self.data_manager.load(inspection_id)
        if inspection:
            inspection.inspection_date = updated_data.get('inspection_date', inspection.inspection_date)
            inspection.brood_status = updated_data.get('brood_status', inspection.brood_status)
            inspection.queen_sighted = updated_data.get('queen_sighted', inspection.queen_sighted)
            inspection.swarm_cells = updated_data.get('swarm_cells', inspection.swarm_cells)
            inspection.food_supply = updated_data.get('food_supply', inspection.food_supply)
            inspection.measures_taken = updated_data.get('measures_taken', inspection.measures_taken)
            inspection.observations = updated_data.get('observations', inspection.observations)
            self.data_manager.update(inspection)
            return inspection
        return None

    def delete_inspection(self, inspection_id):
        return self.data_manager.delete(inspection_id)

inspections_bp = Blueprint('inspections_controller', __name__)
inspections_instance = InspectionsController()

@inspections_bp.route('/hives/<hive_id>/inspections')
def inspections_list(hive_id):
    hive_inspections = inspections_instance.get_all_inspections(hive_id=hive_id)
    return render_template('inspections_list.html', hive_id=hive_id, inspections=hive_inspections)

@inspections_bp.route('/hives/<hive_id>/inspections/new', methods=['GET', 'POST'])
def new_inspection(hive_id):
    if request.method == 'POST':
        inspection_date = request.form['inspection_date']
        brood_status = request.form['brood_status']
        queen_sighted = request.form.get('queen_sighted') == 'on'
        swarm_cells = request.form['swarm_cells']
        food_supply = request.form['food_supply']
        measures_taken = request.form['measures_taken']
        observations = request.form['observations']

        inspection_data = {
            'inspection_date': inspection_date,
            'brood_status': brood_status,
            'queen_sighted': queen_sighted,
            'swarm_cells': swarm_cells,
            'food_supply': food_supply,
            'measures_taken': measures_taken,
            'observations': observations
        }
        inspections_instance.create_inspection(hive_id, inspection_data)
        return redirect(url_for('main.inspections_controller.inspections_list', hive_id=hive_id))
    return render_template('new_inspection.html', hive_id=hive_id)

@inspections_bp.route('/hives/<hive_id>/inspections/<inspection_id>/edit', methods=['GET', 'POST'])
def edit_inspection(hive_id, inspection_id):
    inspection = inspections_instance.get_inspection_by_id(inspection_id)
    if request.method == 'POST':
        updated_data = {
            'inspection_date': request.form['inspection_date'],
            'brood_status': request.form['brood_status'],
            'queen_sighted': request.form.get('queen_sighted') == 'on',
            'swarm_cells': request.form['swarm_cells'],
            'food_supply': request.form['food_supply'],
            'measures_taken': request.form['measures_taken'],
            'observations': request.form['observations']
        }
        inspections_instance.update_inspection(inspection_id, updated_data)
        return redirect(url_for('main.inspections_controller.inspections_list', hive_id=hive_id))
    return render_template('edit_inspection.html', hive_id=hive_id, inspection=inspection)

@inspections_bp.route('/hives/<hive_id>/inspections/<inspection_id>/delete', methods=['POST'])
def delete_inspection(hive_id, inspection_id):
    inspections_instance.delete_inspection(inspection_id)
    return redirect(url_for('main.inspections_controller.inspections_list', hive_id=hive_id))
