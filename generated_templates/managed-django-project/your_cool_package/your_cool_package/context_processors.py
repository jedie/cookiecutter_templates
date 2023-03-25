from your_cool_package import __version__


def your_cool_package_version_string(request):
    return {"version_string": f"v{__version__}"}
