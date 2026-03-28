# Init shit
FROM python:3.13
WORKDIR /usr/local/app

# preinstall
RUN apt-get update
RUN apt-get install -y curl
ENV PYTHONPATH=/usr/local/app

# Manage dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy everything else
COPY ./test_utils ./test_utils
COPY ./tests ./tests
COPY src ./src
COPY .env .env
COPY api-keys api-keys

# prepare to execution
RUN useradd app
USER app

# execute
CMD [ "python", "./src/main.py" ]
# CMD [ "python" , "test_utils/run.py"]
