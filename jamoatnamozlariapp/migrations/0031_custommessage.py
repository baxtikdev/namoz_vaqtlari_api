# Generated by Django 4.2.5 on 2024-04-18 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jamoatnamozlariapp', '0030_alter_subscription_masjid_alter_subscription_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_uz', models.TextField(help_text='Lotincha xabar', verbose_name='Lotin')),
                ('message_cyrl', models.TextField(help_text='Kirillcha xabar', verbose_name='Kirill')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='districtCustomMessage', to='jamoatnamozlariapp.district')),
                ('masjid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='masjidCustomMessage', to='jamoatnamozlariapp.masjid')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='regionCustomMessage', to='jamoatnamozlariapp.region')),
            ],
            options={
                'verbose_name': 'Xabar',
                'verbose_name_plural': 'Xabarlar',
            },
        ),
    ]
