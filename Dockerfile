FROM python:3.12.2-slim

WORKDIR app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

CMD [ "python", "-u", "./update_ddns.py" ]
