# Generated by Django 5.0.6 on 2024-10-22 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cram', '0005_remove_comment_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.FileField(default='https://doodler-bucket.s3.us-east-2.amazonaws.com/default.png', upload_to=''),
        ),
    ]
