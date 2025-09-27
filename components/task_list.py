import flet as ft
from components.task_item import TaskItem

class TaskList(ft.Container):
    def __init__(self, app_state, on_task_change=None):
        super().__init__()
        self.app_state = app_state
        self.on_task_change = on_task_change
        self.padding = 10
        self.expand = True
        
        # Create a container for the task list
        self.tasks_container = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        # Empty state
        self.empty_state = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.icons.CHECK_BOX_OUTLINE_BLANK, size=60, color=ft.colors.GREY_400),
                    ft.Text("No tasks found", size=16, color=ft.colors.GREY_600),
                    ft.Text("Add a new task to get started", size=14, color=ft.colors.GREY_400)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
        
        self.content = ft.Column(
            [self.tasks_container],
            expand=True,
        )
        
        # Initialize the list
        self.update_tasks()
    
    def update_tasks(self):
        """Update the list of tasks based on current filter"""
        filtered_tasks = self.app_state.get_filtered_tasks()
        self.tasks_container.controls.clear()
        
        if not filtered_tasks:
            self.content.controls = [self.empty_state]
        else:
            # Add all tasks to the list
            for task in filtered_tasks:
                task_item = TaskItem(
                    task, 
                    self.app_state,
                    on_change=self.on_task_changed
                )
                self.tasks_container.controls.append(task_item)
            
            self.content.controls = [self.tasks_container]
    
    def on_task_changed(self, e=None):
        """Called when a task is changed"""
        if self.on_task_change:
            self.on_task_change(e)
