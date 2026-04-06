from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
