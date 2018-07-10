#!/bin/bash

chmod +x /mnt/wait-for-it.sh

bash /mnt/wait-for-it.sh --timeout=5 -h mysql2redis -p 3306

until [[ $? == 0 ]]; do
  >&2 echo "database face_eye doesn't exist, waiting"
  bash /mnt/wait-for-it.sh --timeout=5 -h mysql2redis -p 3306
done

python /home/FaceEye/manage.py makemigrations
python /home/FaceEye/manage.py migrate
uwsgi /home/FaceEye/face_eye/face_eye_uwsgi.ini
