# Missionaries and Cannibals Problem

> **Course:** Artificial Intelligence Lab
> **Problem:** 3 – Uninformed Search Strategies
> **Language:** Python 3.10+
> **Dependency:** None (standard library only)

---

## 📌 What is the Missionaries and Cannibals Problem?

A classic AI search problem:

> 3 Missionaries and 3 Cannibals stand on the **left bank** of a river.
> A boat that holds **at most 2 people** must ferry everyone to the **right bank**.
> At no point can cannibals **outnumber missionaries** on either bank (unless there are zero missionaries on that side) — or the missionaries get eaten.

This is a **constraint-satisfying state-space search problem** used to study uninformed search strategies.

---

## 🧩 Problem Formulation

| Element | Definition |
|---------|-----------|
| **State** | `(missionaries_left, cannibals_left, boat_side)` |
| **Initial State** | `(3, 3, 1)` — everyone + boat on the left |
| **Goal State** | `(0, 0, 0)` — everyone + boat on the right |
| **Actions** | Send `(1,0)`, `(2,0)`, `(0,1)`, `(0,2)`, or `(1,1)` across |
| **Constraint** | Cannibals must never outnumber missionaries on either bank |
| **Total States** | 32 possible, ~16 valid |

---

## 🏗 Architecture

```
missionaries_cannibals.py
│
├── State & Validation
│       ├── is_valid(state)          → checks all constraints
│       └── get_successors(state)    → generates all valid next states
│
├── Search Algorithms
│       ├── bfs()                    → Breadth-First Search
│       ├── dfs()                    → Depth-First Search
│       ├── dls(limit)               → Depth-Limited Search
│       └── iddfs()                  → Iterative Deepening DFS
│
├── Output & Visualisation
│       ├── print_path(result)       → step-by-step move table
│       ├── print_result_summary()   → per-algorithm stats
│       └── compare_algorithms()     → side-by-side comparison table
│
└── main()                           → runs all 4 algorithms and compares
```

---

## 🔍 Algorithms Implemented

### 1. BFS — Breadth-First Search
Explores all states level by level. Uses a **FIFO queue**. Guaranteed to find the **shortest path**.

```
Queue: FIFO (collections.deque)
Visited set: prevents revisiting states
Result: optimal (minimum moves)
```

### 2. DFS — Depth-First Search
Explores as deep as possible before backtracking. Uses a **LIFO stack**. Not guaranteed to find the shortest path but uses less memory than BFS for deep solutions.

```
Stack: LIFO (explicit Python list)
Visited set: prevents cycles
Result: valid but not necessarily optimal
```

### 3. DLS — Depth-Limited Search (DFS variant)
DFS with a hard cap on search depth. Prevents infinite loops in cyclic state spaces. Fails if the solution is deeper than the limit.

```
Depth limit: configurable (default = 15)
Implementation: recursive DFS with depth counter
Result: optimal only if limit ≥ actual solution depth
```

### 4. IDDFS — Iterative Deepening DFS (DFS variant)
Repeatedly runs DLS with increasing depth limits (0, 1, 2, …). Combines **BFS optimality** with **DFS memory efficiency**.

```
Depth increments: 0 → 1 → 2 → … until solution found
Memory: O(depth) like DFS
Result: optimal (same as BFS)
```

---

## ⚙️ Requirements

No external packages required. Runs on Python 3.10+ standard library only.

---

## 🚀 How to Run

```bash
python missionaries_cannibals.py
```

All 4 algorithms run automatically and a comparison table is printed at the end.

---

## 💻 Sample Output

```
╔══════════════════════════════════════════════════════════╗
║       MISSIONARIES AND CANNIBALS PROBLEM SOLVER         ║
╚══════════════════════════════════════════════════════════╝

════════════════════════════════════════════════════════════
  Algorithm : BFS
  Found     : ✅ Yes
  Moves     : 11
  Explored  : 15 nodes
  Time      : 0.000035 s
════════════════════════════════════════════════════════════

  Solution path (11 moves):

  Step  Left Bank     Boat   Right Bank    Action
  ───── ───────────── ────── ───────────── ──────────────────────
  0     3M, 3C        →      0M, 0C        Initial state
  1     3M, 1C        ←      0M, 2C        Send 0M + 2C → right
  2     3M, 2C        →      0M, 1C        Send 0M + 1C ← left
  3     3M, 0C        ←      0M, 3C        Send 0M + 2C → right
  4     3M, 1C        →      0M, 2C        Send 0M + 1C ← left
  5     1M, 1C        ←      2M, 2C        Send 2M + 0C → right
  6     2M, 2C        →      1M, 1C        Send 1M + 1C ← left
  7     0M, 2C        ←      3M, 1C        Send 2M + 0C → right
  8     0M, 3C        →      3M, 0C        Send 0M + 1C ← left
  9     0M, 1C        ←      3M, 2C        Send 0M + 2C → right
  10    1M, 1C        →      2M, 2C        Send 1M + 0C ← left
  11    0M, 0C        ←      3M, 3C        Send 1M + 1C → right
```

