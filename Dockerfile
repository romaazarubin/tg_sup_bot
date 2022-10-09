FROM python:3.8

# set a directory for the app

WORKDIR /Desktop/project_working/tg_sup_bot

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#RUN alembic upgrade head
# tell the port number the container should expose
#RUN --add-host=host.docker.internal:host-gateway

EXPOSE 5000

# run the command
CMD ["python", "videoblog/main.py"]

RUN alembic upgrade head