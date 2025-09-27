import flet as ft
import json
import os

class SettingsDialog(ft.AlertDialog):
    def __init__(self, app_state):
        super().__init__()
        self.app_state = app_state
        
        # Initialize settings with defaults
        self.settings = {
            "theme": "system",  # system, light, dark
            "sort_by": "created_at",  # created_at, updated_at, title
            "sort_direction": "desc",  # asc, desc
            "show_completed": True,
            "auto_categorize": True,
        }
        
        # Load settings from file
        self.load_settings()
        
        # Create settings form
        self.modal = True
        self.title = ft.Text("Settings")
        
        # Theme setting
        self.theme_dropdown = ft.Dropdown(
            label="Theme",
            options=[
                ft.dropdown.Option("system", "System Default"),
                ft.dropdown.Option("light", "Light"),
                ft.dropdown.Option("dark", "Dark"),
            ],
            value=self.settings["theme"],
            width=400,
        )
        
        # Sort setting
        self.sort_dropdown = ft.Dropdown(
            label="Sort tasks by",
            options=[
                ft.dropdown.Option("created_at", "Creation Date"),
                ft.dropdown.Option("updated_at", "Last Updated"),
                ft.dropdown.Option("title", "Title"),
            ],
            value=self.settings["sort_by"],
            width=400,
        )
        
        # Sort direction
        self.sort_direction = ft.Dropdown(
            label="Sort direction",
            options=[
                ft.dropdown.Option("desc", "Newest first"),
                ft.dropdown.Option("asc", "Oldest first"),
            ],
            value=self.settings["sort_direction"],
            width=400,
        )
        
        # Show completed toggle
        self.show_completed = ft.Switch(
            label="Show completed tasks in lists",
            value=self.settings["show_completed"],
        )
        
        # Auto categorize toggle
        self.auto_categorize = ft.Switch(
            label="Automatically categorize tasks with AI",
            value=self.settings["auto_categorize"],
        )
        
        # Create content
        self.content = ft.Column(
            [
                ft.Text("Appearance", weight=ft.FontWeight.BOLD),
                self.theme_dropdown,
                ft.Divider(),
                
                ft.Text("Task Display", weight=ft.FontWeight.BOLD),
                self.sort_dropdown,
                self.sort_direction,
                self.show_completed,
                ft.Divider(),
                
                ft.Text("AI Features", weight=ft.FontWeight.BOLD),
                self.auto_categorize,
            ],
            width=400,
            height=400,
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
        )
        
        # Create actions
        self.actions = [
            ft.TextButton("Cancel", on_click=self.close_dialog),
            ft.TextButton("Save", on_click=self.save_settings),
        ]
        self.actions_alignment = ft.MainAxisAlignment.END
    
    def close_dialog(self, e):
        """Close the dialog"""
        self.open = False
        self.app_state.page.update()
    
    def save_settings(self, e):
        """Save settings and close dialog"""
        # Update settings from form values
        self.settings["theme"] = self.theme_dropdown.value
        self.settings["sort_by"] = self.sort_dropdown.value
        self.settings["sort_direction"] = self.sort_direction.value
        self.settings["show_completed"] = self.show_completed.value
        self.settings["auto_categorize"] = self.auto_categorize.value
        
        # Save to file
        try:
            if not os.path.exists("storage"):
                os.makedirs("storage")
                
            with open("storage/settings.json", "w") as file:
                json.dump(self.settings, file, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
        
        # Apply settings
        self.apply_settings()
        
        # Close dialog
        self.close_dialog(e)
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists("storage/settings.json"):
                with open("storage/settings.json", "r") as file:
                    saved_settings = json.load(file)
                    # Update settings with saved values
                    for key, value in saved_settings.items():
                        if key in self.settings:
                            self.settings[key] = value
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def apply_settings(self):
        """Apply settings to the app"""
        # Apply theme
        if self.settings["theme"] == "light":
            self.app_state.page.theme_mode = ft.ThemeMode.LIGHT
        elif self.settings["theme"] == "dark":
            self.app_state.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.app_state.page.theme_mode = ft.ThemeMode.SYSTEM
        
        # Other settings would be applied when needed
        # For example, sorting would be applied when loading tasks
