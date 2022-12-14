# Generated by Django 3.0.2 on 2021-07-13 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreTransaction',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False, unique=True)),
                ('tx_status', models.CharField(choices=[('CANCELLED', 'Cancelled'), ('AWAITING_PAYMENT', 'Awaiting Payment'), ('AWAITING_CONFIRMATIONS', 'Awaiting Confirmations'), ('PAYMENT_COMPLETE', 'Payment Complete')], default='AWAITING_PAYMENT', max_length=255)),
                ('currency', models.CharField(choices=[('BTC', 'Btc'), ('ETH', 'Eth'), ('XRP', 'Xrp'), ('XMR', 'Xmr'), ('BNB', 'Bnb'), ('LTC', 'Ltc'), ('DOGE', 'Doge'), ('USDT.ERC20', 'Usdt')], max_length=255)),
                ('crypto_amount', models.DecimalField(decimal_places=8, max_digits=13)),
                ('exchange_rate', models.DecimalField(decimal_places=6, max_digits=6)),
                ('receiving_address', models.TextField(max_length=64)),
                ('confirmations_needed', models.IntegerField(default=10, max_length=3)),
                ('received_at', models.DateTimeField(blank=True, null=True)),
                ('received_amount', models.IntegerField(default=0, max_length=3)),
                ('received_confirmations', models.IntegerField(default=0, max_length=3)),
                ('destination_tag', models.TextField(max_length=64, null=True)),
                ('qr_code_url', models.TextField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('gift_card', models.TextField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='email address')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
