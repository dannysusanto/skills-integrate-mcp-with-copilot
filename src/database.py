"""Database configuration and utility functions."""

import os
from typing import Optional
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "high_school_db")

# Create MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
activities_collection = db.activities

def init_db():
    """Initialize database with indexes if needed."""
    # Create indexes
    activities_collection.create_index("name", unique=True)

def get_all_activities():
    """Get all activities from the database."""
    return list(activities_collection.find({}, {'_id': 0}))

def get_activity(name: str) -> Optional[dict]:
    """Get a specific activity by name."""
    return activities_collection.find_one({"name": name}, {'_id': 0})

def add_participant(activity_name: str, email: str) -> bool:
    """Add a participant to an activity."""
    result = activities_collection.update_one(
        {"name": activity_name},
        {"$addToSet": {"participants": email}}
    )
    return result.modified_count > 0

def remove_participant(activity_name: str, email: str) -> bool:
    """Remove a participant from an activity."""
    result = activities_collection.update_one(
        {"name": activity_name},
        {"$pull": {"participants": email}}
    )
    return result.modified_count > 0

def seed_initial_activities(activities_data: dict):
    """Seed the database with initial activities if empty."""
    if activities_collection.count_documents({}) == 0:
        # Convert the activities dict to a list of documents
        activities_list = [
            {
                "name": name,
                **data
            }
            for name, data in activities_data.items()
        ]
        activities_collection.insert_many(activities_list)