# Web app — run instructions

This folder contains the static UI (`webapp.html`) and a small helper `run_local.py` that serves the UI
and proxies `/predict` to the model API running in Docker.

Quick steps (recommended)

1. Build the model Docker image and run the container, then start the local Flask proxy + static server:

```bash
# from repo root
cd /workspaces/nolan_edutech_assignement/web_app
./run_all.sh start
```

This does three things:

- builds the Docker image from `../datasets` as `sentiment-api`
- runs the container `sentiment-api-container` exposing port `5000`
- starts `run_local.py` (Flask) which serves `webapp.html` on port `8000` and proxies `/predict` to `localhost:5000`

2. Open the UI in a browser:

```
http://localhost:8000/
```

3. Use the UI: enter `Review_Title` and `Review_Text` and click `Predict` — logs will animate and result will display.

Stop services

```bash
cd /workspaces/nolan_edutech_assignement/web_app
./run_all.sh stop
```

Rebuild only (rebuild image and restart container):

```bash
./run_all.sh rebuild
```

Check status:

```bash
./run_all.sh status
```

Notes and troubleshooting

- The helper script uses `python3 -m pip install --user flask requests` to ensure the local proxy has dependencies. It's recommended to run inside a virtualenv instead of `--user` if you prefer isolation.
- If you see `Prediction failed` in the UI, check the model API logs:
  ```bash
  docker logs -f sentiment-api-container
  tail -n 200 run_local.log
  ```
- If port `8000` or `5000` is already used, edit `run_all.sh` and `run_local.py` accordingly.
- For production, run the model API with a production WSGI server and serve the UI from a proper web server. The current setup is for local development/testing.

Want changes?
- I can make `run_all.sh` create and use a virtualenv, add `systemd` unit files, or produce a `docker-compose.yml` that runs both the API and a static web server together. Tell me which option you prefer.
