# Generated by Django 3.2.15 on 2023-09-30 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shops', '0002_alter_city_options_alter_division_options_and_more'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecast_date', models.DateField(verbose_name='Дата начала прогноза')),
                ('forecast', models.JSONField(default=dict, verbose_name='Прогноз на 14 дней')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecasts', to='categories.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecasts', to='shops.shop')),
            ],
            options={
                'verbose_name': 'Прогноз продаж',
                'verbose_name_plural': 'Прогнозы продаж',
            },
        ),
        migrations.AddConstraint(
            model_name='forecast',
            constraint=models.UniqueConstraint(fields=('store', 'forecast_date', 'product'), name='unique_forecast'),
        ),
    ]
