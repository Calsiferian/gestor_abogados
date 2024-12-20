# Generated by Django 5.1.3 on 2024-11-28 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0002_cliente_abogado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_pago', models.IntegerField()),
                ('fecha_pago', models.DateField()),
                ('tipo_venta', models.CharField(choices=[('mini', 'Mini'), ('nueva', 'Nueva'), ('cuota', 'Cuota')], max_length=5)),
                ('canal_pago', models.CharField(choices=[('nequi', 'Nequi'), ('efectivo', 'Efectivo'), ('transferencia', 'Transferencia Bancaria')], max_length=15)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paymets', to='clients.cliente')),
            ],
        ),
    ]
