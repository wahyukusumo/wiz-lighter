import json
import socket

# status_return = {
#     "method": "getPilot",
#     "env": "pro",
#     "result": {
#         "mac": "ccccccxxxx",
#         "rssi": -55,
#         "state": true,
#         "sceneId": 0,
#         "temp": 6200,
#         "dimming": 40,
#     },
# }

get_status = '{"method": "getPilot", "params": {}}'
turn_off = '{"id":1,"method":"setState","params":{"state":false}}'
turn_off = '{"id":1,"method":"setState","params":{"state":true}}'
temperature = {"id": 1, "method": "setPilot", "params": {"temp": 6200, "dimming": 40}}

SCENES = [
    {"id": 6, "name": "Cozy", "type": "static"},
    {"id": 11, "name": "Warm White", "type": "static"},
    {"id": 12, "name": "Daylight", "type": "static"},
    {"id": 13, "name": "Cool White", "type": "static"},
    {"id": 14, "name": "Night Light", "type": "static"},
    {"id": 15, "name": "Focus", "type": "static"},
    {"id": 16, "name": "Relax", "type": "static"},
    {"id": 17, "name": "True Colors", "type": "static"},
    {"id": 18, "name": "TV Time", "type": "static"},
    {"id": 19, "name": "Plant Growth", "type": "static"},
    {"id": 9, "name": "Wake Up", "type": "static"},
    {"id": 10, "name": "Bedtime", "type": "static"},
    {"id": 1000, "name": "Rhythm", "type": "static"},
    {"id": 1, "name": "Ocean", "type": "dynamic"},
    {"id": 2, "name": "Romance", "type": "dynamic"},
    {"id": 3, "name": "Sunset", "type": "dynamic"},
    {"id": 4, "name": "Party", "type": "dynamic"},
    {"id": 5, "name": "Fireplace", "type": "dynamic"},
    {"id": 7, "name": "Forest", "type": "dynamic"},
    {"id": 8, "name": "Pastel Colors", "type": "dynamic"},
    {"id": 20, "name": "Spring", "type": "dynamic"},
    {"id": 21, "name": "Summer", "type": "dynamic"},
    {"id": 22, "name": "Fall", "type": "dynamic"},
    {"id": 23, "name": "Deepdive", "type": "dynamic"},
    {"id": 24, "name": "Jungle", "type": "dynamic"},
    {"id": 25, "name": "Mojito", "type": "dynamic"},
    {"id": 26, "name": "Club", "type": "dynamic"},
    {"id": 27, "name": "Christmas", "type": "dynamic"},
    {"id": 28, "name": "Halloween", "type": "dynamic"},
    {"id": 29, "name": "Candlelight", "type": "dynamic"},
    {"id": 30, "name": "Golden white", "type": "dynamic"},
    {"id": 31, "name": "Pulse", "type": "dynamic"},
    {"id": 32, "name": "Steampunk", "type": "dynamic"},
]


class WiZ:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name
        self.timeout = 4.0

    def result(self, result: dict) -> bool:
        return result["result"]["success"]

    @property
    def status(self) -> dict:
        params = {"method": "getPilot", "params": {}}
        return self.send_udp(params)

    @property
    def turn_off(self) -> dict:
        params = {"id": 1, "method": "setState", "params": {"state": False}}
        return self.send_udp(params)

    @property
    def turn_on(self) -> dict:
        params = {"id": 1, "method": "setState", "params": {"state": True}}
        return self.send_udp(params)

    def set_state(self, state: bool) -> dict:
        params = {"id": 1, "method": "setState", "params": {"state": state}}
        return self.send_udp(params)

    def set_temperature(self, temp: int, dimming: int = 30) -> dict:
        params = {"temp": temp, "dimming": dimming}
        return self.generate_code(params)

    def set_scene(
        self, scene_id: int, speed: int | None = None, dimming: int = 30
    ) -> dict:
        scene = next((scene for scene in SCENES if scene["id"] == scene_id), None)
        params = {"sceneId": scene_id, "dimming": dimming}

        if scene["type"] == "dynamic":
            params["speed"] = speed

        return self.generate_code(params)

    def set_rgb(self, red: int, green: int, blue: int, dimming: int = 30) -> dict:
        params = {"r": red, "g": green, "b": blue, "dimming": dimming}
        return self.generate_code(params)

    def generate_code(self, params: dict) -> dict:
        params = {"id": 1, "method": "setPilot", "params": params}
        return self.send_udp(params)

    def send_udp(self, command: dict) -> dict | None:
        command = json.dumps(command).encode("utf-8")

        """Send UDP packet to ip:port"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)
        try:
            # Send UDP packet
            sock.sendto(command, (self.ip, self.port))
            # Retrieve data from device
            data, addr = sock.recvfrom(1024)
            message = json.loads(data.decode("utf-8"))
            return message
        except socket.timeout:
            return {
                "method": "setPilot",
                "id": 1,
                "env": "pro",
                "result": {"success": False},
            }
        finally:
            sock.close()


def main():
    lamp = WiZ("192.168.0.185", 38899, "Bedroom Bulb")
    # lamp = WiZ("192.168.0.182", 38822, "Bedroom Bulb")
    temp = lamp.set_scene(scene_id=14, speed=10, dimming=50)
    print(temp)
    # lamp.turn_off
    # print(lamp.status)


if __name__ == "__main__":
    main()
