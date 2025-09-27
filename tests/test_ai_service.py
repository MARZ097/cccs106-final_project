import sys
import os
import unittest

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_service import categorize_task

class TestAIService(unittest.TestCase):
    def test_categorize_task_work(self):
        """Test work category detection"""
        task = categorize_task("Prepare presentation for client meeting")
        self.assertEqual(task, "work")
        
    def test_categorize_task_health(self):
        """Test health category detection"""
        task = categorize_task("Schedule doctor appointment", "Need to get annual checkup")
        self.assertEqual(task, "health")
    
    def test_categorize_task_uncategorized(self):
        """Test uncategorized when no keywords match"""
        task = categorize_task("XYZ123", "Random text with no category keywords")
        self.assertEqual(task, "uncategorized")

if __name__ == "__main__":
    unittest.main()
