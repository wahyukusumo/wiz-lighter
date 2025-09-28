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

static_mode = [
    {"id": 6, "name": "Cozy"},
    {"id": 11, "name": "Warm White"},
    {"id": 12, "name": "Daylight"},
    {"id": 13, "name": "Cool White"},
    {"id": 14, "name": "Night Light"},
    {"id": 15, "name": "Focus"},
    {"id": 16, "name": "Relax"},
    {"id": 17, "name": "True Colors"},
    {"id": 18, "name": "TV Time"},
    {"id": 19, "name": "Plant Growth"},
    {"id": 9, "name": "Wake Up"},
    {"id": 10, "name": "Bedtime"},
    {"id": 1000, "name": "Rhythm"},
]

dynamics_mode = [
    {"id": "1", "name": "Ocean"},
    {"id": "2", "name": "Romance"},
    {"id": "3", "name": "Sunset"},
    {"id": "4", "name": "Party"},
    {"id": "5", "name": "Fireplace"},
    {"id": "7", "name": "Forest"},
    {"id": "8", "name": "Pastel Colors"},
    {"id": "20", "name": "Spring"},
    {"id": "21", "name": "Summer"},
    {"id": "22", "name": "Fall"},
    {"id": "23", "name": "Deepdive"},
    {"id": "24", "name": "Jungle"},
    {"id": "25", "name": "Mojito"},
    {"id": "26", "name": "Club"},
    {"id": "27", "name": "Christmas"},
    {"id": "28", "name": "Halloween"},
    {"id": "29", "name": "Candlelight"},
    {"id": "30", "name": "Golden white"},
    {"id": "31", "name": "Pulse"},
    {"id": "32", "name": "Steampunk"},
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

    def set_temperature(self, temp: int, dimming: int) -> dict:
        params = {"temp": temp, "dimming": dimming}
        return self.generate_code(params)

    def set_scene(self, sceneId: int, speed: int | None, dimming: int) -> dict:
        params = {"sceneId": sceneId, "dimming": dimming}

        if speed:  # only add if not None / not 0
            params["speed"] = speed

        return self.generate_code(params)

    def set_rgb(self, red: int, green: int, blue: int, dimming: int) -> dict:
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


lamp = WiZ("192.168.0.185", 38899, "Bedroom Bulb")
# lamp = WiZ("192.168.0.182", 38822, "Bedroom Bulb")
# temp = lamp.set_rgb(3, 3, 4, 10)
print(lamp.status)
