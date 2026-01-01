#!/usr/bin/env python3
"""
End-to-End PostgreSQL Database Test Script

Tests all major database operations:
- User CRUD operations
- Course CRUD operations
- Unit/Module CRUD operations
- Enrollment operations
- Quiz and Question operations
- Progress tracking
- Relationships and foreign keys
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'django-backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trainer_lms.settings')
django.setup()

from django.db import connection
from courses.models import (
    Profile, Course, Unit, VideoUnit, TextUnit, Quiz, Question,
    Enrollment, UnitProgress, Team, TeamMember
)

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")


def print_error(message):
    print(f"{RED}✗ {message}{RESET}")


def print_info(message):
    print(f"{BLUE}ℹ {message}{RESET}")


def print_section(title):
    print(f"\n{YELLOW}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{RESET}\n")


class PostgreSQLTester:
    def __init__(self):
        self.test_users = []
        self.test_courses = []
        self.test_units = []
        self.test_enrollments = []
        self.test_teams = []

    def check_connection(self):
        """Test database connection"""
        print_section("1. Database Connection Test")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                db_version = cursor.fetchone()[0]
                print_success(f"Connected to PostgreSQL")
                print_info(f"Database: {connection.settings_dict['NAME']}")
                print_info(f"Host: {connection.settings_dict['HOST']}")
                print_info(f"Version: {db_version[:50]}...")
                return True
        except Exception as e:
            print_error(f"Connection failed: {e}")
            return False

    def test_user_operations(self):
        """Test User CRUD operations"""
        print_section("2. User CRUD Operations")

        try:
            # CREATE
            print_info("Creating test users...")
            trainer = Profile.objects.create_user(
                username='test_trainer_pg',
                email='test_trainer_pg@example.com',
                password='testpass123',
                first_name='Test',
                last_name='Trainer',
                primary_role='trainer'
            )
            self.test_users.append(trainer)
            print_success(f"Created trainer: {trainer.email} (ID: {trainer.id})")

            learner = Profile.objects.create_user(
                username='test_learner_pg',
                email='test_learner_pg@example.com',
                password='testpass123',
                first_name='Test',
                last_name='Learner',
                primary_role='trainee'
            )
            self.test_users.append(learner)
            print_success(f"Created learner: {learner.email} (ID: {learner.id})")

            # READ
            print_info("Reading user data...")
            fetched_user = Profile.objects.get(email='test_trainer_pg@example.com')
            assert fetched_user.first_name == 'Test'
            print_success(f"Read user: {fetched_user.full_name}")

            # UPDATE
            print_info("Updating user data...")
            trainer.profile_image_url = 'https://example.com/avatar.jpg'
            trainer.save()
            updated_user = Profile.objects.get(id=trainer.id)
            assert updated_user.profile_image_url == 'https://example.com/avatar.jpg'
            print_success("Updated user profile image")

            # COUNT
            user_count = Profile.objects.count()
            print_info(f"Total users in database: {user_count}")

            return True
        except Exception as e:
            print_error(f"User operations failed: {e}")
            return False

    def test_course_operations(self):
        """Test Course CRUD operations"""
        print_section("3. Course CRUD Operations")

        try:
            trainer = self.test_users[0]

            # CREATE
            print_info("Creating test course...")
            course = Course.objects.create(
                title='PostgreSQL Test Course',
                description='A comprehensive test course',
                about='This course tests PostgreSQL integration',
                outcomes='Students will learn database operations',
                course_type='self_paced',
                status='draft',
                is_mandatory=False,
                estimated_duration_hours=10,
                passing_criteria=70,
                created_by=trainer
            )
            self.test_courses.append(course)
            print_success(f"Created course: {course.title} (ID: {course.id})")

            # READ
            print_info("Reading course data...")
            fetched_course = Course.objects.get(id=course.id)
            assert fetched_course.title == 'PostgreSQL Test Course'
            print_success(f"Read course: {fetched_course.title}")

            # READ WITH RELATIONSHIP
            print_info("Testing foreign key relationship...")
            assert fetched_course.created_by.id == trainer.id
            print_success(f"Course creator: {fetched_course.created_by.full_name}")

            # UPDATE
            print_info("Updating course status...")
            course.status = 'published'
            course.save()
            updated_course = Course.objects.get(id=course.id)
            assert updated_course.status == 'published'
            print_success("Updated course status to 'published'")

            # COUNT
            course_count = Course.objects.count()
            print_info(f"Total courses in database: {course_count}")

            return True
        except Exception as e:
            print_error(f"Course operations failed: {e}")
            return False

    def test_unit_operations(self):
        """Test Unit/Module CRUD operations"""
        print_section("4. Unit/Module CRUD Operations")

        try:
            course = self.test_courses[0]

            # CREATE VIDEO UNIT
            print_info("Creating video unit...")
            video_unit = Unit.objects.create(
                course=course,
                module_type='video',
                title='Introduction Video',
                description='Welcome to the course',
                sequence_order=1,
                is_mandatory=True,
                estimated_duration_minutes=15
            )
            self.test_units.append(video_unit)

            video_details = VideoUnit.objects.create(
                unit=video_unit,
                video_url='https://example.com/intro.mp4',
                duration=900,
                completion_type='full',
                required_watch_percentage=100,
                allow_skip=False,
                allow_rewind=True
            )
            print_success(f"Created video unit: {video_unit.title}")

            # CREATE TEXT UNIT
            print_info("Creating text unit...")
            text_unit = Unit.objects.create(
                course=course,
                module_type='text',
                title='Course Materials',
                description='Reading materials',
                sequence_order=2,
                is_mandatory=True
            )
            self.test_units.append(text_unit)

            text_details = TextUnit.objects.create(
                unit=text_unit,
                content='This is the course content...'
            )
            print_success(f"Created text unit: {text_unit.title}")

            # CREATE QUIZ
            print_info("Creating quiz unit...")
            quiz_unit = Unit.objects.create(
                course=course,
                module_type='quiz',
                title='Final Assessment',
                description='Test your knowledge',
                sequence_order=3,
                is_mandatory=True,
                has_quizzes=True
            )
            self.test_units.append(quiz_unit)

            quiz = Quiz.objects.create(
                unit=quiz_unit,
                time_limit=30,
                passing_score=70,
                attempts_allowed=3,
                show_answers=True,
                randomize_questions=False
            )

            # CREATE QUESTIONS
            print_info("Creating quiz questions...")
            question1 = Question.objects.create(
                quiz=quiz,
                type='multiple_choice',
                text='What is PostgreSQL?',
                options=['A database', 'A programming language', 'An OS', 'A framework'],
                correct_answer='A database',
                points=10,
                order=1
            )

            question2 = Question.objects.create(
                quiz=quiz,
                type='true_false',
                text='PostgreSQL is open source',
                options=['True', 'False'],
                correct_answer='True',
                points=5,
                order=2
            )
            print_success(f"Created quiz with {quiz.questions.count()} questions")

            # READ WITH RELATIONSHIPS
            print_info("Reading units with relationships...")
            course_units = Unit.objects.filter(course=course).order_by('sequence_order')
            print_success(f"Course has {course_units.count()} units")

            for unit in course_units:
                print_info(f"  - Unit {unit.sequence_order}: {unit.title} ({unit.module_type})")

            return True
        except Exception as e:
            print_error(f"Unit operations failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def test_enrollment_operations(self):
        """Test Enrollment and Progress tracking"""
        print_section("5. Enrollment and Progress Tracking")

        try:
            course = self.test_courses[0]
            trainer = self.test_users[0]
            learner = self.test_users[1]

            # CREATE ENROLLMENT
            print_info("Creating enrollment...")
            enrollment = Enrollment.objects.create(
                course=course,
                user=learner,
                assigned_by=trainer,
                status='assigned',
                progress_percentage=0
            )
            self.test_enrollments.append(enrollment)
            print_success(f"Enrolled {learner.full_name} in {course.title}")

            # CREATE UNIT PROGRESS
            print_info("Creating unit progress records...")
            for unit in self.test_units[:2]:
                progress = UnitProgress.objects.create(
                    enrollment=enrollment,
                    unit=unit,
                    status='completed',
                    watch_percentage=100,
                    completed_at=datetime.now()
                )
                print_success(f"Created progress for: {unit.title}")

            # UPDATE ENROLLMENT PROGRESS
            print_info("Updating enrollment progress...")
            enrollment.status = 'in_progress'
            enrollment.progress_percentage = 50
            enrollment.started_at = datetime.now()
            enrollment.save()
            print_success("Updated enrollment progress to 50%")

            # READ PROGRESS
            print_info("Reading enrollment progress...")
            learner_enrollments = Enrollment.objects.filter(user=learner)
            print_success(f"Learner has {learner_enrollments.count()} enrollment(s)")

            for enroll in learner_enrollments:
                unit_progress = UnitProgress.objects.filter(enrollment=enroll)
                print_info(f"  Course: {enroll.course.title}")
                print_info(f"  Progress: {enroll.progress_percentage}%")
                print_info(f"  Completed units: {unit_progress.filter(status='completed').count()}")

            return True
        except Exception as e:
            print_error(f"Enrollment operations failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def test_team_operations(self):
        """Test Team and TeamMember operations"""
        print_section("6. Team Operations")

        try:
            trainer = self.test_users[0]
            learner = self.test_users[1]

            # CREATE TEAM
            print_info("Creating team...")
            team = Team.objects.create(
                team_name='PostgreSQL Test Team',
                description='Test team for database operations',
                status='active',
                manager=trainer,
                created_by=trainer
            )
            self.test_teams.append(team)
            print_success(f"Created team: {team.team_name}")

            # ADD TEAM MEMBERS
            print_info("Adding team members...")
            member1 = TeamMember.objects.create(
                team=team,
                user=learner,
                is_primary_team=True,
                assigned_by=trainer
            )
            print_success(f"Added {learner.full_name} to team")

            # READ TEAM DATA
            print_info("Reading team data...")
            team_members = TeamMember.objects.filter(team=team)
            print_success(f"Team has {team_members.count()} member(s)")

            return True
        except Exception as e:
            print_error(f"Team operations failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def test_complex_queries(self):
        """Test complex queries and aggregations"""
        print_section("7. Complex Queries and Aggregations")

        try:
            # COUNT QUERIES
            print_info("Running count queries...")
            total_users = Profile.objects.count()
            total_courses = Course.objects.count()
            total_units = Unit.objects.count()
            total_enrollments = Enrollment.objects.count()

            print_success(f"Total Users: {total_users}")
            print_success(f"Total Courses: {total_courses}")
            print_success(f"Total Units: {total_units}")
            print_success(f"Total Enrollments: {total_enrollments}")

            # FILTERED QUERIES
            print_info("Running filtered queries...")
            trainers = Profile.objects.filter(primary_role='trainer').count()
            trainees = Profile.objects.filter(primary_role='trainee').count()
            published_courses = Course.objects.filter(status='published').count()

            print_success(f"Trainers: {trainers}")
            print_success(f"Trainees: {trainees}")
            print_success(f"Published Courses: {published_courses}")

            # JOIN QUERIES
            print_info("Running join queries...")
            courses_with_units = Course.objects.filter(units__isnull=False).distinct().count()
            print_success(f"Courses with units: {courses_with_units}")

            return True
        except Exception as e:
            print_error(f"Complex queries failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def cleanup(self):
        """Clean up test data"""
        print_section("8. Cleanup Test Data")

        try:
            print_info("Deleting test data...")

            # Delete in reverse order to respect foreign keys
            for enrollment in self.test_enrollments:
                enrollment.delete()
            print_success("Deleted test enrollments")

            for unit in self.test_units:
                unit.delete()
            print_success("Deleted test units")

            for course in self.test_courses:
                course.delete()
            print_success("Deleted test courses")

            for team in self.test_teams:
                team.delete()
            print_success("Deleted test teams")

            for user in self.test_users:
                user.delete()
            print_success("Deleted test users")

            print_success("Cleanup completed successfully")
            return True
        except Exception as e:
            print_error(f"Cleanup failed: {e}")
            return False

    def run_all_tests(self):
        """Run all tests"""
        print(f"\n{BLUE}{'='*60}")
        print("  PostgreSQL End-to-End Test Suite")
        print(f"{'='*60}{RESET}\n")

        results = {
            'connection': self.check_connection(),
            'users': self.test_user_operations(),
            'courses': self.test_course_operations(),
            'units': self.test_unit_operations(),
            'enrollments': self.test_enrollment_operations(),
            'teams': self.test_team_operations(),
            'queries': self.test_complex_queries(),
            'cleanup': self.cleanup()
        }

        # Summary
        print_section("Test Summary")
        passed = sum(results.values())
        total = len(results)

        for test_name, result in results.items():
            status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
            print(f"  {test_name.capitalize()}: {status}")

        print(f"\n{BLUE}Results: {passed}/{total} tests passed{RESET}")

        if passed == total:
            print(f"{GREEN}✓ All tests passed!{RESET}\n")
            return True
        else:
            print(f"{RED}✗ Some tests failed{RESET}\n")
            return False


if __name__ == '__main__':
    tester = PostgreSQLTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
