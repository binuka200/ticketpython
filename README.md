# Ticket Management System with UI and API with Python  

A simple ticket management system built with Python Django Framework, featuring a full UI and API with JWT authentication and has the basic features needed of a ticketing system and analyzes sentiment based on initial ticket description.

## Features

### User Interface
- Modern, responsive dashboard for ticket management
- Quick ticket creation and management interface
- Advanced filtering and sorting capabilities
- Personal workspace with "My Tickets" view
- File attachment support for tickets and comments
- User profile management
- Ticket following system for updates

### API Features
- User Authentication with JWT
- Ticket Management
- Department and Status Management
- File Attachments
- API Documentation with Swagger
- Docker Containerization

### Key Functionalities
- Create and manage support tickets
- Assign tickets to departments and users
- Track ticket status changes
- Add comments and attachments
- Follow tickets for updates
- Filter and search tickets
- Sentiment analysis on ticket descriptions
- Department transfers
- User role management

## Prerequisites

- Docker and Docker Compose
- Git

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd ticketpython
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Update the `.env` file with your configurations:
- Set a secure SECRET_KEY
- Update database credentials if needed

4. Build and start the containers:
```bash
docker-compose up --build
```

The UI will be available at: http://localhost:8000/

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/api/docs/

## Development

To make initial db migrations:
```bash
docker-compose exec web python ticketsystem/manage.py migrate
```

To create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```
## TODO
- Email Implementation
- Write Tests
-Basic Implementation for now (Needs improvement)


## License

This project is licensed under the MIT License - see the LICENSE file for details. 