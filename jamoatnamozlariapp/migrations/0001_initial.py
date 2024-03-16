# Generated by Django 4.2.8 on 2023-12-19 12:26

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(help_text="Adminning Telegramdagi ID'si", max_length=255, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Admin ismi', max_length=255, verbose_name='Ismi')),
            ],
            options={
                'verbose_name': 'Admin',
                'verbose_name_plural': 'Adminlar',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(help_text='Tumanning lotincha nomi', max_length=255, verbose_name='Lotin')),
                ('name_cyrl', models.CharField(blank=True, help_text='Tumanning kirillcha nomi', max_length=255, null=True, verbose_name='Kirill')),
                ('name_ru', models.CharField(blank=True, help_text='Tumanning ruscha nomi', max_length=255, null=True, verbose_name='Rus')),
            ],
            options={
                'verbose_name': 'Tuman',
                'verbose_name_plural': 'Tumanlar',
            },
        ),
        migrations.CreateModel(
            name='Masjid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(help_text='Masjidning lotincha nomi', max_length=255, verbose_name='Lotin')),
                ('name_cyrl', models.CharField(blank=True, help_text='Masjidning kirillcha nomi', max_length=255, null=True, verbose_name='Kirill')),
                ('name_ru', models.CharField(blank=True, help_text='Masjidning ruscha nomi', max_length=255, null=True, verbose_name='Rus')),
                ('photo', models.CharField(blank=True, help_text='Masjidning rasmi IDsi', max_length=255, null=True, verbose_name='Rasm IDsi')),
                ('photo_file', models.FileField(blank=True, help_text='Masjidning rasm faylini yuklang', max_length=255, null=True, upload_to='', verbose_name='Rasm fayli')),
                ('bomdod', models.CharField(help_text="Masjidda bomdod namozi o'qilish vaqti", max_length=255, verbose_name='Bomdod')),
                ('peshin', models.CharField(help_text="Masjidda peshin namozi o'qilish vaqti", max_length=255, verbose_name='Peshin')),
                ('asr', models.CharField(help_text="Masjidda asr namozi o'qilish vaqti", max_length=255, verbose_name='Asr')),
                ('shom', models.CharField(help_text="Masjidda shom namozi o'qilish vaqti", max_length=255, verbose_name='Shom')),
                ('hufton', models.CharField(help_text="Masjidda xufton namozi o'qilish vaqti", max_length=255, verbose_name='Xufton')),
                ('location', models.CharField(blank=True, help_text='Masjid manzili', max_length=255, null=True, verbose_name='Manzil')),
                ('qisqa_tavsif', models.TextField(blank=True, help_text='Masjid haqida qisqa tavsif', null=True, verbose_name='Qisqa tavsif')),
                ('district', models.ForeignKey(help_text='Masjid joylashgan tuman', on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.district', verbose_name='Tuman')),
            ],
            options={
                'verbose_name': 'Masjid',
                'verbose_name_plural': 'Masjidlar',
            },
        ),
        migrations.CreateModel(
            name='Mintaqa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(help_text='Mintaqaning lotincha nomi', max_length=255, verbose_name='Lotin')),
                ('name_cyrl', models.CharField(blank=True, help_text='Mintaqaning kirillcha nomi', max_length=255, null=True, verbose_name='Kirill')),
                ('name_ru', models.CharField(blank=True, help_text='Mintaqaning ruscha nomi', max_length=255, null=True, verbose_name='Rus')),
                ('mintaqa_id', models.CharField(help_text='Mintaqaning IDsi', max_length=255, verbose_name='Mintaqa IDsi')),
                ('viloyat', models.CharField(choices=[('1', 'Toshkent'), ('2', 'Andijon'), ('99', 'Boshqa')], help_text='Mintaqa joylashgan viloyat', max_length=255, verbose_name='Viloyat')),
            ],
            options={
                'verbose_name': 'Mintaqa',
                'verbose_name_plural': 'Mintaqalar',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(help_text='Viloyat/Shaxarning lotincha nomi', max_length=255, verbose_name='Lotin')),
                ('name_cyrl', models.CharField(blank=True, help_text='Viloyat/Shaxarning kirillcha nomi', max_length=255, null=True, verbose_name='Kirill')),
                ('name_ru', models.CharField(blank=True, help_text='Viloyat/Shaxarning ruscha nomi', max_length=255, null=True, verbose_name='Rus')),
            ],
            options={
                'verbose_name': 'Viloyat/Shaxar',
                'verbose_name_plural': 'Viloyat/Shaxarlar',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(help_text="Foydalanuvchining Telegramdagi ID'si", max_length=255, verbose_name='ID')),
                ('full_name', models.TextField(blank=True, help_text='Foydalanuvchi ismi', null=True, verbose_name='Ismi')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masjid', models.ForeignKey(blank=True, help_text='Masjid', null=True, on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.masjid', verbose_name='Masjid')),
                ('user', models.ForeignKey(help_text='Foydalanuvchi', on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.user', verbose_name='Foydalanuvchi')),
            ],
            options={
                'verbose_name': 'Obuna',
                'verbose_name_plural': 'Obunalar',
            },
        ),
        migrations.CreateModel(
            name='NamozVaqti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('milodiy_oy', models.IntegerField(help_text='Milodiy oy', verbose_name='Milodiy oy')),
                ('xijriy_oy', models.IntegerField(help_text='Xijriy oy', verbose_name='Xijriy oy')),
                ('milodiy_kun', models.IntegerField(help_text='Milodiy kun', verbose_name='Milodiy kun')),
                ('xijriy_kun', models.IntegerField(help_text='Xijriy kun', verbose_name='Xijriy kun')),
                ('vaqtlari', models.CharField(help_text='Tong | Quyosh | Peshin | Asr | Shom | Xufton', max_length=255, verbose_name='Vaqtlari')),
                ('mintaqa', models.ForeignKey(help_text='Mintaqa', on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.mintaqa', verbose_name='Mintaqa')),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='region',
            field=models.ForeignKey(help_text='Tuman joylashgan viloyat/shaxar', on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.region', verbose_name='Viloyat/Shaxar'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.region')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]