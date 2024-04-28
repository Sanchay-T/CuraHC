def base_template(request):
    if request.user.is_superuser:
        return {'base_template_name': 'base_admin.html'}
    return {'base_template_name': 'base.html'}
