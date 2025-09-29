import socket
from flask import Flask, request, render_template, render_template_string
from flask_cors import CORS
import wiz

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


# HTML NAME
ID = "bulb-id"
TEMP = "temperature"
SPEED = "speed"
SCENE = "sceneId"

BULBS = [
    {"id": 0, "name": "Bedroom Bulb", "ip": "192.168.0.185", "port": 38899},
    {"id": 1, "name": "Outside Bulb", "ip": "192.163.0.185", "port": 40404},
]


def check_if_bulb_online():
    for bulb in BULBS:
        wiz = wiz_bulb[bulb["id"]]
        wiz.status


def wiz_bulb(id: int):
    bulb = BULBS[id]
    bulb = wiz.WiZ(ip=bulb["ip"], port=bulb["port"], name=bulb["name"])
    return bulb


@app.route("/", methods=["GET", "POST"])
def index():

    default_bulb = BULBS[0]
    bulb = wiz.WiZ(
        ip=default_bulb["ip"], port=default_bulb["port"], name=default_bulb["name"]
    )
    status = bulb.status

    if request.method == "POST":
        bulb_id = int(request.form.get("bulb-id"))
        bulb_brightness = int(request.form.get("brightness"))

        light_mode = request.form.get("lightMode")

        if light_mode == "mode-temp":
            bulb_temperature = int(request.form.get("temperature"))
            params = f'"temp": {bulb_temperature}, "dimming": {bulb_brightness}'

        if light_mode == "mode-scene":
            scene_type = request.form.get("sceneType")
            scene_id = int(request.form.get("sceneID"))

            if scene_type == "type-static":
                params = f'"sceneId":{scene_id},"dimming":{bulb_brightness}'
            elif scene_type == "type-dynamics":
                speed = int(request.form.get("speed"))
                params = (
                    f'"sceneId":{scene_id},"speed":{speed},"dimming":{bulb_brightness}'
                )

        packet = wiz.set_params(params)

        bulb = next((b for b in BULBS if b["id"] == bulb_id), None)
        # print(f"{bulb["ip"]}:{bulb["port"]} with message: {str(packet)}")
        print(packet)
        # send_udp(bulb["ip"], bulb["port"], str(packet))
        return "", 204

    else:
        return render_template(
            "index.html",
            bulbs=BULBS,
            status=status,
            dynamics=wiz.dynamics_mode,
            statics=wiz.static_mode,
            version=VERSION,
        )


@app.route("/change", methods=["GET", "POST"])
def change_bulb():
    bulb_id = int(request.form.get("bulb-id"))
    bulb = wiz_bulb((bulb_id))

    return bulb.status


@app.route("/toggle", methods=["GET", "POST"])
def toggle():
    if request.method == "POST":
        bulb_id = int(request.form.get("bulb-id"))
        bulb_state = True if request.form.get("toggle") == "on" else False

        bulb = wiz_bulb(bulb_id)
        bulb.set_state(bulb_state)

        # return "", 204
        return bulb.status


@app.route("/temp", methods=["GET", "POST"])
def temp():
    if request.method == "POST":
        bulb_id = int(request.form.get("bulb-id"))
        temp = int(request.form.get("temperature"))
        dimming = int(request.form.get("brightness"))

        bulb = wiz_bulb(bulb_id)
        bulb.set_temperature(temp=temp, dimming=dimming)

        return bulb.status


@app.route("/scene", methods=["GET", "POST"])
def scene():
    if request.method == "POST":
        bulb_id = int(request.form.get("bulb-id"))
        scene_id = int(request.form.get("scene-id"))
        dimming = int(request.form.get("brightness"))
        speed_form = request.form.get("speed")
        speed = int(speed_form) if speed_form not in (None, "") else None

        bulb = wiz_bulb(bulb_id)
        bulb.set_scene(scene_id=scene_id, speed=speed, dimming=dimming)

        return bulb.status


def run_prod_server():
    from waitress import serve

    print(APP_NAME)
    print(f"✅ App is running at http://{HOST}:{PORT}")
    serve(app, host=HOST, port=PORT)


def run_dev_server():
    app.run(host=HOST, port=PORT, use_reloader=True, debug=DEBUG)


if __name__ == "__main__":
    run_dev_server()
