from flask import render_template, request, redirect, url_for, Blueprint, current_app, flash
from app.models.inspection import Inspection
from app.utils.data_manager import DataManager
from app.controllers.hives_controller import HivesController
from app.utils.validators import allowed_file
import os
import uuid

class InspectionsController:
    def __init__(self):
        self.data_manager = DataManager('inspections')
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
            observations=inspection_data['observations'],
            images=inspection_data.get('images', [])
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
            
            # Handle images
            existing_images = inspection.images if inspection.images is not None else []
            new_images = updated_data.get('images', [])
            inspection.images = existing_images + new_images

            self.data_manager.update(inspection)
            return inspection
        return None

    def delete_inspection(self, inspection_id):
        # TODO: Implement deletion of associated image files
        return self.data_manager.delete(inspection_id)

inspections_bp = Blueprint('inspections_controller', __name__)
inspections_instance = InspectionsController()

@inspections_bp.route('/hives/<hive_id>/inspections')
def inspections_list(hive_id):
    hive = inspections_instance.hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404
    hive_inspections = inspections_instance.get_all_inspections(hive_id=hive_id)
    return render_template('inspections_list.html', hive=hive, inspections=hive_inspections)

@inspections_bp.route('/hives/<hive_id>/inspections/new', methods=['GET', 'POST'])
def new_inspection(hive_id):
    hive = inspections_instance.hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404

    if request.method == 'POST':
        inspection_date = request.form['inspection_date']
        brood_status = request.form['brood_status']
        queen_sighted = request.form.get('queen_sighted') == 'on'
        swarm_cells = request.form['swarm_cells']
        food_supply = request.form['food_supply']
        measures_taken = request.form['measures_taken']
        observations = request.form['observations']
        
        # Handle image uploads
        uploaded_files = request.files.getlist('images')
        image_filenames = inspections_instance._save_uploaded_images(uploaded_files)

        inspection_data = {
            'inspection_date': inspection_date,
            'brood_status': brood_status,
            'queen_sighted': queen_sighted,
            'swarm_cells': swarm_cells,
            'food_supply': food_supply,
            'measures_taken': measures_taken,
            'observations': observations,
            'images': image_filenames
        }
        inspections_instance.create_inspection(hive_id, inspection_data)
        return redirect(url_for('main.inspections_controller.inspections_list', hive_id=hive_id))
    return render_template('new_inspection.html', hive=hive, form_labels=Inspection.FORM_LABELS)

@inspections_bp.route('/hives/<hive_id>/inspections/<inspection_id>/edit', methods=['GET', 'POST'])
def edit_inspection(hive_id, inspection_id):
    hive = inspections_instance.hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404

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
        
        # Handle image uploads for existing inspection
        uploaded_files = request.files.getlist('images')
        new_image_filenames = inspections_instance._save_uploaded_images(uploaded_files)
        updated_data['images'] = new_image_filenames

        inspections_instance.update_inspection(inspection_id, updated_data)
        return redirect(url_for('main.inspections_controller.inspections_list', hive_id=hive_id))
    return render_template('edit_inspection.html', hive=hive, inspection=inspection, form_labels=Inspection.FORM_LABELS)

@inspections_bp.route('/hives/<hive_id>/inspections/<inspection_id>/delete', methods=['POST'])
def delete_inspection(hive_id, inspection_id):
    inspections_instance.delete_inspection(inspection_id)
    return redirect(url_for('main.inspections_controller.inspections_list', hive_id=hive_id))
