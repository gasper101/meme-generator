FROM python:3.12-slim

WORKDIR /app

#da da vse trenutne mape v container
COPY . .

#nalozi iz requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#dodatek da nalozi fonte
RUN apt-get update && apt-get install -y \
    fontconfig \
    fonts-dejavu-core \
    libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PORT=5000
EXPOSE 5000

CMD ["python", "app.py"]