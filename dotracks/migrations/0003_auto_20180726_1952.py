# Generated by Django 2.0 on 2018-07-26 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dotracks', '0002_auto_20180716_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='libelle',
            field=models.TextField(blank=True, null=True),
        ),
    ]
