# Generated by Django 3.1.2 on 2020-10-12 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20201012_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jwttoken',
            name='token_secret',
            field=models.CharField(max_length=512),
        ),
    ]
