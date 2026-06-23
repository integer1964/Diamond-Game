import tkinter as tk
from tkinter import messagebox
from copy import deepcopy
from collections import deque
import math, json, os

SAVE_FILE = "diamond_3p_single_best_record.json"

# =========================
# 1. 3인용 말판 레이아웃
# =========================
board_layout = [
    ",,,,,,,,,.",
    ",,,,,,,,.,.",
    ",,,,,,,.,.,.",
    ".,.,.,.,.,.,.,.,.,.",
    ",.,.,.,.,.,.,.,.,.",
    ",,.,.,.,.,.,.,.,.",
    ",,,.,.,.,.,.,.,.",
    ",,.,.,.,.,.,.,.,.",
    ",.,.,.,.,.,.,.,.,.",
    ".,.,.,.,.,.,.,.,.,.",
    ",,,,,,,.,.,.",
    ",,,,,,,,.,.",
    ",,,,,,,,,."
]

valid_cells = set()
for r, line in enumerate(board_layout):
    for c, char in enumerate(line):
        if char == ".":
            valid_cells.add((r, c))

# =========================
# 2. 진영 정의
# =========================
red_camp = {
    (0, 9),
    (1, 8), (1, 10),
    (2, 7), (2, 9), (2, 11),
    (3, 6), (3, 8), (3, 10), (3, 12)
}

bottom_camp = {
    (9, 6), (9, 8), (9, 10), (9, 12),
    (10, 7), (10, 9), (10, 11),
    (11, 8), (11, 10),
    (12, 9)
}

green_camp = {
    (6, 3),
    (7, 2), (7, 4),
    (8, 1), (8, 3), (8, 5),
    (9, 0), (9, 2), (9, 4), (9, 6)
}

upper_right_camp = {
    (3, 12), (3, 14), (3, 16), (3, 18),
    (4, 13), (4, 15), (4, 17),
    (5, 14), (5, 16),
    (6, 15)
}

yellow_camp = {
    (6, 15),
    (7, 14), (7, 16),
    (8, 13), (8, 15), (8, 17),
    (9, 12), (9, 14), (9, 16), (9, 18)
}

upper_left_camp = {
    (3, 0), (3, 2), (3, 4), (3, 6),
    (4, 1), (4, 3), (4, 5),
    (5, 2), (5, 4),
    (6, 3)
}

# =========================
# 3. 방향 및 연결선
# =========================
directions = [
    (0, -2), (0, 2),
    (-1, -1), (-1, 1),
    (1, -1), (1, 1)
]

connections = set()

for r, c in valid_cells:
    for dr, dc in directions:
        nxt = (r + dr, c + dc)

        if nxt in valid_cells:
            connections.add(
                tuple(sorted([(r, c), nxt]))
            )

# =========================
# 4. tkinter UI
# =========================
root = tk.Tk()
root.title("다이아몬드 게임")
root.geometry("1000x800")
root.minsize(700, 700)

canvas = tk.Canvas(
    root,
    width=700,
    height=700,
    bg="white"
)

canvas.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)

side_frame = tk.Frame(root)
side_frame.pack(
    side=tk.RIGHT,
    fill=tk.Y
)

button_frame = tk.Frame(side_frame)
button_frame.pack(pady=10)

info_label = tk.Label(
    side_frame,
    font=("Arial", 14)
)

info_label.pack()

winner_label = tk.Label(
    side_frame,
    font=("Arial", 18, "bold")
)

winner_label.pack(pady=10)

record_label = tk.Label(
    side_frame,
    font=("Arial", 12)
)

record_label.pack()

history_title = tk.Label(
    side_frame,
    text="이동 기록",
    font=("Arial", 14, "bold")
)

history_title.pack()

history_box = tk.Text(
    side_frame,
    width=35,
    height=32
)

history_box.pack(
    padx=10,
    pady=10
)

# =========================
# 5. 상태 변수
# =========================
mode = None

pieces = {}

turn = "red"
turn_count = 1

selected = None
hovered = None

move_targets = []
jump_targets = []

last_moved = None
winner_text = ""

history_stack = []
move_history = []
redo_stack = []

best_turn = None
best_moves = []

replay_mode = False
replay_index = 0
replay_positions = []
replay_moves = []

home_title = None

