from flask import request, render_template
from config import *
import wiz

PORT = config["port"]
BULBS = config["bulbs"]


def wiz_bulb(id: int):
    bulb = BULBS[id]
    bulb = wiz.WiZ(ip=bulb["ip"], port=bulb["port"], name=bulb["name"])
    return bulb


@flaskapp.route("/", methods=["GET", "POST"])
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


@flaskapp.route("/change", methods=["GET", "POST"])
def change_bulb():
    bulb_id = int(request.form.get("bulb-id"))
    bulb = wiz_bulb((bulb_id))

    return bulb.status


@flaskapp.route("/toggle", methods=["GET", "POST"])
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


@flaskapp.route("/temp", methods=["GET", "POST"])
def temp():
    if request.method == "POST":
        bulb_id = int(request.form.get("bulb-id"))
        temp = int(request.form.get("temperature"))
        dimming = int(request.form.get("brightness"))

        bulb = wiz_bulb(bulb_id)
        bulb.set_temperature(temp=temp, dimming=dimming)

        return bulb.status


@flaskapp.route("/scene", methods=["GET", "POST"])
def scene():
    if request.method == "POST":
        bulb_id = int(request.form.get("bulb-id"))
        scene_id = int(request.form.get("scene-id"))
        dimming = int(request.form.get("brightness"))
        speed = int(request.form.get("speed"))

        bulb = wiz_bulb(bulb_id)
        bulb.set_scene(scene_id=scene_id, speed=speed, dimming=dimming)

        return bulb.status


@flaskapp.route("/rgb", methods=["GET", "POST"])
def colors():
    if request.method == "POST":
        bulb_id = int(request.form.get("bulb-id"))
        color = request.form.get("color").lstrip("#")
        dimming = int(request.form.get("brightness"))

        red, green, blue = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
        bulb = wiz_bulb(bulb_id)
        bulb.set_rgb(red=red, green=green, blue=blue, dimming=dimming)

        return bulb.status


def run_prod_server():
    from waitress import serve

    print(NAMEVER)
    print(f"🚀 App is running at http://{HOST}:{PORT}")
    serve(flaskapp, host=HOST, port=PORT)


def run_dev_server():
    flaskapp.run(host=HOST, port=PORT, use_reloader=True, debug=True)


if __name__ == "__main__":
    run_dev_server()
