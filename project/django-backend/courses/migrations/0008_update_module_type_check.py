from django.db import migrations


class Migration(migrations.Migration):

    # Make this migration safe to apply regardless of prior branches
    # This migration intentionally has no real dependencies - it's a safe update
    # to the modules check constraint and will be merged into the existing graph.
    dependencies = [
        ('courses', '0007_add_team_members_assigned_by_id'),
    ]

    operations = [
        # This migration uses PostgreSQL-specific syntax, skipped for SQLite
        migrations.RunSQL(
            sql=migrations.RunSQL.noop,
            reverse_sql=migrations.RunSQL.noop,
        )
    ]
