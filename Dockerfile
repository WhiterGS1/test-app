FROM public.ecr.aws/nginx/nginx:alpine
COPY index.html /usr/share/nginx/html/
RUN echo 'server { listen 80; location /nginx_status { stub_status on; access_log off; } location / { root /usr/share/nginx/html; index index.html; } }' > /etc/nginx/conf.d/default.conf
EXPOSE 80