color_names = {
    "red": "빨강",
    "green": "초록",
    "yellow": "노랑"
}

piece_colors = {
    "red": "#ff4d4d",
    "green": "#2ecc71",
    "yellow": "#f1c40f"
}

inactive_colors = {
    "red": "#ffcccc",
    "green": "#d5f5e3",
    "yellow": "#fef9e7"
}

# =========================
# 6. 최소 기록 저장 / 불러오기
# =========================
def save_best_record():
    if best_turn is None:
        return

    data = {
        "best_turn": best_turn,
        "best_moves": best_moves
    }

    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def load_best_record():
    global best_turn
    global best_moves

    if not os.path.exists(SAVE_FILE):
        return

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        best_turn = data.get("best_turn")
        best_moves = data.get("best_moves", [])

    except (OSError, json.JSONDecodeError):
        best_turn = None
        best_moves = []


def as_tuple(pos):
    return tuple(pos)


load_best_record()

# =========================
# 7. 유틸리티
# =========================
def get_grid_scale():
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    scale_x = w / 22
    scale_y = h / (14 * math.sqrt(3))

    return min(scale_x, scale_y)


def get_piece_radius():
    return get_grid_scale() * 0.45


def center(r, c):
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    gs = get_grid_scale()

    x = w / 2 + (c - 9) * gs
    y = h / 2 + (r - 6) * gs * math.sqrt(3)

    return x, y


def connected(a, b):
    return tuple(sorted([a, b])) in connections


def clear_buttons():
    for widget in button_frame.winfo_children():
        widget.destroy()


def can_move(pos):
    return bool(
        get_normal_moves(pos)
        or get_jump_moves(pos)
    )

# =========================
# 8. 홈 / 시작 / 버튼
# =========================
def show_home():
    global mode
    global replay_mode
    global home_title

    mode = None
    replay_mode = False

    canvas.delete("all")
    clear_buttons()

    history_box.delete("1.0", tk.END)

    info_label.config(text="")
    winner_label.config(text="")
    record_label.config(text="")

    root.update_idletasks()

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    home_title = canvas.create_text(
        w / 2,
        h * 0.2,
        text="다이아몬드 게임",
        font=("Arial", 32, "bold")
    )

    tk.Button(
        button_frame,
        text="1인용 연습 (10개)",
        width=20,
        height=2,
        command=start_single
    ).pack(pady=10)

    tk.Button(
        button_frame,
        text="3인용 게임 (각 10개)",
        width=20,
        height=2,
        command=start_multi
    ).pack(pady=10)

    tk.Button(
        button_frame,
        text="현재 최소횟수 보기",
        width=20,
        height=2,
        command=show_best_replay
    ).pack(pady=10)

    tk.Button(
        button_frame,
        text="단축키 도움말",
        width=20,
        height=2,
        command=show_help
    ).pack(pady=10)


def reset_state():
    global pieces
    global turn
    global turn_count
    global selected
    global hovered
    global move_targets
    global jump_targets
    global last_moved
    global winner_text
    global history_stack
    global move_history
    global redo_stack

    pieces = {}

    turn = "red"
    turn_count = 1

    selected = None
    hovered = None

    move_targets = []
    jump_targets = []

    last_moved = None
    winner_text = ""

    history_stack = []
    move_history = []
    redo_stack = []


def start_single():
    global mode
    global replay_mode

    mode = "single"
    replay_mode = False

    reset_state()

    for pos in red_camp:
        pieces[pos] = "red"

    setup_buttons()
    draw_board()


def start_multi():
    global mode
    global replay_mode

    mode = "multi"
    replay_mode = False

    reset_state()

    for pos in red_camp:
        pieces[pos] = "red"

    for pos in green_camp:
        pieces[pos] = "green"

    for pos in yellow_camp:
        pieces[pos] = "yellow"

    setup_buttons()
    draw_board()


def setup_buttons():
    clear_buttons()

    tk.Button(
        button_frame,
        text="되돌리기 (U)",
        width=15,
        command=undo
    ).pack(pady=3)

    tk.Button(
        button_frame,
        text="다시실행",
        width=15,
        command=redo
    ).pack(pady=3)

    tk.Button(
        button_frame,
        text="다시하기 (R)",
        width=15,
        command=restart_game
    ).pack(pady=3)

    tk.Button(
        button_frame,
        text="홈 (H)",
        width=15,
        command=go_home
    ).pack(pady=3)


