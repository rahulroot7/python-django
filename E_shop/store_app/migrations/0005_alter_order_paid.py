# Generated by Django 4.0.3 on 2022-03-13 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0004_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.CharField(default=False, max_length=200, null=True),
        ),
    ]
