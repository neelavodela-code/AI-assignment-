# Problem 3 - Missionaries and Cannibals

Solving the Missionaries and Cannibals problem using BFS, DFS, and two variants.

## The Problem

3 missionaries and 3 cannibals need to cross a river. The boat holds max 2 people. Cannibals can never outnumber missionaries on either side or the missionaries get eaten. Find a safe sequence of moves.

## How to run

No install needed. Just run:
```
python missionaries_cannibals.py
```

All 4 algorithms run automatically and print their solution steps and a comparison at the end.

## Algorithms

- **BFS** - explores level by level, always finds the shortest path
- **DFS** - explores depth first, faster but not always shortest
- **DLS** - same as DFS but stops at a set depth limit
- **IDDFS** - runs DLS repeatedly with increasing depth until it finds the answer

## Files

- `missionaries_cannibals.py` - main code
