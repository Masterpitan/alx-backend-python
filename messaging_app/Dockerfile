# Use official Python base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory inside the container
WORKDIR /app

# Install system dependencies (for psycopg2/mysqlclient, etc if needed)
RUN apt-get update \
    && apt-get install -y libpq-dev gcc python3-dev musl-dev \
    && apt-get clean

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files into container
COPY . /app/

# Expose Django’s default port -p
EXPOSE 8000

# Run server (you can adjust if using gunicorn later)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
