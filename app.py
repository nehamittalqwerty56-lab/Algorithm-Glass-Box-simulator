import streamlit as st
import time
import heapq

st.set_page_config(page_title="GlassBox Simulator", layout="centered")

st.title("🔍 GlassBox Simulator")
st.subheader("BFS vs DFS vs A* Search Visualization")

st.write("This simulator visualizes how different search algorithms "
         "explore the same problem space step by step.")

GRID_SIZE = 6
START = (0, 0)
GOAL = (5, 5)

speed = st.slider("Animation Speed (seconds)", 0.1, 1.0, 0.5)
algorithm = st.selectbox("Select Algorithm", ["BFS", "DFS", "A*"])


# ---------- Grid Display ----------
def draw_grid(visited):
    grid = []
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            if (i, j) == START:
                row.append("🟦")
            elif (i, j) == GOAL:
                row.append("🟥")
            elif (i, j) in visited:
                row.append("🟩")
            else:
                row.append("⬜")
        grid.append(" ".join(row))
    return "\n".join(grid)


# ---------- Neighbors ----------
def get_neighbors(node):
    x, y = node
    moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [(i, j) for i, j in moves
            if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE]


# ---------- BFS ----------
def bfs():
    queue = [START]
    visited = set([START])
    order = []

    while queue:
        node = queue.pop(0)
        order.append(node)
        if node == GOAL:
            break
        for neighbor in get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


# ---------- DFS ----------
def dfs():
    stack = [START]
    visited = set([START])
    order = []

    while stack:
        node = stack.pop()
        order.append(node)
        if node == GOAL:
            break
        for neighbor in get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    return order


# ---------- A* ----------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar():
    pq = []
    heapq.heappush(pq, (0, START))
    visited = set()
    order = []

    while pq:
        _, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        order.append(node)

        if node == GOAL:
            break

        for neighbor in get_neighbors(node):
            if neighbor not in visited:
                priority = heuristic(neighbor, GOAL)
                heapq.heappush(pq, (priority, neighbor))
    return order


# ---------- Run ----------
if st.button("Run Algorithm"):
    if algorithm == "BFS":
        steps = bfs()
    elif algorithm == "DFS":
        steps = dfs()
    else:
        steps = astar()

    visited = []
    placeholder = st.empty()

    for step in steps:
        visited.append(step)
        placeholder.text(draw_grid(visited))
        time.sleep(speed)

    st.success(f"✅ Goal reached using {algorithm}")
st.markdown("""
🟦 **Start** &nbsp;&nbsp;
🟥 **Goal** &nbsp;&nbsp;
🟩 **Visited** &nbsp;&nbsp;
⬜ **Unvisited**
""")