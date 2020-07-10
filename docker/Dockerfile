FROM python:3.7
MAINTAINER Alexander Koritskiy <koritskiy@informatics.ru>
ADD ./ /orrangeit_app
WORKDIR /orrangeit_app/
CMD exec apt-get update
CMD exec apt-get install build-essential nano python3-dev libmysqlclient-dev
RUN pip install --no-cache-dir -r ./requirements.txt
CMD exec ./docker/run.sh
