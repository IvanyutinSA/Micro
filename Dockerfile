# Init shit
FROM python:3.13
WORKDIR /usr/local/app

# Manage dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy everything else
COPY src ./src
COPY test_utils ./test_utils
COPY tests ./tests
COPY main.py ./
COPY .env .env

# prepare to execution
RUN useradd app
USER app

# execute
# CMD [ "env", "PYTHONPATH=$PWD", "python", "test_utils/run.py" ]
CMD [ "python", "main.py" ]