def go_home():
    answer = messagebox.askyesno(
        "홈으로",
        "홈으로 돌아가면 현재 게임이 초기화됩니다.\n그래도 돌아가시겠습니까?"
    )

    if not answer:
        return

    history_box.delete("1.0", tk.END)

    move_history.clear()
    history_stack.clear()
    redo_stack.clear()

    show_home()


def restart_game():
    answer = messagebox.askyesno(
        "다시하기",
        "정말 다시하시겠습니까?"
    )

    if not answer:
        return

    history_box.delete("1.0", tk.END)

    move_history.clear()
    history_stack.clear()
    redo_stack.clear()

    if mode == "single":
        start_single()

    elif mode == "multi":
        start_multi()

# =========================
# 9. 이동 계산
# =========================
def get_normal_moves(pos):
    r, c = pos
    result = []

    for dr, dc in directions:
        nxt = (r + dr, c + dc)

        if (
            nxt in valid_cells
            and nxt not in pieces
            and connected(pos, nxt)
        ):
            result.append(nxt)

    return result


def get_jump_moves(start):
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
                and mid in pieces
                and end not in pieces
                and connected((r, c), mid)
                and connected(mid, end)
                and end not in visited
            ):
                visited.add(end)
                result.add(end)
                q.append(end)

    return list(result)


def get_jump_path(start, end):
    q = deque()
    q.append((start, [start]))

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
                and mid in pieces
                and nxt not in pieces
                and connected(now, mid)
                and connected(mid, nxt)
                and nxt not in path
            ):
                q.append(
                    (nxt, path + [nxt])
                )

    return [start, end]

# =========================
# 10. 기록 / undo / redo
# =========================
def refresh_history():
    history_box.delete("1.0", tk.END)

    for i, mv in enumerate(move_history, start=1):
        color = color_names.get(
            mv["color"],
            mv["color"]
        )

        history_box.insert(
            tk.END,
            f"{i}. {color} : {as_tuple(mv['from'])} → {as_tuple(mv['to'])}\n"
        )

    history_box.see(tk.END)


def snapshot():
    return {
        "pieces": deepcopy(pieces),
        "turn": turn,
        "turn_count": turn_count,
        "selected": selected,
        "move_targets": deepcopy(move_targets),
        "jump_targets": deepcopy(jump_targets),
        "last_moved": last_moved,
        "winner_text": winner_text,
        "move_history": deepcopy(move_history)
    }


def restore(st):
    global pieces
    global turn
    global turn_count
    global selected
    global move_targets
    global jump_targets
    global last_moved
    global winner_text
    global move_history

    pieces = st["pieces"]
    turn = st["turn"]
    turn_count = st["turn_count"]

    selected = st["selected"]
    move_targets = st["move_targets"]
    jump_targets = st["jump_targets"]

    last_moved = st["last_moved"]
    winner_text = st["winner_text"]
    move_history = st["move_history"]

    refresh_history()
    draw_board()


def save_state():
    history_stack.append(snapshot())


def undo():
    if not history_stack:
        return

    redo_stack.append(snapshot())

    st = history_stack.pop()
    restore(st)


def redo():
    if not redo_stack:
        return

    save_state()

    st = redo_stack.pop()
    restore(st)

# =========================
# 11. 승리 판정 / 턴 종료
# =========================
def check_win():
    global winner_text
    global best_turn
    global best_moves

    if mode == "multi":
        red_win = all(
            pieces.get(pos) == "red"
            for pos in bottom_camp
        )

        green_win = all(
            pieces.get(pos) == "green"
            for pos in upper_right_camp
        )

        yellow_win = all(
            pieces.get(pos) == "yellow"
            for pos in upper_left_camp
        )

        if red_win:
            winner_text = "빨강 승리!"

        elif green_win:
            winner_text = "초록 승리!"

        elif yellow_win:
            winner_text = "노랑 승리!"

        else:
            winner_text = ""

        return

    if mode == "single":
        success = all(
            pieces.get(pos) == "red"
            for pos in bottom_camp
        )

        if success:
            winner_text = "미션 성공!"

            used_turn = turn_count - 1

            if best_turn is None or used_turn < best_turn:
                best_turn = used_turn
                best_moves = deepcopy(move_history)
                save_best_record()

        else:
            winner_text = ""


