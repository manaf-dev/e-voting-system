# Generated by Django 5.0.6 on 2024-12-06 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_customuser_entry_date_customuser_phone_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="entry_date",
            field=models.DateField(),
        ),
    ]