FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_ENV=production

# Expose port 8000 to the outside world
EXPOSE 8000

# Run flask when the container launches
CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "8000", "--call", "app:create_app"]