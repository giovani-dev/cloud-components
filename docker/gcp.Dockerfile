FROM python:3.10.6-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV PORT 8080
ENV HOST 0.0.0.0
ENV STORAGE_BASE /
ENV STORAGE_DIR storage

# Python app installation
WORKDIR $APP_HOME

# https://github.com/oittaa/gcp-storage-emulator/archive/refs/tags/v2022.06.11.zip
RUN apt-get update; \
    apt-get install -y \
        unzip \
        curl
RUN curl -L0 https://github.com/oittaa/gcp-storage-emulator/archive/refs/tags/v2022.06.11.zip -o gcp-storage-emulator.zip; \
    unzip gcp-storage-emulator.zip; \
    mv gcp-storage-emulator-2022.06.11/* .
RUN rm -rf gcp-storage-emulator-2022.06.11;
RUN pip install .

EXPOSE $PORT

# ENTRYPOINT ["gcp-storage-emulator"]
CMD gcp-storage-emulator start