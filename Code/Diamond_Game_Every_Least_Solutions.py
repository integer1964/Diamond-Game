# -*- coding: utf-8 -*-

import tkinter as tk
from collections import deque

# ============================================================
# 2인용 말판 1인 플레이: 48개 11턴 최소해 기보 뷰어
# 외부 파일 없이 SOLUTIONS에 48개 기보 직접 내장
# ============================================================

SOLUTIONS = [
    [((4,2),(3,3)), ((4,0),(2,4)), ((3,1),(3,5)), ((2,1),(4,5)), ((2,2),(4,6)), ((2,0),(2,6)), ((3,0),(4,0)), ((4,0),(4,4)), ((4,1),(2,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((4,2),(3,3)), ((4,0),(2,4)), ((3,1),(3,5)), ((2,1),(4,5)), ((2,2),(2,6)), ((2,0),(4,6)), ((3,0),(4,0)), ((4,0),(4,4)), ((4,1),(2,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((4,2),(3,3)), ((4,0),(2,4)), ((3,1),(3,5)), ((2,2),(2,6)), ((2,1),(4,5)), ((2,0),(4,6)), ((3,0),(4,0)), ((4,0),(4,4)), ((4,1),(2,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((4,2),(3,3)), ((4,0),(2,4)), ((3,1),(3,5)), ((2,2),(2,6)), ((4,1),(4,5)), ((2,0),(4,6)), ((3,0),(2,0)), ((2,0),(4,4)), ((2,1),(2,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((4,2),(3,3)), ((4,0),(2,4)), ((3,1),(3,5)), ((4,1),(4,5)), ((2,2),(4,6)), ((2,0),(2,6)), ((3,0),(2,0)), ((2,0),(4,4)), ((2,1),(2,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((4,2),(3,3)), ((4,0),(2,4)), ((3,1),(3,5)), ((4,1),(4,5)), ((2,2),(2,6)), ((2,0),(4,6)), ((3,0),(2,0)), ((2,0),(4,4)), ((2,1),(2,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((4,2),(3,3)), ((2,0),(2,4)), ((3,1),(3,5)), ((2,1),(4,5)), ((2,2),(4,6)), ((4,0),(2,6)), ((3,0),(4,0)), ((4,0),(4,4)), ((4,1),(2,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((4,2),(3,3)), ((2,0),(2,4)), ((3,1),(3,5)), ((2,1),(4,5)), ((2,2),(2,6)), ((4,0),(4,6)), ((3,0),(4,0)), ((4,0),(4,4)), ((4,1),(2,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((4,2),(3,3)), ((2,0),(2,4)), ((3,1),(3,5)), ((2,2),(2,6)), ((2,1),(4,5)), ((4,0),(4,6)), ((3,0),(4,0)), ((4,0),(4,4)), ((4,1),(2,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((4,2),(3,3)), ((2,0),(2,4)), ((3,1),(3,5)), ((2,2),(2,6)), ((4,1),(4,5)), ((4,0),(4,6)), ((3,0),(2,0)), ((2,0),(4,4)), ((2,1),(2,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((4,2),(3,3)), ((2,0),(2,4)), ((3,1),(3,5)), ((4,1),(4,5)), ((2,2),(4,6)), ((4,0),(2,6)), ((3,0),(2,0)), ((2,0),(4,4)), ((2,1),(2,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((4,2),(3,3)), ((2,0),(2,4)), ((3,1),(3,5)), ((4,1),(4,5)), ((2,2),(2,6)), ((4,0),(4,6)), ((3,0),(2,0)), ((2,0),(4,4)), ((2,1),(2,5)), ((3,2),(3,6)), ((3,3),(3,4))],

    [((2,2),(3,3)), ((4,0),(4,4)), ((3,1),(3,5)), ((2,1),(2,5)), ((4,2),(4,6)), ((2,0),(2,6)), ((3,0),(4,0)), ((4,0),(2,4)), ((4,1),(4,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((2,2),(3,3)), ((4,0),(4,4)), ((3,1),(3,5)), ((2,1),(2,5)), ((4,2),(2,6)), ((2,0),(4,6)), ((3,0),(4,0)), ((4,0),(2,4)), ((4,1),(4,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((2,2),(3,3)), ((4,0),(4,4)), ((3,1),(3,5)), ((4,2),(4,6)), ((2,1),(2,5)), ((2,0),(2,6)), ((3,0),(4,0)), ((4,0),(2,4)), ((4,1),(4,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((2,2),(3,3)), ((4,0),(4,4)), ((3,1),(3,5)), ((4,2),(4,6)), ((4,1),(2,5)), ((2,0),(2,6)), ((3,0),(2,0)), ((2,0),(2,4)), ((2,1),(4,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((2,2),(3,3)), ((4,0),(4,4)), ((3,1),(3,5)), ((4,1),(2,5)), ((4,2),(4,6)), ((2,0),(2,6)), ((3,0),(2,0)), ((2,0),(2,4)), ((2,1),(4,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((2,2),(3,3)), ((4,0),(4,4)), ((3,1),(3,5)), ((4,1),(2,5)), ((4,2),(2,6)), ((2,0),(4,6)), ((3,0),(2,0)), ((2,0),(2,4)), ((2,1),(4,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((2,2),(3,3)), ((2,0),(4,4)), ((3,1),(3,5)), ((2,1),(2,5)), ((4,2),(4,6)), ((4,0),(2,6)), ((3,0),(4,0)), ((4,0),(2,4)), ((4,1),(4,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((2,2),(3,3)), ((2,0),(4,4)), ((3,1),(3,5)), ((2,1),(2,5)), ((4,2),(2,6)), ((4,0),(4,6)), ((3,0),(4,0)), ((4,0),(2,4)), ((4,1),(4,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((2,2),(3,3)), ((2,0),(4,4)), ((3,1),(3,5)), ((4,2),(4,6)), ((2,1),(2,5)), ((4,0),(2,6)), ((3,0),(4,0)), ((4,0),(2,4)), ((4,1),(4,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((2,2),(3,3)), ((2,0),(4,4)), ((3,1),(3,5)), ((4,2),(4,6)), ((4,1),(2,5)), ((4,0),(2,6)), ((3,0),(2,0)), ((2,0),(2,4)), ((2,1),(4,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((2,2),(3,3)), ((2,0),(4,4)), ((3,1),(3,5)), ((4,1),(2,5)), ((4,2),(4,6)), ((4,0),(2,6)), ((3,0),(2,0)), ((2,0),(2,4)), ((2,1),(4,5)), ((3,2),(3,6)), ((3,3),(3,4))],
    [((2,2),(3,3)), ((2,0),(4,4)), ((3,1),(3,5)), ((4,1),(2,5)), ((4,2),(2,6)), ((4,0),(4,6)), ((3,0),(2,0)), ((2,0),(2,4)), ((2,1),(4,5)), ((3,2),(3,6)), ((3,3),(3,4))],

    [((3,2),(3,3)), ((3,0),(3,4)), ((2,1),(4,5)), ((4,2),(4,6)), ((4,6),(3,6)), ((4,0),(4,6)), ((2,0),(2,4)), ((4,1),(2,5)), ((3,1),(3,5)), ((2,2),(2,6)), ((3,3),(4,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((2,1),(4,5)), ((4,2),(4,6)), ((4,6),(3,6)), ((4,0),(4,6)), ((4,1),(2,5)), ((2,0),(2,4)), ((3,1),(3,5)), ((2,2),(2,6)), ((3,3),(4,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((2,1),(4,5)), ((4,2),(4,6)), ((4,6),(3,6)), ((4,0),(2,6)), ((2,0),(2,4)), ((4,1),(2,5)), ((3,1),(3,5)), ((2,2),(4,6)), ((3,3),(4,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((2,1),(4,5)), ((4,2),(4,6)), ((4,6),(3,6)), ((4,0),(2,6)), ((4,1),(2,5)), ((2,0),(2,4)), ((3,1),(3,5)), ((2,2),(4,6)), ((3,3),(4,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((2,1),(4,5)), ((4,2),(4,6)), ((4,6),(3,6)), ((2,0),(4,6)), ((4,0),(2,4)), ((4,1),(2,5)), ((3,1),(3,5)), ((2,2),(2,6)), ((3,3),(4,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((2,1),(4,5)), ((4,2),(4,6)), ((4,6),(3,6)), ((2,0),(2,6)), ((4,0),(2,4)), ((4,1),(2,5)), ((3,1),(3,5)), ((2,2),(4,6)), ((3,3),(4,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((2,1),(2,5)), ((4,2),(2,6)), ((2,6),(3,6)), ((4,0),(4,6)), ((2,0),(2,4)), ((4,1),(4,5)), ((3,1),(3,5)), ((2,2),(2,6)), ((3,3),(4,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((2,1),(2,5)), ((4,2),(2,6)), ((2,6),(3,6)), ((4,0),(4,6)), ((4,1),(4,5)), ((2,0),(2,4)), ((3,1),(3,5)), ((2,2),(2,6)), ((3,3),(4,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((2,1),(2,5)), ((4,2),(2,6)), ((2,6),(3,6)), ((4,0),(2,6)), ((2,0),(2,4)), ((4,1),(4,5)), ((3,1),(3,5)), ((2,2),(4,6)), ((3,3),(4,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((2,1),(2,5)), ((4,2),(2,6)), ((2,6),(3,6)), ((4,0),(2,6)), ((4,1),(4,5)), ((2,0),(2,4)), ((3,1),(3,5)), ((2,2),(4,6)), ((3,3),(4,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((2,1),(2,5)), ((4,2),(2,6)), ((2,6),(3,6)), ((2,0),(4,6)), ((4,0),(2,4)), ((4,1),(4,5)), ((3,1),(3,5)), ((2,2),(2,6)), ((3,3),(4,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((2,1),(2,5)), ((4,2),(2,6)), ((2,6),(3,6)), ((2,0),(2,6)), ((4,0),(2,4)), ((4,1),(4,5)), ((3,1),(3,5)), ((2,2),(4,6)), ((3,3),(4,4))],

    [((3,2),(3,3)), ((3,0),(3,4)), ((4,1),(4,5)), ((2,2),(4,6)), ((4,6),(3,6)), ((4,0),(4,6)), ((2,0),(4,4)), ((2,1),(2,5)), ((3,1),(3,5)), ((4,2),(2,6)), ((3,3),(2,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((4,1),(4,5)), ((2,2),(4,6)), ((4,6),(3,6)), ((4,0),(2,6)), ((2,0),(4,4)), ((2,1),(2,5)), ((3,1),(3,5)), ((4,2),(4,6)), ((3,3),(2,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((4,1),(4,5)), ((2,2),(4,6)), ((4,6),(3,6)), ((2,0),(4,6)), ((4,0),(4,4)), ((2,1),(2,5)), ((3,1),(3,5)), ((4,2),(2,6)), ((3,3),(2,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((4,1),(4,5)), ((2,2),(4,6)), ((4,6),(3,6)), ((2,0),(4,6)), ((2,1),(2,5)), ((4,0),(4,4)), ((3,1),(3,5)), ((4,2),(2,6)), ((3,3),(2,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((4,1),(4,5)), ((2,2),(4,6)), ((4,6),(3,6)), ((2,0),(2,6)), ((4,0),(4,4)), ((2,1),(2,5)), ((3,1),(3,5)), ((4,2),(4,6)), ((3,3),(2,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((4,1),(4,5)), ((2,2),(4,6)), ((4,6),(3,6)), ((2,0),(2,6)), ((2,1),(2,5)), ((4,0),(4,4)), ((3,1),(3,5)), ((4,2),(4,6)), ((3,3),(2,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((4,1),(2,5)), ((2,2),(2,6)), ((2,6),(3,6)), ((4,0),(4,6)), ((2,0),(4,4)), ((2,1),(4,5)), ((3,1),(3,5)), ((4,2),(2,6)), ((3,3),(2,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((4,1),(2,5)), ((2,2),(2,6)), ((2,6),(3,6)), ((4,0),(2,6)), ((2,0),(4,4)), ((2,1),(4,5)), ((3,1),(3,5)), ((4,2),(4,6)), ((3,3),(2,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((4,1),(2,5)), ((2,2),(2,6)), ((2,6),(3,6)), ((2,0),(4,6)), ((4,0),(4,4)), ((2,1),(4,5)), ((3,1),(3,5)), ((4,2),(2,6)), ((3,3),(2,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((4,1),(2,5)), ((2,2),(2,6)), ((2,6),(3,6)), ((2,0),(4,6)), ((2,1),(4,5)), ((4,0),(4,4)), ((3,1),(3,5)), ((4,2),(2,6)), ((3,3),(2,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((4,1),(2,5)), ((2,2),(2,6)), ((2,6),(3,6)), ((2,0),(2,6)), ((4,0),(4,4)), ((2,1),(4,5)), ((3,1),(3,5)), ((4,2),(4,6)), ((3,3),(2,4))],
    [((3,2),(3,3)), ((3,0),(3,4)), ((4,1),(2,5)), ((2,2),(2,6)), ((2,6),(3,6)), ((2,0),(2,6)), ((2,1),(4,5)), ((4,0),(4,4)), ((3,1),(3,5)), ((4,2),(4,6)), ((3,3),(2,4))]
]

# =========================
# 보드 생성
# =========================

valid_cells = set()

for r in range(0, 3):
    for c in range(2, 5):
        valid_cells.add((r, c))

for r in range(4, 7):
    for c in range(2, 5):
        valid_cells.add((r, c))

for r in range(2, 5):
    for c in range(0, 3):
        valid_cells.add((r, c))

for r in range(2, 5):
    for c in range(4, 7):
        valid_cells.add((r, c))

for r in range(2, 5):
    for c in range(2, 5):
        valid_cells.add((r, c))

directions = [
    (-1, 0), (1, 0),
    (0, -1), (0, 1),
    (-1, -1), (-1, 1),
    (1, -1), (1, 1)
]

connections = set()


def add_connection(a, b):
    connections.add(tuple(sorted([a, b])))


squares = [
    [(0,2),(0,3),(0,4), (1,2),(1,3),(1,4), (2,2),(2,3),(2,4)],
    [(4,2),(4,3),(4,4), (5,2),(5,3),(5,4), (6,2),(6,3),(6,4)],
    [(2,0),(2,1),(2,2), (3,0),(3,1),(3,2), (4,0),(4,1),(4,2)],
    [(2,4),(2,5),(2,6), (3,4),(3,5),(3,6), (4,4),(4,5),(4,6)],
    [(2,2),(2,3),(2,4), (3,2),(3,3),(3,4), (4,2),(4,3),(4,4)]
]

for sq in squares:
    sqset = set(sq)

    for r, c in sq:
        for dr, dc in directions:
            nxt = (r + dr, c + dc)

            if nxt in sqset:
                add_connection((r, c), nxt)


def connected(a, b):
    return tuple(sorted([a, b])) in connections


initial_positions = frozenset({
    (2,0),(2,1),(2,2),
    (3,0),(3,1),(3,2),
    (4,0),(4,1),(4,2)
})

goal_positions = frozenset({
    (2,4),(2,5),(2,6),
    (3,4),(3,5),(3,6),
    (4,4),(4,5),(4,6)
})


# =========================
# 이동 경로 계산
# =========================

def get_normal_moves(state, pos):
    r, c = pos
    result = []

    for dr, dc in directions:
        nxt = (r + dr, c + dc)

        if (
            nxt in valid_cells
            and nxt not in state
            and connected(pos, nxt)
        ):
            result.append(nxt)

    return result


def get_jump_moves(state, start):
    visited = {start}
    q = deque([start])
    result = set()

    while q:
        r, c = q.popleft()

        for dr, dc in directions:
            mid = (r + dr, c + dc)
            end = (r + 2 * dr, c + 2 * dc)

            if (
                mid in valid_cells
                and end in valid_cells
                and mid in state
                and end not in state
                and connected((r, c), mid)
                and connected(mid, end)
                and end not in visited
            ):
                visited.add(end)
                result.add(end)
                q.append(end)

    return list(result)


def get_jump_path(state, start, end):
    q = deque([(start, [start])])

    while q:
        now, path = q.popleft()

        if now == end:
            return path

        r, c = now

        for dr, dc in directions:
            mid = (r + dr, c + dc)
            nxt = (r + 2 * dr, c + 2 * dc)

            if (
                mid in valid_cells
                and nxt in valid_cells
                and mid in state
                and nxt not in state
                and connected(now, mid)
                and connected(mid, nxt)
                and nxt not in path
            ):
                q.append((nxt, path + [nxt]))

    return [start, end]


def get_move_path(state, start, end):
    if end in get_normal_moves(state, start):
        return [start, end]

    if end in get_jump_moves(state, start):
        return get_jump_path(state, start, end)

    return [start, end]


def build_replay(solution):
    positions = []
    paths = []

    state = set(initial_positions)
    positions.append(frozenset(state))

    for start, end in solution:
        path = get_move_path(frozenset(state), start, end)
        paths.append(path)

        if start not in state:
            raise ValueError(f"Invalid move: no piece at {start}")

        if end in state:
            raise ValueError(f"Invalid move: destination occupied {end}")

        state.remove(start)
        state.add(end)

        positions.append(frozenset(state))

    return positions, paths


# =========================
# GUI
# =========================

root = tk.Tk()
root.title("2인용 말판 1인 최소해 48개 기보 뷰어")
root.geometry("1150x800")
root.minsize(900, 700)

canvas = tk.Canvas(root, width=720, height=720, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

side_frame = tk.Frame(root)
side_frame.pack(side=tk.RIGHT, fill=tk.Y)

button_frame = tk.Frame(side_frame)
button_frame.pack(pady=8)

info_label = tk.Label(side_frame, font=("Arial", 14, "bold"))
info_label.pack(pady=(4, 2))

move_label = tk.Label(side_frame, font=("Arial", 11), justify="left")
move_label.pack(pady=(0, 8))

select_frame = tk.LabelFrame(side_frame, text="기보 선택")
select_frame.pack(padx=10, pady=6, fill=tk.X)

entry_frame = tk.Frame(select_frame)
entry_frame.pack(pady=5)

solution_entry = tk.Entry(entry_frame, width=8)
solution_entry.pack(side=tk.LEFT, padx=3)

solution_scroll = tk.Scrollbar(select_frame)
solution_scroll.pack(side=tk.RIGHT, fill=tk.Y)

solution_listbox = tk.Listbox(
    select_frame,
    height=12,
    width=32,
    exportselection=False,
    yscrollcommand=solution_scroll.set
)
solution_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
solution_scroll.config(command=solution_listbox.yview)

history_title = tk.Label(
    side_frame,
    text="이동 기록",
    font=("Arial", 14, "bold")
)
history_title.pack(pady=(10, 0))

history_box = tk.Text(side_frame, width=40, height=24)
history_box.pack(padx=10, pady=8)

history_box.tag_configure("current", background="#fff2a8", font=("Arial", 10, "bold"))
history_box.tag_configure("normal", font=("Arial", 10))


current_solution_index = 0
replay_index = 0
replay_positions = []
replay_paths = []
auto_after_id = None


def get_piece_radius():
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    return min(w, h) / 48


def center(r, c):
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    board_size = min(w, h) * 0.75
    cell = board_size / 6

    start_x = (w - board_size) / 2
    start_y = (h - board_size) / 2

    return start_x + c * cell, start_y + r * cell


def hole_color(pos):
    if pos in initial_positions:
        return "#ffdddd"

    if pos in goal_positions:
        return "#ddffdd"

    return "white"


def draw_board():
    canvas.delete("all")

    piece_r = get_piece_radius()
    hole_r = piece_r * 0.6

    # 선
    for a, b in connections:
        x1, y1 = center(*a)
        x2, y2 = center(*b)

        canvas.create_line(
            x1, y1,
            x2, y2,
            fill="gray",
            width=2
        )

    # 구멍
    for pos in valid_cells:
        x, y = center(*pos)

        canvas.create_oval(
            x - hole_r,
            y - hole_r,
            x + hole_r,
            y + hole_r,
            fill=hole_color(pos),
            outline="black",
            width=2
        )

    # 현재 이동 경로
    if replay_paths and 0 < replay_index <= len(replay_paths):
        path = replay_paths[replay_index - 1]

        for a, b in zip(path, path[1:]):
            x1, y1 = center(*a)
            x2, y2 = center(*b)

            canvas.create_line(
                x1, y1,
                x2, y2,
                fill="#8e44ad",
                width=4,
                dash=(6, 4)
            )

        start = path[0]
        end = path[-1]

        sx, sy = center(*start)
        ex, ey = center(*end)

        canvas.create_oval(
            sx - piece_r * 1.4,
            sy - piece_r * 1.4,
            sx + piece_r * 1.4,
            sy + piece_r * 1.4,
            outline="#8e44ad",
            width=3
        )

        canvas.create_oval(
            ex - piece_r * 1.7,
            ey - piece_r * 1.7,
            ex + piece_r * 1.7,
            ey + piece_r * 1.7,
            outline="gold",
            width=4
        )

    # 말
    state = replay_positions[replay_index]

    for pos in state:
        x, y = center(*pos)

        canvas.create_oval(
            x - piece_r,
            y - piece_r,
            x + piece_r,
            y + piece_r,
            fill="red",
            outline="black",
            width=2
        )

    total_turns = len(SOLUTIONS[current_solution_index])

    info_label.config(
        text=f"기보 #{current_solution_index + 1} | {replay_index}/{total_turns}턴"
    )

    if replay_index == 0:
        move_label.config(text="현재 이동: 시작 상태")

    else:
        move = SOLUTIONS[current_solution_index][replay_index - 1]

        move_label.config(
            text=f"현재 이동: {move[0]} → {move[1]}"
        )


def refresh_history():
    history_box.delete("1.0", tk.END)

    sol = SOLUTIONS[current_solution_index]

    for i, move in enumerate(sol, start=1):
        line = f"{i}. {move[0]} → {move[1]}\n"

        if i == replay_index:
            history_box.insert(tk.END, line, "current")
        else:
            history_box.insert(tk.END, line, "normal")

    history_box.see(tk.END)


def stop_auto_play():
    global auto_after_id

    if auto_after_id is not None:
        root.after_cancel(auto_after_id)
        auto_after_id = None


def select_solution(index):
    global current_solution_index
    global replay_index
    global replay_positions
    global replay_paths

    if index < 0 or index >= len(SOLUTIONS):
        return

    stop_auto_play()

    current_solution_index = index
    replay_index = 0

    replay_positions, replay_paths = build_replay(SOLUTIONS[index])

    solution_listbox.selection_clear(0, tk.END)
    solution_listbox.selection_set(index)
    solution_listbox.see(index)

    solution_entry.delete(0, tk.END)
    solution_entry.insert(0, str(index + 1))

    draw_board()
    refresh_history()


def select_from_entry():
    text = solution_entry.get().strip()

    if not text.isdigit():
        return

    idx = int(text) - 1

    if 0 <= idx < len(SOLUTIONS):
        select_solution(idx)


def on_solution_list_select(event=None):
    selection = solution_listbox.curselection()

    if selection:
        select_solution(selection[0])


def prev_solution():
    select_solution(max(0, current_solution_index - 1))


def next_solution():
    select_solution(min(len(SOLUTIONS) - 1, current_solution_index + 1))


def first_turn():
    global replay_index

    stop_auto_play()
    replay_index = 0
    draw_board()
    refresh_history()


def last_turn():
    global replay_index

    stop_auto_play()
    replay_index = len(replay_positions) - 1
    draw_board()
    refresh_history()


def prev_turn():
    global replay_index

    stop_auto_play()

    if replay_index > 0:
        replay_index -= 1
        draw_board()
        refresh_history()


def next_turn():
    global replay_index

    stop_auto_play()

    if replay_index < len(replay_positions) - 1:
        replay_index += 1
        draw_board()
        refresh_history()


def auto_play_step():
    global replay_index
    global auto_after_id

    if replay_index < len(replay_positions) - 1:
        replay_index += 1
        draw_board()
        refresh_history()
        auto_after_id = root.after(700, auto_play_step)

    else:
        auto_after_id = None


def start_auto_play():
    global auto_after_id

    if auto_after_id is None:
        auto_after_id = root.after(700, auto_play_step)


def on_resize(event=None):
    if replay_positions:
        draw_board()


# =========================
# 버튼 / 리스트 초기화
# =========================

tk.Button(
    entry_frame,
    text="이동",
    command=select_from_entry
).pack(side=tk.LEFT, padx=3)

tk.Button(
    button_frame,
    text="이전 기보",
    width=12,
    command=prev_solution
).grid(row=0, column=0, padx=3, pady=3)

tk.Button(
    button_frame,
    text="다음 기보",
    width=12,
    command=next_solution
).grid(row=0, column=1, padx=3, pady=3)

tk.Button(
    button_frame,
    text="처음부터",
    width=12,
    command=first_turn
).grid(row=1, column=0, padx=3, pady=3)

tk.Button(
    button_frame,
    text="끝으로",
    width=12,
    command=last_turn
).grid(row=1, column=1, padx=3, pady=3)

tk.Button(
    button_frame,
    text="이전 턴",
    width=12,
    command=prev_turn
).grid(row=2, column=0, padx=3, pady=3)

tk.Button(
    button_frame,
    text="다음 턴",
    width=12,
    command=next_turn
).grid(row=2, column=1, padx=3, pady=3)

tk.Button(
    button_frame,
    text="자동재생",
    width=12,
    command=start_auto_play
).grid(row=3, column=0, padx=3, pady=3)

tk.Button(
    button_frame,
    text="정지",
    width=12,
    command=stop_auto_play
).grid(row=3, column=1, padx=3, pady=3)

for i, sol in enumerate(SOLUTIONS, start=1):
    first = sol[0]
    last = sol[-1]

    solution_listbox.insert(
        tk.END,
        f"기보 {i:02d} | {first[0]}→{first[1]} ... {last[0]}→{last[1]}"
    )

solution_listbox.bind("<<ListboxSelect>>", on_solution_list_select)

root.bind("<Left>", lambda e: prev_turn())
root.bind("<Right>", lambda e: next_turn())
root.bind("<Home>", lambda e: first_turn())
root.bind("<End>", lambda e: last_turn())
root.bind("<Up>", lambda e: prev_solution())
root.bind("<Down>", lambda e: next_solution())
root.bind("<Return>", lambda e: select_from_entry())

canvas.bind("<Configure>", on_resize)

# 검증
if len(SOLUTIONS) != 48:
    raise RuntimeError(f"SOLUTIONS 개수가 48이 아닙니다: {len(SOLUTIONS)}")

for idx, sol in enumerate(SOLUTIONS, start=1):
    if len(sol) != 11:
        raise RuntimeError(f"기보 #{idx}의 이동 수가 11이 아닙니다: {len(sol)}")

select_solution(0)

root.mainloop()
