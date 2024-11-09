import time
import threading

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
            print("Питание:", "Включено" if self.power_on else "Выключено")

    def reset_times(self):
        self.left_burner_time = 0
        self.right_burner_time = 0
        self.oven_time = 0

    def add_left_burner_time(self):
        with self.lock:
            if self.power_on and self.can_use_left_burner():
                self.left_burner_time += 1
                print("Время работы левой конфорки:", self.left_burner_time, "минут")
            else:
                print("Невозможно добавить время левой конфорке. Духовка работает или печь выключена.")

    def add_right_burner_time(self):
        with self.lock:
            if self.power_on and self.can_use_right_burner():
                self.right_burner_time += 1
                print("Время работы правой конфорки:", self.right_burner_time, "минут")
            else:
                print("Невозможно добавить время правой конфорке. Духовка работает или печь выключена.")

    def add_oven_time(self):
        with self.lock:
            if self.power_on and self.can_use_oven():
                self.oven_time += 1
                print("Время работы духовки:", self.oven_time, "минут")
            else:
                print("Невозможно добавить время духовке. Одна из конфорок работает или печь выключена.")
    
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
                    if self.left_burner_time == 0:
                        print("Левая конфорка выключена")
                if self.right_burner_time > 0:
                    self.right_burner_time -= 1
                    if self.right_burner_time == 0:
                        print("Правая конфорка выключена")
                if self.oven_time > 0:
                    self.oven_time -= 1
                    if self.oven_time == 0:
                        print("Духовка выключена")
            time.sleep(60)

    def start(self):
        threading.Thread(target=self.run_timer, daemon=True).start()

def menu():
    print("\n--- Переносная печь ---")
    print("1. Включить/выключить питание")
    print("2. Добавить 1 минуту на левую конфорку")
    print("3. Добавить 1 минуту на правую конфорку")
    print("4. Добавить 1 минуту на духовку")
    print("5. Выход")
    print("-----------------------")

def main():
    stove = PortableStove()
    stove.start()

    while True:
        menu()
        choice = input("Выберите действие: ")
        if choice == '1':
            stove.toggle_power()
        elif choice == '2':
            stove.add_left_burner_time()
        elif choice == '3':
            stove.add_right_burner_time()
        elif choice == '4':
            stove.add_oven_time()
        elif choice == '5':
            print("Выход")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()
