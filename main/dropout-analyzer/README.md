# Dropout Analyzer

## Overview
The Dropout Analyzer is a web application designed to analyze the dropout rates of students. It provides users with the ability to upload data files or manually enter data to assess dropout risks.

## Project Structure
```
dropout-analyzer
├── app.py                # Main application file that sets up the Flask server and routes
├── model.py              # Contains logic for analyzing dropout rates
├── requirements.txt      # Lists dependencies required for the project
├── uploads               # Directory for storing uploaded files
├── templates             # Contains HTML templates for the web application
│   ├── index.html       # Homepage
│   ├── login.html       # User login form
│   ├── signup.html      # User signup form
│   ├── dashboard.html    # User dashboard after login
│   ├── about.html       # Information about the application
│   ├── contact.html     # Contact form or information
│   ├── upload.html      # File upload form for dropout analysis
│   ├── manual_entry.html # Manual data entry form
│   └── result.html      # Displays results of the dropout analysis
├── static                # Contains static files like CSS and JavaScript
│   ├── css
│   │   └── style.css     # CSS styles for the application
│   └── js
│       └── script.js     # JavaScript for client-side functionality
└── README.md             # Documentation for the project
```

## Setup Instructions
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using:
   ```
   pip install -r requirements.txt
   ```
4. Ensure that the `uploads` directory exists. It will be created automatically when the application starts.
5. Run the application using:
   ```
   python app.py
   ```
6. Open your web browser and go to `http://127.0.0.1:5000` to access the application.

## Usage
- Users can log in with the credentials provided (default: admin/admin).
- After logging in, users can upload files or manually enter data to analyze dropout rates.
- The results of the analysis will be displayed on a separate results page.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.