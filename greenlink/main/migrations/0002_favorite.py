# Generated by Django 3.2.7 on 2021-10-02 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.event')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.member')),
            ],
            options={
                'db_table': 'favorite',
                'unique_together': {('member', 'event')},
            },
        ),
    ]