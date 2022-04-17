# Generated by Django 4.0.4 on 2022-04-15 17:47

import api.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_sobreviventes_latitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Denuncia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autor', models.IntegerField(validators=[api.validators.maior_que_zero])),
                ('doente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='denuncias', to='api.sobreviventes')),
            ],
        ),
    ]
