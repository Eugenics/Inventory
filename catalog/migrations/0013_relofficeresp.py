# Generated by Django 2.1.5 on 2019-03-20 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_hardware'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelOfficeResp',
            fields=[
                ('roe_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Код')),
            ],
            options={
                'db_table': '"inventory"."Rel_Office_Respons_Employee"',
                'ordering': ['roe_id'],
                'managed': False,
            },
        ),
    ]