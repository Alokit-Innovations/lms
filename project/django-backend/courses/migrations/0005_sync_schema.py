from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_remove_course_category_and_more'),
    ]

    operations = [
        # This migration uses PostgreSQL-specific syntax (DO blocks), so it's skipped for SQLite
        # The Django ORM models will handle the schema correctly
        migrations.RunSQL(
            sql=migrations.RunSQL.noop,
            reverse_sql=migrations.RunSQL.noop,
        )
    ]
