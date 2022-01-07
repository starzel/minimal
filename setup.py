from setuptools import setup

setup(
    name='minimal',
    version='0.1',
    description='An simple debugging view for Plone',
    url='https://github.com/starzel/minimal',
    author='Philip Bauer',
    author_email='bauer@starzel.de',
    license='GPL version 2',
    packages=['minimal'],
    include_package_data=True,
    zip_safe=False,
    entry_points={'z3c.autoinclude.plugin': ['target = plone']},
    )
