FROM python:3.12

LABEL maintainer="lmorintrejo@my.bcit.ca"

RUN mkdir /app

# Copy requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Set Working Directory
WORKDIR /app

# Install system dependencies required by mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Dependencies
RUN pip3 install -r requirements.txt

# Copy the source code
COPY . /app

# Make startup script executable before switching users
RUN chmod +x /app/start.sh

# Change permissions and become a non-privileged user
RUN chown -R nobody:nogroup /app
USER nobody

# Port the service listens on in the container
EXPOSE 8090

CMD ["./start.sh"]