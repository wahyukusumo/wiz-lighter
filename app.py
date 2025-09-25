import socket
from flask import Flask, request, render_template, render_template_string
from flask_cors import CORS

VERSION = 0.1
APP_NAME = f"WiZ Light'er v.{VERSION}"
DEBUG = True
HOST = "0.0.0.0"
PORT = 5080

# instantiate the app
app = Flask(APP_NAME)
app.config.from_object(__name__)


# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


def send_udp(udp_ip: str, udp_port: int, message: str) -> None:
    """Send UDP packet to ip:port"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message.encode("utf-8"), (udp_ip, udp_port))
    finally:
        sock.close()


@app.route("/", methods=["GET", "POST"])
def index():
    bulbs = [
        {"id": 0, "name": "Bedroom Bulb", "ip": "192.168.0.185", "port": 38899},
        {"id": 1, "name": "Outside Bulb", "ip": "192.168.0.185", "port": 38899},
    ]

    if request.method == "POST":
        bulb_id = int(request.form.get("id"))
        bulb_state = request.form.get("feature")
        bulb_brightness = int(request.form.get("brightness"))
        bulb_speed = int(request.form.get("speed"))
        bulb_temperature = int(request.form.get("temperature"))

        bulb = next((b for b in bulbs if b["id"] == bulb_id), None)
        packet = f'{{"id": 1, "method": "setPilot", "params": {{"temp": {bulb_temperature}, "dimming": {bulb_brightness}}}}}'
        print(f"{bulb["ip"]}:{bulb["port"]} with message: {str(packet)}")

        send_udp(bulb["ip"], bulb["port"], str(packet))
        return "", 204

    else:
        return render_template("index.html", bulbs=bulbs, version=VERSION)


def run_prod_server():
    from waitress import serve

    print(f"Remote Windows Volume Control v.{VERSION}")
    print(f"✅ App is running at http://{HOST}:{PORT}")
    serve(app, host=HOST, port=PORT)


def run_dev_server():
    app.run(host=HOST, port=PORT, use_reloader=True, debug=DEBUG)


if __name__ == "__main__":
    run_dev_server()
