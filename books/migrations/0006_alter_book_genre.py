from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_book_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(
                choices=[
                    ('Academic', 'Academic'),
                    ('Art & Photography', 'Art & Photography'),
                    ('Biography', 'Biography'),
                    ('Business', 'Business'),
                    ('Children', 'Children'),
                    ('Classics', 'Classics'),
                    ('Comics & Graphic Novels', 'Comics & Graphic Novels'),
                    ('Fantasy', 'Fantasy'),
                    ('History', 'History'),
                    ('Horror', 'Horror'),
                    ('Mystery & Thriller', 'Mystery & Thriller'),
                    ('Poetry', 'Poetry'),
                    ('Romance', 'Romance'),
                    ('Science Fiction', 'Science Fiction'),
                    ('Self-Help', 'Self-Help'),
                    ('Travel', 'Travel'),
                    ('Young Adult', 'Young Adult'),
                ],
                max_length=100,
            ),
        ),
    ]
