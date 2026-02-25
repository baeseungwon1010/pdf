FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY private /app/private
COPY start.sh /app/start.sh

RUN mkdir -p /app/private/storage /app/private/backend/extracted \
  && chmod +x /app/start.sh

EXPOSE 5005


CMD ["/app/start.sh"]
