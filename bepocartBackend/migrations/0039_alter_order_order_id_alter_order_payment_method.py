
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0038_alter_order_razorpay_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(editable=False, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
