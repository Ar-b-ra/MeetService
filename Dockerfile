FROM python:latest
RUN apt update -y && \
    apt upgrade -y && \
    apt install -y --no-install-recommends \
    python3-pip && \
    apt-get install -y redis && apt-get clean && \
    apt autoremove -y && \
    rm -rf /var/lib/apt/lists/*
COPY . /MeetService
WORKDIR /MeetService
# Установка зависимостей
RUN make venv
ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE ${PORT}
CMD ["make run"]