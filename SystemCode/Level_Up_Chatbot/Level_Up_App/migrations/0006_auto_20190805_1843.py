# Generated by Django 2.2.3 on 2019-08-05 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Level_Up_App', '0005_careerposition_educationlevel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionaire',
            name='careerGoal',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='questionaire',
            name='currPosition',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='questionaire',
            name='eduLevel',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minSalary', models.FloatField(default=0.0)),
                ('maxSalary', models.FloatField(default=0.0)),
                ('title', models.CharField(max_length=256)),
                ('URL', models.URLField()),
                ('description', models.CharField(max_length=5000)),
                ('company', models.CharField(max_length=256)),
                ('eduLvl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Level_Up_App.EducationLevel')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Level_Up_App.CareerPosition')),
                ('skillRequired', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Level_Up_App.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='CareerSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('careerpos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Level_Up_App.CareerPosition')),
                ('skillRequired', models.ManyToManyField(to='Level_Up_App.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='CareerPathMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yearsreq', models.IntegerField(default=0)),
                ('initialpos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='careerpathmap_init_pos', to='Level_Up_App.CareerPosition')),
                ('nextpos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='careerpathmap_next_pos', to='Level_Up_App.CareerPosition')),
            ],
        ),
        migrations.CreateModel(
            name='CareerPathHeuristic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heuristiccost', models.IntegerField(default=0)),
                ('careerpos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Level_Up_App.CareerPosition')),
            ],
        ),
    ]
