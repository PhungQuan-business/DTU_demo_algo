# tạo container để chạy RS
# đẩy code vào folder
# viết API
# docker build + Dockerfile để tạo image
# docker run để tạo container

FROM python:3.10.13-bullseye

WORKDIR /usr/app/src

RUN mkdir DTU_code && cd DTU_code
COPY . ./
RUN pip install -r requirements.txt

CMD ["python3", "surpriseRS.py"]