from setuptools import setup
import os
import shutil

APP = ['main.py']

ASSETS = ['icon.png', 'move1.wav', 'move2.wav', 'move3.wav', 'droid-sans.regular.ttf']

DATA_FILES = ASSETS

OPTIONS = {
    'iconfile': 'icon.icns'
}

setup(
    app=APP,
    name='Match Charm',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app', 'pygame'],
    version='1.0',
    description='Connect and reveal a board of expanding sizes',
    author='Mentalio',
    author_email='maxim@stankiewicz.id.au'
)

current_path = os.path.dirname(os.path.abspath(__file__))

destination_dir = os.path.abspath(os.path.join(current_path, "dist/Match Charm.app"))

shutil.rmtree('build')
shutil.move(destination_dir, current_path)
shutil.rmtree('dist')
