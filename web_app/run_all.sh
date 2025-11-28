#!/usr/bin/env bash
set -euo pipefail

# run_all.sh - helper to build the Docker API, run the container,
# and start the local Flask proxy server that serves the web UI.

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATASETS_DIR="$ROOT_DIR/.."/datasets

IMAGE_NAME="sentiment-api"
CONTAINER_NAME="sentiment-api-container"

function usage() {
  echo "Usage: $0 {start|stop|rebuild|status}" >&2
  exit 1
}

if [ $# -lt 1 ]; then
  usage
fi

cmd="$1"

case "$cmd" in
  start)
    echo "Building Docker image..."
    cd "$DATASETS_DIR"
    docker build -t "$IMAGE_NAME" .

    echo "Starting container (removes any existing container named $CONTAINER_NAME)..."
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker run -d --name "$CONTAINER_NAME" -p 5000:5000 "$IMAGE_NAME"

    echo "Installing Python deps (venv recommended)..."
    python3 -m pip install --user flask requests || true

    echo "Starting local Flask server (serves web_app and proxies /predict)..."
    # run in background and log to file
    nohup python3 "$ROOT_DIR/run_local.py" > "$ROOT_DIR/run_local.log" 2>&1 &
    echo "run_local.py started (logs -> $ROOT_DIR/run_local.log)"
    ;;

  stop)
    echo "Stopping local Flask server..."
    pkill -f "run_local.py" || true
    echo "Stopping and removing Docker container $CONTAINER_NAME..."
    docker rm -f "$CONTAINER_NAME" || true
    ;;

  rebuild)
    echo "Rebuilding image and restarting container..."
    cd "$DATASETS_DIR"
    docker build -t "$IMAGE_NAME" .
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker run -d --name "$CONTAINER_NAME" -p 5000:5000 "$IMAGE_NAME"
    ;;

  status)
    docker ps --filter "name=$CONTAINER_NAME"
    if pgrep -f "run_local.py" >/dev/null; then
      echo "run_local.py running"
    else
      echo "run_local.py not running"
    fi
    ;;

  *)
    usage
    ;;
esac
