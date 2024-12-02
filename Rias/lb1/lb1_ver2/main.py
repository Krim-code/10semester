import json
import numpy as np
import pandas as pd
from scipy import stats
from rich.console import Console
from rich.table import Table
from rich import box

# Инициализация консоли Rich для красивого вывода
console = Console()

# Функция для загрузки JSON
def load_ir_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data["ir_data"]

def calc_variant11(filename):
    ir_data = load_ir_data(filename)
    
    # Индексы изменения цен
    inflation_indexes = {
        2018: 1.08,
        2019: 1.10,
        2020: 1.12,
        2021: 1.15,
        2022: 1.20
    }

    # Функции для расчета коэффициентов инфляции
    def calculate_inflation_factor(start_year, end_year):
        return np.prod([inflation_indexes[year] for year in range(start_year, end_year + 1)])

    # Функции для расчета стоимости
    def calculate_development_cost(development_years):
        total_cost = 0
        for year, details in development_years.items():
            yearly_cost = sum(emp["salary"] + emp["deductions"] for emp in details["employees"])
            yearly_cost += details["materials_costs"]
            inflation_factor = calculate_inflation_factor(int(year), 2022)
            yearly_cost *= inflation_factor
            total_cost += yearly_cost
            console.print(f"[bold yellow]Год {year}[/bold yellow]: Стоимость разработки = {yearly_cost:.2f}")
        return round(total_cost, 0)

    def calculate_acquisition_cost(acquisition_cost, acquisition_year):
        inflation_factor = calculate_inflation_factor(acquisition_year, 2022)
        total_cost = round(acquisition_cost * inflation_factor, 0)
        console.print(f"[green]Стоимость приобретения с учетом инфляции: {total_cost:.2f}[/green]")
        return total_cost

    def calculate_maintenance_cost(maintenance, years):
        yearly_cost = sum(emp["salary"] + emp["deductions"] for emp in maintenance["employees"])
        yearly_cost += maintenance["materials_costs"]
        total_cost = yearly_cost * years
        console.print(f"[cyan]Стоимость обслуживания за {years} лет: {total_cost:.2f}")
        return round(total_cost, 0)

    # Основной расчет стоимости для каждого ИР
    results = []
    for ir in ir_data:
        console.rule(f"[bold red]Расчет для {ir['name']}[/bold red]")
        
        acquisition_cost = ir.get("acquisition_cost", 0)
        if acquisition_cost:
            acquisition_cost = calculate_acquisition_cost(acquisition_cost, ir["acquisition_year"])
        
        development_cost = 0
        if "development_years" in ir:
            development_cost = calculate_development_cost(ir["development_years"])
        
        maintenance_cost = 0
        if "maintenance" in ir:
            maintenance_cost = calculate_maintenance_cost(ir["maintenance"], ir["current_year"])
        
        profit = ir.get("profit", 0)
        total_cost = acquisition_cost + development_cost + maintenance_cost - profit
        results.append({"ИР": ir["name"], "Стоимость": total_cost})
        
        console.print(f"[bold magenta]Итоговая стоимость для {ir['name']}: {total_cost:.2f}[/bold magenta]\n")

    # Присвоение рангов и сортировка
    results_df = pd.DataFrame(results)
    results_df['Ранг'] = results_df['Стоимость'].rank(ascending=False).astype(int)

    # Функции интерполяции и экстраполяции
    def extrapolate(price_list, dE, index, index_near):
        if index < index_near:
            return round(price_list[index_near] / (dE ** (index_near - index)), 3)
        else:
            return round(price_list[index_near] * (dE ** (index - index_near)), 3)

    def interpolate(price_list, dE, index, left, right):
        left_price = price_list[left] * (dE ** (index - left))
        right_price = price_list[right] / (dE ** (right - index))
        return round((left_price + right_price) / 2, 3)

    # Проверка условий и применение интерполяции/экстраполяции
    sorted_rang_price = results_df.sort_values('Ранг')['Стоимость'].values
    dEk_values = [
        (sorted_rang_price[j] / sorted_rang_price[i]) ** (1 / (j - i))
        for i, j in zip(range(len(sorted_rang_price) - 1), range(1, len(sorted_rang_price)))
        if sorted_rang_price[i] > 0 and sorted_rang_price[j] > 0
    ]

    # Вычисляем delta_dEk, используя безопасное значение, если список пуст
    delta_dEk = round(stats.gmean(dEk_values), 3) if dEk_values else 1.0

    console.rule("[bold red]Проверка условий 1.13 и 1.15 с интерполяцией и экстраполяцией[/bold red]")
    for i in range(len(sorted_rang_price)):
        if sorted_rang_price[i] == 0:
            left = next((j for j in range(i - 1, -1, -1) if sorted_rang_price[j] != 0), None)
            right = next((j for j in range(i + 1, len(sorted_rang_price)) if sorted_rang_price[j] != 0), None)
            
            if left is not None and right is not None:
                value = interpolate(sorted_rang_price, delta_dEk, i, left, right)
                console.print(f"[yellow]Интерполяция для ранга {i+1}: {value}[/yellow]")
                sorted_rang_price[i] = value
            elif left is not None:
                value = extrapolate(sorted_rang_price, delta_dEk, i, left)
                console.print(f"[yellow]Экстраполяция слева для ранга {i+1}: {value}[/yellow]")
                sorted_rang_price[i] = value
            elif right is not None:
                value = extrapolate(sorted_rang_price, delta_dEk, i, right)
                console.print(f"[yellow]Экстраполяция справа для ранга {i+1}: {value}[/yellow]")
                sorted_rang_price[i] = value

    # Таблица с итогами для всех рангов
    table = Table(title="Итоги расчета рангов", box=box.SQUARE)
    table.add_column("Ранг", justify="center", style="cyan")
    table.add_column("Стоимость", justify="right", style="green")

    for idx, cost in enumerate(sorted_rang_price):
        table.add_row(f"{idx + 1}", f"{cost:.2f}")
    
    console.print(table)

    return results_df

# Запуск функции для варианта 11 с JSON-файлом
calc_variant11("ir_data.json")
