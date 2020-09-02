FROM nginx

RUN mkdir -p /etc/ssl/certs
RUN mkdir -p /var/run/nginx
RUN rm /etc/nginx/conf.d/default.conf
RUN rm /etc/nginx/nginx.conf
COPY proxy.conf /etc/nginx
COPY nginx.conf /etc/nginx
COPY default.conf /etc/nginx/conf.d
