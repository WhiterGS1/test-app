# Backend stage
FROM public.ecr.aws/docker/library/python:3.9-slim as backend
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend.py .
EXPOSE 5000
CMD ["python", "backend.py"]

# Frontend stage
FROM public.ecr.aws/nginx/nginx:alpine as frontend
COPY index.html /usr/share/nginx/html/
RUN echo -e 'server {\n  listen 80;\n  location /nginx_status {\n    stub_status on;\n    access_log off;\n  }\n  location /api/ {\n    proxy_pass http://backend-service:5000/;\n  }\n  location / {\n    root /usr/share/nginx/html;\n    index index.html;\n  }\n}' > /etc/nginx/conf.d/default.conf
EXPOSE 80