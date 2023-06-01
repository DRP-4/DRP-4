FROM alpine:latest
RUN apk add --no-cache npm
COPY . .
RUN npm install
ENTRYPOINT ["npm run build"]
