#!/usr/bin/env python3
"""Seed sample users for testing the LMS application"""
import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trainer_lms.settings')
django.setup()

from courses.models import Profile
from rest_framework.authtoken.models import Token

def create_users():
    """Create sample trainers and learners"""
    users_data = [
        # Trainers
        {
            'username': 'trainer1@example.com',
            'email': 'trainer1@example.com',
            'password': 'trainer123',
            'first_name': 'John',
            'last_name': 'Trainer',
            'primary_role': 'trainer',
        },
        {
            'username': 'trainer2@example.com',
            'email': 'trainer2@example.com',
            'password': 'trainer123',
            'first_name': 'Sarah',
            'last_name': 'Instructor',
            'primary_role': 'trainer',
        },
        # Learners (trainees)
        {
            'username': 'learner1@example.com',
            'email': 'learner1@example.com',
            'password': 'learner123',
            'first_name': 'Alice',
            'last_name': 'Student',
            'primary_role': 'trainee',
        },
        {
            'username': 'learner2@example.com',
            'email': 'learner2@example.com',
            'password': 'learner123',
            'first_name': 'Bob',
            'last_name': 'Learner',
            'primary_role': 'trainee',
        },
        {
            'username': 'learner3@example.com',
            'email': 'learner3@example.com',
            'password': 'learner123',
            'first_name': 'Charlie',
            'last_name': 'Brown',
            'primary_role': 'trainee',
        },
        {
            'username': 'learner4@example.com',
            'email': 'learner4@example.com',
            'password': 'learner123',
            'first_name': 'Diana',
            'last_name': 'Ross',
            'primary_role': 'trainee',
        },
        {
            'username': 'learner5@example.com',
            'email': 'learner5@example.com',
            'password': 'learner123',
            'first_name': 'Ethan',
            'last_name': 'Hunt',
            'primary_role': 'trainee',
        },
    ]

    created_count = 0
    for user_data in users_data:
        username = user_data['username']
        email = user_data['email']

        # Check if user already exists
        if Profile.objects.filter(email=email).exists():
            print(f"User {email} already exists, skipping...")
            existing_user = Profile.objects.get(email=email)
            # Ensure token exists for existing user
            Token.objects.get_or_create(user=existing_user)
            continue

        # Create new user
        try:
            user = Profile.objects.create_user(
                username=username,
                email=email,
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
            )
            user.primary_role = user_data['primary_role']
            user.save()

            # Create auth token for the user
            token, _ = Token.objects.get_or_create(user=user)

            print(f"Created {user_data['primary_role']}: {email} (Token: {token.key})")
            created_count += 1
        except Exception as e:
            print(f"Error creating user {email}: {e}")

    print(f"\n✓ Seeding complete! Created {created_count} new users.")
    print(f"Total users in database: {Profile.objects.count()}")
    print(f"\nTrainers: {Profile.objects.filter(primary_role='trainer').count()}")
    print(f"Learners: {Profile.objects.filter(primary_role='trainee').count()}")

    # Print sample login credentials
    print("\n" + "="*60)
    print("SAMPLE LOGIN CREDENTIALS")
    print("="*60)
    print("\nTrainer Account:")
    print("  Email: trainer1@example.com")
    print("  Password: trainer123")
    print("\nLearner Account:")
    print("  Email: learner1@example.com")
    print("  Password: learner123")
    print("="*60)

if __name__ == '__main__':
    create_users()
