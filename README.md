# URL Shortener Website #

## Project Description

This project is an individual assignment made for the Software Development & DevOps course.

### Core functionalities
- connection between the front and backend (through user-friendly buttons and input areas)
- REST API endpoint for generating a short URL 
- creating entries for a persistent sqlite database
- displaying the generated URL on the website

### Tech Stack for the project
- Frontend: HTML/CSS/JS
- Backend: Django + Django REST Framework
- Database: SQLite

## Setup ##
### 1. Clone the repository into your desired folder. You can do it either through SSH or HTTPS. ###

- SSH

```bash
    git clone git@github.com:BigosKAR/URL-Shortener.git
```
- HTTPS

```bash
    git clone https://github.com/BigosKAR/URL-Shortener.git
```

### 2. Change into the clone directory.
```bash
    cd URL-Shortener
```

### 3. Create and activate the virtual environment.

```bash
    python -m venv .venv
```

To activate the environment run:

- On Windows (cmd.exe)
```powershell
    .venv\Scripts\activate.bat
```

- On Windows (Git Bash)
```bash
    source .venv/Scripts/activate
```

- On Linux
```bash
    source .venv/bin/activate
```

### 4. Download the required packages

```bash
    pip install -r requirements.txt
```

### 5. Set up database and run the server
To set up the database, run:
```bash
    python manage.py migrate
```

To run the server, execute:
```bash
    python manage.py runserver
```

## AI Usage
This repository does not contain AI-Generated code. 

AI has rarely been used as a last resort whenever online sites/forums did not provide necessary information. 

In the case it was utilized, it has been told not to give code but rather hints to direct me towards the correct solution. 