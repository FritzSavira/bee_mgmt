from flask import Blueprint, render_template, request, redirect, url_for
from .utils.data_manager import DataManager
from .controllers.hives_controller import HivesController
from .controllers.queens_controller import QueensController
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

@bp.route('/')
def index():
    hives = hives_controller.get_all_hives()
    overdue_inspections = hives_controller.get_overdue_inspections()
    overdue_treatments = hives_controller.get_overdue_treatments()
    return render_template('index.html', hives=hives, overdue_inspections=overdue_inspections, overdue_treatments=overdue_treatments)

@bp.route('/hives/new', methods=['GET', 'POST'])
def new_hive():
    if request.method == 'POST':
        hive_data = {
            'stocknummer': request.form['stocknummer'],
            'standort': request.form['standort'],
            'beutentyp': request.form['beutentyp'],
            'zargen_anzahl': request.form['zargen_anzahl']
        }
        hives_controller.create_hive(hive_data)
        return redirect(url_for('main.index'))
    return render_template('new_hive.html')

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
            'zargen_anzahl': request.form['zargen_anzahl']
        }
        hives_controller.update_hive(hive_id, updated_data)
        return redirect(url_for('main.index'))
    return render_template('edit_hive.html', hive=hive)

@bp.route('/hives/<hive_id>/delete', methods=['POST'])
def delete_hive(hive_id):
    hives_controller.delete_hive(hive_id)
    return redirect(url_for('main.index'))

@bp.route('/hives/<hive_id>')
def hive_detail(hive_id):
    hive = hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404
    queens = queens_instance.get_all_queens(hive_id=hive_id)
    inspections = inspections_instance.get_all_inspections(hive_id=hive_id)
    treatments = treatments_instance.get_all_treatments(hive_id=hive_id)
    feedings = feeding_instance.get_all_feedings(hive_id=hive_id)
    varroa_controls = varroa_controls_instance.get_all_varroa_controls(hive_id=hive_id)
    splits = splits_instance.get_all_splits(hive_id=hive_id)
    return render_template('hive_detail.html', hive=hive, queens=queens, inspections=inspections, treatments=treatments, feedings=feedings, varroa_controls=varroa_controls, splits=splits)

# Queen Routes
@bp.route('/hives/<hive_id>/queens')
def list_queens(hive_id):
    hive = hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404
    queens = queens_instance.get_all_queens(hive_id=hive_id)
    return render_template('queens_list.html', hive=hive, queens=queens)

@bp.route('/hives/<hive_id>/queens/new', methods=['GET', 'POST'])
def new_queen(hive_id):
    hive = hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404

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
        return redirect(url_for('main.list_queens', hive_id=hive_id))
    return render_template('new_queen.html', hive=hive)

@bp.route('/hives/<hive_id>/queens/<queen_id>/edit', methods=['GET', 'POST'])
def edit_queen(hive_id, queen_id):
    hive = hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404
    queen = queens_instance.get_queen_by_id(queen_id)
    if not queen or queen.hive_id != hive_id:
        return "Queen not found", 404

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
        return redirect(url_for('main.list_queens', hive_id=hive_id))
    return render_template('edit_queen.html', hive=hive, queen=queen)

@bp.route('/hives/<hive_id>/queens/<queen_id>/delete', methods=['POST'])
def delete_queen(hive_id, queen_id):
    queens_instance.delete_queen(queen_id)
    return redirect(url_for('main.list_queens', hive_id=hive_id))



# Treatment Routes
@bp.route('/hives/<hive_id>/treatments')
def list_treatments(hive_id):
    hive = hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404
    treatments = treatments_instance.get_all_treatments(hive_id=hive_id)
    return render_template('treatments_list.html', hive=hive, treatments=treatments)

@bp.route('/hives/<hive_id>/treatments/new', methods=['GET', 'POST'])
def new_treatment(hive_id):
    hive = hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404

    if request.method == 'POST':
        treatment_data = {
            'hive_id': hive_id,
            'treatment_date': request.form['treatment_date'],
            'treatment_type': request.form['treatment_type'],
            'used_agent': request.form['used_agent'],
            'dosage': request.form['dosage'],
            'duration': request.form['duration'],
            'efficacy_observation': request.form['efficacy_observation']
        }
        treatments_instance.create_treatment(hive_id, treatment_data)
        return redirect(url_for('main.list_treatments', hive_id=hive_id))
    return render_template('new_treatment.html', hive=hive)

@bp.route('/hives/<hive_id>/treatments/<treatment_id>/edit', methods=['GET', 'POST'])
def edit_treatment(hive_id, treatment_id):
    hive = hives_controller.get_hive_by_id(hive_id)
    if not hive:
        return "Hive not found", 404
    treatment = treatments_controller.get_treatment_by_id(treatment_id)
    if not treatment or treatment.hive_id != hive_id:
        return "Treatment not found", 404

    if request.method == 'POST':
        updated_data = {
            'treatment_date': request.form['treatment_date'],
            'treatment_type': request.form['treatment_type'],
            'used_agent': request.form['used_agent'],
            'dosage': request.form['dosage'],
            'duration': request.form['duration'],
            'efficacy_observation': request.form['efficacy_observation']
        }
        treatments_instance.update_treatment(treatment_id, updated_data)
        return redirect(url_for('main.list_treatments', hive_id=hive_id))
    return render_template('edit_treatment.html', hive=hive, treatment=treatment)

@bp.route('/hives/<hive_id>/treatments/<treatment_id>/delete', methods=['POST'])
def delete_treatment(hive_id, treatment_id):
    treatments_instance.delete_treatment(treatment_id)
    return redirect(url_for('main.list_treatments', hive_id=hive_id))

@bp.route('/reports/harvests')
def harvests_report():
    total_yield = harvests_instance.get_total_honey_yield()
    return render_template('harvests_report.html', total_yield=total_yield)
