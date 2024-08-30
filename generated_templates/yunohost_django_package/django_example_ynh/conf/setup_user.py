def setup_project_user(user):
    """
    Setup user for the project.
    Called from django_yunohost_integration.sso_auth
    """
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user
