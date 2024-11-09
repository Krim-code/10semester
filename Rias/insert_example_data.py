from database import create_tables, insert_resource

def insert_example_data():
    # Сведения о новых технологиях - разрабатываемый и приносящий прибыль
    insert_resource(
        name="Сведения о новых технологиях",
        category="Первая",
        rank=8,
        type_="Developed",
        cost=None,
        purchase_year=None,
        profit=7800000,
        expense=1352000  # Суммируем затраты (например, на разработку, зарплаты и прочее)
    )

    # Решения совещаний - обслуживаемый и приносящий прибыль
    insert_resource(
        name="Решения совещаний",
        category="Первая",
        rank=4,
        type_="Maintained",
        cost=None,
        purchase_year=None,
        profit=4500000,
        expense=920000  # Пример суммы затрат на обслуживание
    )

    # Бухгалтерские документы - обслуживаемый
    insert_resource(
        name="Бухгалтерские документы",
        category="Первая",
        rank=7,
        type_="Maintained",
        cost=None,
        purchase_year=None,
        profit=None,
        expense=1130000  # Пример суммы затрат на обслуживание
    )

    # Маркетинговые исследования - разрабатываемый и приносящий прибыль
    insert_resource(
        name="Маркетинговые исследования",
        category="Первая",
        rank=7,
        type_="Developed",
        cost=None,
        purchase_year=None,
        profit=3400000,
        expense=1090000  # Пример затрат на разработку
    )

    # АСУ бизнес-процессами - приобретённый, разрабатываемый и обслуживаемый
    insert_resource(
        name="АСУ бизнес-процессами",
        category="Первая",
        rank=6,
        type_="Acquired",
        cost=1620000,
        purchase_year=2021,
        profit=None,
        expense=900000  # Затраты на обслуживание и развитие
    )

    print("Примерные данные успешно добавлены в базу!")

if __name__ == "__main__":
    create_tables()  # На случай, если таблица еще не создана
    insert_example_data()
