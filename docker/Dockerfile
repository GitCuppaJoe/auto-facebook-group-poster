ARG APP_IMAGE=selenium/standalone-chrome:4.0.0-rc-2-20210930

#===================================================
# Base Image
#===================================================
FROM $APP_IMAGE as base
LABEL author=GitCuppaJoe

# Necessary Environment Vars
ENV BOT_USERNAME= \
    BOT_PASSWORD= \
    BOT_GROUP_ID=

# Run the following commands as privileged user
USER root

WORKDIR /install

COPY requirements.txt .

RUN \
    echo "Installing Miscellaneous Packages" \
        && apt-get update \
        && apt-get install -y \
            python3-distutils \
            python3-venv \ 
            python3-dev \
        && \
    echo "Installing Python Requirements" \
        && wget https://bootstrap.pypa.io/get-pip.py \
        && python3 get-pip.py \
        && pip3 install -r requirements.txt \
        && \
    echo "Cleaning Up Mess" \
        && rm get-pip.py && rm requirements.txt

#===================================================
# Application Builder Image
#===================================================
FROM base as builder

# Copy application files
WORKDIR /app

COPY fb_poster .

RUN \
    echo "Creating Log Contents" \
        && mkdir -m755 logs \
        && touch /app/logs/FBPostLogging.log \
        && chmod 777 /app/logs/FBPostLogging.log

EXPOSE 5000

#===================================================
# Debug Image
#===================================================
FROM builder as debug

RUN pip3 install -U debugpy

CMD ["/app/entry_point.sh", "debug"]

EXPOSE 5678
EXPOSE 7900

#===================================================
# Release Image
#===================================================
FROM builder as release

# Run the following commands as non-privileged user
USER 1200:1201

CMD /app/entry_point.sh