FROM nginx

# Install php for Snipe-it
# Follows official Snipe-it Dockerfile: https://hub.docker.com/r/snipe/snipe-it/dockerfile
# Note that this Dockerfile dereives from Debian while the Snipe-it image uses Ubuntu
RUN apt-get update && apt-get install -y \
curl \
git \
gnupg2 \
supervisor \
wget

RUN wget -q https://packages.sury.org/php/apt.gpg -O- | apt-key add -
RUN echo "deb https://packages.sury.org/php/ buster main" | tee /etc/apt/sources.list.d/php.list

RUN apt-get install -y \
php7.3 \
php7.3-bcmath \
php7.3-cli \
php7.3-curl \
php7.3-fpm \
php7.3-gd \
php7.3-mbstring \
php7.3-mysql \
php7.3-xml \
php7.3-zip \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN useradd -m --uid 1000 --gid 50 docker

RUN phpenmod gd
RUN phpenmod bcmath

RUN sed -i 's/variables_order = .*/variables_order = "EGPCS"/' /etc/php/7.3/cli/php.ini

RUN git clone https://github.com/snipe/snipe-it /var/www/html

WORKDIR /var/www/html
RUN cp docker/docker.env /var/www/html/.env

RUN chown -R docker:www-data /var/www/html
RUN chmod -R g+w /var/www/html/storage

RUN \
	rm -r "/var/www/html/storage/private_uploads" && ln -fs "/var/lib/snipeit/data/private_uploads" "/var/www/html/storage/private_uploads" \
      && rm -rf "/var/www/html/public/uploads" && ln -fs "/var/lib/snipeit/data/uploads" "/var/www/html/public/uploads" \
      && rm -r "/var/www/html/storage/app/backups" && ln -fs "/var/lib/snipeit/dumps" "/var/www/html/storage/app/backups" \
      && mkdir -p "/var/lib/snipeit/keys" && ln -fs "/var/lib/snipeit/keys/oauth-private.key" "/var/www/html/storage/oauth-private.key" \
      && ln -fs "/var/lib/snipeit/keys/oauth-public.key" "/var/www/html/storage/oauth-public.key" \
      && chown docker "/var/lib/snipeit/keys/" \
      && chmod +x /var/www/html/artisan \
      && echo "Finished setting up application in /var/www/html"


############## DEPENDENCIES via COMPOSER ###################

#global install of composer
RUN cd /tmp;curl -sS https://getcomposer.org/installer | php;mv /tmp/composer.phar /usr/local/bin/composer

# Get dependencies
USER docker
RUN cd /var/www/html;composer install && rm -rf /home/docker/.composer/cache
USER root

VOLUME ["/var/lib/snipeit"]

############### APPLICATION INSTALL/INIT #################

#RUN php artisan app:install
# too interactive! Try something else

#COPY docker/app_install.exp /tmp/app_install.exp
#RUN chmod +x /tmp/app_install.exp
#RUN /tmp/app_install.exp

############### DATA VOLUME #################

VOLUME ["/var/lib/snipeit"]

##### START SERVER

RUN service php7.3-fpm start

COPY startup.sh /
COPY supervisord.conf /
COPY www.conf /etc/php/7.3/fpm/pool.d/
RUN cp docker/supervisor-exit-event-listener /usr/bin/supervisor-exit-event-listener
RUN chmod +x /startup.sh /usr/bin/supervisor-exit-event-listener

RUN mkdir -p /etc/ssl/certs
RUN rm /etc/nginx/conf.d/default.conf /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx
COPY intranet.conf /etc/nginx/conf.d

CMD ["/startup.sh"]
