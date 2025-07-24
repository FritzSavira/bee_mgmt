from flask import render_template, request, redirect, url_for, Blueprint, current_app, flash
from app.models.varroa_control import VarroaControl
from app.utils.data_manager import DataManager
from app.controllers.hives_controller import HivesController
from app.utils.validators import allowed_file
import os
import uuid

class VarroaControlsController:
    def __init__(self):
        self.data_manager = DataManager('varroa_controls')
        self.hives_controller = HivesController()

    def _save_uploaded_images(self, files):
        image_filenames = []
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        for file in files:
            if file and file.filename and allowed_file(file.filename):
                unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
                file.save(os.path.join(upload_folder, unique_filename))
                image_filenames.append(unique_filename)
            elif file and file.filename:
                # Flash message for invalid file type
                flash(f"{{ _('Invalid file type for') }} '{file.filename}'. {{ _('Allowed types are') }}: {{ ', '.join(current_app.config['ALLOWED_EXTENSIONS']) }}", 'danger')
        return image_filenames

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
            infestation_level=varroa_control_data['infestation_level'],
            images=varroa_control_data.get('images', [])
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
            
            # Handle images
            existing_images = varroa_control.images if varroa_control.images is not None else []
            new_images = updated_data.get('images', [])
            varroa_control.images = existing_images + new_images

            self.data_manager.update(varroa_control)
            return varroa_control
        return None

    def delete_varroa_control(self, varroa_control_id):
        # TODO: Implement deletion of associated image files
        return self.data_manager.delete(varroa_control_id)

varroa_controls_bp = Blueprint('varroa_controls_controller', __name__)
varroa_controls_instance = VarroaControlsController()

@varroa_controls_bp.route('/hives/<hive_id>/varroa_controls')
def varroa_controls_list(hive_id):
    hive = varroa_controls_instance.hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404
    hive_varroa_controls = varroa_controls_instance.get_all_varroa_controls(hive_id=hive_id)
    return render_template('varroa_controls_list.html', hive=hive, varroa_controls=hive_varroa_controls)

@varroa_controls_bp.route('/hives/<hive_id>/varroa_controls/new', methods=['GET', 'POST'])
def new_varroa_control(hive_id):
    hive = varroa_controls_instance.hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404
    if request.method == 'POST':
        varroa_control_data = {
            'control_date': request.form['control_date'],
            'mite_count': request.form['mite_count'],
            'method': request.form['method'],
            'infestation_level': request.form['infestation_level']
        }
        # Handle image uploads
        uploaded_files = request.files.getlist('images')
        image_filenames = varroa_controls_instance._save_uploaded_images(uploaded_files)
        varroa_control_data['images'] = image_filenames

        varroa_controls_instance.create_varroa_control(hive_id, varroa_control_data)
        return redirect(url_for('main.varroa_controls_controller.varroa_controls_list', hive_id=hive_id))
    return render_template('new_varroa_control.html', hive=hive, form_labels=VarroaControl.FORM_LABELS)

@varroa_controls_bp.route('/hives/<hive_id>/varroa_controls/<varroa_control_id>/edit', methods=['GET', 'POST'])
def edit_varroa_control(hive_id, varroa_control_id):
    hive = varroa_controls_instance.hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404
    varroa_control = varroa_controls_instance.get_varroa_control_by_id(varroa_control_id)
    if request.method == 'POST':
        updated_data = {
            'control_date': request.form['control_date'],
            'mite_count': request.form['mite_count'],
            'method': request.form['method'],
            'infestation_level': request.form['infestation_level']
        }
        # Handle image uploads for existing varroa control
        uploaded_files = request.files.getlist('images')
        new_image_filenames = varroa_controls_instance._save_uploaded_images(uploaded_files)
        updated_data['images'] = new_image_filenames

        varroa_controls_instance.update_varroa_control(varroa_control_id, updated_data)
        return redirect(url_for('main.varroa_controls_controller.varroa_controls_list', hive_id=hive_id))
    return render_template('edit_varroa_control.html', hive=hive, varroa_control=varroa_control, form_labels=VarroaControl.FORM_LABELS)

@varroa_controls_bp.route('/hives/<hive_id>/varroa_controls/<varroa_control_id>/delete', methods=['POST'])
def delete_varroa_control(hive_id, varroa_control_id):
    varroa_controls_instance.delete_varroa_control(varroa_control_id)
    return redirect(url_for('main.varroa_controls_controller.varroa_controls_list', hive_id=hive_id))
