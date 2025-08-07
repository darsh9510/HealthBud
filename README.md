# HealthBud

A Django-based health management application with chat functionality and machine learning capabilities.

## Features

- User authentication and registration
- Doctor verification system
- Chat rooms for health discussions
- Disease recommendation system
- Machine learning integration

## Setup and Installation

### Prerequisites

- Python 3.12+
- Django 5.2+

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd HealthBud
   ```

2. **Install required packages**
   ```bash
   pip install django requests dill numpy
   ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Usage

1. **Registration**: Users can register as patients or doctors
2. **Login**: Authenticate using your credentials
3. **Chat Rooms**: Join or create chat rooms for health discussions
4. **Disease Info**: Get disease information and recommendations
5. **Doctor Verification**: Doctors can verify their credentials through external API

## Project Structure

- `healthbuddy/` - Main Django application
- `p1/` - Django project settings
- `templates/` - HTML templates
- `static/` - CSS and static files
- `db.sqlite3` - SQLite database
- `manage.py` - Django management script

## API Integration

The application integrates with external APIs for doctor verification using the Neurelo service.

## Note

This is a development server. For production deployment, use a proper WSGI/ASGI server and configure proper security settings.