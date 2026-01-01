# Export and Local Testing Instructions

## 🎯 Quick Start - 3 Steps to Local Setup

### Step 1: Export from Bolt
In Bolt, click the menu (⋮) and select **"Export"** or **"Download"**. Extract the files to your local machine.

### Step 2: Set Up Databases
```bash
# PostgreSQL
createdb lms
psql lms < project/postgres_table\ 1.sql

# MongoDB
mongosh
use lms
# Collections created automatically on first use
```

### Step 3: Run Test Scripts
```bash
cd project/scripts
python test_postgresql_e2e.py  # Test PostgreSQL
python test_mongodb_e2e.py     # Test MongoDB
```

---

## 📋 Complete Setup Process

### 1. Export Project Files

**From Bolt:**
- Click menu (⋮) → Export/Download
- Save ZIP file
- Extract to your preferred location (e.g., `~/Projects/lms-trainer`)

### 2. Install Required Software

| Software | Version | Download Link |
|----------|---------|---------------|
| Python | 3.10+ | https://www.python.org/downloads/ |
| Node.js | 18+ | https://nodejs.org/ |
| PostgreSQL | 14+ | https://www.postgresql.org/download/ |
| MongoDB | 6+ | https://www.mongodb.com/try/download/community |

**Verify installations:**
```bash
python --version    # 3.10+
node --version      # 18+
psql --version      # 14+
mongod --version    # 6+
```

### 3. Database Setup

#### PostgreSQL Setup
```bash
# 1. Start PostgreSQL
# Windows: net start postgresql-x64-14
# Mac: brew services start postgresql@14
# Linux: sudo systemctl start postgresql

# 2. Create database and user
psql -U postgres
```

```sql
CREATE DATABASE lms;
CREATE USER lms_user WITH PASSWORD 'lms_password';
GRANT ALL PRIVILEGES ON DATABASE lms TO lms_user;
ALTER DATABASE lms OWNER TO lms_user;
\q
```

#### MongoDB Setup
```bash
# 1. Start MongoDB
# Windows: net start MongoDB
# Mac: brew services start mongodb-community
# Linux: sudo systemctl start mongod

# 2. Verify connection
mongosh
use lms
exit
```

### 4. Backend Configuration

```bash
cd project/django-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

**Edit `.env`:**
```env
DB_ENGINE=postgresql
DB_NAME=lms
DB_USER=lms_user
DB_PASSWORD=lms_password
DB_HOST=localhost
DB_PORT=5432

MONGODB_ENABLED=True
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=lms
```

**Run migrations:**
```bash
python manage.py migrate
```

### 5. Run Database Tests

#### Test PostgreSQL
```bash
cd ../scripts
python test_postgresql_e2e.py
```

**Expected Output:**
```
✓ All tests passed!
Results: 8/8 tests passed
```

**What it tests:**
- ✅ Connection to PostgreSQL
- ✅ User create/read/update operations
- ✅ Course management
- ✅ Unit/module handling
- ✅ Enrollments and progress
- ✅ Teams and members
- ✅ Complex queries
- ✅ Data cleanup

#### Test MongoDB
```bash
python test_mongodb_e2e.py
```

**Expected Output:**
```
✓ All tests passed!
Results: 6/6 tests passed
```

**What it tests:**
- ✅ Connection to MongoDB
- ✅ Module content (videos, PDFs, presentations)
- ✅ Media files (video, audio, images)
- ✅ Question media
- ✅ Collection statistics
- ✅ Data cleanup

### 6. Start the Application

#### Terminal 1 - Backend:
```bash
cd django-backend
python manage.py runserver 0.0.0.0:8000
```

#### Terminal 2 - Frontend:
```bash
cd project  # frontend directory
npm install
npm run dev
```

#### Access Application:
Open browser to: `http://localhost:5173`

**Test Login:**
- Email: `trainer1@example.com`
- Password: `trainer123`

---

## 🔍 Verification Checklist

### PostgreSQL Verification

```bash
psql -U lms_user -d lms
```

```sql
-- Check tables exist
\dt

-- Count records
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'courses', COUNT(*) FROM courses
UNION ALL
SELECT 'modules', COUNT(*) FROM modules
UNION ALL
SELECT 'enrollments', COUNT(*) FROM enrollments;

-- Test relationships
SELECT
    c.title as course,
    u.email as creator,
    COUNT(m.module_id) as num_modules
FROM courses c
JOIN users u ON c.created_by = u.user_id
LEFT JOIN modules m ON c.course_id = m.course_id
GROUP BY c.course_id, c.title, u.email;
```

