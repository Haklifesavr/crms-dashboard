# Use the official Python 3.8 image
FROM python:3.8

# Set working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run database migrations
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# Collect static files
# Note: Assuming your Django settings are configured correctly for static files
# RUN python manage.py collectstatic --noinput

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
# Command to run the development server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080"]


# FROM python:3.8

# ARG APP_HOME=/app
# WORKDIR ${APP_HOME}

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# COPY requirements.txt ${APP_HOME}
# # install python dependencies
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . ${APP_HOME}

# # running migrations
# RUN python manage.py migrate

# # gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "config.wsgi"]
