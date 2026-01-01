"""
MongoDB Service for LMS Content Storage

Handles storage and retrieval of:
- Module content items (videos, PDFs, presentations, etc.)
- Media files with metadata
- Test question media

This service provides a clean interface to MongoDB operations
and abstracts the database connection logic.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure, OperationFailure
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class MongoDBService:
    """Service class for MongoDB operations"""

    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._client:
            self.connect()

    def connect(self):
        """Establish connection to MongoDB"""
        try:
            if not getattr(settings, 'MONGODB_ENABLED', False):
                logger.warning("MongoDB is disabled in settings")
                return False

            self._client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            self._client.admin.command('ping')
            self._db = self._client[settings.MONGODB_DB_NAME]
            logger.info(f"Connected to MongoDB: {settings.MONGODB_DB_NAME}")
            return True
        except (ConnectionFailure, Exception) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False

    def is_connected(self) -> bool:
        """Check if MongoDB connection is active"""
        if not self._client:
            return False
        try:
            self._client.admin.command('ping')
            return True
        except:
            return False

    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    # ==================== Module Content Items ====================

    def create_module_content(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Create a module content item

        Args:
            data: Dictionary containing content data

        Returns:
            String ID of created document or None
        """
        if not self.is_connected():
            return None

        try:
            data['created_at'] = datetime.utcnow()
            data['updated_at'] = datetime.utcnow()

            result = self._db.module_content_items.insert_one(data)
            logger.info(f"Created module content: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating module content: {e}")
            return None

    def get_module_content(self, module_id: str) -> List[Dict[str, Any]]:
        """
        Get all content items for a module

        Args:
            module_id: UUID string of the module

        Returns:
            List of content items
        """
        if not self.is_connected():
            return []

        try:
            cursor = self._db.module_content_items.find(
                {'module_id': module_id}
            ).sort('sequence_order', ASCENDING)

            items = list(cursor)
            # Convert ObjectId to string for JSON serialization
            for item in items:
                item['_id'] = str(item['_id'])

            return items
        except Exception as e:
            logger.error(f"Error getting module content: {e}")
            return []

    def update_module_content(self, content_id: str, data: Dict[str, Any]) -> bool:
        """
        Update a module content item

        Args:
            content_id: MongoDB ObjectId as string
            content_data: Dictionary containing updated data

        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            return False

        try:
            from bson.objectid import ObjectId
            data['updated_at'] = datetime.utcnow()

            result = self._db.module_content_items.update_one(
                {'_id': ObjectId(content_id)},
                {'$set': data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating module content: {e}")
            return False

    def delete_module_content(self, content_id: str) -> bool:
        """
        Delete a module content item

        Args:
            content_id: MongoDB ObjectId as string

        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            return False

        try:
            from bson.objectid import ObjectId
            result = self._db.module_content_items.delete_one(
                {'_id': ObjectId(content_id)}
            )
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting module content: {e}")
            return False

    # ==================== Media Files ====================

    def create_media_file(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Create a media file record

        Args:
            data: Dictionary containing media file data

        Returns:
            String ID of created document or None
        """
        if not self.is_connected():
            return None

        try:
            data['created_at'] = datetime.utcnow()
            data['updated_at'] = datetime.utcnow()

            result = self._db.media_files.insert_one(data)
            logger.info(f"Created media file: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating media file: {e}")
            return None

    def get_media_file(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a media file by ID

        Args:
            file_id: MongoDB ObjectId as string

        Returns:
            Media file document or None
        """
        if not self.is_connected():
            return None

        try:
            from bson.objectid import ObjectId
            file_doc = self._db.media_files.find_one({'_id': ObjectId(file_id)})
            if file_doc:
                file_doc['_id'] = str(file_doc['_id'])
            return file_doc
        except Exception as e:
            logger.error(f"Error getting media file: {e}")
            return None

    def get_media_files_by_type(self, file_type: str) -> List[Dict[str, Any]]:
        """
        Get all media files of a specific type

        Args:
            file_type: Type of media (video, audio, pdf, ppt, image)

        Returns:
            List of media files
        """
        if not self.is_connected():
            return []

        try:
            cursor = self._db.media_files.find({'file_type': file_type})
            files = list(cursor)

            for file in files:
                file['_id'] = str(file['_id'])

            return files
        except Exception as e:
            logger.error(f"Error getting media files by type: {e}")
            return []

    def update_media_file(self, file_id: str, data: Dict[str, Any]) -> bool:
        """
        Update a media file record

        Args:
            file_id: MongoDB ObjectId as string
            data: Dictionary containing updated data

        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            return False

        try:
            from bson.objectid import ObjectId
            data['updated_at'] = datetime.utcnow()

            result = self._db.media_files.update_one(
                {'_id': ObjectId(file_id)},
                {'$set': data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating media file: {e}")
            return False

    # ==================== Test Question Media ====================

    def create_question_media(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Create a test question media record

        Args:
            data: Dictionary containing question media data

        Returns:
            String ID of created document or None
        """
        if not self.is_connected():
            return None

        try:
            data['created_at'] = datetime.utcnow()

            result = self._db.test_question_media.insert_one(data)
            logger.info(f"Created question media: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating question media: {e}")
            return None

    def get_question_media(self, question_id: str) -> List[Dict[str, Any]]:
        """
        Get all media for a specific question

        Args:
            question_id: UUID string of the question

        Returns:
            List of media items
        """
        if not self.is_connected():
            return []

        try:
            cursor = self._db.test_question_media.find({'question_id': question_id})
            media = list(cursor)

            for item in media:
                item['_id'] = str(item['_id'])

            return media
        except Exception as e:
            logger.error(f"Error getting question media: {e}")
            return []

    # ==================== Utility Methods ====================

    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get statistics for a collection"""
        if not self.is_connected():
            return {}

        try:
            stats = self._db.command('collStats', collection_name)
            return {
                'count': stats.get('count', 0),
                'size': stats.get('size', 0),
                'avg_obj_size': stats.get('avgObjSize', 0),
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}


# Singleton instance
mongo_service = MongoDBService()
