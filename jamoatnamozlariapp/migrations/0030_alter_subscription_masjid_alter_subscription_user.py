# Generated by Django 4.2.5 on 2024-03-15 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("jamoatnamozlariapp", "0029_takbirvaqtlari_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="masjid",
            field=models.ForeignKey(
                blank=True,
                help_text="Masjid",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="masjidSubscription",
                to="jamoatnamozlariapp.masjid",
                verbose_name="Masjid",
            ),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="user",
            field=models.ForeignKey(
                help_text="Foydalanuvchi",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="userSubscription",
                to="jamoatnamozlariapp.user",
                verbose_name="Foydalanuvchi",
            ),
        ),
    ]
