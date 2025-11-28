from flask import Flask, send_from_directory, request, Response
import requests

app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/')
def index():
    return send_from_directory('.', 'webapp.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)


@app.route('/predict', methods=['POST'])
def proxy_predict():
    # Forward the JSON body to the model API running on localhost:5000
    try:
        resp = requests.post('http://localhost:5000/predict', json=request.get_json(), timeout=30)
    except requests.exceptions.RequestException:
        return Response('{"error": "upstream request failed"}', status=502, content_type='application/json')

    return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('Content-Type', 'application/json'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
