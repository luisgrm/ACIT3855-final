FROM python:3.12

LABEL maintainer="lmorintrejo@my.bcit.ca"

RUN mkdir /app

# Copy requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Set Working Directory
WORKDIR /app

# Install Dependencies
RUN pip3 install -r requirements.txt

# Copy the source code
COPY . /app

# Change permissions and become a non-privileged user
RUN chown -R nobody:nogroup /app
USER nobody

# Port the service listens on in the container 
EXPOSE 8080

# Entrypoint = run Python
ENTRYPOINT ["python3"]

# Default = run app.py
CMD ["app.py"]