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

## Pictures

![image (25)](https://github.com/user-attachments/assets/4271bb0e-3b1f-4155-8751-b55fd9b410c4)
![image (26)](https://github.com/user-attachments/assets/f37543da-879b-4b62-b5d1-65749768eef6)
![image (27)](https://github.com/user-attachments/assets/7f71f636-72dd-47b6-a83b-a3a728793ae8)
![image (29)](https://github.com/user-attachments/assets/2b584420-2939-4495-8589-e553d9210069)


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
