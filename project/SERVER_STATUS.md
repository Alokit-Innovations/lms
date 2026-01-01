# LMS Application - Server Status

## ✓ BOTH SERVERS ARE RUNNING!

### Backend Server (Django)
- **Status:** ✓ Running
- **URL:** http://localhost:8000
- **API Base:** http://localhost:8000/api/
- **Database:** SQLite (db.sqlite3)
- **Process ID:** Check with `ps aux | grep manage.py`

### Frontend Server (Vite)
- **Status:** ✓ Running
- **URL:** http://localhost:5173
- **Dev Mode:** Hot reload enabled
- **API Proxy:** Configured to forward /api/* to Django backend
- **Process ID:** Check with `ps aux | grep vite`

---

## 🔑 Login Credentials

### Trainer Account
```
Email: trainer1@example.com
Password: trainer123
Token: 2a0ab6081523143e0a58e9ca56ad04f6027c9484
```

### Learner Accounts
```
Email: learner1@example.com
Password: learner123

Email: learner2@example.com
Password: learner123

Email: learner3@example.com
Password: learner123

Email: learner4@example.com
Password: learner123

Email: learner5@example.com
Password: learner123
```

---

## 🧪 Testing the Application

### 1. Open in Browser
Navigate to: **http://localhost:5173**

### 2. Login as Trainer
- Use email: `trainer1@example.com`
- Use password: `trainer123`

### 3. Test Course Creation
1. Click "Create Course" from dashboard
2. Fill in course details
3. Add units (video, text, quiz, etc.)
4. Assign to learners

### 4. Test API Directly
```bash
# Get auth token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"trainer1@example.com","password":"trainer123"}'

# Create a course (use token from above)
curl -X POST http://localhost:8000/api/courses/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Test Course","description":"Course description","status":"draft"}'
```

---

## 📊 Database Information

### Current Configuration
- **Type:** SQLite
- **Location:** `django-backend/db.sqlite3`
- **Users:** 7 (2 trainers, 5 learners)
- **Migrations:** All applied successfully

### PostgreSQL Configuration (Available)
The PostgreSQL configuration via Pinggy tunnel is commented out in `settings.py`.

**To switch to PostgreSQL:**
1. Verify Pinggy tunnel is running on your local machine
2. Test connection from this environment
3. Uncomment PostgreSQL config in `settings.py`
4. Run migrations: `python3 manage.py migrate`
5. Seed users: `python3 seed_users.py`

**Current Pinggy URL:** `dktsk-2401-4900-1c2c-1c4b-edd3-b246-f49f-47fd.a.free.pinggy.link`

---

## 🛠️ Server Management

### Check Server Status
```bash
# Check if servers are running
ps aux | grep -E "(manage.py|vite)" | grep -v grep

# Check Django logs
tail -f /tmp/django-server.log

# Check Vite logs
tail -f /tmp/vite-server.log
```

### Stop Servers
```bash
# Stop Django
pkill -f "manage.py runserver"

# Stop Vite
pkill -f "vite"
```

### Restart Servers
```bash
# Restart Django
cd django-backend
python3 manage.py runserver 0.0.0.0:8000 > /tmp/django-server.log 2>&1 &

# Restart Vite
cd /path/to/project
npx vite --host 0.0.0.0 > /tmp/vite-server.log 2>&1 &
```

---

## 🔍 Troubleshooting

### Frontend not loading?
1. Check Vite is running: `ps aux | grep vite`
2. Check logs: `tail -f /tmp/vite-server.log`
3. Restart: `pkill -f vite && npx vite --host 0.0.0.0 > /tmp/vite-server.log 2>&1 &`

### API calls failing?
1. Check Django is running: `ps aux | grep manage.py`
2. Check logs: `tail -f /tmp/django-server.log`
3. Test API: `curl http://localhost:8000/api/profiles/me/`

### Cannot login?
1. Verify credentials are correct
2. Check if users exist: `cd django-backend && python3 manage.py shell -c "from courses.models import Profile; print(Profile.objects.count())"`
3. Re-seed users: `python3 seed_users.py`

### Database issues?
```bash
# Reset database
cd django-backend
rm -f db.sqlite3
python3 manage.py migrate
python3 seed_users.py
```

---

## 📝 API Endpoints Available

### Authentication
- POST `/api/auth/login/` - Login
- POST `/api/auth/register/` - Register

### Courses
- GET `/api/courses/` - List courses
- POST `/api/courses/` - Create course
- GET `/api/courses/{id}/` - Get course details
- PUT `/api/courses/{id}/` - Update course
- DELETE `/api/courses/{id}/` - Delete course

### Units
- GET `/api/units/?course_id={id}` - List units
- POST `/api/units/` - Create unit
- GET `/api/units/{id}/` - Get unit details
- PUT `/api/units/{id}/` - Update unit
- DELETE `/api/units/{id}/` - Delete unit

### Enrollments
- GET `/api/enrollments/` - List enrollments
- POST `/api/enrollments/` - Create enrollment

### More endpoints in API_DOCUMENTATION.md

---

## ✅ What's Working

- ✓ User authentication (login/register)
- ✓ Course creation and management
- ✓ Unit creation (all 11 types)
- ✓ Course assignment to learners
- ✓ Database persistence
- ✓ Frontend-backend communication
- ✓ API proxy configuration

---

## 📌 Next Steps

1. **Test the application** - Open http://localhost:5173 and login
2. **Create courses** - Add various unit types
3. **Assign courses** - Test enrollment functionality
4. **Configure PostgreSQL** (optional) - Once Pinggy tunnel is verified

---

**Application Status:** ✅ READY TO USE

Both servers are running and ready for testing. The application is fully functional with SQLite.

To switch to your PostgreSQL database:
1. Ensure Pinggy tunnel is accessible from this environment
2. Test connection: `cd django-backend && python3 quick_test.py`
3. If successful, uncomment PostgreSQL config in `settings.py`
4. Restart Django server
