# Generated by Django 4.2 on 2023-05-09 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_item_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='itemrequest',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=300, null=True),
        ),
    ]
