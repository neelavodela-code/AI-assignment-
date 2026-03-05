"""
Missionaries and Cannibals Problem
====================================
Solve using BFS, DFS, and their variants:
  - BFS (Breadth-First Search)
  - DFS (Depth-First Search)
  - DFS with Depth Limit
  - Iterative Deepening DFS (IDDFS)

Problem Statement:
  3 Missionaries and 3 Cannibals are on the left bank of a river.
  A boat that holds at most 2 people must ferry all of them to the right bank.
  At no point (on either bank OR in the boat) can cannibals outnumber
  missionaries — unless there are zero missionaries on that side.

State: (missionaries_left, cannibals_left, boat_side)
  boat_side = 1 → boat is on the LEFT bank
  boat_side = 0 → boat is on the RIGHT bank

Goal: (0, 0, 0)  — everyone on the right bank
"""

from collections import deque
import time


# ─────────────────────────────────────────────────────────
# STATE REPRESENTATION & VALIDATION
# ─────────────────────────────────────────────────────────

INITIAL_STATE = (3, 3, 1)   # (M_left, C_left, boat_on_left)
GOAL_STATE    = (0, 0, 0)
TOTAL_M = 3
TOTAL_C = 3

# All possible moves: (missionaries_in_boat, cannibals_in_boat)
MOVES = [(1,0), (2,0), (0,1), (0,2), (1,1)]


def is_valid(state: tuple) -> bool:
    """Return True if the state satisfies all problem constraints."""
    m, c, _ = state
    m_right = TOTAL_M - m
    c_right = TOTAL_C - c

    # Counts must be non-negative and within total
    if not (0 <= m <= TOTAL_M and 0 <= c <= TOTAL_C):
        return False

    # Missionaries not outnumbered on either side (unless 0 missionaries there)
    if m > 0 and c > m:
        return False
    if m_right > 0 and c_right > m_right:
        return False

    return True


def get_successors(state: tuple) -> list[tuple]:
    """Generate all valid next states from the current state."""
    m, c, boat = state
    successors = []

    for dm, dc in MOVES:
        if boat == 1:                           # boat moves LEFT → RIGHT
            new_state = (m - dm, c - dc, 0)
        else:                                   # boat moves RIGHT → LEFT
            new_state = (m + dm, c + dc, 1)

        if is_valid(new_state):
            successors.append(new_state)

    return successors


def reconstruct_path(parent: dict, state: tuple) -> list[tuple]:
    """Trace back from goal to start using the parent map."""
    path = []
    while state is not None:
        path.append(state)
        state = parent[state]
    return list(reversed(path))


# ─────────────────────────────────────────────────────────
# SEARCH ALGORITHMS
# ─────────────────────────────────────────────────────────

def bfs(start=INITIAL_STATE, goal=GOAL_STATE) -> dict:
    """
    Breadth-First Search.
    Guaranteed to find the shortest path.
    """
    queue    = deque([start])
    parent   = {start: None}
    visited  = {start}
    nodes_explored = 0

    t0 = time.perf_counter()

    while queue:
        state = queue.popleft()
        nodes_explored += 1

        if state == goal:
            elapsed = time.perf_counter() - t0
            path = reconstruct_path(parent, state)
            return {
                "algorithm":      "BFS",
                "found":          True,
                "path":           path,
                "path_length":    len(path) - 1,
                "nodes_explored": nodes_explored,
                "time_sec":       round(elapsed, 6),
            }

        for succ in get_successors(state):
            if succ not in visited:
                visited.add(succ)
                parent[succ] = state
                queue.append(succ)

    elapsed = time.perf_counter() - t0
    return {"algorithm": "BFS", "found": False, "nodes_explored": nodes_explored,
            "time_sec": round(elapsed, 6)}


def dfs(start=INITIAL_STATE, goal=GOAL_STATE) -> dict:
    """
    Depth-First Search (iterative with explicit stack).
    Not guaranteed to find the shortest path.
    """
    stack   = [(start, [start])]
    visited = {start}
    nodes_explored = 0

    t0 = time.perf_counter()

    while stack:
        state, path = stack.pop()
        nodes_explored += 1

        if state == goal:
            elapsed = time.perf_counter() - t0
            return {
                "algorithm":      "DFS",
                "found":          True,
                "path":           path,
                "path_length":    len(path) - 1,
                "nodes_explored": nodes_explored,
                "time_sec":       round(elapsed, 6),
            }

        for succ in reversed(get_successors(state)):
            if succ not in visited:
                visited.add(succ)
                stack.append((succ, path + [succ]))

    elapsed = time.perf_counter() - t0
    return {"algorithm": "DFS", "found": False, "nodes_explored": nodes_explored,
            "time_sec": round(elapsed, 6)}


def dls(start=INITIAL_STATE, goal=GOAL_STATE, limit: int = 15) -> dict:
    """
    Depth-Limited Search — DFS variant with a depth ceiling.
    """
    nodes_explored = 0

    def _dls_recursive(state, path, depth):
        nonlocal nodes_explored
        nodes_explored += 1

        if state == goal:
            return path
        if depth == 0:
            return None

        for succ in get_successors(state):
            if succ not in path:                # avoid cycles in current path
                result = _dls_recursive(succ, path + [succ], depth - 1)
                if result is not None:
                    return result
        return None

    t0   = time.perf_counter()
    path = _dls_recursive(start, [start], limit)
    elapsed = time.perf_counter() - t0

    if path:
        return {
            "algorithm":      f"DLS (limit={limit})",
            "found":          True,
            "path":           path,
            "path_length":    len(path) - 1,
            "nodes_explored": nodes_explored,
            "time_sec":       round(elapsed, 6),
        }
    return {"algorithm": f"DLS (limit={limit})", "found": False,
            "nodes_explored": nodes_explored, "time_sec": round(elapsed, 6)}


