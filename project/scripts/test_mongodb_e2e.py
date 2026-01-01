#!/usr/bin/env python3
"""
End-to-End MongoDB Test Script

Tests MongoDB operations for content storage:
- Module content items (videos, PDFs, presentations)
- Media files with metadata
- Test question media
- CRUD operations
- Query operations
"""

import os
import sys
import django
from datetime import datetime
import uuid

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'django-backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trainer_lms.settings')
django.setup()

from courses.mongodb_service import mongo_service

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


class MongoDBTester:
    def __init__(self):
        self.test_module_ids = []
        self.test_content_ids = []
        self.test_media_ids = []
        self.test_question_ids = []

    def check_connection(self):
        """Test MongoDB connection"""
        print_section("1. MongoDB Connection Test")
        try:
            if not mongo_service.is_connected():
                mongo_service.connect()

            if mongo_service.is_connected():
                print_success("Connected to MongoDB")
                print_info(f"Database: {mongo_service._db.name}")

                # Get server info
                server_info = mongo_service._client.server_info()
                print_info(f"MongoDB Version: {server_info['version']}")
                return True
            else:
                print_error("Failed to connect to MongoDB")
                print_info("Make sure MongoDB is running and MONGODB_ENABLED=True in .env")
                return False
        except Exception as e:
            print_error(f"Connection failed: {e}")
            return False

    def test_module_content_operations(self):
        """Test Module Content CRUD operations"""
        print_section("2. Module Content CRUD Operations")

        try:
            module_id = str(uuid.uuid4())
            self.test_module_ids.append(module_id)

            # CREATE - Video Content
            print_info("Creating video content item...")
            video_data = {
                'module_id': module_id,
                'content_type': 'video',
                'title': 'Introduction to PostgreSQL',
                'description': 'Learn the basics of PostgreSQL',
                'file_reference': 's3://lms-bucket/videos/intro-postgresql.mp4',
                'file_size_bytes': 52428800,  # 50 MB
                'duration_seconds': 1200,  # 20 minutes
                'thumbnail_url': 's3://lms-bucket/thumbnails/intro-postgresql.jpg',
                'sequence_order': 1,
                'metadata': {
                    'format': 'mp4',
                    'resolution': '1080p',
                    'mime_type': 'video/mp4'
                }
            }

            video_id = mongo_service.create_module_content(video_data)
            if video_id:
                self.test_content_ids.append(video_id)
                print_success(f"Created video content (ID: {video_id})")
            else:
                print_error("Failed to create video content")
                return False

            # CREATE - PDF Content
            print_info("Creating PDF content item...")
            pdf_data = {
                'module_id': module_id,
                'content_type': 'pdf',
                'title': 'PostgreSQL Course Materials',
                'description': 'Comprehensive study materials',
                'file_reference': 's3://lms-bucket/pdfs/postgresql-guide.pdf',
                'file_size_bytes': 5242880,  # 5 MB
                'duration_seconds': 0,
                'thumbnail_url': 's3://lms-bucket/thumbnails/pdf-preview.jpg',
                'sequence_order': 2,
                'metadata': {
                    'format': 'pdf',
                    'resolution': None,
                    'mime_type': 'application/pdf'
                }
            }

            pdf_id = mongo_service.create_module_content(pdf_data)
            if pdf_id:
                self.test_content_ids.append(pdf_id)
                print_success(f"Created PDF content (ID: {pdf_id})")
            else:
                print_error("Failed to create PDF content")
                return False

            # CREATE - Presentation Content
            print_info("Creating presentation content item...")
            ppt_data = {
                'module_id': module_id,
                'content_type': 'ppt',
                'title': 'Database Design Principles',
                'description': 'Slide deck on database design',
                'file_reference': 's3://lms-bucket/presentations/db-design.pptx',
                'file_size_bytes': 10485760,  # 10 MB
                'duration_seconds': 0,
                'thumbnail_url': 's3://lms-bucket/thumbnails/ppt-preview.jpg',
                'sequence_order': 3,
                'metadata': {
                    'format': 'pptx',
                    'resolution': None,
                    'mime_type': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
                }
            }

            ppt_id = mongo_service.create_module_content(ppt_data)
            if ppt_id:
                self.test_content_ids.append(ppt_id)
                print_success(f"Created presentation content (ID: {ppt_id})")
            else:
                print_error("Failed to create presentation content")
                return False

            # READ - Get all content for module
            print_info("Reading module content...")
            contents = mongo_service.get_module_content(module_id)
            if len(contents) == 3:
                print_success(f"Retrieved {len(contents)} content items for module")
                for content in contents:
                    print_info(f"  - {content['title']} ({content['content_type']})")
            else:
                print_error(f"Expected 3 items, got {len(contents)}")
                return False

            # UPDATE
            print_info("Updating video content...")
            update_data = {
                'title': 'Introduction to PostgreSQL - Updated',
                'duration_seconds': 1500  # Extended to 25 minutes
            }
            if mongo_service.update_module_content(video_id, update_data):
                print_success("Updated video content")

                # Verify update
                updated_contents = mongo_service.get_module_content(module_id)
                updated_video = next((c for c in updated_contents if c['_id'] == video_id), None)
                if updated_video and updated_video['duration_seconds'] == 1500:
                    print_success("Verified update: duration changed to 1500 seconds")
                else:
                    print_error("Update verification failed")
                    return False
            else:
                print_error("Failed to update video content")
                return False

            return True
        except Exception as e:
            print_error(f"Module content operations failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def test_media_file_operations(self):
        """Test Media File CRUD operations"""
        print_section("3. Media File CRUD Operations")

        try:
            uploader_id = str(uuid.uuid4())

            # CREATE - Video Media
            print_info("Creating video media file...")
            video_media = {
                'file_type': 'video',
                'title': 'Advanced SQL Tutorial',
                'file_path': 's3://lms-bucket/media/advanced-sql.mp4',
                'file_size_bytes': 104857600,  # 100 MB
                'duration_seconds': 3600,  # 1 hour
                'thumbnail_path': 's3://lms-bucket/media/thumbnails/advanced-sql.jpg',
                'upload_metadata': {
                    'uploaded_by': uploader_id,
                    'upload_date': datetime.utcnow(),
                    'original_filename': 'advanced-sql-tutorial.mp4'
                },
                'encoding_status': 'completed'
            }

            video_media_id = mongo_service.create_media_file(video_media)
            if video_media_id:
                self.test_media_ids.append(video_media_id)
                print_success(f"Created video media (ID: {video_media_id})")
            else:
                print_error("Failed to create video media")
                return False

            # CREATE - Audio Media
            print_info("Creating audio media file...")
            audio_media = {
                'file_type': 'audio',
                'title': 'Database Podcast Episode 1',
                'file_path': 's3://lms-bucket/media/podcast-ep1.mp3',
                'file_size_bytes': 20971520,  # 20 MB
                'duration_seconds': 1800,  # 30 minutes
                'thumbnail_path': None,
                'upload_metadata': {
                    'uploaded_by': uploader_id,
                    'upload_date': datetime.utcnow(),
                    'original_filename': 'podcast-episode-1.mp3'
                },
                'encoding_status': 'completed'
            }

            audio_media_id = mongo_service.create_media_file(audio_media)
            if audio_media_id:
                self.test_media_ids.append(audio_media_id)
                print_success(f"Created audio media (ID: {audio_media_id})")
            else:
                print_error("Failed to create audio media")
                return False

            # CREATE - Image Media
            print_info("Creating image media file...")
            image_media = {
                'file_type': 'image',
                'title': 'Database Schema Diagram',
                'file_path': 's3://lms-bucket/media/schema-diagram.png',
                'file_size_bytes': 2097152,  # 2 MB
                'duration_seconds': 0,
                'thumbnail_path': 's3://lms-bucket/media/thumbnails/schema-diagram-thumb.png',
                'upload_metadata': {
                    'uploaded_by': uploader_id,
                    'upload_date': datetime.utcnow(),
                    'original_filename': 'database-schema.png'
                },
                'encoding_status': 'completed'
            }

            image_media_id = mongo_service.create_media_file(image_media)
            if image_media_id:
                self.test_media_ids.append(image_media_id)
                print_success(f"Created image media (ID: {image_media_id})")
            else:
                print_error("Failed to create image media")
                return False

            # READ - Get specific media file
            print_info("Reading specific media file...")
            fetched_media = mongo_service.get_media_file(video_media_id)
            if fetched_media and fetched_media['title'] == 'Advanced SQL Tutorial':
                print_success(f"Retrieved media: {fetched_media['title']}")
            else:
                print_error("Failed to retrieve media file")
                return False

            # READ - Get media by type
            print_info("Reading media files by type...")
            video_files = mongo_service.get_media_files_by_type('video')
            audio_files = mongo_service.get_media_files_by_type('audio')
            image_files = mongo_service.get_media_files_by_type('image')

            print_success(f"Video files: {len(video_files)}")
            print_success(f"Audio files: {len(audio_files)}")
            print_success(f"Image files: {len(image_files)}")

            # UPDATE
            print_info("Updating media encoding status...")
            if mongo_service.update_media_file(video_media_id, {'encoding_status': 'processing'}):
                print_success("Updated media file")

                # Verify update
                updated_media = mongo_service.get_media_file(video_media_id)
                if updated_media and updated_media['encoding_status'] == 'processing':
                    print_success("Verified update: status changed to 'processing'")
                else:
                    print_error("Update verification failed")
                    return False
            else:
                print_error("Failed to update media file")
                return False

            return True
        except Exception as e:
            print_error(f"Media file operations failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def test_question_media_operations(self):
        """Test Question Media operations"""
        print_section("4. Question Media Operations")

        try:
            question_id = str(uuid.uuid4())
            self.test_question_ids.append(question_id)

            # CREATE - Image for question
            print_info("Creating question image...")
            question_image = {
                'question_id': question_id,
                'media_type': 'image',
                'file_reference': 's3://lms-bucket/questions/diagram-q1.png',
                'file_size_bytes': 1048576,  # 1 MB
                'metadata': {
                    'format': 'png',
                    'dimensions': '1920x1080',
                    'duration_seconds': None
                }
            }

            image_id = mongo_service.create_question_media(question_image)
            if image_id:
                print_success(f"Created question image (ID: {image_id})")
            else:
                print_error("Failed to create question image")
                return False

            # CREATE - Video for question
            print_info("Creating question video...")
            question_video = {
                'question_id': question_id,
                'media_type': 'video',
                'file_reference': 's3://lms-bucket/questions/demo-q1.mp4',
                'file_size_bytes': 5242880,  # 5 MB
                'metadata': {
                    'format': 'mp4',
                    'dimensions': '1280x720',
                    'duration_seconds': 60
                }
            }

            video_id = mongo_service.create_question_media(question_video)
            if video_id:
                print_success(f"Created question video (ID: {video_id})")
            else:
                print_error("Failed to create question video")
                return False

            # READ - Get all media for question
            print_info("Reading question media...")
            question_media = mongo_service.get_question_media(question_id)
            if len(question_media) == 2:
                print_success(f"Retrieved {len(question_media)} media items for question")
                for media in question_media:
                    print_info(f"  - {media['media_type']} ({media['metadata']['format']})")
            else:
                print_error(f"Expected 2 items, got {len(question_media)}")
                return False

            return True
        except Exception as e:
            print_error(f"Question media operations failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def test_collection_stats(self):
        """Test collection statistics"""
        print_section("5. Collection Statistics")

        try:
            print_info("Getting collection statistics...")

            # Module content stats
            content_stats = mongo_service.get_collection_stats('module_content_items')
            print_success(f"Module Content Items:")
            print_info(f"  Count: {content_stats.get('count', 0)}")
            print_info(f"  Size: {content_stats.get('size', 0)} bytes")

            # Media files stats
            media_stats = mongo_service.get_collection_stats('media_files')
            print_success(f"Media Files:")
            print_info(f"  Count: {media_stats.get('count', 0)}")
            print_info(f"  Size: {media_stats.get('size', 0)} bytes")

            # Question media stats
            question_stats = mongo_service.get_collection_stats('test_question_media')
            print_success(f"Question Media:")
            print_info(f"  Count: {question_stats.get('count', 0)}")
            print_info(f"  Size: {question_stats.get('size', 0)} bytes")

            return True
        except Exception as e:
            print_error(f"Collection stats failed: {e}")
            return False

    def cleanup(self):
        """Clean up test data"""
        print_section("6. Cleanup Test Data")

        try:
            print_info("Deleting test data...")

            # Delete module content
            for content_id in self.test_content_ids:
                if mongo_service.delete_module_content(content_id):
                    print_success(f"Deleted content: {content_id}")

            # Note: Media files and question media don't have delete methods in the service
            # In production, you would implement these as needed

            print_success("Cleanup completed successfully")
            return True
        except Exception as e:
            print_error(f"Cleanup failed: {e}")
            return False

    def run_all_tests(self):
        """Run all tests"""
        print(f"\n{BLUE}{'='*60}")
        print("  MongoDB End-to-End Test Suite")
        print(f"{'='*60}{RESET}\n")

        results = {
            'connection': self.check_connection()
        }

        # Only run other tests if connection succeeds
        if results['connection']:
            results.update({
                'module_content': self.test_module_content_operations(),
                'media_files': self.test_media_file_operations(),
                'question_media': self.test_question_media_operations(),
                'stats': self.test_collection_stats(),
                'cleanup': self.cleanup()
            })
        else:
            print_info("\nSkipping remaining tests due to connection failure")
            print_info("Please check:")
            print_info("  1. MongoDB is running (mongod service)")
            print_info("  2. MONGODB_ENABLED=True in .env")
            print_info("  3. MONGODB_URI is correct in .env")

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
            print(f"{YELLOW}⚠ Some tests failed or were skipped{RESET}\n")
            return False


if __name__ == '__main__':
    tester = MongoDBTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
