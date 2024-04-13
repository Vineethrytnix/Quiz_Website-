# Generated by Django 4.2.9 on 2024-01-17 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_question_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100, null=True)),
                ('cid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.creator')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='qcid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.quiz_category'),
        ),
    ]