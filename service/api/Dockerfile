FROM nginx:1.21.6-alpine
RUN apk update && apk upgrade
RUN apk add python3 
RUN apk add py3-pip
RUN pip install --upgrade pip
Run pip install flask
RUN pip install flask-restful
RUN pip install flask-cors

WORKDIR /var/www/api/