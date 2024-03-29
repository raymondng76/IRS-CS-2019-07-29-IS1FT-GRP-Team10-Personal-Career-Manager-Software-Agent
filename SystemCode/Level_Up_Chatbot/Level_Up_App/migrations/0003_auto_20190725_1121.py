# Generated by Django 2.2.3 on 2019-07-25 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Level_Up_App', '0002_auto_20190724_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionaire',
            name='careerGoal',
            field=models.CharField(choices=[('ASSTSOFTENG', 'Assistant Software Engineer'), ('ASSOSOFTENG', 'Associate Software Engineer'), ('SOFTENG', 'Software Engineer'), ('SENISOFTENG', 'Senior Software Engineer'), ('STAFSOFTENG', 'Staff Software Engineer'), ('PRINSOFTENG', 'Principle Software Engineer'), ('SOFTMAN', 'Software Manager'), ('SENISOFTMAN', 'Senior Software Manager'), ('SOFTDIR', 'Software Director'), ('SENSOFTDIR', 'Senior Software Director'), ('SOFTVP', 'Vice President, Software'), ('SENSOFTVP', 'Senior Vice President, Software'), ('CTO', 'Chief Technology Officer')], default='Software Engineer', max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
