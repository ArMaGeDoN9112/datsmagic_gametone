from matplotlib import pyplot as plt
from matplotlib.colors import BASE_COLORS

from RewindClient import RewindClient

a = RewindClient()
def draw_obj(obj, color, radius, mapSize, fill=False):
    mapSize = mapSize['x'] // 1000
    a.circle(obj.x / mapSize, obj.y / mapSize, radius / mapSize, color=color, fill=fill)

def draw_pop(obj, radius, mapSize, msg):
    mapSize = mapSize['x'] // 1000
    a.circle_popup(obj.x / mapSize, obj.y / mapSize, radius / mapSize, message=msg)

def make_msg(obj):
    a.message(msg=f"X: {obj.x}, Y: {obj.y}, {obj.health}")

def draw_line(obj, mapSize):
    mapSize = mapSize['x'] // 1000
    a.line(obj.x / mapSize, obj.y / mapSize,
           obj.x  / mapSize + obj.velocity["x"]  / mapSize + obj.selfAcceleration['x']  / mapSize,
           obj.y / mapSize + obj.velocity["y"] / mapSize + obj.selfAcceleration['y'] / mapSize,
           color=RewindClient.BLUE)
    a.line(obj.x / mapSize, obj.y / mapSize,
           obj.x  / mapSize + obj.selfAcceleration['x'],
           obj.y / mapSize + obj.selfAcceleration['y'],
           color=RewindClient.RED)
    a.line(obj.x / mapSize, obj.y / mapSize,
           obj.x / mapSize + obj.anomalyAcceleration['x'],
           obj.y / mapSize + obj.anomalyAcceleration['y'],
           color=RewindClient.DARK_RED)
