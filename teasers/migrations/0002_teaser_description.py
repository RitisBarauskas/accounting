# Generated by Django 4.1.4 on 2022-12-15 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teasers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teaser',
            name='description',
            field=models.TextField(default=1111, verbose_name='Описание'),
            preserve_default=False,
        ),
    ]