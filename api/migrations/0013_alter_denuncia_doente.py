# Generated by Django 4.0.4 on 2022-04-15 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_denuncia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denuncia',
            name='doente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='denuncias', to='api.sobreviventes'),
        ),
    ]
