import os
import sys
import csv
import time
import threading
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

# --- 센서 및 트레이 라이브러리 ---
from pynput import mouse, keyboard
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

# --- Matplotlib 스타일 설정 ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# =========================================================
# [1] 경로 및 설정 관리
# =========================================================
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SAVE_DIR = os.path.join(BASE_DIR, "Data")
if not os.path.exists(SAVE_DIR):
    try:
        os.makedirs(SAVE_DIR)
    except PermissionError:
        SAVE_DIR = os.path.join(os.path.expanduser("~"), "Documents", "KM_TRACK_Data")
        if not os.path.exists(SAVE_DIR): os.makedirs(SAVE_DIR)

CONFIG_FILE = os.path.join(BASE_DIR, "config.txt")
PC_NAME = "UnknownPC"

def load_or_ask_pc_name():
    global PC_NAME
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                name = f.read().strip()
                if name:
                    PC_NAME = name
                    return
        except: pass

    input_root = tk.Tk()
    input_root.withdraw()
    input_root.attributes('-topmost', True)
    
    while True:
        name = simpledialog.askstring("KM-TRACK 설정", "연구용 PC 식별 이름을 입력해주세요.\n(예: Participant_01, Office_A 등)", parent=input_root)
        if name and name.strip():
            PC_NAME = name.strip()
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    f.write(PC_NAME)
            except: pass
            break
        else:
            if name is None: sys.exit(0)
    input_root.destroy()

# --- 전역 변수 ---
lock = threading.Lock()
counters = {"keyboard": 0, "mouse_click": 0, "mouse_move": 0}
stop_event = threading.Event()
root = None

def get_log_file_path(date_obj=None):
    if date_obj is None:
        date_obj = datetime.now()
    date_str = date_obj.strftime("%Y-%m-%d")
    return os.path.join(SAVE_DIR, f"{date_str}_{PC_NAME}.csv")

# =========================================================
# [2] 데이터 수집 로직
# =========================================================
def save_to_file(row):
    file_path = get_log_file_path()
    file_exists = os.path.exists(file_path)
    try:
        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Keyboard_Count", "Mouse_Click_Count", "Mouse_Move_Count"])
            writer.writerows([row])
    except Exception: pass

def processor_loop():
    while not stop_event.is_set():
        time.sleep(3)
        current_data = None
        with lock:
            total = counters["keyboard"] + counters["mouse_click"] + counters["mouse_move"]
            if total > 0:
                current_data = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    counters["keyboard"],
                    counters["mouse_click"],
                    counters["mouse_move"]
                ]
                counters["keyboard"] = 0
                counters["mouse_click"] = 0
                counters["mouse_move"] = 0
        if current_data:
            save_to_file(current_data)

def on_press(key):
    with lock: counters["keyboard"] += 1

def on_click(x, y, button, pressed):
    if pressed:
        with lock: counters["mouse_click"] += 1

def on_move(x, y):
    with lock: counters["mouse_move"] += 1

def start_sensor():
    m_listener = mouse.Listener(on_move=on_move, on_click=on_click)
    k_listener = keyboard.Listener(on_press=on_press)
    m_listener.start()
    k_listener.start()
    m_listener.join()
    k_listener.join()

