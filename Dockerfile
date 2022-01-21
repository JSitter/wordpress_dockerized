FROM webdevops/php-apache:7.3
RUN apt-get update && apt-get upgrade -y && apt-get install -y git libpng-dev
COPY ./wp-core/ /app
WORKDIR /app/
