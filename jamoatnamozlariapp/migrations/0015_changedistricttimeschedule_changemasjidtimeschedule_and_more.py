# Generated by Django 5.0.1 on 2024-01-23 19:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamoatnamozlariapp', '0014_district_is_active_masjid_is_active_region_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeDistrictTimeSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Sana')),
                ('bomdod', models.CharField(blank=True, default='00:00', help_text='Masjidda bomdod namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Bomdod')),
                ('peshin', models.CharField(blank=True, default='00:00', help_text='Masjidda peshin namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Peshin')),
                ('asr', models.CharField(blank=True, default='00:00', help_text='Masjidda asr namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Asr')),
                ('shom', models.CharField(blank=True, default='00:00', help_text='Masjidda shom namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Shom')),
                ('hufton', models.CharField(blank=True, default='00:00', help_text='Masjidda xufton namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Xufton')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.district')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeMasjidTimeSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Sana')),
                ('bomdod', models.CharField(blank=True, default='00:00', help_text='Masjidda bomdod namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Bomdod')),
                ('peshin', models.CharField(blank=True, default='00:00', help_text='Masjidda peshin namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Peshin')),
                ('asr', models.CharField(blank=True, default='00:00', help_text='Masjidda asr namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Asr')),
                ('shom', models.CharField(blank=True, default='00:00', help_text='Masjidda shom namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Shom')),
                ('hufton', models.CharField(blank=True, default='00:00', help_text='Masjidda xufton namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Xufton')),
                ('masjid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.masjid')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeRegionTimeSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Sana')),
                ('bomdod', models.CharField(blank=True, default='00:00', help_text='Masjidda bomdod namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Bomdod')),
                ('peshin', models.CharField(blank=True, default='00:00', help_text='Masjidda peshin namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Peshin')),
                ('asr', models.CharField(blank=True, default='00:00', help_text='Masjidda asr namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Asr')),
                ('shom', models.CharField(blank=True, default='00:00', help_text='Masjidda shom namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Shom')),
                ('hufton', models.CharField(blank=True, default='00:00', help_text='Masjidda xufton namozi oʻqilish vaqti', max_length=255, null=True, verbose_name='Xufton')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.region')),
            ],
        ),
    ]
