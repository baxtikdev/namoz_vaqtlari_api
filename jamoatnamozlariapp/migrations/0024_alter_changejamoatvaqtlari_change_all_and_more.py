# Generated by Django 5.0.2 on 2024-02-18 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamoatnamozlariapp', '0023_alter_changejamoatvaqtlari_district_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changejamoatvaqtlari',
            name='change_all',
            field=models.BooleanField(default=False, help_text="Barcha masjidlar ma'lumotlarini o'zgartirish", verbose_name='Barcha masjidlar'),
        ),
        migrations.AlterField(
            model_name='changejamoatvaqtlari',
            name='change_district',
            field=models.BooleanField(default=False, help_text="Tanlangan tuman masjidlari ma'lumotlarini o'zgartirish", verbose_name="Tumanni o'zgartirish"),
        ),
        migrations.AlterField(
            model_name='changejamoatvaqtlari',
            name='change_masjid',
            field=models.BooleanField(default=False, help_text="Tanlangan masjid ma'lumotlarini o'zgartirish", verbose_name="Masjidni o'zgartirish"),
        ),
        migrations.AlterField(
            model_name='changejamoatvaqtlari',
            name='change_region',
            field=models.BooleanField(default=False, help_text="Tanlangan viloyat masjidlari ma'lumotlarini o'zgartirish", verbose_name="Viloyatni o'zgartirish"),
        ),
    ]