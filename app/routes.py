from flask import Blueprint, render_template, request, redirect, url_for, current_app
from datetime import datetime
from .utils.data_manager import DataManager
from .controllers.hives_controller import HivesController
from .controllers.queens_controller import QueensController, queens_bp
from .controllers.inspections_controller import inspections_bp, inspections_instance
from .controllers.treatments_controller import treatments_bp, treatments_instance
from .controllers.feeding_controller import feeding_bp, feeding_instance
from .controllers.harvests_controller import harvests_bp, harvests_instance
from .controllers.varroa_controls_controller import varroa_controls_bp, varroa_controls_instance
from .controllers.splits_controller import splits_bp, splits_instance

bp = Blueprint('main', __name__)
hives_controller = HivesController()
queens_instance = QueensController()
bp.register_blueprint(inspections_bp, url_prefix='/')
bp.register_blueprint(treatments_bp, url_prefix='/')
bp.register_blueprint(feeding_bp, url_prefix='/')
bp.register_blueprint(harvests_bp, url_prefix='/')
bp.register_blueprint(varroa_controls_bp, url_prefix='/')
bp.register_blueprint(splits_bp, url_prefix='/')
bp.register_blueprint(queens_bp, url_prefix='/')

@bp.route('/')
def index():
    hives = hives_controller.get_all_hives()
    overdue_inspections = hives_controller.get_overdue_inspections()
    overdue_treatments = hives_controller.get_overdue_treatments()
    return render_template('index.html', hives=hives, overdue_inspections=overdue_inspections, overdue_treatments=overdue_treatments)

from .models.hive import Hive

@bp.route('/hives/new', methods=['GET', 'POST'])
def new_hive():
    if request.method == 'POST':
        hive_data = {
            'stocknummer': request.form['stocknummer'],
            'standort': request.form['standort'],
            'beutentyp': request.form['beutentyp'],
            'zargen_anzahl': request.form['zargen_anzahl'],
            'colony_strength': request.form.get('colony_strength'),
            'temperament': request.form.get('temperament'),
            'swarming_tendency': request.form.get('swarming_tendency'),
            'comb_settling': request.form.get('comb_settling'),
            'honey_yield_rating': request.form.get('honey_yield_rating')
        }
        hives_controller.create_hive(hive_data)
        return redirect(url_for('main.index'))
    return render_template('new_hive.html', form_labels=Hive.FORM_LABELS)

@bp.route('/hives/<hive_id>/edit', methods=['GET', 'POST'])
def edit_hive(hive_id):
    hive = hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404

    if request.method == 'POST':
        updated_data = {
            'stocknummer': request.form['stocknummer'],
            'standort': request.form['standort'],
            'beutentyp': request.form['beutentyp'],
            'zargen_anzahl': request.form['zargen_anzahl'],
            'colony_strength': request.form.get('colony_strength'),
            'temperament': request.form.get('temperament'),
            'swarming_tendency': request.form.get('swarming_tendency'),
            'comb_settling': request.form.get('comb_settling'),
            'honey_yield_rating': request.form.get('honey_yield_rating')
        }
        hives_controller.update_hive(hive_id, updated_data)
        return redirect(url_for('main.index'))
    return render_template('edit_hive.html', hive=hive, form_labels=Hive.FORM_LABELS)

@bp.route('/hives/<hive_id>/delete', methods=['POST'])
def delete_hive(hive_id):
    hives_controller.delete_hive(hive_id)
    return redirect(url_for('main.index'))

