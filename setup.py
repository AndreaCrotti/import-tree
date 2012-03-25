from setuptools import setup

version = '0.1'

optional_requires = [
    'pygraphviz'
]

tests_require = [
    'nose', 'mock'
]

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
    tests_require = tests_require,
    packages=['import_tree'],
    description="generate the import tree",
    entry_points=entry_points,
    )
