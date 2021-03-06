# Generated by Django 2.2 on 2019-05-30 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0009_auto_20190518_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificationitem',
            name='resume',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='curriculum.Resume'),
        ),
        migrations.AddField(
            model_name='experience',
            name='resume',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='curriculum.Resume'),
        ),
        migrations.AddField(
            model_name='languageitem',
            name='resume',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='curriculum.Resume'),
        ),
        migrations.AddField(
            model_name='projectitem',
            name='resume',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='curriculum.Resume'),
        ),
        migrations.AddField(
            model_name='skillitem',
            name='resume',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='curriculum.Resume'),
        ),
        migrations.AddField(
            model_name='training',
            name='resume',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='trainings', to='curriculum.Resume'),
        ),
    ]
