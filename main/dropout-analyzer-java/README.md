# Dropout Analyzer - Java Spring Boot Version

This is a Java Spring Boot conversion of the original Python Flask dropout analyzer application. The application maintains the same functionality and output behavior as the original Python version.

## Features

- Student data management (manual entry and CSV upload)
- Dropout risk analysis and prediction
- University marks tracking
- Statistics and visualization
- User authentication and session management
- News feed integration

## Prerequisites

- Java 11 or higher
- MySQL 8.0 or higher
- Maven 3.6 or higher

## Setup Instructions

### 1. Database Setup

1. Install and start MySQL server
2. Create a database named `students_db`
3. Update the database credentials in `src/main/resources/application.properties` if needed:
   ```properties
   spring.datasource.username=root
   spring.datasource.password=password
   ```

### 2. Build the Application

```bash
mvn clean install
```

### 3. Run the Application

```bash
mvn spring-boot:run
```

The application will start on `http://localhost:8080`

### 4. Access the Application

- Open your browser and go to `http://localhost:8080`
- Login with admin credentials: `admin` / `admin`
- Or create a new account via signup

## Project Structure

```
src/main/java/com/example/dropoutanalyzer/
├── DropoutAnalyzerApplication.java          # Main application class
├── controller/
│   ├── MainController.java                  # Web controllers for pages
│   └── ApiController.java                   # REST API endpoints
├── model/
│   ├── Student.java                         # Student entity
│   ├── UniversityMarks.java                 # University marks entity
│   └── DropoutStudentDetails.java           # Dropout details entity
├── repository/
│   ├── StudentRepository.java               # Student data access
│   ├── UniversityMarksRepository.java       # Marks data access
│   └── DropoutStudentDetailsRepository.java # Dropout details data access
└── service/
    └── DropoutAnalysisService.java          # Business logic service

src/main/resources/
├── application.properties                   # Application configuration
├── static/css/style.css                     # CSS stylesheets
└── templates/                               # Thymeleaf templates
    └── base.html                            # Base template
```

## Key Differences from Python Version

- **Framework**: Flask → Spring Boot
- **ORM**: SQLAlchemy → JPA/Hibernate
- **Templates**: Jinja2 → Thymeleaf
- **Database**: SQLite (original) → MySQL (configurable)
- **Session Management**: Flask sessions → HttpSession
- **File Upload**: Werkzeug → Spring Multipart

## API Endpoints

- `GET /api/news` - Get news feed
- `GET /api/stats` - Get statistics data
- `GET /api/student-marks/{studentId}` - Get student marks and dropout percentage

## Configuration

The application can be configured via `application.properties`:

- Database connection settings
- Server port configuration
- File upload limits
- Session timeout
- Logging levels

## Troubleshooting

1. **Database Connection Issues**: Ensure MySQL is running and credentials are correct
2. **Port Conflicts**: Change `server.port` in `application.properties` if 8080 is in use
3. **File Upload Issues**: Check upload directory permissions and size limits

## Original Python Features Preserved

- Same dropout calculation algorithm
- Identical user interface and styling
- Same CSV processing logic
- Same authentication flow
- Same data models and relationships
- Same API responses and data formats
