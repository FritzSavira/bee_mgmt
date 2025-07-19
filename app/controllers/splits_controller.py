from flask import render_template, request, redirect, url_for, Blueprint
from app.models.split import Split
from app.utils.data_manager import DataManager
from app.controllers.hives_controller import HivesController

class SplitsController:
    def __init__(self):
        self.data_manager = DataManager('splits')
        self.hives_controller = HivesController()

    def get_all_splits(self, hive_id=None):
        splits = self.data_manager.load_all()
        if hive_id:
            return [s for s in splits if s.hive_id == hive_id]
        return splits

    def get_split_by_id(self, split_id):
        return self.data_manager.load(split_id)

    def create_split(self, hive_id, split_data):
        split = Split(
            hive_id=hive_id,
            split_date=split_data['split_date'],
            method=split_data['method'],
            new_hive_id=split_data['new_hive_id']
        )
        self.data_manager.save(split)
        return split

    def update_split(self, split_id, updated_data):
        split = self.data_manager.load(split_id)
        if split:
            split.split_date = updated_data.get('split_date', split.split_date)
            split.method = updated_data.get('method', split.method)
            split.new_hive_id = updated_data.get('new_hive_id', split.new_hive_id)
            self.data_manager.update(split)
            return split
        return None

    def delete_split(self, split_id):
        return self.data_manager.delete(split_id)

splits_bp = Blueprint('splits_controller', __name__)
splits_instance = SplitsController()

@splits_bp.route('/hives/<hive_id>/splits')
def splits_list(hive_id):
    hive_splits = splits_instance.get_all_splits(hive_id=hive_id)
    return render_template('splits_list.html', hive_id=hive_id, splits=hive_splits)

@splits_bp.route('/hives/<hive_id>/splits/new', methods=['GET', 'POST'])
def new_split(hive_id):
    if request.method == 'POST':
        split_data = {
            'split_date': request.form['split_date'],
            'method': request.form['method'],
            'new_hive_id': request.form['new_hive_id']
        }
        splits_instance.create_split(hive_id, split_data)
        return redirect(url_for('main.splits_controller.splits_list', hive_id=hive_id))
    hive = splits_instance.hives_controller.get_hive_by_id(hive_id)
    if request.method == 'POST':
        # ... (existing POST logic)
        pass # Placeholder for existing POST logic
    return render_template('new_split.html', hive=hive)

@splits_bp.route('/hives/<hive_id>/splits/<split_id>/edit', methods=['GET', 'POST'])
def edit_split(hive_id, split_id):
    split = splits_instance.get_split_by_id(split_id)
    hive = splits_instance.hives_controller.get_hive_by_id(hive_id)
    if request.method == 'POST':
        updated_data = {
            'split_date': request.form['split_date'],
            'method': request.form['method'],
            'new_hive_id': request.form['new_hive_id']
        }
        splits_instance.update_split(split_id, updated_data)
        return redirect(url_for('main.splits_controller.splits_list', hive_id=hive_id))
    return render_template('edit_split.html', hive=hive, split=split)

@splits_bp.route('/hives/<hive_id>/splits/<split_id>/delete', methods=['POST'])
def delete_split(hive_id, split_id):
    splits_instance.delete_split(split_id)
    return redirect(url_for('main.splits_controller.splits_list', hive_id=hive_id))