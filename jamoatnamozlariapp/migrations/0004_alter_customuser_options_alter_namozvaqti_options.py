# Generated by Django 5.0 on 2023-12-20 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jamoatnamozlariapp', '0003_alter_customuser_admin_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Adminstrator', 'verbose_name_plural': 'Adminstratorlar'},
        ),
        migrations.AlterModelOptions(
            name='namozvaqti',
            options={'verbose_name': 'Namoz vaqti', 'verbose_name_plural': 'Namoz vaqtlari'},
        ),
    ]
