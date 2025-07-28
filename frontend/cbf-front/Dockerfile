# --- Estágio de Build ---
FROM node:18 AS build-stage

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# --- Estágio de Produção ---
FROM nginx:stable-alpine AS production-stage

# Copia os ficheiros compilados
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Remove a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia a nossa nova configuração de SPA
COPY nginx.conf /etc/nginx/conf.d

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]