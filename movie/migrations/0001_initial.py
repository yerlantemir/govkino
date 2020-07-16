# Generated by Django 3.0.5 on 2020-07-04 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('release_date', models.DateTimeField()),
                ('url', models.URLField()),
            ],
        ),
    ]
