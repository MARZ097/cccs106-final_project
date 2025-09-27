import flet as ft
from components.task_list import TaskList
from components.task_form import TaskForm
from components.filter_bar import FilterBar
from components.stats_panel import StatsPanel
from components.settings_dialog import SettingsDialog

class HomePage(ft.View):
    def __init__(self, app_state):
        super().__init__(route="/")
        self.app_state = app_state
        self.settings_dialog = SettingsDialog(app_state)
        
        # App header
        self.header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("TaskSmart AI", size=30, weight="bold"),
                    ft.IconButton(
                        icon=ft.Icons.SETTINGS,
                        tooltip="Settings",
                        on_click=self.show_settings
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=ft.padding.only(left=20, right=20, top=20, bottom=10),
        )
        
        # Task statistics panel
        self.stats_panel = StatsPanel(app_state)
        
        # Task form for adding new tasks
        self.task_form = TaskForm(app_state, on_add=self.refresh_view)
        
        # Filter bar
        self.filter_bar = FilterBar(
            app_state, 
            on_filter_change=self.refresh_view
        )
        
        # Task list
        self.task_list = TaskList(
            app_state,
            on_task_change=self.refresh_view
        )
        
        # Put everything together
        self.content = ft.Container(
            content=ft.Column(
                [
                    self.header,
                    self.stats_panel,
                    self.task_form,
                    self.filter_bar,
                    ft.Divider(height=1),
                    self.task_list,
                ],
                spacing=10,
                expand=True,
            ),
            expand=True,
            padding=10,
        )
        
        # Add everything to the view
        self.controls = [self.content, self.settings_dialog]
    
    def refresh_view(self, e=None):
        """Refresh all components with current data"""
        self.task_list.update_tasks()
        self.stats_panel.update_stats()
        self.update()
    
    def show_settings(self, e):
        """Show the settings dialog"""
        self.settings_dialog.open = True
        self.update()
