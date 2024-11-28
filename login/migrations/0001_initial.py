from django.db import migrations
from django.contrib.auth.models import Group, User

def create_roles_and_users(apps, schema_editor):
    # Crear roles (grupos)
    admin_group, created = Group.objects.get_or_create(name='Administrador')
    user_group, created = Group.objects.get_or_create(name='Usuario Regular')
    moderator_group, created = Group.objects.get_or_create(name='Moderador')

    # Crear tres usuarios de prueba con diferentes roles
    admin_user = User.objects.create_user(username='admin_user', password='admin_password')
    regular_user = User.objects.create_user(username='regular_user', password='regular_password')
    moderator_user = User.objects.create_user(username='moderator_user', password='moderator_password')

    # Asignar roles a los usuarios
    admin_group.user_set.add(admin_user)
    user_group.user_set.add(regular_user)
    moderator_group.user_set.add(moderator_user)

class Migration(migrations.Migration):

    dependencies = [
        # Si es la primera migración, no debe depender de ninguna otra
    ]

    operations = [
        migrations.RunPython(create_roles_and_users),
    ]
