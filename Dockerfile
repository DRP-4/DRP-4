FROM alpine:latest
# Install the (non-python) dependencies
RUN apk add --no-cache npm python3-dev py3-pip py3-virtualenv
# Setup the user `npc` for the server
RUN adduser -D npc
USER npc
WORKDIR /home/npc
# Setup venv
RUN virtualenv venv
ENV VIRTUAL_ENV=/home/npc/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Setup app directory
RUN mkdir /home/npc/app
WORKDIR /home/npc/app
# Install python backend dependencies
COPY --chown=npc api/requirements.txt api/requirements.txt
RUN pip3 install -r api/requirements.txt
# Install frontend dependencies
COPY --chown=npc package.json package-lock.json ./
RUN npm install
# Copy the source over (subject to .dockerignore)
COPY --chown=npc . .
# Build the frontend
RUN npm run build
# Start the server
WORKDIR /home/npc/app/api
CMD ["/bin/sh", "-c", "flask run --host=0.0.0.0 --port=$PORT"]
