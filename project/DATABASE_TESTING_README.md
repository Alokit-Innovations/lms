# Database Testing Guide

This document provides instructions for testing PostgreSQL and MongoDB integration in the LMS Trainer Module.

## Overview

The LMS Trainer Module uses a dual-database architecture:
- **PostgreSQL**: For relational data (users, courses, enrollments, etc.)
- **MongoDB**: For flexible content storage (media files, module content, etc.)

## Test Scripts

Two comprehensive test scripts are provided to verify end-to-end database operations:

### 1. PostgreSQL Test Script
**Location:** `scripts/test_postgresql_e2e.py`

**What it tests:**
- ✓ Database connection
- ✓ User CRUD operations (Create, Read, Update, Delete)
- ✓ Course CRUD operations
- ✓ Unit/Module CRUD operations (Video, Text, Quiz)
- ✓ Quiz and Question operations
- ✓ Enrollment and Progress tracking
- ✓ Team and Team Member operations
- ✓ Complex queries and aggregations
- ✓ Foreign key relationships
- ✓ Automatic cleanup of test data

**How to run:**
```bash
cd project/scripts
python test_postgresql_e2e.py
```

**Expected results:**
- All 8 test sections should pass
- Test data is automatically cleaned up
- Colored output for easy reading (green=success, red=error, blue=info)

### 2. MongoDB Test Script
**Location:** `scripts/test_mongodb_e2e.py`

**What it tests:**
- ✓ MongoDB connection
- ✓ Module Content CRUD operations (Video, PDF, Presentation)
- ✓ Media File CRUD operations (Video, Audio, Image)
- ✓ Question Media operations
- ✓ Collection statistics
- ✓ Automatic cleanup of test data

**How to run:**
```bash
cd project/scripts
python test_mongodb_e2e.py
```

**Expected results:**
- All 6 test sections should pass
- Test data is automatically cleaned up
- Colored output for easy reading

## Configuration Requirements

### PostgreSQL
Before running the PostgreSQL test, ensure:

1. PostgreSQL is installed and running
2. Database and user are created
3. `.env` file is configured in `django-backend/` directory:

```env
DB_ENGINE=postgresql
DB_NAME=lms
DB_USER=lms_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

4. Migrations are applied:
```bash
cd django-backend
python manage.py migrate
```

### MongoDB
Before running the MongoDB test, ensure:

1. MongoDB is installed and running
2. `.env` file includes MongoDB configuration:

```env
MONGODB_ENABLED=True
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=lms
```

## Test Output Example

### PostgreSQL Test Output
```
==============================================================
  PostgreSQL End-to-End Test Suite
==============================================================

==============================================================
  1. Database Connection Test
==============================================================

✓ Connected to PostgreSQL
ℹ Database: lms
ℹ Host: localhost
ℹ Version: PostgreSQL 14.x...

==============================================================
  2. User CRUD Operations
==============================================================

ℹ Creating test users...
✓ Created trainer: test_trainer_pg@example.com (ID: 550e8400...)
✓ Created learner: test_learner_pg@example.com (ID: 550e8400...)
ℹ Reading user data...
✓ Read user: Test Trainer
ℹ Updating user data...
✓ Updated user profile image
ℹ Total users in database: 5

[... more test sections ...]

==============================================================
  Test Summary
==============================================================

  Connection: PASS
  Users: PASS
  Courses: PASS
  Units: PASS
  Enrollments: PASS
  Teams: PASS
  Queries: PASS
  Cleanup: PASS

Results: 8/8 tests passed
✓ All tests passed!
```

### MongoDB Test Output
```
==============================================================
  MongoDB End-to-End Test Suite
==============================================================

==============================================================
  1. MongoDB Connection Test
==============================================================

✓ Connected to MongoDB
ℹ Database: lms
ℹ MongoDB Version: 6.0.x

==============================================================
  2. Module Content CRUD Operations
==============================================================

ℹ Creating video content item...
✓ Created video content (ID: 507f1f77bcf86cd799439011)
ℹ Creating PDF content item...
✓ Created PDF content (ID: 507f1f77bcf86cd799439012)
[... more content ...]
ℹ Reading module content...
✓ Retrieved 3 content items for module
  ℹ - Introduction to PostgreSQL (video)
  ℹ - PostgreSQL Course Materials (pdf)
  ℹ - Database Design Principles (ppt)

[... more test sections ...]

==============================================================
  Test Summary
==============================================================

  Connection: PASS
  Module_content: PASS
  Media_files: PASS
  Question_media: PASS
  Stats: PASS
  Cleanup: PASS

Results: 6/6 tests passed
✓ All tests passed!
```

## Troubleshooting Test Failures

### PostgreSQL Test Failures

**Connection Error:**
- Verify PostgreSQL service is running
- Check credentials in `.env` file
- Ensure database `lms` exists
- Test manual connection: `psql -U lms_user -d lms`

**Migration Error:**
- Run migrations: `python manage.py migrate`
- Check for migration conflicts
- Verify user has necessary permissions

**Foreign Key Error:**
- Ensure migrations created all tables
- Check database integrity
- Review error traceback for specific issue

### MongoDB Test Failures

**Connection Error:**
- Verify MongoDB service is running: `mongosh`
- Check `MONGODB_ENABLED=True` in `.env`
- Verify `MONGODB_URI` is correct
- Test manual connection: `mongosh`

**Schema Validation Error:**
- Collections use JSON schema validation
- Ensure data matches expected format
- Check error message for validation details

**Write Error:**
- Verify MongoDB has write permissions
- Check disk space
- Review MongoDB logs

## Manual Testing

### PostgreSQL Manual Test

```bash
# Connect to database
psql -U lms_user -d lms

