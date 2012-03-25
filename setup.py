from setuptools import setup

version = '0.1'

entry_points = {
    'console_scripts': [
        'import-tree = import_tree.import_tree:main'
    ]
}

setup(
    name="import_tree",
    author="Andrea Crotti",
    author_email="andrea.crotti.0gmail.com",
    version=version,
    packages=['import_tree'],
    install_requires=['pygraphviz'],
    description="generate the import tree",
    entry_points=entry_points,
    )
