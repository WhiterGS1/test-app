FROM public.ecr.aws/nginx/nginx:alpine
COPY index.html /usr/share/nginx/html/
RUN echo -e 'server {\n  listen 80;\n  location /nginx_status {\n    stub_status on;\n    access_log off;\n  }\n  location / {\n    root /usr/share/nginx/html;\n    index index.html;\n  }\n}' > /etc/nginx/conf.d/default.conf
EXPOSE 80