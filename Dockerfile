FROM python:3.10
# Python docker images: https://github.com/docker-library/docs/tree/master/python/

USER root

# Copy the src
WORKDIR /app
COPY website/ /app/website/
COPY ./requirements.txt /app
COPY ./.env /app
COPY ./main.py /app

RUN ls -la /app

# Install python dependencies
RUN python3 --version
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /app/requirements.txt
RUN pip3 list --format=columns

USER 1001

EXPOSE 5000
ENTRYPOINT ["flask", "--app", "main", "run", "--host", "0.0.0.0"]