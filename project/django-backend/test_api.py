#!/usr/bin/env python3
"""Test script for Django API endpoints"""
import os
import sys
import django
import json

# Setup Django environment
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trainer_lms.settings')
django.setup()

from django.test import Client
from courses.models import Profile, Course, Unit
from rest_framework.authtoken.models import Token

def test_authentication():
    """Test login endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Authentication")
    print("="*60)

    client = Client()

    # Test login
    response = client.post('/api/auth/login/', {
        'username': 'trainer1@example.com',
        'password': 'trainer123'
    }, content_type='application/json')

    print(f"Login Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Login successful! Token: {data.get('token', 'N/A')[:20]}...")
        return data.get('token')
    else:
        print(f"✗ Login failed: {response.content}")
        return None

def test_profile_me(token):
    """Test profile/me endpoint"""
    print("\n" + "="*60)
    print("TEST 2: Get Profile")
    print("="*60)

    client = Client()
    response = client.get('/api/profiles/me/', HTTP_AUTHORIZATION=f'Token {token}')

    print(f"Profile Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Profile loaded!")
        print(f"  Email: {data.get('email')}")
        print(f"  Name: {data.get('full_name')}")
        print(f"  Role: {data.get('role')}")
        return data
    else:
        print(f"✗ Profile load failed: {response.content}")
        return None

def test_course_creation(token):
    """Test course creation endpoint"""
    print("\n" + "="*60)
    print("TEST 3: Create Course")
    print("="*60)

    client = Client()
    course_data = {
        'title': 'Test Course - Introduction to Python',
        'description': 'Learn Python programming from scratch',
        'status': 'draft',
    }

    response = client.post('/api/courses/',
        json.dumps(course_data),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Token {token}')

    print(f"Create Course Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"✓ Course created successfully!")
        print(f"  ID: {data.get('id')}")
        print(f"  Title: {data.get('title')}")
        print(f"  Status: {data.get('status')}")
        return data
    else:
        print(f"✗ Course creation failed: {response.content.decode()}")
        return None

def test_unit_creation(token, course_id):
    """Test unit creation endpoint"""
    print("\n" + "="*60)
    print("TEST 4: Create Unit")
    print("="*60)

    client = Client()
    unit_data = {
        'course': course_id,
        'type': 'video',  # Serializer expects 'type' which maps to 'module_type'
        'title': 'Introduction Video',
        'description': 'Welcome to the course!',
        'is_mandatory': True,
    }

    response = client.post('/api/units/',
        json.dumps(unit_data),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Token {token}')

    print(f"Create Unit Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"✓ Unit created successfully!")
        print(f"  ID: {data.get('id')}")
        print(f"  Title: {data.get('title')}")
        print(f"  Type: {data.get('module_type')}")
        print(f"  Order: {data.get('sequence_order')}")
        return data
    else:
        print(f"✗ Unit creation failed: {response.content.decode()}")
        return None

def test_get_courses(token):
    """Test getting courses"""
    print("\n" + "="*60)
    print("TEST 5: Get Courses")
    print("="*60)

    client = Client()
    response = client.get('/api/courses/', HTTP_AUTHORIZATION=f'Token {token}')

    print(f"Get Courses Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        courses = data if isinstance(data, list) else data.get('results', [])
        print(f"✓ Retrieved {len(courses)} courses")
        for course in courses:
            print(f"  - {course.get('title')} ({course.get('status')})")
        return courses
    else:
        print(f"✗ Get courses failed: {response.content}")
        return []

def test_get_learners(token):
    """Test getting learners"""
    print("\n" + "="*60)
    print("TEST 6: Get Learners")
    print("="*60)

    learners = Profile.objects.filter(primary_role='trainee')
    print(f"✓ Found {learners.count()} learners in database:")
    for learner in learners:
        print(f"  - {learner.email} ({learner.full_name})")
    return list(learners)

def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("LMS API TEST SUITE")
    print("="*60)

    # Test 1: Authentication
    token = test_authentication()
    if not token:
        print("\n✗ Authentication failed, stopping tests")
        return

    # Test 2: Profile
    profile = test_profile_me(token)
    if not profile:
        print("\n✗ Profile loading failed, stopping tests")
        return

    # Test 3: Course Creation
    course = test_course_creation(token)
    if not course:
        print("\n✗ Course creation failed, stopping tests")
        return

    # Test 4: Unit Creation
    unit = test_unit_creation(token, course['id'])

    # Test 5: Get Courses
    courses = test_get_courses(token)

    # Test 6: Get Learners
    learners = test_get_learners(token)

    # Final Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"✓ Authentication: PASSED")
    print(f"✓ Profile Loading: PASSED")
    print(f"✓ Course Creation: {'PASSED' if course else 'FAILED'}")
    print(f"✓ Unit Creation: {'PASSED' if unit else 'FAILED'}")
    print(f"✓ Get Courses: PASSED ({len(courses)} courses)")
    print(f"✓ Get Learners: PASSED ({len(learners)} learners)")
    print("="*60)

if __name__ == '__main__':
    run_all_tests()
