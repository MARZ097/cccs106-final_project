import re

# Categories for tasks
CATEGORIES = [
    "work", 
    "personal",
    "health",
    "finance",
    "education",
    "shopping",
    "home",
    "social",
    "travel",
    "entertainment"
]

# Keywords associated with each category
CATEGORY_KEYWORDS = {
    "work": ["work", "project", "meeting", "client", "deadline", "report", "presentation", "email", "call", "conference"],
    "personal": ["personal", "self", "hobby", "journal", "reflection", "goal", "plan", "habit", "routine"],
    "health": ["health", "exercise", "workout", "gym", "doctor", "medicine", "fitness", "diet", "nutrition", "meditation"],
    "finance": ["finance", "money", "bill", "payment", "budget", "invest", "expense", "tax", "salary", "bank", "pay"],
    "education": ["education", "learn", "study", "class", "course", "book", "read", "research", "homework", "assignment", "exam"],
    "shopping": ["shopping", "buy", "purchase", "store", "grocery", "order", "online", "amazon", "delivery", "pickup"],
    "home": ["home", "house", "clean", "repair", "fix", "maintenance", "garden", "decorate", "furniture", "appliance"],
    "social": ["social", "friend", "family", "party", "dinner", "lunch", "message", "call", "visit", "meet"],
    "travel": ["travel", "trip", "vacation", "flight", "hotel", "booking", "reservation", "ticket", "passport", "visa"],
    "entertainment": ["entertainment", "movie", "show", "game", "music", "concert", "event", "festival", "play", "stream", "watch"]
}

def categorize_task(title, description=""):
    """
    Categorize a task based on its title and description using a rule-based approach.
    This is a simple AI feature that can be enhanced with more sophisticated NLP later.
    """
    # Combine title and description, convert to lowercase
    text = (title + " " + description).lower()
    
    # Count keyword matches for each category
    category_scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Look for whole words only using regex
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.findall(pattern, text)
            score += len(matches)
        category_scores[category] = score
    
    # Find the category with the highest score
    if any(category_scores.values()):
        best_category = max(category_scores.items(), key=lambda x: x[1])[0]
        return best_category
    
    # If no keywords match, return "uncategorized"
    return "uncategorized"
