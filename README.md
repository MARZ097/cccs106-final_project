# TaskSmart AI - Task Management Application

TaskSmart AI is a cross-platform task management application built with Flet (Python + Flutter) that uses AI to automatically categorize tasks based on their content.

## Features

- **Task Management**: Create, edit, delete, and complete tasks
- **AI Categorization**: Automatic task categorization using rule-based AI
- **Data Visualization**: Visual representation of task categories and completion status
- **Filtering**: Filter tasks by status and category
- **Cross-Platform**: Works on desktop, web, and mobile
- **Data Persistence**: Local JSON storage for tasks and settings
- **Responsive UI**: Clean, modern interface that adapts to different screen sizes
- **Settings Management**: Customize application behavior

## Project Structure

```
/app
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md               # Documentation
├── /components             # Reusable UI components
├── /models                 # Data models
├── /services               # Business logic and AI
├── /state                  # State management
├── /storage                # Data persistence (created at runtime)
├── /tests                  # Unit tests
└── /views                  # Page views
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone [repository-url]
   cd tasksmart-ai
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

To run the desktop application:
```
python main.py
```

To run as a web application:
```
python -m flet.web main.py
```

## AI Feature

The application uses a rule-based AI system to automatically categorize tasks based on keywords in the title and description. The categorization system analyzes task content and assigns one of the following categories:

- Work
- Personal
- Health
- Finance
- Education
- Shopping
- Home
- Social
- Travel
- Entertainment
- Uncategorized (default)

This AI feature could be enhanced in future versions to use more sophisticated natural language processing techniques or external AI APIs.

## Testing

Run the tests with:
```
python -m unittest discover -s tests
```

## Customization

The application supports customization through the settings panel:
- Theme (Light/Dark/System)
- Task sorting options
- AI categorization toggle

## Future Enhancements

Potential future improvements:
- Cloud synchronization
- Advanced AI categorization using machine learning
- Task scheduling and reminders
- Collaboration features
- Mobile app deployment

## Technologies Used

- Flet: UI framework
- Python: Backend logic
- Matplotlib: Data visualization
- JSON: Data storage