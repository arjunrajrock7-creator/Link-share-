FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# The standard python image already includes gcc, git, and other build tools
# which ensures 100% success rate for packages like TgCrypto.

# Install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port for health check
EXPOSE 8080

# Command to run the bot
CMD ["python3", "bot.py"]
