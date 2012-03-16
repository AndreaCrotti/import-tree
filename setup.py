from setuptools import setup

package = 'import tree'
version = '0.1'

setup(
    name=package,
    version=version,
    install_requires=['pygraphviz'],
    description="generate the import tree",
    )
