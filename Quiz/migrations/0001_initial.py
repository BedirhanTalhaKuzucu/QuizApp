# Generated by Django 4.0.5 on 2022-07-01 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('categoryName', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='quiz', to='Quiz.category')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=250)),
                ('difficulty', models.CharField(choices=[('H', 'Hard'), ('M', 'Middle'), ('E', 'Easy')], default='M', max_length=1)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('quizTitle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='questions', to='Quiz.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('answer', models.CharField(max_length=200)),
                ('is_right', models.BooleanField(default=False)),
                ('questionTitle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='Quiz.question')),
            ],
        ),
    ]
