# Generated by Django 5.2.3 on 2025-07-04 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("items", "0003_alter_coin_name_alter_coin_tirage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coin",
            name="country",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="coin",
            name="denomination",
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name="coin",
            name="material",
            field=models.CharField(
                blank=True, default="Unknown", max_length=30, null=True
            ),
        ),
        migrations.AlterField(
            model_name="coin",
            name="tirage",
            field=models.CharField(
                blank=True, default="Unknown", max_length=20, null=True
            ),
        ),
    ]
