# Start from a small Linux image that already has Python 3.12.
FROM python:3.12-slim

# Do all following work inside /app in the image.
WORKDIR /app

# Copy ONLY requirements.txt first, then install the dependencies.
# (Doing this before copying the code lets Docker reuse the installed
#  packages on later builds when only your code changed — much faster.)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the application code in.
COPY app.py .

RUN useradd -u 1000 -m appuser
USER 1000

# Document that the app listens on port 8000.
EXPOSE 8000

# The command that starts the app when the container runs.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:create_app()"]