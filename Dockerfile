# Light image — four belts (White to Blue) / 110 challenges. python3 only (YAML vendored).
# Build: docker build -t pi-sdr-academy .
# Run:   docker run --rm -p 8080:8080 pi-sdr-academy

FROM python:3.12-alpine

WORKDIR /app

# Alpine's built-in vi is the editor here (vim is not in the base image and the
# build stays offline). run.sh switches to vim automatically where it exists.

# Prefer vendored pure-Python YAML (no pip on closed networks).
COPY vendor/yaml /app/vendor/yaml
COPY platform/academy ./academy
COPY curriculum ./curriculum
COPY run.sh ./run.sh

ENV PYTHONPATH=/app/vendor:/app \
    ACADEMY_CURRICULUM=/app/curriculum \
    ACADEMY_DATA=/data \
    ACADEMY_WORKSPACE=/challenge \
    ACADEMY_FLAG_PATH=/data/flag.txt \
    HOST=0.0.0.0 \
    PORT=8080 \
    EDITOR=vi \
    VISUAL=vi \
    GIT_EDITOR=vi \
    SUDO_EDITOR=vi

RUN mkdir -p /data /challenge && chmod +x /app/run.sh

EXPOSE 8080
VOLUME ["/data", "/challenge"]

CMD ["./run.sh"]
