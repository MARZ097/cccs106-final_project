import flet as ft
import json
import os
from datetime import datetime
from models.task import Task
from services.ai_service import categorize_task

class AppState:
    def __init__(self, page: ft.Page):
        self.page = page
        self.tasks = []
        self.current_filter = "all"  # all, active, completed
        self.load_tasks()
        
    def add_task(self, title, description=""):
        """Add a new task and save it"""
        task_id = self._generate_id()
        category = categorize_task(title, description)
        
        new_task = Task(
            id=task_id,
            title=title,
            description=description,
            category=category,
            created_at=datetime.now().isoformat(),
            completed=False
        )
        
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task
    
    def delete_task(self, task_id):
        """Delete a task by ID"""
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()
    
    def toggle_task(self, task_id):
        """Toggle the completion status of a task"""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                task.updated_at = datetime.now().isoformat()
                break
        self.save_tasks()
    
    def update_task(self, task_id, title=None, description=None, category=None):
        """Update task details"""
        for task in self.tasks:
            if task.id == task_id:
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description
                if category is not None:
                    task.category = category
                task.updated_at = datetime.now().isoformat()
                
                # Re-categorize if title or description changed
                if title is not None or description is not None:
                    task.category = categorize_task(task.title, task.description)
                break
        self.save_tasks()
    
    def get_filtered_tasks(self):
        """Get tasks based on current filter"""
        if self.current_filter == "active":
            return [task for task in self.tasks if not task.completed]
        elif self.current_filter == "completed":
            return [task for task in self.tasks if task.completed]
        else:
            return self.tasks
            
    def set_filter(self, filter_name):
        """Set the current filter"""
        self.current_filter = filter_name
    
    def load_tasks(self):
        """Load tasks from storage"""
        try:
            if not os.path.exists("storage"):
                os.makedirs("storage")
                
            if os.path.exists("storage/tasks.json"):
                with open("storage/tasks.json", "r") as file:
                    tasks_data = json.load(file)
                    self.tasks = [Task(**task) for task in tasks_data]
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to storage"""
        try:
            if not os.path.exists("storage"):
                os.makedirs("storage")
                
            with open("storage/tasks.json", "w") as file:
                tasks_data = [task.to_dict() for task in self.tasks]
                json.dump(tasks_data, file, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def _generate_id(self):
        """Generate a unique ID for a new task"""
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1
