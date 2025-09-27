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
            "work": ft.Colors.BLUE,
            "personal": ft.Colors.PURPLE,
            "health": ft.Colors.GREEN,
            "finance": ft.Colors.AMBER,
            "education": ft.Colors.DEEP_ORANGE,
            "shopping": ft.Colors.PINK,
            "home": ft.Colors.TEAL,
            "social": ft.Colors.INDIGO,
            "travel": ft.Colors.BROWN,
            "entertainment": ft.Colors.RED,
            "uncategorized": ft.Colors.GREY
        }
        
        # Update UI based on task state
        self.update_ui()
    
    def update_ui(self):
        """Update the UI based on task state"""
        # Get category color
        category_color = self.category_colors.get(
            self.task.category, 
            ft.Colors.GREY
        )
        
        # Set UI based on completion status
        if self.task.completed:
            title_style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH,
                decoration_thickness=2,
                color=ft.Colors.GREY
            )
            bg_color = ft.Colors.GREY_100
        else:
            title_style = None
            bg_color = ft.Colors.WHITE
            
        # Format date
        created_date = datetime.fromisoformat(self.task.created_at)
        date_str = created_date.strftime("%b %d, %Y")
        
        # Create task card content
        self.content = ft.Row(
            [
                # Checkbox for completion status with direct page update
                ft.Checkbox(
                    value=self.task.completed,
                    on_change=self.toggle_completed,
                    data=self.task.id,  # Store task ID in data attribute
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
                                        color=ft.Colors.WHITE,
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
                            color=ft.Colors.GREY_700 if self.task.description else ft.Colors.GREY_400,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ) if self.task.description else ft.Container(height=0),
                        
                        # Date
                        ft.Text(
                            date_str,
                            size=12,
                            color=ft.Colors.GREY_500,
                        ),
                    ],
                    spacing=5,
                    expand=True,
                ),
                
                # Task actions
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Edit",
                            icon=ft.Icons.EDIT,
                            on_click=lambda e: self.edit_task(e),
                            bgcolor=ft.Colors.BLUE_400,
                            color=ft.Colors.WHITE,
                            data=self.task.id,  # Store task ID for reference
                        ),
                        ft.ElevatedButton(
                            "Delete",
                            icon=ft.Icons.DELETE,
                            bgcolor=ft.Colors.RED_400, 
                            color=ft.Colors.WHITE,
                            on_click=lambda e: self.delete_task(e),
                            data=self.task.id,  # Store task ID for reference
                        ),
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Set container styling
        self.bgcolor = bg_color
        self.border = ft.border.all(1, ft.Colors.GREY_300)
        
    def toggle_completed(self, e):
        """Toggle task completion status with forced update"""
        # Get checkbox state directly from the event
        is_completed = e.control.value
        
        # Update the task in app state with explicit completed status
        self.app_state.toggle_task(self.task.id, completed=is_completed)
        
        # Update local task object
        self.task.completed = is_completed
        
        # Force UI update with immediate feedback
        self.update_ui()
        self.app_state.page.update()
        
        # Show brief success message
        self.app_state.page.snack_bar = ft.SnackBar(
            content=ft.Text("Task status updated"),
            bgcolor=ft.Colors.GREEN_700,
            duration=1000,
        )
        self.app_state.page.snack_bar.open = True
        
        # Notify listeners for list refresh
        if self.on_change:
            self.on_change(e)
    
    def edit_task(self, e):
        """Show dialog to edit task"""
        # Create a dialog for editing with better UI
        title_field = ft.TextField(
            label="Task title",
            value=self.task.title,
            autofocus=True,
            border=ft.InputBorder.OUTLINE,
            filled=True,
            expand=True,
        )
        
        description_field = ft.TextField(
            label="Description (optional)",
            value=self.task.description or "",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border=ft.InputBorder.OUTLINE,
            filled=True,
            expand=True,
        )
        
        # Add feedback message
        feedback = ft.Text("", size=14, color=ft.Colors.RED_500)
        
        def close_dlg(e):
            dialog.open = False
            self.app_state.page.update()
        
        def save_changes(e):
            # Basic validation
            if not title_field.value or title_field.value.isspace():
                feedback.value = "Task title cannot be empty"
                feedback.update()
                return
                
            # Show saving indicator
            save_button.text = "Saving..."
            save_button.disabled = True
            save_button.update()
            
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
                    
            # Show success message
            self.app_state.page.snack_bar = ft.SnackBar(
                content=ft.Text("Task updated successfully"),
                bgcolor=ft.Colors.GREEN_700,
                duration=1500,
            )
            self.app_state.page.snack_bar.open = True
            
            # Update UI
            self.update_ui()
            close_dlg(e)
            
            # Notify listeners
            if self.on_change:
                self.on_change(e)
        
        # Create buttons with better styling
        cancel_button = ft.ElevatedButton(
            "Cancel",
            on_click=close_dlg,
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.GREY_300,
        )
        
        save_button = ft.ElevatedButton(
            "Save",
            on_click=save_changes,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_500,
        )
        
        # Create dialog
        dialog = ft.AlertDialog(
            title=ft.Text("Edit Task"),
            content=ft.Column(
                [
                    ft.Text("Edit task details below:", size=14),
                    title_field,
                    description_field,
                    feedback,
                ],
                width=400,
                height=250,
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                cancel_button,
                save_button,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # Show dialog
        self.app_state.page.dialog = dialog
        dialog.open = True
        self.app_state.page.update()
    
    def delete_task(self, e):
        """Handle task delete with confirmation"""
        def close_dlg(e):
            dialog.open = False
            self.app_state.page.update()
        
        def confirm_delete(e):
            # Show immediate visual feedback
            self.opacity = 0.5
            dialog.open = False
            self.app_state.page.update()
            
            # Delete immediately for better responsiveness
            self.app_state.delete_task(self.task.id)
            
            # Show brief success message
            self.app_state.page.snack_bar = ft.SnackBar(
                content=ft.Text("Task deleted successfully"),
                bgcolor=ft.Colors.GREEN_700,
                duration=1500,
            )
            self.app_state.page.snack_bar.open = True
            self.app_state.page.update()
            
            # Notify listeners
            if self.on_change:
                self.on_change(e)
        
        # Create compact dialog with clear buttons
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete Task"),
            content=ft.Text(f"Delete '{self.task.title}'?"),
            actions=[
                ft.ElevatedButton(
                    "Cancel",
                    on_click=close_dlg,
                    color=ft.Colors.BLACK,
                    bgcolor=ft.Colors.GREY_300,
                ),
                ft.ElevatedButton(
                    "Delete",
                    on_click=confirm_delete,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.RED_600,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # Show dialog
        self.app_state.page.dialog = dialog
        dialog.open = True
        self.app_state.page.update()
