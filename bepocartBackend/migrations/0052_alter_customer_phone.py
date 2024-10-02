import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0050_alter_customer_email'),  # Use the last valid migration
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(
                blank=True, 
                max_length=15, 
                null=True, 
                unique=True, 
                validators=[django.core.validators.RegexValidator(
                    message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.', 
                    regex=r'^\+?1?\d{9,15}$'
                )]
            ),
        ),
    ]
#import django.core.validators
#from django.db import migrations, models

#class Migration(migrations.Migration):

 #   dependencies = [
  #      ('bepocartBackend', '0050_alter_customer_email'),  # Adjusted to the last existing migration
   # ]

#    operations = [
#        migrations.AlterField(
#            model_name='customer',
#            name='phone',
#            field=models.CharField(
#                blank=True, 
#                max_length=15, 
#                null=True, 
#                unique=True, 
#                validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.', regex='^\+?1?\d{9,15}$')]
#            ),
#        ),
#    ]

# import django.core.validators
# from django.db import migrations, models


#class Migration(migrations.Migration):

#    dependencies  = [
#        ('bepocartBackend', '0051_merge_20240907_0749')
  #  ]

 #   operations = [
   #     migrations.AlterField(
    #        model_name='customer',
     #       name='phone',
      #      field=models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must contain only digits.', regex='^\\d+$')]),
      #  ),
   # ]
#
