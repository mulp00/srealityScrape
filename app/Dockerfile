# syntax=docker/dockerfile:1
FROM python:3.10-slim
WORKDIR /proj01

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev

COPY proj01/requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install scrapy-playwright
RUN apt-get install -y libglib2.0-0\
    libnss3\
    libnspr4\
    libatk1.0-0\
    libatk-bridge2.0-0\
    libcups2\
    libdrm2\
    libdbus-1-3\
    libatspi2.0-0\
    libxcomposite1\
    libxdamage1\
    libxext6\
    libxfixes3\
    libxrandr2\
    libgbm1\
    libxkbcommon0\
    libpango-1.0-0\
    libcairo2\
    libasound2\
    libwayland-client0

RUN playwright install

# Run the application:
COPY . .
EXPOSE 8080

ENV PYTHONBUFFERED=1

CMD ["python", "runme.py"]