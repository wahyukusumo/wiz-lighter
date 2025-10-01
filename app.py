from flask import Flask, request, render_template
from flask_cors import CORS
import wiz
import yaml

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


# Open the YAML file in read mode
with open("config.yaml", "r") as file:
    data = yaml.safe_load(file)

BULBS = data["bulbs"]


def wiz_bulb(id: int):
    bulb = BULBS[id]
    bulb = wiz.WiZ(ip=bulb["ip"], port=bulb["port"], name=bulb["name"])
    return bulb


@app.route("/", methods=["GET", "POST"])
def index():

    bulb = wiz_bulb(0)
    status = bulb.status

    return render_template(
        "index.jinja-html",
        bulbs=BULBS,
        status=status,
        scenes=wiz.SCENES,
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
        # bulb_state = True if request.form.get("toggle") == "on" else False

        bulb = wiz_bulb(bulb_id)
        status = bulb.status
        if status["result"]["state"]:
            bulb.set_state(False)
        else:
            bulb.set_state(True)

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
        speed = int(request.form.get("speed"))

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
