import os
import pathlib
import shutil
from zipfile import ZipFile

import yaml



def get_database_connection():
    db_name = os.getenv("TRANSIT_DATABASE_DB")
    host = os.getenv("TRANSIT_DATABASE_HOST")
    passwd = os.getenv("TRANSIT_DATABASE_PASSWORD")
    user = os.getenv("TRANSIT_DATABASE_USER")
    port = os.getenv("TRANSIT_DATABASE_PORT")

    db_uri = F"postgres://{user}:{passwd}@{host}:{port}/{db_name}"
    return db_uri


def load_yaml(directory):
    with open(directory) as stream:
        return yaml.load(stream, Loader=yaml.FullLoader) or {}


def dump_yaml(content):
    return yaml.dump(content, default_flow_style=False, allow_unicode=True)


def load_databases(dashboard_path):
    db_path = os.path.join(dashboard_path, 'databases')
    connections = {}
    for filename in os.listdir(db_path):
        f = os.path.join(db_path, filename)
        data = load_yaml(f)
        data['sqlalchemy_uri'] = get_database_connection()
        connections[filename] = dump_yaml(data)
    return connections


def overwrite_database_definition(dashboard_path):
    db_path = os.path.join(dashboard_path, 'databases')
    for filename in os.listdir(db_path):
        f = os.path.join(db_path, filename)
        data = load_yaml(f)
        data['sqlalchemy_uri'] = get_database_connection()
        with open(f, 'w') as db_file:
            yaml.dump(data, db_file, default_flow_style=False, allow_unicode=True)


def load_datasets(dashboard_path):
    dataset_path = os.path.join(dashboard_path, 'datasets')
    datasets = {}
    for ds in os.listdir(dataset_path):
        dir_ = os.path.join(dataset_path, ds)
        for filename in os.listdir(dir_):
            dataset_file = os.path.join(dir_, filename)
            datasets[dataset_file] = load_yaml(dataset_file)
    return datasets


def load_charts(dashboard_path):
    chart_path = os.path.join(dashboard_path, 'charts')
    charts = {}
    for chart in chart_path:
        full_path = os.path.join(chart_path, chart)
        charts[full_path] = load_yaml(full_path)
    return charts


def load_dashboards_definition(dashboard_path):
    chart_path = os.path.join(dashboard_path, 'dashboards')
    charts = {}
    for chart in chart_path:
        full_path = os.path.join(chart_path, chart)
        charts[full_path] = load_yaml(full_path)
    return charts


def zipdir(dashboard_path):
    dashboard_path = pathlib.Path(dashboard_path)
    f_name = F"import_{os.path.basename(dashboard_path)}"
    save_path = os.path.join(dashboard_path.parent, f_name)
    shutil.make_archive(save_path, 'zip', dashboard_path)
    return save_path


def execute_import_assets(upload):
    from superset.commands.importers.v1.utils import get_contents_from_bundle
    from superset.dashboards.commands.importers.v1 import ImportDashboardsCommand

    with ZipFile(upload) as bundle:
        contents = get_contents_from_bundle(bundle)
        command = ImportDashboardsCommand(contents, passwords={})
        command.run()


def overwrite_database_connection_stirngs(dashboard_outer):
    for filename in os.listdir(dashboard_outer):
        dashboard_inner = os.path.join(dashboard_outer, filename)
        # checking if it is a file
        if os.path.isdir(dashboard_inner) and 'dashboard' in filename:
            overwrite_database_definition(dashboard_inner)


def load_transit_dashboards() -> None:
    """Loads dashboards for TransIT projects"""
    # Relative from cli
    dashboards_path = pathlib.Path(__file__)\
        .parent.parent.parent\
        .joinpath('transit_data')

    for filename in os.listdir(dashboards_path):
        dashboard_outer = os.path.join(dashboards_path, filename)
        if not os.path.isdir(dashboard_outer):
            continue

        overwrite_database_connection_stirngs(dashboard_outer)
        zip_file = zipdir(dashboard_outer)
        # Extension added manually
        zip_file = F"{zip_file}.zip"
        execute_import_assets(zip_file)