def end_turn():
    global turn
    global turn_count
    global selected
    global move_targets
    global jump_targets

    selected = None
    move_targets = []
    jump_targets = []

    turn_count += 1

    if mode == "multi":
        if turn == "red":
            turn = "green"

        elif turn == "green":
            turn = "yellow"

        else:
            turn = "red"

    check_win()
    draw_board()

# =========================
# 12. 그리기
# =========================
def hole_color_at(pos):
    if pos in bottom_camp:
        return "#ffe6e6"

    if pos in upper_right_camp:
        return "#e6f9ec"

    if pos in upper_left_camp:
        return "#fffde6"

    if pos in red_camp:
        return "#fff2f2"

    if pos in green_camp:
        return "#f2fbf5"

    if pos in yellow_camp:
        return "#fffef2"

    return "white"


def draw_static_board(piece_r, hole_r):
    for a, b in connections:
        x1, y1 = center(*a)
        x2, y2 = center(*b)

        canvas.create_line(
            x1, y1,
            x2, y2,
            fill="#e2e2e2",
            width=2
        )

    for pos in valid_cells:
        x, y = center(*pos)

        canvas.create_oval(
            x - hole_r,
            y - hole_r,
            x + hole_r,
            y + hole_r,
            fill=hole_color_at(pos),
            outline="#7f8c8d",
            width=2
        )


def draw_board():
    canvas.delete("all")

    piece_r = get_piece_radius()
    hole_r = piece_r * 0.6

    if mode == "multi":
        border_colors = {
            "red": "#ff9999",
            "green": "#99dd99",
            "yellow": "#ffeb99"
        }

        w = canvas.winfo_width()
        h = canvas.winfo_height()

        canvas.create_rectangle(
            5,
            5,
            w - 5,
            h - 5,
            outline=border_colors.get(turn, "white"),
            width=8
        )

    draw_static_board(piece_r, hole_r)

    for pos in move_targets:
        x, y = center(*pos)

        canvas.create_oval(
            x - piece_r * 0.8,
            y - piece_r * 0.8,
            x + piece_r * 0.8,
            y + piece_r * 0.8,
            fill="",
            outline="#85C1E9",
            width=3
        )

    for pos in jump_targets:
        x, y = center(*pos)

        canvas.create_oval(
            x - piece_r * 0.8,
            y - piece_r * 0.8,
            x + piece_r * 0.8,
            y + piece_r * 0.8,
            fill="",
            outline="#00FF00",
            width=4
        )

    if last_moved:
        x, y = center(*last_moved)

        canvas.create_oval(
            x - piece_r * 1.5,
            y - piece_r * 1.5,
            x + piece_r * 1.5,
            y + piece_r * 1.5,
            outline="cyan",
            width=3
        )

    for pos, color in pieces.items():
        x, y = center(*pos)

        p_color = piece_colors.get(color, color)

        if not can_move(pos):
            p_color = inactive_colors.get(color, p_color)

        canvas.create_oval(
            x - piece_r,
            y - piece_r,
            x + piece_r,
            y + piece_r,
            fill=p_color,
            outline="black",
            width=2
        )

    if hovered and hovered != selected:
        x, y = center(*hovered)

        canvas.create_oval(
            x - piece_r * 1.4,
            y - piece_r * 1.4,
            x + piece_r * 1.4,
            y + piece_r * 1.4,
            outline="#bbbbbb",
            width=2
        )

    if selected:
        x, y = center(*selected)

        canvas.create_oval(
            x - piece_r * 1.6,
            y - piece_r * 1.6,
            x + piece_r * 1.6,
            y + piece_r * 1.6,
            outline="blue",
            width=4
        )

    if mode == "multi":
        info_label.config(
            text=f"{turn_count}턴 | 현재 차례: {color_names.get(turn)}"
        )

        record_label.config(text="")

    elif mode == "single":
        info_label.config(
            text=f"{turn_count}턴 진행 중"
        )

        if best_turn is None:
            record_label.config(
                text="현재 최소횟수 : 없음"
            )

        else:
            record_label.config(
                text=f"현재 최소횟수 : {best_turn}"
            )

    winner_label.config(text=winner_text)

