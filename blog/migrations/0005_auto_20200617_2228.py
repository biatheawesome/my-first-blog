# Generated by Django 2.2.13 on 2020-06-17 19:28

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200617_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to='images/'),
        ),
    ]
