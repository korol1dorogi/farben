# Generated by Django 5.1.7 on 2025-03-30 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inn', models.CharField(help_text='10 или 12 цифр', max_length=12, unique=True, verbose_name='ИНН')),
                ('last_name', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя')),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ['last_name', 'first_name'],
            },
        ),
    ]
