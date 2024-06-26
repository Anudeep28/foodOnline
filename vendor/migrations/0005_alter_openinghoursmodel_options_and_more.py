# Generated by Django 5.0.2 on 2024-04-13 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_openinghoursmodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinghoursmodel',
            options={'ordering': ('day', '-from_hours')},
        ),
        migrations.AlterUniqueTogether(
            name='openinghoursmodel',
            unique_together={('vendor', 'day', 'from_hours', 'to_hours')},
        ),
    ]
