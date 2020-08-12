# Generated by Django 3.0.8 on 2020-08-12 08:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200810_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='status',
            field=models.IntegerField(choices=[(10, 'Open'), (20, 'Submitted')], default=10),
        ),
        migrations.AlterField(
            model_name='basketline',
            name='basket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basketlines', to='main.Basket'),
        ),
        migrations.AlterField(
            model_name='basketline',
            name='quantity',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