def iddfs(start=INITIAL_STATE, goal=GOAL_STATE, max_depth: int = 30) -> dict:
    """
    Iterative Deepening DFS.
    Combines BFS's optimality with DFS's low memory usage.
    """
    total_nodes = 0

    t0 = time.perf_counter()

    for depth in range(max_depth + 1):
        nodes_this_iter = 0

        def _dls(state, path, d):
            nonlocal nodes_this_iter
            nodes_this_iter += 1

            if state == goal:
                return path
            if d == 0:
                return None

            for succ in get_successors(state):
                if succ not in path:
                    result = _dls(succ, path + [succ], d - 1)
                    if result is not None:
                        return result
            return None

        path = _dls(start, [start], depth)
        total_nodes += nodes_this_iter

        if path:
            elapsed = time.perf_counter() - t0
            return {
                "algorithm":      "IDDFS",
                "found":          True,
                "path":           path,
                "path_length":    len(path) - 1,
                "nodes_explored": total_nodes,
                "depth_reached":  depth,
                "time_sec":       round(elapsed, 6),
            }

    elapsed = time.perf_counter() - t0
    return {"algorithm": "IDDFS", "found": False, "nodes_explored": total_nodes,
            "time_sec": round(elapsed, 6)}


# ─────────────────────────────────────────────────────────
# PRETTY PRINTING
# ─────────────────────────────────────────────────────────

BOAT_SYMBOL = "⛵"
PERSON      = "🧑"
SKULL       = "💀"

def _bank_str(m: int, c: int) -> str:
    return f"M={'M'*m+'·'*(TOTAL_M-m)}  C={'C'*c+'·'*(TOTAL_C-c)}"


def print_path(result: dict):
    if not result["found"]:
        print(f"  No solution found.")
        return

    path = result["path"]
    print(f"\n  Solution path ({len(path)-1} moves):\n")
    print(f"  {'Step':<5} {'Left Bank':<22} {'Boat':<6} {'Right Bank':<22} {'Action'}")
    print(f"  {'─'*5} {'─'*22} {'─'*6} {'─'*22} {'─'*30}")

    for i, state in enumerate(path):
        m, c, boat = state
        m_r = TOTAL_M - m
        c_r = TOTAL_C - c
        boat_pos = "←" if boat == 0 else "→"

        if i == 0:
            action = "Initial state"
        else:
            pm, pc, pb = path[i-1]
            dm = abs(m - pm)
            dc = abs(c - pc)
            direction = "→ right" if pb == 1 else "← left"
            action = f"Send {dm}M + {dc}C {direction}"

        left  = f"{m}M, {c}C"
        right = f"{m_r}M, {c_r}C"
        print(f"  {i:<5} {left:<22} {boat_pos:<6} {right:<22} {action}")


def print_result_summary(result: dict):
    print(f"\n{'═'*60}")
    print(f"  Algorithm : {result['algorithm']}")
    print(f"  Found     : {'✅ Yes' if result['found'] else '❌ No'}")
    if result["found"]:
        print(f"  Moves     : {result['path_length']}")
        if "depth_reached" in result:
            print(f"  Depth     : {result['depth_reached']}")
    print(f"  Explored  : {result['nodes_explored']} nodes")
    print(f"  Time      : {result['time_sec']} s")
    print(f"{'═'*60}")
    if result["found"]:
        print_path(result)


def compare_algorithms(results: list[dict]):
    print(f"\n\n{'═'*70}")
    print(f"  PERFORMANCE COMPARISON")
    print(f"{'═'*70}")
    print(f"  {'Algorithm':<22} {'Found':<7} {'Moves':<8} {'Nodes':<12} {'Time (s)'}")
    print(f"  {'─'*22} {'─'*7} {'─'*8} {'─'*12} {'─'*10}")
    for r in results:
        found  = "Yes" if r["found"] else "No"
        moves  = str(r.get("path_length", "—"))
        nodes  = str(r["nodes_explored"])
        t      = str(r["time_sec"])
        print(f"  {r['algorithm']:<22} {found:<7} {moves:<8} {nodes:<12} {t}")
    print(f"{'═'*70}")


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║       MISSIONARIES AND CANNIBALS PROBLEM SOLVER         ║
║                                                          ║
║  3 Missionaries + 3 Cannibals must cross the river.     ║
║  Boat holds max 2 people.                               ║
║  Cannibals must NEVER outnumber Missionaries.           ║
╚══════════════════════════════════════════════════════════╝
""")

    results = []

    print("Running BFS...")
    r1 = bfs()
    print_result_summary(r1)
    results.append(r1)

    print("\nRunning DFS...")
    r2 = dfs()
    print_result_summary(r2)
    results.append(r2)

    print("\nRunning DLS (depth limit = 15)...")
    r3 = dls(limit=15)
    print_result_summary(r3)
    results.append(r3)

    print("\nRunning IDDFS...")
    r4 = iddfs()
    print_result_summary(r4)
    results.append(r4)

    compare_algorithms(results)


if __name__ == "__main__":
    main()
