from doit.task import clean_targets
import shutil


def task_test_client():
	return {
		'actions':['python3 -m unittest -v test.py'],
		'file_dep': ['test.py'],
		}

def task_html():
	return {
		'actions': ['sphinx-build -M html moodserver/moodserver _build'],
		'clean': [lambda: shutil.rmtree('docs/build')],
		}
		
def task_whlserver():
	return {
		'actions': ['python3 -m build -n -w moodserver'],
		'file_dep': ['moodserver/pyproject.toml', 'moodserver/moodserver/po/ru/LC_MESSAGES/server.mo'],
		'targets': ['moodserver/dist/*.whl'],
		}

def task_whlclient():
	return {
		'actions': ['python3 -m build -n -w moodclient'],
		'file_dep': ['moodclient/pyproject.toml'],
		'targets': ['moodclient/dist/*.whl'],
		}

def task_wheels():
	return {
		'actions': [],
		'task_dep': ['whlserver', 'whlclient'],
		}