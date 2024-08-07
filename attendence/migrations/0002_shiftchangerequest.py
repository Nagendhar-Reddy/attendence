# Generated by Django 4.0.1 on 2024-07-25 09:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('attendence', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftChangeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], max_length=3)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('staff1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requesting_staff', to=settings.AUTH_USER_MODEL)),
                ('staff2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiving_staff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
