# Generated by Django 3.0.5 on 2022-04-14 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0008_auto_20220414_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='cake',
            name='type',
            field=models.CharField(choices=[('Bánh sinh nhật', 'Bánh sinh nhật'), ('Bánh mặn', 'Bánh mặn'), ('Bánh ngọt', 'Bánh ngọ')], max_length=200, null=True),
        ),
    ]