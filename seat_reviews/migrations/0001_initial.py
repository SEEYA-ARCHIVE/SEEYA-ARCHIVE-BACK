# Generated by Django 4.0.3 on 2022-04-10 08:19


import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('concert_halls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=512), size=None)),
                ('artist', models.CharField(blank=True, max_length=128, null=True)),
                ('seat_row', models.CharField(blank=True, max_length=128, null=True)),
                ('seat_num', models.CharField(blank=True, max_length=128, null=True)),
                ('review', models.TextField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('seat_area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seat_reviews', to='concert_halls.seatarea')),
            ],
        ),
    ]
