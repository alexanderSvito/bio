# Generated by Django 3.1.2 on 2020-10-13 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20201013_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='jwttoken',
            name='issuer_ip_address',
            field=models.GenericIPAddressField(default='1.1.1.1', unpack_ipv4=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='security',
            name='unsuccessful_login_attempts',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='LoginAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(max_length=32, null=True)),
                ('platform', models.CharField(max_length=32, null=True)),
                ('browser', models.CharField(max_length=32, null=True)),
                ('fingerprint', models.CharField(max_length=128)),
                ('issuer_ip_address', models.GenericIPAddressField(unpack_ipv4=True)),
                ('attempted_at', models.DateTimeField(auto_now_add=True)),
                ('is_successful', models.BooleanField()),
                ('security', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logins', to='users.security')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
