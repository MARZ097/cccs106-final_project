import flet as ft
from services.ai_service import CATEGORIES

class FilterBar(ft.Container):
    def __init__(self, app_state, on_filter_change=None):
        super().__init__()
        self.app_state = app_state
        self.on_filter_change = on_filter_change
        self.padding = 10
        
        # Status filter tabs
        self.status_tabs = ft.Tabs(
            selected_index=0,
            on_change=self.on_status_tab_change,
            tabs=[
                ft.Tab(text="All"),
                ft.Tab(text="Active"),
                ft.Tab(text="Completed")
            ],
            expand=1,
        )
        
        # Category filter dropdown
        self.category_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("all", "All Categories")
            ] + [
                ft.dropdown.Option(category, category.capitalize())
                for category in CATEGORIES
            ],
            width=200,
            value="all",
            on_change=self.on_category_change,
        )
        
        # Create content
        self.content = ft.Row(
            [
                ft.Text("Filter:", weight=ft.FontWeight.BOLD),
                self.status_tabs,
                ft.Text("Category:"),
                self.category_dropdown,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    
    def on_status_tab_change(self, e):
        """Handle status tab change"""
        # Map selected index to filter
        status_filters = ["all", "active", "completed"]
        self.app_state.current_filter = status_filters[self.status_tabs.selected_index]
        
        # Notify listeners
        if self.on_filter_change:
            self.on_filter_change(e)
    
    def on_category_change(self, e):
        """Handle category filter change"""
        # TODO: Implement category filtering in app_state
        # This will be implemented in a future enhancement
        
        # Notify listeners
        if self.on_filter_change:
            self.on_filter_change(e)
