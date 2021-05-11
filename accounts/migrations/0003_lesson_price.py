# Generated by Django 3.2.2 on 2021-05-06 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210506_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(default=45)),
                ('description_short', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('teacher_pk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_price', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(default=45)),
                ('is_cansalled', models.BooleanField(default=False)),
                ('is_payed', models.BooleanField(default=False)),
                ('start_datetime', models.DateTimeField()),
                ('student_pk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_lesson', to=settings.AUTH_USER_MODEL)),
                ('teacher_pk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_lesson', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]