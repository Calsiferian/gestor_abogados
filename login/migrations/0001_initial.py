from django.db import migrations
from django.contrib.auth.models import Group, User

def create_roles_and_users(apps, schema_editor):
    # Crear roles (grupos)
  
    user_group, _ = Group.objects.get_or_create(name='Usuario Regular')
    moderator_group, _ = Group.objects.get_or_create(name='Moderador')

    # Eliminar usuario administrador existente, si existe
    try:
        admin_user = User.objects.get(username='admin_user')
        admin_user.delete()
    except User.DoesNotExist:
        pass

    # Crear un nuevo superusuario
    superuser = User.objects.create_superuser(
        username='super_admin',
        password='super_password',
        email='super_admin@example.com'
    )

    # Asignar superusuario al grupo de administrador
    moderator_group.user_set.add(superuser)

    # Crear 10 usuarios regulares y asignarlos al grupo
    for i in range(1, 11):
        regular_user = User.objects.create_user(
            username=f'regular_user_{i}',
            password=f'regular_password_{i}'
        )
        user_group.user_set.add(regular_user)

    # (Opcional) Mantener el usuario moderador
    moderator_user, created = User.objects.get_or_create(
        username='moderator_user',
        defaults={'password': 'moderator_password'}
    )
    if created:
        moderator_user.set_password('moderator_password')  # Asegura el hashing
        moderator_user.save()

    moderator_group.user_set.add(moderator_user)

class Migration(migrations.Migration):

    dependencies = [
          # Dependencia de la migración '0001_initial' de la app 'login'
    ]

    operations = [
        migrations.RunPython(create_roles_and_users),
    ]
