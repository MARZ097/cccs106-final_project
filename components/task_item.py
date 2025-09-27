import flet as ft
from models.task import Task
from datetime import datetime

class TaskItem(ft.Container):
    def __init__(self, task: Task, app_state, on_change=None):
        super().__init__()
        self.task = task
        self.app_state = app_state
        self.on_change = on_change
        self.padding = 10
        self.border_radius = 5
        
        # Category colors
        self.category_colors = {
            "work": ft.colors.BLUE,
            "personal": ft.colors.PURPLE,
            "health": ft.colors.GREEN,
            "finance": ft.colors.AMBER,
            "education": ft.colors.DEEP_ORANGE,
            "shopping": ft.colors.PINK,
            "home": ft.colors.TEAL,
            "social": ft.colors.INDIGO,
            "travel": ft.colors.BROWN,
            "entertainment": ft.colors.RED,
            "uncategorized": ft.colors.GREY
        }
        
        # Update UI based on task state
        self.update_ui()
    
    def update_ui(self):
        """Update the UI based on task state"""
        # Get category color
        category_color = self.category_colors.get(
            self.task.category, 
            ft.colors.GREY
        )
        
        # Set UI based on completion status
        if self.task.completed:
            title_style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH,
                decoration_thickness=2,
                color=ft.colors.GREY
            )
            bg_color = ft.colors.GREY_100
        else:
            title_style = None
            bg_color = ft.colors.WHITE
            
        # Format date
        created_date = datetime.fromisoformat(self.task.created_at)
        date_str = created_date.strftime("%b %d, %Y")
        
        # Create task card content
        self.content = ft.Row(
            [
                # Checkbox for completion status
                ft.Checkbox(
                    value=self.task.completed,
                    on_change=self.toggle_completed,
                ),
                
                # Task content
                ft.Column(
                    [
                        # Title and category row
                        ft.Row(
                            [
                                ft.Text(
                                    self.task.title,
                                    size=16,
                                    style=title_style,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    expand=True,
                                ),
                                ft.Container(
                                    ft.Text(
                                        self.task.category,
                                        size=12,
                                        color=ft.colors.WHITE,
                                    ),
                                    bgcolor=category_color,
                                    border_radius=15,
                                    padding=ft.padding.only(left=12, right=12, top=5, bottom=5),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        
                        # Description (if any)
                        ft.Text(
                            self.task.description or "No description",
                            size=14,
                            color=ft.colors.GREY_700 if self.task.description else ft.colors.GREY_400,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ) if self.task.description else ft.Container(height=0),
                        
                        # Date
                        ft.Text(
                            date_str,
                            size=12,
                            color=ft.colors.GREY_500,
                        ),
                    ],
                    spacing=5,
                    expand=True,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                ),
                
                # Task actions
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            tooltip="Edit task",
                            on_click=self.edit_task,
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            tooltip="Delete task",
                            on_click=self.delete_task,
                        ),
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Set container styling
        self.bgcolor = bg_color
        self.border = ft.border.all(1, ft.colors.GREY_300)
        
    def toggle_completed(self, e):
        """Toggle task completion status"""
        self.app_state.toggle_task(self.task.id)
        self.task.completed = not self.task.completed
        self.update_ui()
        if self.on_change:
            self.on_change(e)
    
    def edit_task(self, e):
        """Show dialog to edit task"""
        # Create a dialog for editing
        title_field = ft.TextField(
            label="Task title",
            value=self.task.title,
            autofocus=True
        )
        description_field = ft.TextField(
            label="Description (optional)",
            value=self.task.description or "",
            multiline=True,
            min_lines=3,
            max_lines=5
        )
        
        def close_dlg(e):
            dialog.open = False
            self.app_state.page.update()
        
        def save_changes(e):
            # Update task with new values
            self.app_state.update_task(
                self.task.id,
                title=title_field.value,
                description=description_field.value
            )
            
            # Get the updated task
            for task in self.app_state.tasks:
                if task.id == self.task.id:
                    self.task = task
                    break
                    
            # Update UI
            self.update_ui()
            close_dlg(e)
            
            # Notify listeners
            if self.on_change:
                self.on_change(e)
        
        # Create dialog
        dialog = ft.AlertDialog(
            title=ft.Text("Edit Task"),
            content=ft.Column(
                [
                    title_field,
                    description_field,
                ],
                width=400,
                height=200,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=close_dlg),
                ft.TextButton("Save", on_click=save_changes),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # Show dialog
        self.app_state.page.dialog = dialog
        dialog.open = True
        self.app_state.page.update()
    
    def delete_task(self, e):
        """Show confirmation and delete task"""
        def close_dlg(e):
            dialog.open = False
            self.app_state.page.update()
        
        def confirm_delete(e):
            # Delete the task
            self.app_state.delete_task(self.task.id)
            close_dlg(e)
            
            # Notify listeners
            if self.on_change:
                self.on_change(e)
        
        # Create dialog
        dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text(f"Are you sure you want to delete task: {self.task.title}?"),
            actions=[
                ft.TextButton("Cancel", on_click=close_dlg),
                ft.TextButton("Delete", on_click=confirm_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # Show dialog
        self.app_state.page.dialog = dialog
        dialog.open = True
        self.app_state.page.update()
