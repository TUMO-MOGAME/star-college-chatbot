"""
Image content manager for Star College Chatbot
"""
import os
import json
import logging
import re
from typing import Dict, List, Optional, Tuple, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageContentManager:
    """Manager for image content and metadata"""
    
    def __init__(self, database_path: str = "static/images/database.json"):
        """
        Initialize the image content manager
        
        Args:
            database_path: Path to the image database JSON file
        """
        self.database_path = database_path
        self.database = self._load_database()
        self.image_base_url = "/static/images/"
    
    def _load_database(self) -> Dict:
        """
        Load the image database from JSON file
        
        Returns:
            Dictionary containing the image database
        """
        try:
            if not os.path.exists(self.database_path):
                logger.warning(f"Image database not found at {self.database_path}")
                return {"locations": [], "students": []}
            
            with open(self.database_path, 'r') as f:
                database = json.load(f)
            
            logger.info(f"Loaded image database with {len(database.get('locations', []))} locations and {len(database.get('students', []))} students")
            return database
        except Exception as e:
            logger.error(f"Error loading image database: {str(e)}")
            return {"locations": [], "students": []}
    
    def find_matching_images(self, query: str) -> List[Dict]:
        """
        Find images that match the given query
        
        Args:
            query: User query string
            
        Returns:
            List of matching image entries
        """
        query = query.lower()
        matches = []
        
        # Check for location-related queries
        if self._is_location_query(query):
            matches.extend(self._find_matching_locations(query))
        
        # Check for student-related queries
        if self._is_student_query(query):
            matches.extend(self._find_matching_students(query))
        
        return matches
    
    def _is_location_query(self, query: str) -> bool:
        """
        Check if the query is related to locations
        
        Args:
            query: User query string
            
        Returns:
            True if the query is about locations, False otherwise
        """
        location_indicators = [
            "where", "location", "place", "building", "campus", 
            "room", "facility", "address", "map", "direction"
        ]
        
        return any(indicator in query for indicator in location_indicators)
    
    def _is_student_query(self, query: str) -> bool:
        """
        Check if the query is related to students
        
        Args:
            query: User query string
            
        Returns:
            True if the query is about students, False otherwise
        """
        student_indicators = [
            "student", "learner", "pupil", "scholar", "top", "best", 
            "achievement", "performer", "academic", "winner", "champion",
            "olympiad", "competition", "medal", "award"
        ]
        
        return any(indicator in query for indicator in student_indicators)
    
    def _find_matching_locations(self, query: str) -> List[Dict]:
        """
        Find locations that match the query
        
        Args:
            query: User query string
            
        Returns:
            List of matching location entries
        """
        matches = []
        
        for location in self.database.get("locations", []):
            # Check if location name is in query
            if location["name"].lower() in query:
                matches.append(self._prepare_image_data(location, "location"))
                continue
            
            # Check if any keywords match
            if any(keyword in query for keyword in location["keywords"]):
                matches.append(self._prepare_image_data(location, "location"))
        
        return matches
    
    def _find_matching_students(self, query: str) -> List[Dict]:
        """
        Find students that match the query
        
        Args:
            query: User query string
            
        Returns:
            List of matching student entries
        """
        matches = []
        
        for student in self.database.get("students", []):
            # Check if student name is in query
            if student["name"].lower() in query:
                matches.append(self._prepare_image_data(student, "student"))
                continue
            
            # Check if any keywords match
            if any(keyword in query for keyword in student["keywords"]):
                matches.append(self._prepare_image_data(student, "student"))
        
        return matches
    
    def _prepare_image_data(self, entry: Dict, entry_type: str) -> Dict:
        """
        Prepare image data for response
        
        Args:
            entry: Database entry
            entry_type: Type of entry (location or student)
            
        Returns:
            Dictionary with prepared image data
        """
        image_url = self.image_base_url + entry["image"]
        
        if entry_type == "location":
            caption = f"{entry['name']} - {entry['description']}"
        else:  # student
            caption = f"{entry['name']} ({entry['grade']}) - {entry['achievement']}"
        
        return {
            "type": entry_type,
            "name": entry["name"],
            "description": entry.get("description", entry.get("achievement", "")),
            "image_url": image_url,
            "caption": caption
        }
    
    def enhance_response_with_images(self, question: str, answer: str) -> Dict:
        """
        Enhance the response with relevant images
        
        Args:
            question: User question
            answer: Original text answer
            
        Returns:
            Dictionary with enhanced response including images
        """
        matching_images = self.find_matching_images(question.lower())
        
        if not matching_images:
            # No matching images found
            return {
                "text": answer,
                "has_images": False
            }
        
        # Get the most relevant image (first match)
        image_data = matching_images[0]
        
        # Create enhanced response
        enhanced_response = {
            "text": answer,
            "has_images": True,
            "images": [
                {
                    "url": image_data["image_url"],
                    "caption": image_data["caption"],
                    "type": image_data["type"]
                }
            ]
        }
        
        return enhanced_response
