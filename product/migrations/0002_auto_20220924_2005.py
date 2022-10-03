# Generated by Django 3.2.13 on 2022-09-24 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extraproductpicture',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='product',
            name='long_description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='short_description',
        ),
        migrations.AddField(
            model_name='productvariation',
            name='on_promotion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productvariation',
            name='show',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='ExtraVariationProductPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/%Y/%m/%d')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('uploaded_at', models.DateField(auto_now=True)),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productvariation')),
            ],
        ),
    ]
