from flask import render_template, request, redirect, url_for, Blueprint, current_app, flash
from app.models.feeding import Feeding
from app.utils.data_manager import DataManager
from app.controllers.hives_controller import HivesController
from app.utils.validators import allowed_file
import os
import uuid

class FeedingController:
    def __init__(self):
        self.data_manager = DataManager('feeding')
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
            concentration=feeding_data['concentration'],
            images=feeding_data.get('images', [])
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
            
            # Handle images
            existing_images = feeding.images if feeding.images is not None else []
            new_images = updated_data.get('images', [])
            feeding.images = existing_images + new_images

            self.data_manager.update(feeding)
            return feeding
        return None

    def delete_feeding(self, feeding_id):
        # TODO: Implement deletion of associated image files
        return self.data_manager.delete(feeding_id)

feeding_bp = Blueprint('feeding_controller', __name__)
feeding_instance = FeedingController()

@feeding_bp.route('/hives/<hive_id>/feeding')
def feeding_list(hive_id):
    hive = feeding_instance.hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404
    hive_feedings = feeding_instance.get_all_feedings(hive_id=hive_id)
    return render_template('feeding_list.html', hive=hive, feedings=hive_feedings)

@feeding_bp.route('/hives/<hive_id>/feeding/new', methods=['GET', 'POST'])
def new_feeding(hive_id):
    hive = feeding_instance.hives_controller.get_hive_by_id(hive_id)
    if request.method == 'POST':
        feeding_data = {
            'feeding_date': request.form['feeding_date'],
            'food_type': request.form['food_type'],
            'amount': request.form['amount'],
            'concentration': request.form['concentration']
        }
        # Handle image uploads
        uploaded_files = request.files.getlist('images')
        image_filenames = feeding_instance._save_uploaded_images(uploaded_files)
        feeding_data['images'] = image_filenames

        feeding_instance.create_feeding(hive_id, feeding_data)
        return redirect(url_for('main.feeding_controller.feeding_list', hive_id=hive_id))
    return render_template('new_feeding.html', hive_id=hive_id, hive=hive, form_labels=Feeding.FORM_LABELS)

@feeding_bp.route('/hives/<hive_id>/feeding/<feeding_id>/edit', methods=['GET', 'POST'])
def edit_feeding(hive_id, feeding_id):
    hive = feeding_instance.hives_controller.get_hive_by_id(hive_id)
    feeding = feeding_instance.get_feeding_by_id(feeding_id)
    if request.method == 'POST':
        updated_data = {
            'feeding_date': request.form['feeding_date'],
            'food_type': request.form['food_type'],
            'amount': request.form['amount'],
            'concentration': request.form['concentration']
        }
        # Handle image uploads for existing feeding
        uploaded_files = request.files.getlist('images')
        new_image_filenames = feeding_instance._save_uploaded_images(uploaded_files)
        updated_data['images'] = new_image_filenames

        feeding_instance.update_feeding(feeding_id, updated_data)
        return redirect(url_for('main.feeding_controller.feeding_list', hive_id=hive_id))
    return render_template('edit_feeding.html', hive_id=hive_id, feeding=feeding, hive=hive, form_labels=Feeding.FORM_LABELS)

@feeding_bp.route('/hives/<hive_id>/feeding/<feeding_id>/delete', methods=['POST'])
def delete_feeding(hive_id, feeding_id):
    feeding_instance.delete_feeding(feeding_id)
    return redirect(url_for('main.feeding_controller.feeding_list', hive_id=hive_id))
