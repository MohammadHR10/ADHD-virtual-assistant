# Builder stage
FROM python:3.12-slim as builder

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y gcc && pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app/hi

# Upgrade and clean up apt packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Copy installed Python packages from the builder stage
COPY --from=builder /root/.local /root/.local

# Update PATH environment variable
ENV PATH=/root/.local/bin:$PATH

# Copy the rest of the application's code from the host to the container at /app
COPY ./hi .

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run the command to start the Streamlit application
CMD ["streamlit", "run", "frontend2.py", "--server.port=10000", "--server.address=0.0.0.0"]
