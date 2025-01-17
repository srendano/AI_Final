configuration = {
"text_size": 300,
"tile_size": 80,
"type": "load", #random
"seed": None,
"file": "./student/map2a.txt",
"map_size": [11, 6],
"delay": 0.1,
"debugMap": False,
"debug": False,
"save": False, #True
"hazards": False,
"basicTile": "street",
"maxBags": 2,
"agent":{
    "graphics":{
        "default": "game/graphics/logistics/deliver103.jpg"
        },
    "id": "agent",
    "marker": 'A',
    "start": [0,0],
    },
"maptiles": {
    "street": {
        "graphics":{
            "default": "game/graphics/logistics/street101.jpg",
            "traversed": "game/graphics/logistics/street101Traversed.jpg"
            },
        "id":  "street",
        "marker": 'T',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1},
        },
    "pizza": {
        "graphics":{
            "default": "game/graphics/logistics/pizza101.jpg",
            "traversed": "game/graphics/logistics/pizza101.jpg"
            },
        "id":  "pizza",
        "marker": 'Z',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1},
        },
    "customer0": {
        "graphics":{
            "default": "game/graphics/logistics/customer100.png",
            "traversed": "game/graphics/logistics/customer100.png"
            },
        "id":  "customer0",
        "marker": '0',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "unload": True, "objects": 0},
        },
    "customer1": {
        "graphics":{
            "default": "game/graphics/logistics/customer100_1.png",
            "traversed": "game/graphics/logistics/customer100_1.png"
            },
        "id":  "customer1",
        "marker": '1',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "unload": True, "objects": 1},
        },
    "customer2": {
        "graphics":{
            "default": "game/graphics/logistics/customer100_2.png",
            "traversed": "game/graphics/logistics/customer100_2.png"
            },
        "id":  "customer2",
        "marker": '2',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "unload": True, "objects": 2},
        },
    "customer3": {
        "graphics":{
            "default": "game/graphics/logistics/customer100_3.png",
            "traversed": "game/graphics/logistics/customer100_3.png"
            },
        "id":  "customer3",
        "marker": '3',
        "num": 3,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "unload": True, "objects": 3},
        },
    "start": {
        "graphics":{
            "default": "game/graphics/logistics/base101.png",
            "traversed": "game/graphics/logistics/base101.png"
            },
        "id":  "start",
        "marker": 'W',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1},
        },
    "building": {
        "graphics":{
            "default": "game/graphics/logistics/building102.jpg",
            "traversed": "game/graphics/logistics/building102.jpg"
            },
        "id":  "building",
        "marker": 'X',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "blocked": True},
        }
    }
}
