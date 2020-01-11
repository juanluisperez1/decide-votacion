# Generated by Django 2.0 on 2020-01-08 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0012_auto_20200104_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='province',
            field=models.CharField(choices=[('S', 'Sevillistán'), ('H', 'Huelvistán'), ('C', 'Cadistán')], max_length=1, null=True, verbose_name='Province'),
        ),
    ]
