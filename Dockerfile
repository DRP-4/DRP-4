FROM alpine:latest
# Install the (non-python) dependencies
RUN apk add --no-cache npm python3-dev py3-pip libpq-dev build-base
# Setup the user `npc` for the server
RUN adduser -D npc
USER npc
RUN mkdir /home/npc/app
WORKDIR /home/npc/app
ENV PATH="/home/npc/.local/bin:${PATH}"
# Install python backend dependencies
COPY --chown=npc api/requirements.txt api/requirements.txt
RUN pip3 install --user -r api/requirements.txt
# Install frontend dependencies
COPY --chown=npc package.json package-lock.json ./
RUN npm install
# Copy the source over (subject to .dockerignore and api/.dockerignore)
COPY --chown=npc . .
# Build the frontend
RUN npm run build
# Start the server
WORKDIR /home/npc/app/api
CMD ["/bin/sh", "-c", "flask run --host=0.0.0.0 --port=$PORT"]
