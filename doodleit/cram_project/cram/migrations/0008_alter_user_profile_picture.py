# Generated by Django 5.0.6 on 2024-10-23 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cram', '0007_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.FileField(default='https://doodler-bucket.s3.us-east-2.amazonaws.com/default_NjtZ1Pn.png', upload_to=''),
        ),
    ]
