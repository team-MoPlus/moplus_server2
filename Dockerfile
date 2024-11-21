#
FROM python:3.10

#
WORKDIR /code

#
COPY requirements.txt ./

#
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#
COPY . .

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