### MongoDB Verification

```bash
mongosh
```

```javascript
use lms

// Check collections
show collections

// Count documents
db.module_content_items.countDocuments()
db.media_files.countDocuments()

// View sample data
db.module_content_items.findOne()

// Query by module
db.module_content_items.find({
    module_id: "your-module-id-here"
}).sort({sequence_order: 1})
```

---

## 🧪 End-to-End Test Workflow

### 1. Create a Course (PostgreSQL)
```bash
# Via UI: Login → Create Course
# Or via script:
cd scripts
python create_course_backend.py
```

**Verify:**
```sql
SELECT course_id, title, status, created_at
FROM courses
ORDER BY created_at DESC
LIMIT 1;
```

### 2. Add Units (PostgreSQL)
```bash
# Via UI: Course → Add Unit → Video Unit
# Or via script:
python create_unit_backend.py
```

**Verify:**
```sql
SELECT m.title, m.module_type, m.sequence_order
FROM modules m
WHERE m.course_id = 'your-course-id'
ORDER BY m.sequence_order;
```

### 3. Add Content (MongoDB)
```python
from courses.mongodb_service import mongo_service

mongo_service.create_module_content({
    'module_id': 'your-module-id',
    'content_type': 'video',
    'title': 'Introduction Video',
    'file_reference': 's3://bucket/intro.mp4',
    'sequence_order': 1,
    'metadata': {
        'format': 'mp4',
        'resolution': '1080p',
        'mime_type': 'video/mp4'
    }
})
```

**Verify:**
```javascript
db.module_content_items.find({
    module_id: "your-module-id"
})
```

### 4. Enroll User (PostgreSQL)
```bash
# Via UI: Course → Assign to Learners
```

**Verify:**
```sql
SELECT
    u.email as learner,
    c.title as course,
    e.status,
    e.progress_percentage
FROM enrollments e
JOIN users u ON e.user_id = u.user_id
JOIN courses c ON e.course_id = c.course_id;
```

### 5. Track Progress (PostgreSQL)
```sql
SELECT
    u.email,
    c.title as course,
    m.title as unit,
    up.status,
    up.watch_percentage
FROM unit_progress up
JOIN enrollments e ON up.enrollment_id = e.id
JOIN users u ON e.user_id = u.user_id
JOIN courses c ON e.course_id = c.course_id
JOIN modules m ON up.unit_id = m.module_id;
```

---

## 🚨 Troubleshooting

### PostgreSQL Not Connecting

**Error:** `psql: error: connection to server failed`

**Solutions:**
```bash
# Check if running
# Mac: brew services list | grep postgresql
# Linux: sudo systemctl status postgresql
# Windows: sc query postgresql-x64-14

# Start service if needed
# Mac: brew services start postgresql@14
# Linux: sudo systemctl start postgresql
# Windows: net start postgresql-x64-14

# Test connection
psql -U postgres -d postgres
```

### MongoDB Not Connecting

**Error:** `MongoServerError: connect ECONNREFUSED`

**Solutions:**
```bash
# Check if running
# Mac: brew services list | grep mongodb
# Linux: sudo systemctl status mongod
# Windows: sc query MongoDB

# Start service if needed
# Mac: brew services start mongodb-community
# Linux: sudo systemctl start mongod
# Windows: net start MongoDB

# Test connection
mongosh
```

### Migration Errors

**Error:** `django.db.utils.ProgrammingError: relation "users" does not exist`

**Solution:**
```bash
cd django-backend

# Drop and recreate (CAUTION: deletes all data)
psql -U postgres
DROP DATABASE lms;
CREATE DATABASE lms;
GRANT ALL PRIVILEGES ON DATABASE lms TO lms_user;
\q

# Run migrations
python manage.py migrate
```

### Test Script Failures

**PostgreSQL test fails:**
1. Check `.env` file has correct database credentials
2. Ensure migrations are applied
3. Verify database user has necessary permissions
4. Check test output for specific error

**MongoDB test fails:**
1. Check `MONGODB_ENABLED=True` in `.env`
2. Verify MongoDB is running: `mongosh`
3. Check `MONGODB_URI` is correct
4. Review test output for connection errors

---

## 📊 Expected Test Results

### PostgreSQL Test - Detailed Output

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

