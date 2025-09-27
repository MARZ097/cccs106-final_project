import flet as ft
from views.home_page import HomePage
from state.app_state import AppState

def main(page: ft.Page):
    # App configuration
    page.title = "TaskSmart AI"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 0
    
    # Initialize app state
    app_state = AppState(page)
    
    # Configure routing
    def route_change(e):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(
                HomePage(app_state)
            )
        
        page.update()
    
    # Handle routing
    page.on_route_change = route_change
    page.go("/")  # Initial route

if __name__ == "__main__":
    ft.app(target=main)
