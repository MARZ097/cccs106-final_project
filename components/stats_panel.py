import flet as ft
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter

class StatsPanel(ft.Container):
    def __init__(self, app_state):
        super().__init__()
        self.app_state = app_state
        self.bgcolor = ft.Colors.WHITE
        self.padding = 10
        self.border = ft.border.all(1, ft.Colors.GREY_300)
        self.border_radius = 10
        self.margin = ft.margin.only(bottom=10)
        self.expand = False
        
        # Create a toggle for expanded view
        self.expanded = False
        
        # Simple stats row
        self.stats_row = ft.Row(
            [
                self.create_stat_card("Total Tasks", "0", ft.Colors.BLUE),
                self.create_stat_card("Completed", "0", ft.Colors.GREEN),
                self.create_stat_card("Active", "0", ft.Colors.AMBER),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )
        
        # Chart placeholder
        self.chart_container = ft.Container(
            height=0,
            visible=False,
        )
        
        # Toggle button for expanded view
        self.expand_button = ft.IconButton(
            icon=ft.Icons.INSERT_CHART,
            tooltip="Show statistics",
            on_click=self.toggle_expanded
        )
        
        # Put everything together
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Task Statistics", size=16, weight=ft.FontWeight.BOLD),
                        self.expand_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                self.stats_row,
                self.chart_container
            ],
            spacing=10,
        )
        
        # Update stats
        self.update_stats()
    
    def create_stat_card(self, label, value, color):
        """Create a stat card with label and value"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(label, size=12, color=ft.Colors.GREY_700),
                    ft.Text(value, size=24, color=color, weight=ft.FontWeight.BOLD),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            padding=10,
            border_radius=5,
            alignment=ft.alignment.center,
        )
    
    def update_stats(self):
        """Update statistics with current data"""
        # Get task counts
        total_tasks = len(self.app_state.tasks)
        completed_tasks = len([t for t in self.app_state.tasks if t.completed])
        active_tasks = total_tasks - completed_tasks
        
        # Update stat cards
        self.stats_row.controls[0].content.controls[1].value = str(total_tasks)
        self.stats_row.controls[1].content.controls[1].value = str(completed_tasks)
        self.stats_row.controls[2].content.controls[1].value = str(active_tasks)
        
        # Update chart if expanded
        if self.expanded:
            self.update_chart()
            
        # Only call update() if the control has been added to a page
        if self.page:
            self.update()
    
    def update_chart(self):
        """Generate and update the chart"""
        try:
            # Get category distribution
            categories = [task.category for task in self.app_state.tasks]
            category_counts = Counter(categories)
            
            # Create pie chart
            plt.figure(figsize=(8, 4))
            plt.clf()
            
            # Create category subplot
            plt.subplot(1, 2, 1)
            labels = list(category_counts.keys())
            sizes = list(category_counts.values())
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title('Tasks by Category')
            
            # Create completion status subplot
            plt.subplot(1, 2, 2)
            completed = len([t for t in self.app_state.tasks if t.completed])
            active = len(self.app_state.tasks) - completed
            plt.bar(['Active', 'Completed'], [active, completed], color=['orange', 'green'])
            plt.title('Task Completion')
            
            # Save chart to buffer
            buffer = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            
            # Convert to base64 string
            image_data = base64.b64encode(buffer.getvalue()).decode()
            
            # Create image control
            img = ft.Image(
                src_base64=image_data,
                fit=ft.ImageFit.CONTAIN,
                expand=True,
            )
            
            # Update chart container
            self.chart_container.content = img
            self.chart_container.height = 300
            self.chart_container.visible = True
            
        except Exception as e:
            print(f"Error generating chart: {e}")
            # Fallback to text
            self.chart_container.content = ft.Text(
                "Unable to generate chart. Try adding more tasks.",
                color=ft.Colors.GREY_600
            )
            self.chart_container.height = 50
            self.chart_container.visible = True
            
        # Note: We don't call self.update() here because it's called by the parent method
    
    def toggle_expanded(self, e):
        """Toggle expanded view with chart"""
        self.expanded = not self.expanded
        
        if self.expanded:
            self.expand_button.icon = ft.Icons.INSERT_CHART_OUTLINED
            self.expand_button.tooltip = "Hide statistics"
            self.update_chart()
        else:
            self.expand_button.icon = ft.Icons.INSERT_CHART
            self.expand_button.tooltip = "Show statistics"
            self.chart_container.height = 0
            self.chart_container.visible = False
        
        # This will be called from an event handler, so the control should be on page
        self.update()
