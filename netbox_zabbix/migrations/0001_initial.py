import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dcim', '0221_cable_connector_positions'),
        ('extras', '0133_make_cf_minmax_decimal'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZabbixDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict)),
                ('zabbix_id', models.IntegerField()),
                ('sync', models.BooleanField()),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='zabbixdevice', to='dcim.device')),
                ('tags', models.ManyToManyField(blank=True, related_name='netbox_zabbix_zabbixdevice_related', to='extras.tag')),
            ],
            options={
                'ordering': ['device'],
            },
        ),
        migrations.CreateModel(
            name='ZabbixHost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict)),
                ('name', models.CharField(max_length=255)),
                ('hostname', models.CharField(max_length=255)),
                ('tags', models.ManyToManyField(blank=True, related_name='netbox_zabbix_zabbixhost_related', to='extras.tag')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddConstraint(
            model_name='zabbixhost',
            constraint=models.UniqueConstraint(django.db.models.functions.Lower('name'), name='netbox_zabbix_zabbixhost_unique_name', violation_error_message='Name must be unique.'),
        ),
    ]
