# Generated by Django 4.2.3 on 2023-07-19 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_recipe_ingredients'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
    ]
