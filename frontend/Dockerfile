FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install streamlit requests

# Copy the UI code
COPY ui.py .

# Expose Streamlit port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "ui.py", "--server.address=0.0.0.0"]
