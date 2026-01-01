# Local Setup Guide - LMS Trainer Module

This guide will help you export the project from Bolt and set it up on your local system with PostgreSQL and MongoDB.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Exporting from Bolt](#exporting-from-bolt)
3. [Database Setup](#database-setup)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Testing the Databases](#testing-the-databases)
7. [Running the Application](#running-the-application)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **PostgreSQL 14+** - [Download](https://www.postgresql.org/download/)
- **MongoDB 6+** - [Download](https://www.mongodb.com/try/download/community)
- **Git** - [Download](https://git-scm.com/downloads)

### Check Installations
```bash
python --version  # Should be 3.10 or higher
node --version    # Should be 18 or higher
psql --version    # PostgreSQL version
mongod --version  # MongoDB version
```

---

## Exporting from Bolt

### Method 1: Download as ZIP
1. In Bolt, click the menu icon (three dots)
2. Select "Export" or "Download"
3. Extract the ZIP file to your desired location

### Method 2: Git Clone (if available)
```bash
git clone <repository-url>
cd <project-folder>
```

---

## Database Setup

### PostgreSQL Setup

#### 1. Start PostgreSQL Service

**Windows:**
```cmd
net start postgresql-x64-14
```

**macOS:**
```bash
brew services start postgresql@14
```

**Linux:**
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### 2. Create Database and User

```bash
# Connect to PostgreSQL
psql -U postgres

# In psql prompt:
CREATE DATABASE lms;
CREATE USER lms_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE lms TO lms_user;
ALTER DATABASE lms OWNER TO lms_user;

# Exit psql
\q
```

#### 3. Verify Connection
```bash
psql -U lms_user -d lms -h localhost
```

### MongoDB Setup

#### 1. Start MongoDB Service

**Windows:**
```cmd
net start MongoDB
```

**macOS:**
```bash
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### 2. Create Database and Collections

```bash
# Connect to MongoDB
mongosh

# Switch to lms database (creates it if doesn't exist)
use lms

# Exit
exit
```

#### 3. Initialize MongoDB Collections (Optional)

The collections will be created automatically when first used, but you can initialize them with the provided script:

```bash
cd project
python mongo_collection.py
```

---

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd project/django-backend
```

### 2. Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `django-backend` directory:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:5174

# Database Configuration
DB_ENGINE=postgresql

# PostgreSQL Settings
DB_NAME=lms
DB_USER=lms_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# MongoDB Settings
MONGODB_ENABLED=True
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=lms
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

This will create all the necessary tables in PostgreSQL.

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Create Initial Test Users

```bash
python ../scripts/seed_sample_users.py
```

This creates:
- Trainer: `trainer1@example.com` / `trainer123`
- Learners: `learner1@example.com` / `learner123`, etc.

---

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd ..  # Back to project root
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment Variables

Create `.env` file in the project root:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### 4. Build the Frontend (Optional)
```bash
npm run build
```

---

## Testing the Databases

### Test PostgreSQL Connection and Operations

```bash
cd project/scripts
python test_postgresql_e2e.py
```

This comprehensive test will:
- ✓ Test database connection
- ✓ Test User CRUD operations
- ✓ Test Course CRUD operations
- ✓ Test Unit/Module CRUD operations
- ✓ Test Enrollment and Progress tracking
- ✓ Test Team operations
- ✓ Test complex queries
- ✓ Clean up test data

**Expected Output:**
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
...

Results: 8/8 tests passed
✓ All tests passed!
```

### Test MongoDB Connection and Operations

```bash
python test_mongodb_e2e.py
```

This comprehensive test will:
- ✓ Test MongoDB connection
- ✓ Test Module Content CRUD operations
- ✓ Test Media File CRUD operations
- ✓ Test Question Media operations
- ✓ Test collection statistics
- ✓ Clean up test data

**Expected Output:**
```
==============================================================
  MongoDB End-to-End Test Suite
==============================================================

==============================================================
  1. MongoDB Connection Test
==============================================================

✓ Connected to MongoDB
ℹ Database: lms
...

Results: 6/6 tests passed
✓ All tests passed!
```

---

## Running the Application

### 1. Start the Backend Server

```bash
cd django-backend
python manage.py runserver 0.0.0.0:8000
```

You should see:
```
Starting development server at http://0.0.0.0:8000/
```

### 2. Start the Frontend Development Server

Open a **new terminal** window:

```bash
cd project  # Navigate to frontend directory
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.x.x:5173/
```

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

### 4. Login with Test Credentials

**Trainer Account:**
- Email: `trainer1@example.com`
- Password: `trainer123`

**Learner Accounts:**
- Email: `learner1@example.com` / Password: `learner123`
- Email: `learner2@example.com` / Password: `learner123`
- Email: `learner3@example.com` / Password: `learner123`

---

## Verifying Database Operations

### Check PostgreSQL Data

```bash
psql -U lms_user -d lms

# View all tables
\dt

# Count users
SELECT COUNT(*) FROM users;

# View courses
SELECT course_id, title, status FROM courses;

# Exit
\q
```

### Check MongoDB Data

```bash
mongosh

use lms

# Show collections
show collections

# Count documents
db.module_content_items.countDocuments()
db.media_files.countDocuments()
db.test_question_media.countDocuments()

# View sample documents
db.module_content_items.findOne()

# Exit
exit
```

---

## Troubleshooting

### PostgreSQL Issues

**Connection Refused:**
```bash
# Check if PostgreSQL is running
# Windows:
sc query postgresql-x64-14

# macOS:
brew services list | grep postgresql

# Linux:
sudo systemctl status postgresql
```

**Authentication Failed:**
- Check your `.env` file credentials
- Verify user exists: `psql -U postgres -c "\du"`
- Reset password if needed:
  ```sql
  ALTER USER lms_user WITH PASSWORD 'new_password';
  ```

**Migration Errors:**
```bash
# Drop and recreate database (CAUTION: Deletes all data)
psql -U postgres
DROP DATABASE lms;
CREATE DATABASE lms;
GRANT ALL PRIVILEGES ON DATABASE lms TO lms_user;
\q

# Run migrations again
python manage.py migrate
```

### MongoDB Issues

**Connection Failed:**
```bash
# Check if MongoDB is running
# Windows:
sc query MongoDB

# macOS:
brew services list | grep mongodb

# Linux:
sudo systemctl status mongod
```

**Port Already in Use:**
- Check if another service is using port 27017
- Change MongoDB port in `/etc/mongod.conf` or `mongod.cfg`
- Update `MONGODB_URI` in `.env` accordingly

### Backend Issues

**ModuleNotFoundError:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install specific package
pip install psycopg2-binary pymongo
```

**Port 8000 Already in Use:**
```bash
# Use a different port
python manage.py runserver 8001

# Update frontend .env
VITE_API_BASE_URL=http://localhost:8001/api
```

### Frontend Issues

**Module Not Found:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Port 5173 Already in Use:**
```bash
# Vite will automatically use the next available port
# Or specify a different port
npm run dev -- --port 3000
```

---

## Data Storage Architecture

### PostgreSQL (Relational Data)
Stores all core application data:
- Users and authentication
- Courses and course metadata
- Units/modules structure
- Enrollments and progress
- Quizzes and questions
- Teams and team members
- Assignments and submissions

### MongoDB (Content and Media)
Stores flexible content data:
- **module_content_items**: Videos, PDFs, presentations linked to modules
- **media_files**: Large media files with encoding status and metadata
- **test_question_media**: Images, videos, audio for quiz questions

### Why Both?
- **PostgreSQL**: Ensures data integrity with foreign keys and transactions
- **MongoDB**: Flexible schema for varying content types and metadata
- **Best of Both Worlds**: Structured data in PostgreSQL, flexible content in MongoDB

---

## Next Steps

1. ✅ Test both databases using the provided test scripts
2. ✅ Create your first course through the UI
3. ✅ Add different unit types (video, text, quiz, etc.)
4. ✅ Assign courses to learners
5. ✅ Track progress and view reports
6. ✅ Verify data is being stored in both databases

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [React + Vite Documentation](https://vitejs.dev/guide/)

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review error logs in the terminal
3. Verify database connections using the test scripts
4. Ensure all environment variables are correctly set

---

**Happy Learning! 🚀**
