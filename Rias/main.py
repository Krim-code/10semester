import tkinter as tk
from tkinter import ttk
from database import create_tables, insert_resource, fetch_resources, delete_resource

# Сначала создаём таблицы, чтобы избежать ошибок
create_tables()

def calculate_cost(resource):
    total_cost = 0
    type_ = resource["type"]
    start_year = resource["start_year"]
    duration = resource["duration"]
    cost = resource["cost"]
    expense = resource["expense"]
    profit = resource["profit"]

    # Индексы инфляции
    inflation = {2018: 1.08, 2019: 1.10, 2020: 1.12, 2021: 1.15, 2022: 1.17}

    if type_ == "Приобретённый":
        purchase_year = resource["purchase_year"]
        total_cost = cost * inflation.get(purchase_year, 1)
    elif type_ == "Разрабатываемый":
        for year in range(start_year, start_year + duration):
            total_cost += resource["material_expense"] * inflation.get(year, 1)
            salaries = map(int, resource["salary"].split(","))
            total_cost += sum(salaries)
    elif type_ == "Обслуживаемый":
        total_cost = expense
    elif type_ == "Приносящий прибыль":
        total_cost = profit - expense

    return round(total_cost)

def update_form():
    type_ = type_combobox.get()
    cost_label.grid_remove()
    cost_entry.grid_remove()
    purchase_year_label.grid_remove()
    purchase_year_entry.grid_remove()
    profit_label.grid_remove()
    profit_entry.grid_remove()
    expense_label.grid_remove()
    expense_entry.grid_remove()
    start_year_label.grid_remove()
    start_year_entry.grid_remove()
    duration_label.grid_remove()
    duration_entry.grid_remove()
    employees_label.grid_remove()
    employees_entry.grid_remove()
    salary_label.grid_remove()
    salary_entry.grid_remove()
    deductions_label.grid_remove()
    deductions_entry.grid_remove()
    material_expense_label.grid_remove()
    material_expense_entry.grid_remove()

    if type_ == "Приобретённый":
        cost_label.grid()
        cost_entry.grid()
        purchase_year_label.grid()
        purchase_year_entry.grid()
    elif type_ == "Разрабатываемый" or type_ == "Приносящий прибыль":
        start_year_label.grid()
        start_year_entry.grid()
        duration_label.grid()
        duration_entry.grid()
        employees_label.grid()
        employees_entry.grid()
        salary_label.grid()
        salary_entry.grid()
        deductions_label.grid()
        deductions_entry.grid()
        material_expense_label.grid()
        material_expense_entry.grid()
    elif type_ == "Обслуживаемый":
        expense_label.grid()
        expense_entry.grid()

def refresh_table():
    for item in table.get_children():
        table.delete(item)
    resources = fetch_resources()
    for resource in resources:
        table.insert("", "end", values=resource)

def add_resource():
    name = name_entry.get()
    category = category_entry.get()
    rank = int(rank_entry.get())
    type_ = type_combobox.get()
    cost = int(cost_entry.get()) if cost_entry.get() else None
    purchase_year = int(purchase_year_entry.get()) if purchase_year_entry.get() else None
    profit = int(profit_entry.get()) if profit_entry.get() else None
    expense = int(expense_entry.get()) if expense_entry.get() else None
    start_year = int(start_year_entry.get()) if start_year_entry.get() else None
    duration = int(duration_entry.get()) if duration_entry.get() else None
    num_employees = int(employees_entry.get()) if employees_entry.get() else None
    salary = salary_entry.get()
    deductions = deductions_entry.get()
    material_expense = int(material_expense_entry.get()) if material_expense_entry.get() else None

    insert_resource(name, category, rank, type_, cost, purchase_year, profit, expense,
                    start_year, duration, num_employees, salary, deductions, material_expense)

    refresh_table()

def delete_selected_resource():
    selected_item = table.selection()
    if selected_item:
        item = table.item(selected_item)
        resource_id = item["values"][0]
        delete_resource(resource_id)
        refresh_table()

# Создаём окно
app = tk.Tk()
app.title("Управление ИР")

# Форма добавления ресурса
tk.Label(app, text="Название").grid(row=0, column=0)
name_entry = tk.Entry(app)
name_entry.grid(row=0, column=1)

tk.Label(app, text="Категория").grid(row=1, column=0)
category_entry = tk.Entry(app)
category_entry.grid(row=1, column=1)

tk.Label(app, text="Ранг").grid(row=2, column=0)
rank_entry = tk.Entry(app)
rank_entry.grid(row=2, column=1)

tk.Label(app, text="Тип").grid(row=3, column=0)
type_combobox = ttk.Combobox(app, values=["Приобретённый", "Разрабатываемый", "Обслуживаемый", "Приносящий прибыль"])
type_combobox.grid(row=3, column=1)
type_combobox.bind("<<ComboboxSelected>>", lambda event: update_form())

# Специфические поля
cost_label = tk.Label(app, text="Стоимость")
cost_entry = tk.Entry(app)
purchase_year_label = tk.Label(app, text="Год приобретения")
purchase_year_entry = tk.Entry(app)

profit_label = tk.Label(app, text="Прибыль")
profit_entry = tk.Entry(app)

expense_label = tk.Label(app, text="Затраты")
expense_entry = tk.Entry(app)

start_year_label = tk.Label(app, text="Год начала")
start_year_entry = tk.Entry(app)

duration_label = tk.Label(app, text="Длительность")
duration_entry = tk.Entry(app)

employees_label = tk.Label(app, text="Кол-во сотрудников")
employees_entry = tk.Entry(app)

salary_label = tk.Label(app, text="Зарплата (через запятую)")
salary_entry = tk.Entry(app)

deductions_label = tk.Label(app, text="Отчисления (через запятую)")
deductions_entry = tk.Entry(app)

material_expense_label = tk.Label(app, text="Расходы на материалы")
material_expense_entry = tk.Entry(app)

tk.Button(app, text="Добавить ИР", command=add_resource).grid(row=15, column=0, columnspan=2)
tk.Button(app, text="Удалить ИР", command=delete_selected_resource).grid(row=16, column=0, columnspan=2)

# Таблица для отображения ресурсов
columns = ("id", "Название", "Категория", "Ранг", "Тип", "Стоимость", "Год приобретения", "Прибыль", "Затраты",
           "Год начала", "Длительность", "Кол-во сотрудников", "Зарплата", "Отчисления", "Расходы на материалы")
table_frame = tk.Frame(app)
table_frame.grid(row=17, column=0, columnspan=3)

# Добавляем скроллбары
x_scrollbar = tk.Scrollbar(table_frame, orient="horizontal")
y_scrollbar = tk.Scrollbar(table_frame, orient="vertical")
table = ttk.Treeview(table_frame, columns=columns, show="headings", xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

x_scrollbar.config(command=table.xview)
y_scrollbar.config(command=table.yview)

x_scrollbar.pack(side="bottom", fill="x")
y_scrollbar.pack(side="right", fill="y")
table.pack(side="left", fill="both", expand=True)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120)

refresh_table()
create_tables()
app.mainloop()
