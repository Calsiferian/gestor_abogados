def is_moderator(request):
    """
    Verifica si el usuario está en el grupo 'Moderador' y agrega esa información al contexto.
    """
    if request.user.is_authenticated:
        return {'is_moderator': request.user.groups.filter(name='Moderador').exists()}
    return {'is_moderator': False}
