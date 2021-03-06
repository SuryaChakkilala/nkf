# Generated by Django 3.2.5 on 2022-03-14 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='food',
            name='description',
            field=models.TextField(default='-'),
        ),
        migrations.AlterField(
            model_name='food',
            name='name',
            field=models.TextField(default='_'),
        ),
    ]
