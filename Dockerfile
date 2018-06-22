FROM python:3.6-slim

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list

RUN apt-get update \
    && apt-get install -y git cmake gcc build-essential libglib2.0-0 libsm6 libxrender-dev

# Add files in current dir to container
COPY . /home/FaceEye/

# Install project dependences
RUN cd /home/FaceEye \
    && pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

# Clean
RUN apt-get remove -y git cmake gcc build-essential

# Add user
RUN useradd face \
    && chown -R face:face /home/FaceEye

# Run app
CMD uwsgi /home/FaceEye/face_eye/face_eye_uwsgi.ini