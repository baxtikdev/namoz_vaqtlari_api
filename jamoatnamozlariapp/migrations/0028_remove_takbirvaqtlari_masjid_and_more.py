# Generated by Django 4.2.5 on 2024-03-15 11:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("jamoatnamozlariapp", "0027_takbirvaqtlari"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="takbirvaqtlari",
            name="masjid",
        ),
        migrations.RemoveField(
            model_name="takbirvaqtlari",
            name="region",
        ),
    ]
