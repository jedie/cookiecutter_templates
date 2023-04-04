from {{ cookiecutter.package_name }} import __version__


def {{ cookiecutter.package_name }}_version_string(request):
    return {"version_string": f"v{__version__}"}