# =========================================================
# [3] GUI 및 그래프 로직
# =========================================================
class MonitoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"KM-TRACK Dashboard - [{PC_NAME}]")
        self.root.geometry("1000x850")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        nav_frame = tk.Frame(root, bg="white", pady=10)
        nav_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(nav_frame, text="⏱ 조회 기간:", bg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(20, 10))
        
        self.time_range = tk.StringVar(value="30m")
        style = ttk.Style()
        style.configure('TRadiobutton', background='white', font=('Arial', 10))
        
        modes = [("1분", "1m"), ("30분", "30m"), ("6시간", "6h"), ("24시간", "24h")]
        for text, mode in modes:
            ttk.Radiobutton(nav_frame, text=text, variable=self.time_range, 
                            value=mode, command=self.update_graphs).pack(side=tk.LEFT, padx=10)

        self.fig, self.axs = plt.subplots(4, 1, figsize=(8, 10), sharex=True)
        self.fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95], h_pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.root.after(10000, self.auto_refresh)
        self.update_graphs()

    def hide_window(self):
        self.root.withdraw()

    def show_window(self):
        self.root.deiconify()
        self.update_graphs()

    def auto_refresh(self):
        if self.root.state() == "normal":
            self.update_graphs()
        self.root.after(10000, self.auto_refresh)

    def get_resampled_data(self):
        now = datetime.now()
        mode = self.time_range.get()
        
        if mode == "1m": delta = timedelta(minutes=1); bucket_sec = 3
        elif mode == "30m": delta = timedelta(minutes=30); bucket_sec = 30
        elif mode == "6h": delta = timedelta(hours=6); bucket_sec = 60
        else: delta = timedelta(hours=24); bucket_sec = 300

        scale_factor = 10.0 / bucket_sec
        start_time = now - delta
        
        time_buckets = {}
        curr = start_time
        while curr <= now:
            bucket_key = curr.replace(microsecond=0)
            time_buckets[bucket_key] = {"k": 0, "c": 0, "m": 0}
            curr += timedelta(seconds=bucket_sec)

        target_dates = []
        temp_date = start_time.date()
        while temp_date <= now.date():
            target_dates.append(temp_date)
            temp_date += timedelta(days=1)
            
        for d in target_dates:
            file_path = get_log_file_path(d)
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        reader = csv.reader(f)
                        next(reader, None)
                        for row in reader:
                            if not row: continue
                            ts = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                            if ts >= start_time and ts <= now:
                                for bucket_time in time_buckets:
                                    if bucket_time <= ts < bucket_time + timedelta(seconds=bucket_sec):
                                        time_buckets[bucket_time]["k"] += int(row[1])
                                        time_buckets[bucket_time]["c"] += int(row[2])
                                        time_buckets[bucket_time]["m"] += int(row[3])
                                        break
                except Exception: pass

        sorted_times = sorted(time_buckets.keys())
        keys = [time_buckets[t]["k"] * scale_factor for t in sorted_times]
        clicks = [time_buckets[t]["c"] * scale_factor for t in sorted_times]
        moves = [time_buckets[t]["m"] * scale_factor for t in sorted_times]
        totals = [k+c+m for k,c,m in zip(keys, clicks, moves)]
        
        return sorted_times, keys, clicks, moves, totals

    def update_graphs(self):
        times, keys, clicks, moves, totals = self.get_resampled_data()
        colors = ['#2ecc71', '#e74c3c', '#3498db', '#34495e']
        titles = ["Keyboard (Counts/10s)", "Mouse Clicks (Counts/10s)", "Mouse Movement (Counts/10s)", "Total Activity (Counts/10s)"]

        for i, ax in enumerate(self.axs):
            ax.clear()
            ax.plot(times, [keys, clicks, moves, totals][i], color=colors[i], linewidth=1.5)
            ax.set_ylim(bottom=0); ax.margins(x=0)
            ax.set_title(titles[i], fontsize=10, fontweight='bold', loc='left')
            ax.tick_params(axis='both', which='major', labelsize=8)
            ax.grid(True, linestyle='--', alpha=0.6)
            
            mode = self.time_range.get()
            xfmt = mdates.DateFormatter('%H:%M') if mode in ["6h", "24h"] else mdates.DateFormatter('%H:%M:%S')
            ax.xaxis.set_major_formatter(xfmt)
        self.canvas.draw()

# =========================================================
# [4] 트레이 및 메인 실행
# =========================================================
def quit_app(icon, item):
    icon.stop(); stop_event.set(); root.quit(); os._exit(0)

def open_gui(icon, item):
    root.after(0, app.show_window)

def create_image():
    image = Image.new('RGB', (64, 64), (255, 255, 255))
    ImageDraw.Draw(image).rectangle((16, 16, 48, 48), fill='#3498db')
    return image

def setup_tray():
    menu = pystray.Menu(item('모니터링 열기', open_gui, default=True), item('종료', quit_app))
    icon = pystray.Icon("KM-TRACK", create_image(), "KM-TRACK (HAR Monitor)", menu)
    icon.run()

if __name__ == "__main__":
    mutex_name = "Global\\KM_TRACK_Unique_v1"
    my_mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    if ctypes.windll.kernel32.GetLastError() == 183:
        temp = tk.Tk(); temp.withdraw()
        messagebox.showwarning("알림", "KM-TRACK이 이미 실행 중입니다.")
        sys.exit(0)

    load_or_ask_pc_name()
    root = tk.Tk(); app = MonitoringApp(root); root.withdraw()

    threading.Thread(target=processor_loop, daemon=True).start()
    threading.Thread(target=start_sensor, daemon=True).start()
    threading.Thread(target=setup_tray, daemon=True).start()
    root.mainloop()