==============================================================
  2. User CRUD Operations
==============================================================
✓ Created trainer: test_trainer_pg@example.com
✓ Created learner: test_learner_pg@example.com
✓ Read user: Test Trainer
✓ Updated user profile image

==============================================================
  3. Course CRUD Operations
==============================================================
✓ Created course: PostgreSQL Test Course
✓ Read course: PostgreSQL Test Course
✓ Course creator: Test Trainer
✓ Updated course status to 'published'

==============================================================
  4. Unit/Module CRUD Operations
==============================================================
✓ Created video unit: Introduction Video
✓ Created text unit: Course Materials
✓ Created quiz with 2 questions
✓ Course has 3 units

==============================================================
  5. Enrollment and Progress Tracking
==============================================================
✓ Enrolled Test Learner in PostgreSQL Test Course
✓ Created progress for: Introduction Video
✓ Created progress for: Course Materials
✓ Updated enrollment progress to 50%

==============================================================
  6. Team Operations
==============================================================
✓ Created team: PostgreSQL Test Team
✓ Added Test Learner to team
✓ Team has 1 member(s)

==============================================================
  7. Complex Queries and Aggregations
==============================================================
✓ Total Users: 2
✓ Total Courses: 1
✓ Total Units: 3
✓ Total Enrollments: 1

==============================================================
  8. Cleanup Test Data
==============================================================
✓ Deleted test enrollments
✓ Deleted test units
✓ Deleted test courses
✓ Deleted test teams
✓ Deleted test users
✓ Cleanup completed successfully

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

### MongoDB Test - Detailed Output

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
✓ Created video content (ID: 507f1f77bcf86cd799439011)
✓ Created PDF content (ID: 507f1f77bcf86cd799439012)
✓ Created presentation content (ID: 507f1f77bcf86cd799439013)
✓ Retrieved 3 content items for module
  ℹ - Introduction to PostgreSQL (video)
  ℹ - PostgreSQL Course Materials (pdf)
  ℓ - Database Design Principles (ppt)
✓ Updated video content
✓ Verified update: duration changed to 1500 seconds

==============================================================
  3. Media File CRUD Operations
==============================================================
✓ Created video media (ID: 507f1f77bcf86cd799439014)
✓ Created audio media (ID: 507f1f77bcf86cd799439015)
✓ Created image media (ID: 507f1f77bcf86cd799439016)
✓ Retrieved media: Advanced SQL Tutorial
✓ Video files: 1
✓ Audio files: 1
✓ Image files: 1
✓ Updated media file
✓ Verified update: status changed to 'processing'

==============================================================
  4. Question Media Operations
==============================================================
✓ Created question image (ID: 507f1f77bcf86cd799439017)
✓ Created question video (ID: 507f1f77bcf86cd799439018)
✓ Retrieved 2 media items for question
  ℹ - image (png)
  ℹ - video (mp4)

==============================================================
  5. Collection Statistics
==============================================================
✓ Module Content Items:
  ℹ Count: 3
  ℹ Size: 1024 bytes
✓ Media Files:
  ℹ Count: 3
  ℹ Size: 2048 bytes
✓ Question Media:
  ℹ Count: 2
  ℹ Size: 512 bytes

==============================================================
  6. Cleanup Test Data
==============================================================
✓ Deleted content: 507f1f77bcf86cd799439011
✓ Deleted content: 507f1f77bcf86cd799439012
✓ Deleted content: 507f1f77bcf86cd799439013
✓ Cleanup completed successfully

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

---

## 📚 Additional Documentation

- **[LOCAL_SETUP_GUIDE.md](./LOCAL_SETUP_GUIDE.md)** - Complete local setup instructions
- **[DATABASE_TESTING_README.md](./DATABASE_TESTING_README.md)** - Detailed testing guide
- **[README.md](./README.md)** - Project overview
- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - API reference

---

## ✅ Success Criteria

Your setup is complete when:

1. ✅ PostgreSQL test script passes (8/8 tests)
2. ✅ MongoDB test script passes (6/6 tests)
3. ✅ Backend starts without errors
4. ✅ Frontend loads in browser
5. ✅ Can login with test credentials
6. ✅ Can create and view courses
7. ✅ Data persists in both databases

---

**Need Help?**
- Check the troubleshooting sections above
- Review error messages carefully
- Verify all environment variables
- Ensure both databases are running
- Test database connections manually

**Happy Testing! 🚀**
