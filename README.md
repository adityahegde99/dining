# Dining AI Web App

## Overview
The Dining AI Web App is a Flask-based web application designed to provide meal recommendations based on user input, dietary restrictions, and nutritional goals. It utilizes an AI model to suggest high-protein meals and optimizes serving sizes based on calorie and protein targets.

## Project Structure
```
dining-ai-webapp
├── app
│   ├── __init__.py        # Initializes the Flask application
│   ├── routes.py          # Defines the application routes
│   ├── forms.py           # Contains form classes for user input
│   └── utils.py           # Utility functions for data processing
├── templates
│   └── index.html         # Main HTML template for the web app
├── static
│   └── style.css          # CSS styles for the web app
├── FinalAI.py             # Main logic for the AI meal recommendation system
├── requirements.txt       # Lists project dependencies
├── Procfile               # Commands for running the app on Render
├── .gitignore             # Files to be ignored by Git
└── README.md              # Project documentation
```

## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/dining-ai-webapp.git
   cd dining-ai-webapp
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   flask run
   ```

## Usage
- Navigate to `http://127.0.0.1:5000` in your web browser to access the application.
- Input your meal preferences, dietary restrictions, and nutritional goals to receive meal recommendations.

## Deployment
To deploy the application on Render:
1. Push your code to GitHub.
2. Create a new web service on Render and connect it to your GitHub repository.
3. Set the build command to `pip install -r requirements.txt` and the start command to `gunicorn app:app`.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.