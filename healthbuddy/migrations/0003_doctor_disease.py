# Generated by Django 5.0.2 on 2024-02-10 11:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthbuddy', '0002_alter_rooms_participent_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='disease',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='healthbuddy.disease'),
        ),
    ]