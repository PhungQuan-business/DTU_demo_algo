# tạo container để chạy RS
# đẩy code vào folder
# viết API
# docker build + Dockerfile để tạo image
# docker run để tạo container

# File này đã bị move sang folder mới nên cần sửa lại đường dẫn


FROM python:3.10.13-bullseye

#change directory
WORKDIR /usr/app/src

RUN mkdir DTU_code && cd DTU_code

COPY ./requirements.txt  ./
RUN pip install -r requirements.txt

# copy all files from local to container directory
COPY . ./

# CMD ["python3", "-m", 'flask', 'run', '--host=0.0.0.0']
CMD ["python3", "surpriseRS.py"]