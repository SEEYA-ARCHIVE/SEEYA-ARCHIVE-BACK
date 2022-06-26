# Generated by Django 4.0.3 on 2022-05-26 13:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('concert_halls', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seat_reviews', '0005_alter_comment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='seat_area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seat_area_reviews', to='concert_halls.seatarea'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]
