# Database Migrations README

This folder contains PostgreSQL (16+) migration scripts for the E-Learning platform.

Structure
- Files are numbered V001__... to V061__... and should be executed in order.
- Each file is a standalone migration that uses transactions (BEGIN/COMMIT).

Target
- PostgreSQL 16+
- UUID primary keys via gen_random_uuid() (pgcrypto extension required)
- created_at, updated_at, deleted_at support
- Soft delete is implemented via deleted_at fields where applicable
- Partitioning is used for large/time-series tables (activity_logs, notifications, api_logs, sessions, watch_history, etc.)
- Indexes and constraints included for performance and data integrity

How to run
1. Create the database (example):
   sudo -u postgres psql -c "CREATE DATABASE elearning OWNER postgres;"

2. Apply migrations (two options):
   - Using psql sequentially:
     psql -h <host> -U <user> -d elearning -f migrations/V001__extensions_and_utils.sql
     psql -h <host> -U <user> -d elearning -f migrations/V002__users.sql
     ...
   - Using Flyway: place files in sql/ and run flyway migrate (configure flyway.conf)

3. Run seed script to create admin owner and default settings:
   psql -h <host> -U <user> -d elearning -f migrations/seed/seed_initial.sql

Notes & Best Practices
- Backup your database before running migrations in production.
- Run migrations in a maintenance window for large changes.
- Monitor long-running operations and indexing.
- Configure WAL, checkpointing, and autovacuum for large loads.

Contact
- For questions about the schema design or to request additional migrations, open an issue in the repository.
