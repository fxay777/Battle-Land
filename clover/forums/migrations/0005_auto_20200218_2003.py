# Generated by Django 2.2.2 on 2020-02-19 04:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forums', '0004_auto_20200218_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='threadreply',
            name='edited_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='threadreply',
            name='edited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_edited_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
