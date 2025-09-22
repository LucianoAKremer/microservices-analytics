FROM node:20
WORKDIR /usr/src/app
COPY app/ ./app/
COPY package*.json ./
RUN npm install
EXPOSE 8001
CMD ["node", "app/main.js"]

