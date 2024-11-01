# FROM python:3.12
FROM --platform=linux/amd64 python:3.12 as build

# Set the working directory in the container
WORKDIR /usr/src/app

# Set the timezone to Asia/Kolkata
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install pipenv globally
RUN pip install pipenv

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install project dependencies using pip
RUN pip install -r requirements.txt

# Copy the rest of the application files to the working directory
COPY . .

ENV MODE=Production
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

# RUN  python manage.py collectstatic
RUN python manage.py collectstatic --noinput
# Set executable permissions on entrypoint.sh
RUN chmod a+x entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Set the entrypoint command to execute entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
