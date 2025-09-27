import flet as ft
from services.ai_service import CATEGORIES

class TaskForm(ft.Container):
    def __init__(self, app_state, on_add=None):
        super().__init__()
        self.app_state = app_state
        self.on_add = on_add
        self.padding = 10
        self.bgcolor = ft.Colors.BLUE_50
        self.border_radius = 10
        
        # Create form fields
        self.title_field = ft.TextField(
            label="Task title",
            hint_text="Enter task title",
            autofocus=True,
            expand=True,
            border=ft.InputBorder.OUTLINE,
            filled=True,
            height=50
        )
        
        self.description_field = ft.TextField(
            label="Description (optional)",
            hint_text="Enter task description",
            multiline=True,
            min_lines=1,
            max_lines=3,
            expand=True,
            border=ft.InputBorder.OUTLINE,
            filled=True
        )
        
        # Create submit button with direct event handler
        self.add_button = ft.ElevatedButton(
            "Add Task",
            icon=ft.Icons.ADD,
            on_click=lambda e: self.add_task(e),
            bgcolor=ft.Colors.BLUE_500,
            color=ft.Colors.WHITE,
            height=45,
            width=120
        )
        
        # Expanded view toggle
        self.expanded = False
        self.expand_button = ft.IconButton(
            icon=ft.Icons.EXPAND_MORE,
            tooltip="Show description",
            on_click=self.toggle_expanded
        )
        
        # Create content
        self.content = ft.Column(
            [
                ft.Text("Add New Task", size=16, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        self.title_field,
                        self.expand_button,
                        self.add_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
            ],
            spacing=10
        )
    
    def toggle_expanded(self, e):
        """Toggle expanded view with description field"""
        self.expanded = not self.expanded
        
        if self.expanded:
            self.expand_button.icon = ft.Icons.EXPAND_LESS
            self.expand_button.tooltip = "Hide description"
            self.content.controls = [
                ft.Text("Add New Task", size=16, weight=ft.FontWeight.BOLD),
                self.title_field,
                self.description_field,
                self.add_button
            ]
        else:
            self.expand_button.icon = ft.Icons.EXPAND_MORE
            self.expand_button.tooltip = "Show description"
            self.content.controls = [
                ft.Text("Add New Task", size=16, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        self.title_field,
                        self.expand_button,
                        self.add_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
            ]
        
        self.update()
    
    def add_task(self, e):
        """Add a new task with improved feedback"""
        # Disable button to prevent multiple submissions
        self.add_button.disabled = True
        self.add_button.text = "Adding..."
        self.update()
        
        title = self.title_field.value.strip()
        description = self.description_field.value.strip()
        
        if not title:
            # Show error if title is empty
            self.title_field.error_text = "Title is required"
            self.add_button.disabled = False
            self.add_button.text = "Add Task"
            self.update()
            return
        
        # Add the task
        new_task = self.app_state.add_task(title, description)
        
        # Show success message with category info
        self.app_state.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Task added in category: {new_task.category}"),
            action="OK",
            bgcolor=ft.Colors.GREEN_700,
            duration=2000,
        )
        self.app_state.page.snack_bar.open = True
        self.app_state.page.update()
        
        # Clear form
        self.title_field.value = ""
        self.description_field.value = ""
        self.title_field.error_text = None
        self.add_button.disabled = False
        self.add_button.text = "Add Task"
        
        # Focus title field for next entry
        self.title_field.focus()
        
        # Notify listeners
        if self.on_add:
            self.on_add(e)
        
        self.update()
