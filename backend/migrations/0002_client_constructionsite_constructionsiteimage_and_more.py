# Generated by Django 5.0.3 on 2024-07-17 09:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='FIO')),
                ('phone', models.CharField(max_length=255, verbose_name='Telefon')),
                ('comment', models.CharField(default='-', max_length=255, verbose_name='Izoh')),
            ],
            options={
                'verbose_name': 'client(1)',
                'verbose_name_plural': 'clientlar(1)',
            },
        ),
        migrations.CreateModel(
            name='ConstructionSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ConstructionSiteImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='construction_site_images/')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('construction_site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='backend.constructionsite')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='nomi')),
                ('weight', models.IntegerField(default=0, verbose_name='qoldiq(tonna)')),
            ],
            options={
                'verbose_name': 'ingredient(1)',
                'verbose_name_plural': 'ingredientlar(1)',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'kirim(1)',
                'verbose_name_plural': 'kirim(1)',
            },
        ),
        migrations.CreateModel(
            name='InventoryIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=0, verbose_name='soni')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Ingredient', to='backend.ingredient')),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Inventory', to='backend.inventory')),
            ],
            options={
                'verbose_name': 'kirim(maxssulot)(1)',
                'verbose_name_plural': 'kirim(maxssulot)(1)',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('cash', models.IntegerField(default=0, verbose_name='Summa')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Client', to='backend.client')),
            ],
            options={
                'verbose_name': 'chiqim(1)',
                'verbose_name_plural': 'chiqim(1)',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='Narxi')),
                ('count', models.IntegerField(verbose_name='soni')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Order', to='backend.order')),
            ],
            options={
                'verbose_name': 'chiqim(maxsulot)(1)',
                'verbose_name_plural': 'chiqim(maxsulot)(1)',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.IntegerField(verbose_name='Summa')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ClientForPayment', to='backend.client')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('construction_site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.constructionsite')),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='nomi')),
            ],
            options={
                'verbose_name': 'maxsulot(1)',
                'verbose_name_plural': 'maxsulotlar(1)',
            },
        ),
        migrations.CreateModel(
            name='ProductIngedients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=0, verbose_name='soni')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product', to='backend.ingredient')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductIngr', to='backend.product')),
            ],
            options={
                'verbose_name': 'Maxsulot uchun ingredientlar(1)',
            },
        ),
        migrations.CreateModel(
            name='ResponsiblePerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('сonstruction_site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.constructionsite')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('requisite', models.TextField(verbose_name='rekvizitlar')),
            ],
        ),
        migrations.DeleteModel(
            name='News',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductFromOrder', to='backend.product'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='responsible_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.responsibleperson'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.store'),
        ),
    ]
