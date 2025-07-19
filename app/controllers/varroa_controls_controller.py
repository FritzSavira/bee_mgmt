from flask import render_template, request, redirect, url_for, Blueprint
from app.models.varroa_control import VarroaControl
from app.utils.data_manager import DataManager

class VarroaControlsController:
    def __init__(self):
        self.data_manager = DataManager('varroa_controls')

    def get_all_varroa_controls(self, hive_id=None):
        varroa_controls = self.data_manager.load_all()
        if hive_id:
            return [vc for vc in varroa_controls if vc.hive_id == hive_id]
        return varroa_controls

    def get_varroa_control_by_id(self, varroa_control_id):
        return self.data_manager.load(varroa_control_id)

    def create_varroa_control(self, hive_id, varroa_control_data):
        varroa_control = VarroaControl(
            hive_id=hive_id,
            control_date=varroa_control_data['control_date'],
            mite_count=varroa_control_data['mite_count'],
            method=varroa_control_data['method'],
            infestation_level=varroa_control_data['infestation_level']
        )
        self.data_manager.save(varroa_control)
        return varroa_control

    def update_varroa_control(self, varroa_control_id, updated_data):
        varroa_control = self.data_manager.load(varroa_control_id)
        if varroa_control:
            varroa_control.control_date = updated_data.get('control_date', varroa_control.control_date)
            varroa_control.mite_count = updated_data.get('mite_count', varroa_control.mite_count)
            varroa_control.method = updated_data.get('method', varroa_control.method)
            varroa_control.infestation_level = updated_data.get('infestation_level', varroa_control.infestation_level)
            self.data_manager.update(varroa_control)
            return varroa_control
        return None

    def delete_varroa_control(self, varroa_control_id):
        return self.data_manager.delete(varroa_control_id)

varroa_controls_bp = Blueprint('varroa_controls_controller', __name__)
varroa_controls_instance = VarroaControlsController()

@varroa_controls_bp.route('/hives/<hive_id>/varroa_controls')
def varroa_controls_list(hive_id):
    hive_varroa_controls = varroa_controls_instance.get_all_varroa_controls(hive_id=hive_id)
    return render_template('varroa_controls_list.html', hive_id=hive_id, varroa_controls=hive_varroa_controls)

@varroa_controls_bp.route('/hives/<hive_id>/varroa_controls/new', methods=['GET', 'POST'])
def new_varroa_control(hive_id):
    if request.method == 'POST':
        varroa_control_data = {
            'control_date': request.form['control_date'],
            'mite_count': request.form['mite_count'],
            'method': request.form['method'],
            'infestation_level': request.form['infestation_level']
        }
        varroa_controls_instance.create_varroa_control(hive_id, varroa_control_data)
        return redirect(url_for('main.varroa_controls_controller.varroa_controls_list', hive_id=hive_id))
    return render_template('new_varroa_control.html', hive_id=hive_id)

@varroa_controls_bp.route('/hives/<hive_id>/varroa_controls/<varroa_control_id>/edit', methods=['GET', 'POST'])
def edit_varroa_control(hive_id, varroa_control_id):
    varroa_control = varroa_controls_instance.get_varroa_control_by_id(varroa_control_id)
    if request.method == 'POST':
        updated_data = {
            'control_date': request.form['control_date'],
            'mite_count': request.form['mite_count'],
            'method': request.form['method'],
            'infestation_level': request.form['infestation_level']
        }
        varroa_controls_instance.update_varroa_control(varroa_control_id, updated_data)
        return redirect(url_for('main.varroa_controls_controller.varroa_controls_list', hive_id=hive_id))
    return render_template('edit_varroa_control.html', hive_id=hive_id, varroa_control=varroa_control)

@varroa_controls_bp.route('/hives/<hive_id>/varroa_controls/<varroa_control_id>/delete', methods=['POST'])
def delete_varroa_control(hive_id, varroa_control_id):
    varroa_controls_instance.delete_varroa_control(varroa_control_id)
    return redirect(url_for('main.varroa_controls_controller.varroa_controls_list', hive_id=hive_id))