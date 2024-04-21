# tạo container để chạy RS
# đẩy code vào folder
# viết API
# docker build + Dockerfile để tạo image
# docker run để tạo container

FROM python:3.9-alpine
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./flask_api.py .
EXPOSE 5000
CMD ["python", "flask_api.py"]
