# Generated by Django 5.1.6 on 2025-04-20 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_producto_imagen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='stock',
        ),
    ]
