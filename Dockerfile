FROM python:3.10-buster

# Create workdir repository
WORKDIR /mdm_test

# Copy requirements file in the workdir repository
COPY requirements.txt .

# Install project requirements
RUN pip install -r requirements.txt

# Copy project files in the workdir repository
COPY api/ api/
COPY rps/ rps/
COPY tests/ tests/
COPY main.py .

RUN python -m unittest discover -s tests/ -p 'test_*.py'

CMD python main.py --host $WEB_APP_HOST --port $WEB_APP_PORT --debug $DEBUG