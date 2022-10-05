# Generated by Django 4.0.6 on 2022-09-29 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_monthly_sales_report_sales_report_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupan',
            name='maximum_usage',
            field=models.IntegerField(blank=True),
        ),
        migrations.CreateModel(
            name='Product_offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date_and_time', models.DateField()),
                ('end_date_and_time', models.DateField()),
                ('discount_amount', models.CharField(blank=True, max_length=5)),
                ('discount_percentage', models.CharField(blank=True, max_length=5)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.add_category')),
            ],
        ),
    ]