"""{{ cookiecutter.package_name }} - {{ cookiecutter.package_description }}"""

from importlib.metadata import version


__version__ = version('{{ cookiecutter.package_name }}')
__author__ = '{{ cookiecutter.full_name }} <{{ cookiecutter.author_email }}>'