# Check tables
\dt

# Count users
SELECT COUNT(*) FROM users;

# View courses
SELECT course_id, title, status, created_at FROM courses;

# View enrollments with user info
SELECT
    e.id,
    u.email as learner_email,
    c.title as course_title,
    e.status,
    e.progress_percentage
FROM enrollments e
JOIN users u ON e.user_id = u.user_id
JOIN courses c ON e.course_id = c.course_id;

# Exit
\q
```

### MongoDB Manual Test

```bash
# Connect to MongoDB
mongosh

# Switch to lms database
use lms

# Show collections
show collections

# Count documents
db.module_content_items.countDocuments()
db.media_files.countDocuments()

# Find sample documents
db.module_content_items.find().pretty()

# Find by module_id
db.module_content_items.find(
    {module_id: "your-module-id"}
).sort({sequence_order: 1})

# Find media by type
db.media_files.find({file_type: "video"})

# Exit
exit
```

## Integration Testing

After successful database tests, verify the full stack:

1. **Start Backend:**
   ```bash
   cd django-backend
   python manage.py runserver
   ```

2. **Create Course via API:**
   ```bash
   curl -X POST http://localhost:8000/api/courses/ \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Test Course",
       "description": "Test Description"
     }'
   ```

3. **Verify in PostgreSQL:**
   ```sql
   SELECT * FROM courses WHERE title = 'Test Course';
   ```

4. **Add Content to MongoDB:**
   ```python
   from courses.mongodb_service import mongo_service

   mongo_service.create_module_content({
       'module_id': 'your-module-id',
       'content_type': 'video',
       'title': 'Test Video',
       'file_reference': 's3://bucket/video.mp4',
       'sequence_order': 1,
       'metadata': {
           'format': 'mp4',
           'resolution': '1080p',
           'mime_type': 'video/mp4'
       }
   })
   ```

5. **Verify in MongoDB:**
   ```javascript
   db.module_content_items.find({module_id: "your-module-id"})
   ```

## Continuous Testing

For development, consider:

1. **Run tests before commits:**
   ```bash
   python scripts/test_postgresql_e2e.py && \
   python scripts/test_mongodb_e2e.py
   ```

2. **Add to CI/CD pipeline:**
   - Include both test scripts in your CI configuration
   - Ensure databases are available in CI environment
   - Set up test databases separate from production

3. **Monitor test execution time:**
   - PostgreSQL tests: ~5-10 seconds
   - MongoDB tests: ~3-5 seconds
   - Total: ~10-15 seconds

## Data Verification

After running the application, verify data integrity:

### Check Referential Integrity (PostgreSQL)
```sql
-- Courses should have valid creators
SELECT c.title
FROM courses c
LEFT JOIN users u ON c.created_by = u.user_id
WHERE u.user_id IS NULL;

-- Enrollments should have valid users and courses
SELECT e.id
FROM enrollments e
LEFT JOIN users u ON e.user_id = u.user_id
WHERE u.user_id IS NULL;
```

### Check Content Consistency (MongoDB + PostgreSQL)
```python
# Get all module IDs from PostgreSQL
module_ids = Unit.objects.values_list('id', flat=True)

# Check which have content in MongoDB
for module_id in module_ids:
    content = mongo_service.get_module_content(str(module_id))
    print(f"Module {module_id}: {len(content)} content items")
```

## Performance Testing

### PostgreSQL Query Performance
```sql
-- Enable timing
\timing

-- Test complex query
EXPLAIN ANALYZE
SELECT
    c.title,
    COUNT(DISTINCT e.user_id) as enrolled_users,
    COUNT(DISTINCT m.module_id) as total_modules
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
LEFT JOIN modules m ON c.course_id = m.course_id
GROUP BY c.course_id, c.title;
```

### MongoDB Query Performance
```javascript
// Enable profiling
db.setProfilingLevel(2)

// Run queries
db.module_content_items.find({module_id: "test-id"}).explain("executionStats")

// View slow queries
db.system.profile.find().sort({ts: -1}).limit(5).pretty()
```

## Success Criteria

Both databases are working correctly when:

1. ✅ All test scripts pass without errors
2. ✅ Data is correctly stored and retrieved
3. ✅ Foreign key relationships are maintained
4. ✅ MongoDB flexible schema handles varying content
5. ✅ No data loss during CRUD operations
6. ✅ Performance is acceptable (< 100ms for simple queries)
7. ✅ Cleanup operations work correctly

## Next Steps

After successful testing:
1. Review the [LOCAL_SETUP_GUIDE.md](./LOCAL_SETUP_GUIDE.md) for deployment
2. Set up production databases with proper security
3. Configure database backups
4. Implement monitoring and alerting
5. Consider read replicas for scaling

---

**Questions or Issues?**
Refer to the troubleshooting sections in this guide and the LOCAL_SETUP_GUIDE.md.
