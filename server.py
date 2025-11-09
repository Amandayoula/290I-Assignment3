from fastapi import FastAPI, File, UploadFile
import uvicorn
from utils import *
from dijkstra import dijkstra
import numpy as np

# create FastAPI app
app = FastAPI()

# global variable for active graph
active_graph = None

@app.get("/")
async def root():
    return {"message": "Welcome to the Shortest Path Solver!"}


@app.post("/upload_graph_json")
async def create_upload_file(file: UploadFile):
    # Check if file is a JSON file
    if file.filename is None or not file.filename.endswith('.json'):
        return {"Upload Error": "Invalid file type"}
    
    try:
        global active_graph
        active_graph = create_graph_from_json(file)
        return {"Upload Success": file.filename}
    except Exception as e:
        return {"Upload Error": "Invalid file type"}


@app.get("/solve_shortest_path")
async def get_shortest_path(starting_node_id: str, end_node_id: str):
    global active_graph
    
    # Check if no graph has been uploaded
    if active_graph is None:
        return {"Solver Error": "No active graph, please upload a graph first."}
    
    # Check if start or end node ID exists in the graph
    if starting_node_id not in active_graph.nodes or end_node_id not in active_graph.nodes:
        return {"Solver Error": "Invalid start or end node ID."}
    
    # Get start and end nodes
    start_node = active_graph.nodes[starting_node_id]
    end_node = active_graph.nodes[end_node_id]
    
    dijkstra(active_graph, start_node)
    
    path = []
    current_node = end_node
    
    if end_node.dist == np.inf:
        return {"shortest_path": None, "total_distance": None}
    
    while current_node is not None:
        path.insert(0, current_node.id)
        current_node = current_node.prev
    
    total_distance = end_node.dist
    
    return {"shortest_path": path, "total_distance": total_distance}

if __name__ == "__main__":
    print("Server is running at http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
    