import time
import threading
import tkinter as tk
from tkinter import messagebox

class PortableStove:
    def __init__(self):
        self.power_on = False
        self.left_burner_time = 0
        self.right_burner_time = 0
        self.oven_time = 0
        self.lock = threading.Lock()
    
    def toggle_power(self):
        with self.lock:
            self.power_on = not self.power_on
            if not self.power_on:
                self.reset_times()
            return self.power_on

    def reset_times(self):
        self.left_burner_time = 0
        self.right_burner_time = 0
        self.oven_time = 0

    def add_left_burner_time(self):
        with self.lock:
            if self.power_on and self.can_use_left_burner():
                self.left_burner_time += 1
                return self.left_burner_time
            return None

    def add_right_burner_time(self):
        with self.lock:
            if self.power_on and self.can_use_right_burner():
                self.right_burner_time += 1
                return self.right_burner_time
            return None

    def add_oven_time(self):
        with self.lock:
            if self.power_on and self.can_use_oven():
                self.oven_time += 1
                return self.oven_time
            return None

    def can_use_left_burner(self):
        return self.oven_time == 0

    def can_use_right_burner(self):
        return self.oven_time == 0

    def can_use_oven(self):
        return self.left_burner_time == 0 and self.right_burner_time == 0

    def run_timer(self):
        while True:
            with self.lock:
                if self.left_burner_time > 0:
                    self.left_burner_time -= 1
                if self.right_burner_time > 0:
                    self.right_burner_time -= 1
                if self.oven_time > 0:
                    self.oven_time -= 1
            time.sleep(60)

    def start(self):
        threading.Thread(target=self.run_timer, daemon=True).start()

class PortableStoveApp:
    def __init__(self, root, stove):
        self.stove = stove
        self.stove.start()

        root.title("Переносная Печь")

        self.power_label = tk.Label(root, text="Питание: Выключено", font=("Arial", 14))
        self.power_label.pack()

        self.left_burner_btn = tk.Button(root, text="Левая конфорка +1 мин", command=self.left_burner)
        self.left_burner_btn.pack()

        self.right_burner_btn = tk.Button(root, text="Правая конфорка +1 мин", command=self.right_burner)
        self.right_burner_btn.pack()

        self.oven_btn = tk.Button(root, text="Духовка +1 мин", command=self.oven)
        self.oven_btn.pack()

        self.toggle_power_btn = tk.Button(root, text="Включить/Выключить Питание", command=self.toggle_power)
        self.toggle_power_btn.pack()

        self.update_status()

    def toggle_power(self):
        power_state = self.stove.toggle_power()
        if power_state:
            self.power_label.config(text="Питание: Включено")
        else:
            self.power_label.config(text="Питание: Выключено")

    def left_burner(self):
        time = self.stove.add_left_burner_time()
        if time is None:
            messagebox.showerror("Ошибка", "Невозможно включить левую конфорку!")
        else:
            messagebox.showinfo("Левая конфорка", f"Время работы: {time} мин")

    def right_burner(self):
        time = self.stove.add_right_burner_time()
        if time is None:
            messagebox.showerror("Ошибка", "Невозможно включить правую конфорку!")
        else:
            messagebox.showinfo("Правая конфорка", f"Время работы: {time} мин")

    def oven(self):
        time = self.stove.add_oven_time()
        if time is None:
            messagebox.showerror("Ошибка", "Невозможно включить духовку!")
        else:
            messagebox.showinfo("Духовка", f"Время работы: {time} мин")

    def update_status(self):
        # Обновлять статус каждые несколько секунд, можно сделать и для таймера, если нужно
        root.after(1000, self.update_status)

if __name__ == "__main__":
    stove = PortableStove()
    root = tk.Tk()
    app = PortableStoveApp(root, stove)
    root.mainloop()
