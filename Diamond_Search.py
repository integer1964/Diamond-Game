from collections import deque

# =========================
# 보드 생성
# =========================

valid_cells = set()

# 위
for r in range(0, 3):
    for c in range(2, 5):
        valid_cells.add((r, c))

# 아래
for r in range(4, 7):
    for c in range(2, 5):
        valid_cells.add((r, c))

# 왼쪽
for r in range(2, 5):
    for c in range(0, 3):
        valid_cells.add((r, c))

# 오른쪽
for r in range(2, 5):
    for c in range(4, 7):
        valid_cells.add((r, c))

# 중앙
for r in range(2, 5):
    for c in range(2, 5):
        valid_cells.add((r, c))

# =========================
# 방향
# =========================

directions = [
    (-1, 0), (1, 0),
    (0, -1), (0, 1),
    (-1, -1), (-1, 1),
    (1, -1), (1, 1)
]

# =========================
# 연결
# =========================

connections = set()

def add_connection(a, b):
    connections.add(tuple(sorted([a, b])))

squares = [

    [
        (0,2),(0,3),(0,4),
        (1,2),(1,3),(1,4),
        (2,2),(2,3),(2,4)
    ],

    [
        (4,2),(4,3),(4,4),
        (5,2),(5,3),(5,4),
        (6,2),(6,3),(6,4)
    ],

    [
        (2,0),(2,1),(2,2),
        (3,0),(3,1),(3,2),
        (4,0),(4,1),(4,2)
    ],

    [
        (2,4),(2,5),(2,6),
        (3,4),(3,5),(3,6),
        (4,4),(4,5),(4,6)
    ],

    [
        (2,2),(2,3),(2,4),
        (3,2),(3,3),(3,4),
        (4,2),(4,3),(4,4)
    ]
]

for sq in squares:

    sqset = set(sq)

    for r, c in sq:

        for dr, dc in directions:

            nr, nc = r + dr, c + dc

            if (nr, nc) in sqset:
                add_connection((r, c), (nr, nc))

# =========================
# 목표 / 초기 상태
# =========================

goal = frozenset({
    (2,4),(2,5),(2,6),
    (3,4),(3,5),(3,6),
    (4,4),(4,5),(4,6)
})

initial = frozenset({
    (2,0),(2,1),(2,2),
    (3,0),(3,1),(3,2),
    (4,0),(4,1),(4,2)
})

LIMIT = 11

# =========================
# 유틸
# =========================

def connected(a, b):
    return tuple(sorted([a, b])) in connections

def is_goal(state):
    return state == goal

# =========================
# 이동 계산
# =========================

def get_normal_moves(state, pos):

    r, c = pos

    result = []

    for dr, dc in directions:

        nr, nc = r + dr, c + dc

        if (
            (nr, nc) in valid_cells
            and (nr, nc) not in state
            and connected((r, c), (nr, nc))
        ):
            result.append((nr, nc))

    return result

def get_jump_moves(state, start):

    visited = set()
    visited.add(start)

    q = deque([start])

    result = set()

    while q:

        r, c = q.popleft()

        for dr, dc in directions:

            mr, mc = r + dr, c + dc
            jr, jc = r + 2 * dr, c + 2 * dc

            if (
                (mr, mc) in valid_cells
                and (jr, jc) in valid_cells
                and (mr, mc) in state
                and (jr, jc) not in state
                and connected((r, c), (mr, mc))
                and connected((mr, mc), (jr, jc))
            ):

                nxt = (jr, jc)

                if nxt not in visited:
                    visited.add(nxt)
                    result.add(nxt)
                    q.append(nxt)

    return list(result)

# =========================
# 가지치기
# =========================

def impossible(state, depth):

    remain = LIMIT - depth

    if remain < 0:
        return True

    outside = 0

    for p in state:
        if p not in goal:
            outside += 1

    if outside > remain:
        return True

    return False

# =========================
# 탐색
# =========================

visited_best = {}

searched = 0
blocked = 0

solutions = []

def dfs(state, depth, path):

    global searched
    global blocked

    searched += 1

    # 진행 상황 출력
    if searched % 100000 == 0:

        print(
            f"[탐색 {searched:,}] "
            f"[막힘 {blocked:,}] "
            f"[해답 {len(solutions):,}] "
            f"[DP 상태 {len(visited_best):,}] "
            f"[깊이 {depth}]"
        )

    # 성공
    if is_goal(state):

        solutions.append(path[:])
        return

    # 가지치기
    if impossible(state, depth):

        blocked += 1
        return

    # DP
    if state in visited_best:

        if visited_best[state] < depth:
            return

    visited_best[state] = depth

    # 이동 생성
    all_moves = []

    for piece in state:

        for nxt in get_jump_moves(state, piece):
            all_moves.append((piece, nxt))

        for nxt in get_normal_moves(state, piece):
            all_moves.append((piece, nxt))

    # DFS
    for piece, nxt in all_moves:

        ns = set(state)

        ns.remove(piece)
        ns.add(nxt)

        ns = frozenset(ns)

        dfs(
            ns,
            depth + 1,
            path + [(piece, nxt)]
        )

# =========================
# 실행
# =========================

print("11턴 이하 모든 해답 탐색 시작\n")

dfs(initial, 0, [])

print("\n====================")
print("탐색 종료")
print("====================")

print(f"\n총 탐색 수 : {searched:,}")
print(f"총 막힘 수 : {blocked:,}")
print(f"총 해답 수 : {len(solutions):,}")
print(f"저장된 DP 상태 수 : {len(visited_best):,}")

# =========================
# 해답 출력
# =========================

print("\n====================")
print("가능한 모든 해답")
print("====================\n")

for idx, sol in enumerate(solutions, start=1):

    print(f"===== 해답 #{idx} =====")
    print(f"총 이동 수 : {len(sol)}\n")

    for i, mv in enumerate(sol, start=1):
        print(f"{i}. {mv[0]} → {mv[1]}")

    print()
