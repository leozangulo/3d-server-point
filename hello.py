from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit

import numpy as np
from boid import Boid

app = Flask(__name__, static_url_path='')


    
def updatePositions(flock):
    positions = []
    for boid in flock:
        boid.apply_behaviour(flock)
        boid.update()
        pos = boid.edges()
        positions.append(pos)
    return positions

def positionsToJSON(ps):
    posDICT = []
    for p in ps:
        pos = {
            "x" : p[0],
            "z" : p[1],
            "y" : p[2]
        }
        posDICT.append(pos)
    print(posDICT)
    return json.dumps(posDICT)


# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return jsonify([{"message":"Forbidden"}])

@app.route('/api/points', methods=['GET'])
def get_visitor():
    # Size of the board:
    width = 30
    height = 30

    # Set the number of agents here:
    flock = [Boid(*np.random.rand(2)*30, width, height) for _ in range(20)]

    positions = updatePositions(flock)
    return positionsToJSON(positions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
