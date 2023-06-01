FROM alpine:latest
RUN apk add --no-cache npm
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
CMD ["npm", "run", "dev"]
