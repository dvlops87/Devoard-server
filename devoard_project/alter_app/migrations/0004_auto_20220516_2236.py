# Generated by Django 3.0 on 2022-05-16 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alter_app', '0003_alter_alter_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alter',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
