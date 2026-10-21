FROM ghcr.io/open-webui/open-webui:main

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# replace a file inside the image
#COPY ./main_open_webui.py /app/backend/open_webui/main.py