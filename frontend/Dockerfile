FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html

# nginx:alpine procesa /etc/nginx/templates/*.template con envsubst al arrancar.
# El filtro limita la sustitución a BACKEND_URL, para que no toque las variables
# propias de nginx ($uri, $host, $remote_addr).
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
ENV NGINX_ENVSUBST_FILTER="BACKEND_URL"
ENV BACKEND_URL="http://backend:8000"

EXPOSE 80
