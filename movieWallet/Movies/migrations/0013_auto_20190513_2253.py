# Generated by Django 2.1 on 2019-05-14 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0012_auto_20160726_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='Poster',
            field=models.FileField(default='default.jpg', upload_to=''),
        ),
    ]