# =========================
# 13. 최소 기록 리플레이
# =========================
def reset_selection_state():
    global selected
    global hovered
    global move_targets
    global jump_targets
    global last_moved

    selected = None
    hovered = None
    move_targets = []
    jump_targets = []
    last_moved = None


def show_best_replay():
    global replay_mode
    global replay_index
    global replay_positions
    global replay_moves
    global mode

    if best_turn is None:
        messagebox.showinfo(
            "정보",
            "저장된 최소 기록이 없습니다."
        )

        return

    mode = None
    replay_mode = True

    reset_selection_state()
    clear_buttons()
    canvas.delete("all")

    replay_moves = deepcopy(best_moves)
    replay_positions = []
    replay_index = 0

    st = {}

    for pos in red_camp:
        st[pos] = "red"

    replay_positions.append(
        deepcopy(st)
    )

    for mv in replay_moves:
        ns = deepcopy(
            replay_positions[-1]
        )

        a = as_tuple(mv["from"])
        b = as_tuple(mv["to"])

        if a in ns:
            ns[b] = ns[a]
            del ns[a]

        replay_positions.append(ns)

    replay_buttons()
    draw_replay()


def replay_buttons():
    clear_buttons()

    tk.Button(
        button_frame,
        text="이전 턴",
        width=15,
        command=prev_replay
    ).pack(pady=3)

    tk.Button(
        button_frame,
        text="다음 턴",
        width=15,
        command=next_replay
    ).pack(pady=3)

    tk.Button(
        button_frame,
        text="처음부터",
        width=15,
        command=reset_replay
    ).pack(pady=3)

    tk.Button(
        button_frame,
        text="홈",
        width=15,
        command=show_home
    ).pack(pady=3)


def draw_replay():
    canvas.delete("all")

    piece_r = get_piece_radius()
    hole_r = piece_r * 0.6

    draw_static_board(piece_r, hole_r)

    if 0 < replay_index <= len(replay_moves):
        mv = replay_moves[replay_index - 1]

        path = mv.get(
            "path",
            [mv["from"], mv["to"]]
        )

        path = [
            as_tuple(p)
            for p in path
        ]

        for a, b in zip(path, path[1:]):
            x1, y1 = center(*a)
            x2, y2 = center(*b)

            canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="#8e44ad",
                width=4,
                dash=(6, 4)
            )

        sx, sy = center(*path[0])
        ex, ey = center(*path[-1])

        canvas.create_oval(
            sx - piece_r * 0.9,
            sy - piece_r * 0.9,
            sx + piece_r * 0.9,
            sy + piece_r * 0.9,
            outline="#8e44ad",
            width=3
        )

        canvas.create_oval(
            ex - piece_r * 1.2,
            ey - piece_r * 1.2,
            ex + piece_r * 1.2,
            ey + piece_r * 1.2,
            outline="cyan",
            width=4
        )

    st = replay_positions[replay_index]

    for pos, color in st.items():
        x, y = center(*pos)

        canvas.create_oval(
            x - piece_r,
            y - piece_r,
            x + piece_r,
            y + piece_r,
            fill=piece_colors.get(color, color),
            outline="black",
            width=2
        )

    info_label.config(
        text=f"기보 재생 : {replay_index}/{best_turn}"
    )

    winner_label.config(
        text=f"최소횟수 : {best_turn}"
    )

    record_label.config(text="")

    history_box.delete("1.0", tk.END)

    for i, mv in enumerate(replay_moves, start=1):
        path = mv.get(
            "path",
            [mv["from"], mv["to"]]
        )

        path_text = " → ".join(
            str(as_tuple(p))
            for p in path
        )

        if i == replay_index:
            history_box.insert(
                tk.END,
                f">>> {i}. {path_text} <<<\n"
            )

        else:
            history_box.insert(
                tk.END,
                f"{i}. {path_text}\n"
            )

    history_box.see(tk.END)


def next_replay():
    global replay_index

    if (
        replay_mode
        and replay_index < len(replay_positions) - 1
    ):
        replay_index += 1
        draw_replay()


def prev_replay():
    global replay_index

    if (
        replay_mode
        and replay_index > 0
    ):
        replay_index -= 1
        draw_replay()


def reset_replay():
    global replay_index

    if replay_mode:
        replay_index = 0
        draw_replay()