### Performance Comparison Table

```
══════════════════════════════════════════════════════════════════════
  PERFORMANCE COMPARISON
══════════════════════════════════════════════════════════════════════
  Algorithm              Found   Moves    Nodes        Time (s)
  ────────────────────── ─────── ──────── ──────────── ──────────
  BFS                    Yes     11       15           0.000035
  DFS                    Yes     11       13           0.000027
  DLS (limit=15)         Yes     11       14           0.000025
  IDDFS                  Yes     11       163          0.000194
══════════════════════════════════════════════════════════════════════
```

---

## 📊 Algorithm Comparison & Analysis

| Property | BFS | DFS | DLS | IDDFS |
|----------|-----|-----|-----|-------|
| **Optimal?** | ✅ Yes | ❌ No | ❌ No (unless limit ≥ depth) | ✅ Yes |
| **Complete?** | ✅ Yes | ✅ Yes (with cycle check) | ⚠️ Only if within limit | ✅ Yes |
| **Time Complexity** | O(b^d) | O(b^m) | O(b^l) | O(b^d) |
| **Space Complexity** | O(b^d) | O(b·m) | O(b·l) | O(b·d) |
| **Nodes Explored** | 15 | 13 | 14 | 163 |
| **Best for** | Shortest path | Low memory | Known depth | Best of both |

Where: `b` = branching factor, `d` = solution depth, `m` = max depth, `l` = depth limit

**Key observations from results:**
- BFS, DFS, and DLS all find the optimal 11-move solution with very similar node counts (13–15)
- IDDFS explores 163 nodes because it re-explores nodes at each depth increment — this is the cost of its memory efficiency
- All algorithms complete in under 0.0002 seconds due to the small state space

---

## 🔌 API Reference

### Run a single algorithm

```python
from missionaries_cannibals import bfs, dfs, dls, iddfs

result = bfs()
print(result["path_length"])     # 11
print(result["nodes_explored"])  # 15
print(result["found"])           # True

for state in result["path"]:
    m, c, boat = state
    print(f"Left: {m}M {c}C | Boat: {'left' if boat else 'right'}")
```

### Custom start/goal state

```python
from missionaries_cannibals import bfs

# Solve for 2 missionaries and 2 cannibals
result = bfs(start=(2, 2, 1), goal=(0, 0, 0))
print(result)
```

### Use DLS with custom depth limit

```python
from missionaries_cannibals import dls

result = dls(limit=20)
print(result["path_length"])
```

---

## 🧪 Testing

```python
from missionaries_cannibals import bfs, dfs, dls, iddfs, is_valid, GOAL_STATE

# All algorithms should find a solution
assert bfs()["found"]   == True
assert dfs()["found"]   == True
assert dls()["found"]   == True
assert iddfs()["found"] == True

# BFS and IDDFS must find the optimal path
assert bfs()["path_length"]   == 11
assert iddfs()["path_length"] == 11

# Goal state must be the last element in each path
assert bfs()["path"][-1]   == GOAL_STATE
assert iddfs()["path"][-1] == GOAL_STATE

# State validation
assert is_valid((3, 3, 1)) == True    # valid initial state
assert is_valid((1, 3, 1)) == False   # 3 cannibals > 1 missionary → invalid
assert is_valid((0, 3, 0)) == True    # 0 missionaries → cannibals are safe
```

---

## 📂 Files

| File | Description |
|------|-------------|
| `missionaries_cannibals.py` | Main implementation |
| `README_missionaries_cannibals.md` | This file |

---

## 🔗 References

- Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.), Chapter 3 – Solving Problems by Searching.
- Nilsson, N. J. (1998). *Artificial Intelligence: A New Synthesis.* Morgan Kaufmann.
