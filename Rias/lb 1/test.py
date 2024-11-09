import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

class MultiTypeIR:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.development_costs = []
        self.servicing_costs = []
        self.purchase_cost = 0
        self.profit = 0
    
    def add_development_cost(self, year, salaries, deductions, materials):
        self.development_costs.append({
            "year": year,
            "salaries": salaries,
            "deductions": deductions,
            "materials": materials
        })

    def add_servicing_cost(self, year, salaries, deductions, materials):
        self.servicing_costs.append({
            "year": year,
            "salaries": salaries,
            "deductions": deductions,
            "materials": materials
        })

    def set_purchase_cost(self, cost):
        self.purchase_cost = round(cost)
    
    def set_profit(self, profit):
        self.profit = round(profit)

    def calculate_total_development_cost(self):
        total_cost = 0
        for cost in self.development_costs:
            total_cost += sum(map(round, cost["salaries"])) + sum(map(round, cost["deductions"])) + round(cost["materials"])
        return total_cost

    def calculate_total_servicing_cost(self):
        total_cost = 0
        for cost in self.servicing_costs:
            total_cost += sum(map(round, cost["salaries"])) + sum(map(round, cost["deductions"])) + round(cost["materials"])
        return total_cost

    def get_final_value(self):
        total_cost = self.purchase_cost + self.calculate_total_development_cost() + self.calculate_total_servicing_cost()
        return round(total_cost - self.profit)

class MultiTypeIRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Универсальный информационный ресурс")
        self.root.geometry("600x600")
        self.style = ttk.Style()
        self.apply_style()

        ttk.Label(root, text="Название ИР:", style='TLabel').grid(row=0, column=0, pady=10, padx=10)
        self.ir_name = ttk.Entry(root, style='TEntry')
        self.ir_name.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(root, text="Категория ИР:", style='TLabel').grid(row=1, column=0, pady=10, padx=10)
        self.ir_category = ttk.Entry(root, style='TEntry')
        self.ir_category.grid(row=1, column=1, padx=10, pady=10)

        self.notebook = ttk.Notebook(root, style='TNotebook')
        self.notebook.grid(row=2, column=0, columnspan=3, pady=20, padx=10, sticky='nsew')

        self.create_development_tab()
        self.create_servicing_tab()
        self.create_purchase_tab()

        ttk.Button(root, text="Сохранить данные", command=self.save_data, style='TButton').grid(row=3, column=0, pady=10)
        ttk.Button(root, text="Загрузить данные", command=self.load_data, style='TButton').grid(row=3, column=1, pady=10)

        self.ir = MultiTypeIR("", "")

    def apply_style(self):
        self.style.configure('TLabel', font=('Helvetica', 12), foreground='#333', padding=5)
        self.style.configure('TEntry', font=('Helvetica', 12), padding=5)
        self.style.configure('TButton', font=('Helvetica', 12), background='#007aff', foreground='white', padding=10)
        self.style.map('TButton', background=[('active', '#005bb5')], foreground=[('active', 'white')])
        self.style.configure('TNotebook', background='#f0f0f0', padding=10)
        self.style.configure('TNotebook.Tab', font=('Helvetica', 12), padding=[10, 5])
        self.style.theme_use('clam')

    def create_development_tab(self):
        self.development_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.development_tab, text="Разработка")

        self.dev_listbox = tk.Listbox(self.development_tab, font=('Helvetica', 12), relief='flat', bg='#f9f9f9', fg='#333')
        self.dev_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.dev_listbox.bind("<Double-Button-1>", self.edit_development_cost)

        ttk.Button(self.development_tab, text="Добавить данные разработки", command=self.add_development_dialog, style='TButton').grid(row=1, column=0, columnspan=2, pady=10)

    def create_servicing_tab(self):
        self.servicing_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.servicing_tab, text="Обслуживание")

        self.serv_listbox = tk.Listbox(self.servicing_tab, font=('Helvetica', 12), relief='flat', bg='#f9f9f9', fg='#333')
        self.serv_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.serv_listbox.bind("<Double-Button-1>", self.edit_servicing_cost)

        ttk.Button(self.servicing_tab, text="Добавить данные обслуживания", command=self.add_servicing_dialog, style='TButton').grid(row=1, column=0, columnspan=2, pady=10)

    def create_purchase_tab(self):
        self.purchase_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.purchase_tab, text="Покупка")

        ttk.Label(self.purchase_tab, text="Стоимость покупки:", style='TLabel').grid(row=0, column=0, pady=10)
        self.purchase_cost = ttk.Entry(self.purchase_tab, style='TEntry')
        self.purchase_cost.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Button(self.purchase_tab, text="Установить стоимость покупки", command=self.set_purchase_cost, style='TButton').grid(row=1, column=0, columnspan=2, pady=10)

    def add_development_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить данные разработки")

        ttk.Label(dialog, text="Год разработки:", style='TLabel').grid(row=0, column=0, pady=10)
        dev_year = ttk.Combobox(dialog, values=[i for i in range(1980, 2031)], style='TEntry')
        dev_year.grid(row=0, column=1, padx=10)

        ttk.Label(dialog, text="Зарплаты (через запятую):", style='TLabel').grid(row=1, column=0, pady=10)
        dev_salaries = ttk.Entry(dialog, style='TEntry')
        dev_salaries.grid(row=1, column=1, padx=10)

        ttk.Label(dialog, text="Отчисления (через запятую):", style='TLabel').grid(row=2, column=0, pady=10)
        dev_deductions = ttk.Entry(dialog, style='TEntry')
        dev_deductions.grid(row=2, column=1, padx=10)

        ttk.Label(dialog, text="Материалы:", style='TLabel').grid(row=3, column=0, pady=10)
        dev_materials = ttk.Entry(dialog, style='TEntry')
        dev_materials.grid(row=3, column=1, padx=10)

        def add_cost():
            year = int(dev_year.get())
            salaries = list(map(int, dev_salaries.get().split(',')))
            deductions = list(map(int, dev_deductions.get().split(',')))
            materials = int(dev_materials.get())

            self.ir.add_development_cost(year, salaries, deductions, materials)
            self.update_dev_listbox()
            dialog.destroy()

        ttk.Button(dialog, text="Сохранить", command=add_cost, style='TButton').grid(row=4, column=0, columnspan=2, pady=10)

    def add_servicing_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить данные обслуживания")

        ttk.Label(dialog, text="Год обслуживания:", style='TLabel').grid(row=0, column=0, pady=10)
        serv_year = ttk.Combobox(dialog, values=[i for i in range(1980, 2031)], style='TEntry')
        serv_year.grid(row=0, column=1, padx=10)

        ttk.Label(dialog, text="Зарплаты (через запятую):", style='TLabel').grid(row=1, column=0, pady=10)
        serv_salaries = ttk.Entry(dialog, style='TEntry')
        serv_salaries.grid(row=1, column=1, padx=10)

        ttk.Label(dialog, text="Отчисления (через запятую):", style='TLabel').grid(row=2, column=0, pady=10)
        serv_deductions = ttk.Entry(dialog, style='TEntry')
        serv_deductions.grid(row=2, column=1, padx=10)

        ttk.Label(dialog, text="Материалы:", style='TLabel').grid(row=3, column=0, pady=10)
        serv_materials = ttk.Entry(dialog, style='TEntry')
        serv_materials.grid(row=3, column=1, padx=10)

        def add_cost():
            year = int(serv_year.get())
            salaries = list(map(int, serv_salaries.get().split(',')))
            deductions = list(map(int, serv_deductions.get().split(',')))
            materials = int(serv_materials.get())

            self.ir.add_servicing_cost(year, salaries, deductions, materials)
            self.update_serv_listbox()
            dialog.destroy()

        ttk.Button(dialog, text="Сохранить", command=add_cost, style='TButton').grid(row=4, column=0, columnspan=2, pady=10)

    def edit_development_cost(self, event):
        index = self.dev_listbox.curselection()[0]
        cost = self.ir.development_costs[index]
        self.open_edit_dialog("разработки", cost, index, self.ir.development_costs, self.update_dev_listbox)

    def edit_servicing_cost(self, event):
        index = self.serv_listbox.curselection()[0]
        cost = self.ir.servicing_costs[index]
        self.open_edit_dialog("обслуживания", cost, index, self.ir.servicing_costs, self.update_serv_listbox)

    def open_edit_dialog(self, title, cost, index, cost_list, update_function):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Редактировать данные {title}")

        ttk.Label(dialog, text="Год:").grid(row=0, column=0)
        year_entry = ttk.Entry(dialog)
        year_entry.insert(0, cost["year"])
        year_entry.grid(row=0, column=1)

        ttk.Label(dialog, text="Зарплаты (через запятую):").grid(row=1, column=0)
        salaries_entry = ttk.Entry(dialog)
        salaries_entry.insert(0, ",".join(map(str, cost["salaries"])))
        salaries_entry.grid(row=1, column=1)

        ttk.Label(dialog, text="Отчисления (через запятую):").grid(row=2, column=0)
        deductions_entry = ttk.Entry(dialog)
        deductions_entry.insert(0, ",".join(map(str, cost["deductions"])))
        deductions_entry.grid(row=2, column=1)

        ttk.Label(dialog, text="Материалы:").grid(row=3, column=0)
        materials_entry = ttk.Entry(dialog)
        materials_entry.insert(0, cost["materials"])
        materials_entry.grid(row=3, column=1)

        def save_changes():
            cost_list[index] = {
                "year": int(year_entry.get()),
                "salaries": list(map(int, salaries_entry.get().split(','))),
                "deductions": list(map(int, deductions_entry.get().split(','))),
                "materials": int(materials_entry.get())
            }
            update_function()
            dialog.destroy()

        ttk.Button(dialog, text="Сохранить", command=save_changes).grid(row=4, column=0, columnspan=2)

    def update_dev_listbox(self):
        self.dev_listbox.delete(0, tk.END)
        for cost in self.ir.development_costs:
            self.dev_listbox.insert(tk.END, f"{cost['year']}: зарплаты {cost['salaries']}, отчисления {cost['deductions']}, материалы {cost['materials']}")

    def update_serv_listbox(self):
        self.serv_listbox.delete(0, tk.END)
        for cost in self.ir.servicing_costs:
            self.serv_listbox.insert(tk.END, f"{cost['year']}: зарплаты {cost['salaries']}, отчисления {cost['deductions']}, материалы {cost['materials']}")

    def set_purchase_cost(self):
        cost = int(self.purchase_cost.get())
        self.ir.set_purchase_cost(cost)
        messagebox.showinfo("Стоимость установлена", "Стоимость покупки установлена!")

    def save_data(self):
        data = {
            "name": self.ir_name.get(),
            "category": self.ir_category.get(),
            "purchase_cost": self.ir.purchase_cost,
            "profit": self.ir.profit,
            "development_costs": self.ir.development_costs,
            "servicing_costs": self.ir.servicing_costs,
        }

        if os.path.exists("multi_ir_data.json"):
            with open("multi_ir_data.json", "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        if isinstance(existing_data, list):
            existing_data.append(data)
        else:
            existing_data = [existing_data, data]

        with open("multi_ir_data.json", "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Сохранение", "Данные успешно сохранены в файл.")

    def load_data(self):
        try:
            with open("multi_ir_data.json", "r", encoding="utf-8") as f:
                data_list = json.load(f)
            
            if isinstance(data_list, list):
                self.show_ir_selection_window(data_list)
            else:
                self.populate_fields(data_list)

            messagebox.showinfo("Загрузка", "Данные успешно загружены.")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке данных: {e}")

    def show_ir_selection_window(self, data_list):
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Выберите ИР")

        ttk.Label(selection_window, text="Выберите ИР для загрузки:", style='TLabel').pack(pady=10)

        for idx, ir_data in enumerate(data_list):
            ir_name = ir_data.get("name", f"ИР {idx + 1}")
            btn = ttk.Button(selection_window, text=ir_name, command=lambda d=ir_data: self.populate_fields(d), style='TButton')
            btn.pack(pady=5)

    def populate_fields(self, data):
        self.ir_name.delete(0, tk.END)
        self.ir_name.insert(0, data.get("name", ""))

        self.ir_category.delete(0, tk.END)
        self.ir_category.insert(0, data.get("category", ""))

        self.ir.set_purchase_cost(data.get("purchase_cost", 0))
        self.ir.set_profit(data.get("profit", 0))
        self.ir.development_costs = data.get("development_costs", [])
        self.ir.servicing_costs = data.get("servicing_costs", [])

        self.update_dev_listbox()
        self.update_serv_listbox()
        self.update_summary()

    def update_summary(self):
        total_dev_cost = self.ir.calculate_total_development_cost()
        total_serv_cost = self.ir.calculate_total_servicing_cost()
        final_value = self.ir.get_final_value()

        summary = (
            f"Общая стоимость разработки: {total_dev_cost} руб.\n"
            f"Общая стоимость обслуживания: {total_serv_cost} руб.\n"
            f"Стоимость покупки: {self.ir.purchase_cost} руб.\n"
            f"Прибыль: {self.ir.profit} руб.\n"
            f"Финальная стоимость (с учётом прибыли): {final_value} руб."
        )

        if hasattr(self, "summary_label"):
            self.summary_label.config(text=summary)
        else:
            self.summary_label = ttk.Label(self.root, text=summary, justify=tk.LEFT, style='TLabel')
            self.summary_label.grid(row=4, column=0, columnspan=3)

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiTypeIRApp(root)
    root.mainloop()