# =========================
# 14. 이벤트 처리
# =========================
def find_clicked_cell(event):
    gs = get_grid_scale()
    click_radius = gs * 0.7

    for pos in valid_cells:
        cx, cy = center(*pos)

        if (
            (event.x - cx) ** 2
            + (event.y - cy) ** 2
            <= click_radius ** 2
        ):
            return pos

    return None


def click(event):
    global selected
    global move_targets
    global jump_targets
    global last_moved

    if mode is None:
        return

    clicked = find_clicked_cell(event)

    if clicked is None:
        selected = None
        move_targets = []
        jump_targets = []
        draw_board()
        return

    if selected:
        if (
            clicked in move_targets
            or clicked in jump_targets
        ):
            save_state()
            redo_stack.clear()

            old = selected

            if clicked in jump_targets:
                path = get_jump_path(old, clicked)

            else:
                path = [old, clicked]

            pieces[clicked] = pieces[selected]
            del pieces[selected]

            move_history.append({
                "color": turn,
                "from": old,
                "to": clicked,
                "path": path
            })

            refresh_history()

            last_moved = clicked

            end_turn()
            return

        selected = None
        move_targets = []
        jump_targets = []
        draw_board()
        return

    if clicked in pieces:
        if mode == "single" and pieces[clicked] != "red":
            return

        if mode == "multi" and pieces[clicked] != turn:
            return

        selected = clicked

        move_targets = get_normal_moves(clicked)
        jump_targets = get_jump_moves(clicked)

        if not move_targets and not jump_targets:
            draw_board()
            root.after(120, cancel_selection)
            return

        draw_board()


def motion(event):
    global hovered

    if mode is None:
        return

    hovered = None

    pos = find_clicked_cell(event)

    if pos in pieces:
        if mode == "single" and pieces[pos] == "red":
            hovered = pos

        elif mode == "multi" and pieces[pos] == turn:
            hovered = pos

    draw_board()


def cancel_selection(event=None):
    global selected
    global move_targets
    global jump_targets

    selected = None
    move_targets = []
    jump_targets = []

    if replay_mode:
        draw_replay()

    else:
        draw_board()


def replay_key(event):
    if event.keysym == "Right":
        next_replay()

    elif event.keysym == "Left":
        prev_replay()


def shortcut_key(event):
    key = event.keysym.lower()

    if key == "h":
        if replay_mode:
            show_home()

        else:
            go_home()

    elif key == "r" and not replay_mode:
        restart_game()

    elif key == "u" and not replay_mode:
        undo()


def show_help():
    help_window = tk.Toplevel(root)
    help_window.title("단축키 도움말")

    win_w = 320
    win_h = 210

    x = root.winfo_x() + (root.winfo_width() - win_w) // 2
    y = root.winfo_y() + (root.winfo_height() - win_h) // 2

    help_window.geometry(
        f"{win_w}x{win_h}+{x}+{y}"
    )

    help_window.resizable(False, False)

    text = (
        "[단축키 안내]\n\n"
        "H : 홈화면으로 이동\n"
        "R : 게임 다시하기\n"
        "U : 한 턴 되돌리기\n"
        "ESC : 선택된 말 취소\n"
        "← → : 최소기록 replay 이동"
    )

    tk.Label(
        help_window,
        text=text,
        font=("Arial", 13),
        justify="left"
    ).pack(
        padx=25,
        pady=(18, 2),
        anchor="w"
    )

    tk.Button(
        help_window,
        text="닫기",
        width=10,
        command=help_window.destroy
    ).pack(pady=2)


def resize_redraw(event):
    if replay_mode:
        draw_replay()

    elif mode is not None:
        draw_board()

    elif home_title is not None:
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        canvas.coords(
            home_title,
            w / 2,
            h * 0.2
        )

# =========================
# 15. 실행
# =========================
canvas.bind("<Button-1>", click)
canvas.bind("<Motion>", motion)

root.bind("<Escape>", cancel_selection)

root.bind("h", shortcut_key)
root.bind("r", shortcut_key)
root.bind("u", shortcut_key)

root.bind("<Right>", replay_key)
root.bind("<Left>", replay_key)

root.bind("<Configure>", resize_redraw)

show_home()
root.mainloop()
