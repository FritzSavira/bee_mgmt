from flask import render_template, request, redirect, url_for, Blueprint, current_app, flash
from app.models.treatment import Treatment
from app.utils.data_manager import DataManager
from app.controllers.hives_controller import HivesController
from app.utils.validators import allowed_file
import os
import uuid

class TreatmentsController:
    def __init__(self):
        self.data_manager = DataManager('treatments')
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

    def get_all_treatments(self, hive_id=None):
        treatments = self.data_manager.load_all()
        if hive_id:
            return [t for t in treatments if t.hive_id == hive_id]
        return treatments

    def get_treatment_by_id(self, treatment_id):
        return self.data_manager.load(treatment_id)

    def create_treatment(self, hive_id, treatment_data):
        treatment = Treatment(
            hive_id=hive_id,
            treatment_date=treatment_data['treatment_date'],
            treatment_type=treatment_data['treatment_type'],
            used_agent=treatment_data['used_agent'],
            dosage=treatment_data['dosage'],
            duration=treatment_data['duration'],
            efficacy_observation=treatment_data['efficacy_observation'],
            images=treatment_data.get('images', [])
        )
        self.data_manager.save(treatment)
        return treatment

    def update_treatment(self, treatment_id, updated_data):
        treatment = self.data_manager.load(treatment_id)
        if treatment:
            treatment.treatment_date = updated_data.get('treatment_date', treatment.treatment_date)
            treatment.treatment_type = updated_data.get('treatment_type', treatment.treatment_type)
            treatment.used_agent = updated_data.get('used_agent', treatment.used_agent)
            treatment.dosage = updated_data.get('dosage', treatment.dosage)
            treatment.duration = updated_data.get('duration', treatment.duration)
            treatment.efficacy_observation = updated_data.get('efficacy_observation', treatment.efficacy_observation)
            
            # Handle images
            existing_images = treatment.images if treatment.images is not None else []
            new_images = updated_data.get('images', [])
            treatment.images = existing_images + new_images

            self.data_manager.update(treatment)
            return treatment
        return None

    def delete_treatment(self, treatment_id):
        # TODO: Implement deletion of associated image files
        return self.data_manager.delete(treatment_id)

treatments_bp = Blueprint('treatments_controller', __name__)
treatments_instance = TreatmentsController()

@treatments_bp.route('/hives/<hive_id>/treatments')
def treatments_list(hive_id):
    hive = treatments_instance.hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404
    hive_treatments = treatments_instance.get_all_treatments(hive_id=hive_id)
    return render_template('treatments_list.html', hive=hive, treatments=hive_treatments)

@treatments_bp.route('/hives/<hive_id>/treatments/new', methods=['GET', 'POST'])
def new_treatment(hive_id):
    hive = treatments_instance.hives_controller.get_hive_by_id(hive_id)
    if request.method == 'POST':
        treatment_data = {
            'treatment_date': request.form['treatment_date'],
            'treatment_type': request.form['treatment_type'],
            'used_agent': request.form['used_agent'],
            'dosage': request.form['dosage'],
            'duration': request.form['duration'],
            'efficacy_observation': request.form['efficacy_observation']
        }
        # Handle image uploads
        uploaded_files = request.files.getlist('images')
        image_filenames = treatments_instance._save_uploaded_images(uploaded_files)
        treatment_data['images'] = image_filenames

        treatments_instance.create_treatment(hive_id, treatment_data)
        return redirect(url_for('main.treatments_controller.treatments_list', hive_id=hive_id))
    return render_template('new_treatment.html', hive=hive, form_labels=Treatment.FORM_LABELS)

@treatments_bp.route('/hives/<hive_id>/treatments/<treatment_id>/edit', methods=['GET', 'POST'])
def edit_treatment(hive_id, treatment_id):
    hive = treatments_instance.hives_controller.get_hive_by_id(hive_id)
    treatment = treatments_instance.get_treatment_by_id(treatment_id)
    if request.method == 'POST':
        updated_data = {
            'treatment_date': request.form['treatment_date'],
            'treatment_type': request.form['treatment_type'],
            'used_agent': request.form['used_agent'],
            'dosage': request.form['dosage'],
            'duration': request.form['duration'],
            'efficacy_observation': request.form['efficacy_observation']
        }
        # Handle image uploads for existing treatment
        uploaded_files = request.files.getlist('images')
        new_image_filenames = treatments_instance._save_uploaded_images(uploaded_files)
        updated_data['images'] = new_image_filenames

        treatments_instance.update_treatment(treatment_id, updated_data)
        return redirect(url_for('main.treatments_controller.treatments_list', hive_id=hive_id))
    return render_template('edit_treatment.html', hive=hive, treatment=treatment, form_labels=Treatment.FORM_LABELS)

@treatments_bp.route('/hives/<hive_id>/treatments/<treatment_id>/delete', methods=['POST'])
def delete_treatment(hive_id, treatment_id):
    treatments_instance.delete_treatment(treatment_id)
    return redirect(url_for('main.treatments_controller.treatments_list', hive_id=hive_id))