@bp.route('/hives/<hive_id>')
def hive_detail(hive_id):
    hive = hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404

    # The queen is needed for the header, but not part of the timeline
    queens = queens_instance.get_all_queens(hive_id=hive_id)

    # Get all event types
    inspections = inspections_instance.get_all_inspections(hive_id=hive_id)
    treatments = treatments_instance.get_all_treatments(hive_id=hive_id)
    feedings = feeding_instance.get_all_feedings(hive_id=hive_id)
    harvests = harvests_instance.get_all_harvests(hive_id=hive_id)
    varroa_controls = varroa_controls_instance.get_all_varroa_controls(hive_id=hive_id)
    splits = splits_instance.get_all_splits(hive_id=hive_id)

    timeline_events = []

    # Add a 'type' and a proper 'date' object to each event for sorting and rendering
    # This assumes date strings are in 'YYYY-MM-DD' format.
    for event in inspections:
        try:
            event.event_key = 'inspection'
            event.date = datetime.strptime(event.inspection_date, '%Y-%m-%d')
            timeline_events.append(event)
        except (ValueError, TypeError):
            continue # Skip events with invalid date formats

    for event in treatments:
        try:
            event.event_key = 'treatment'
            event.date = datetime.strptime(event.treatment_date, '%Y-%m-%d')
            timeline_events.append(event)
        except (ValueError, TypeError):
            continue

    for event in feedings:
        try:
            event.event_key = 'feeding'
            event.date = datetime.strptime(event.feeding_date, '%Y-%m-%d')
            timeline_events.append(event)
        except (ValueError, TypeError):
            continue
        
    for event in harvests:
        try:
            event.event_key = 'harvest'
            event.date = datetime.strptime(event.harvest_date, '%Y-%m-%d')
            timeline_events.append(event)
        except (ValueError, TypeError):
            continue

    for event in varroa_controls:
        try:
            event.event_key = 'varroa_control'
            event.date = datetime.strptime(event.control_date, '%Y-%m-%d')
            timeline_events.append(event)
        except (ValueError, TypeError):
            continue

    for event in splits:
        try:
            event.event_key = 'split'
            event.date = datetime.strptime(event.split_date, '%Y-%m-%d')
            timeline_events.append(event)
        except (ValueError, TypeError):
            continue

    for event in queens:
        try:
            event.event_key = 'queen'
            if event.introduction_date:
                event.date = datetime.strptime(event.introduction_date, '%Y-%m-%d')
            elif event.birth_date:
                event.date = datetime.strptime(event.birth_date, '%Y-%m-%d')
            else:
                continue # Skip if neither date is available
            timeline_events.append(event)
        except (ValueError, TypeError):
            continue

    # Sort all events by date, newest first
    timeline_events.sort(key=lambda x: x.date, reverse=True)

    return render_template('hive_detail.html', hive=hive, queens=queens, timeline_events=timeline_events)

@bp.route('/reports/harvests')
def harvests_report():
    total_yield = harvests_instance.get_total_honey_yield()
    return render_template('harvests_report.html', total_yield=total_yield)

@bp.route('/hives/<hive_id>/<event_type>/<event_id>/images/<image_filename>/delete', methods=['POST'])
def delete_image(hive_id, event_type, event_id, image_filename):
    # Map event_type to the correct CONTROLLER instance
    controller_map = {
        'inspection': inspections_instance,
        'treatment': treatments_instance,
        'feeding': feeding_instance,
        'harvest': harvests_instance,
        'varroa_control': varroa_controls_instance,
        'split': splits_instance,
        'queen': queens_instance
    }

    controller = controller_map.get(event_type)
    if not controller:
        current_app.logger.error(f"Unknown event type: {event_type}")
        return "Unknown event type", 400

    # Access the DataManager instance from the controller
    data_manager = controller.data_manager
    if not data_manager: # Should not happen if controllers are properly initialized
        current_app.logger.error(f"DataManager not found for controller {event_type}")
        return "Internal Server Error", 500

    # Load the event/record using the DataManager
    event = data_manager.load(event_id)
    if not event:
        current_app.logger.error(f"Event {event_id} of type {event_type} not found.")
        return f"{event_type.capitalize()} not found", 404

    # Remove image from the event's image list
    if hasattr(event, 'images') and image_filename in event.images:
        event.images.remove(image_filename)
        # Delete the physical file
        dm_for_file_deletion = DataManager(event_type) # Use a generic DataManager for file deletion
        if dm_for_file_deletion.delete_file(image_filename):
            # Update the event in the data store
            data_manager.update(event)
            current_app.logger.info(f"Image {image_filename} deleted from {event_type} {event_id}.")
        else:
            current_app.logger.error(f"Failed to delete physical file {image_filename}.")
            # Even if physical file deletion fails, update the record to remove the reference
            data_manager.update(event)
    else:
        current_app.logger.warning(f"Image {image_filename} not found in {event_type} {event_id} or event has no images attribute.")

    return redirect(url_for('main.hive_detail', hive_id=hive_id))

@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
