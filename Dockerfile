FROM alpine:latest
RUN apk add --no-cache npm python3 py3-pip
WORKDIR /app
COPY api/requirements.txt api/requirements.txt
RUN pip3 install -r api/requirements.txt
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build
RUN mv dist /www
WORKDIR /app/api
CMD ["/bin/sh", "-c", "python -m flask run --host=0.0.0.0 --port=$PORT"]
