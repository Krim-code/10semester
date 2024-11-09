import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

# Данные по варианту 11
z_factors = np.array([
    [-1, -1, -1, -1], [-1, -1, -1, 1], [-1, -1, 1, -1], [-1, -1, 1, 1], 
    [-1, 1, -1, -1], [-1, 1, -1, 1], [-1, 1, 1, -1], [-1, 1, 1, 1],
    [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, -1], [1, -1, 1, 1],
    [1, 1, -1, -1], [1, 1, -1, 1], [1, 1, 1, -1], [1, 1, 1, 1]
])

# Значения y (результаты экспериментов для трех повторов)
y_observations = np.array([
    [-9.79, -11.10, -10.12], [1.51, 1.53, 1.26], [-23.81, -24.97, -23.58], 
    [25.53, 22.75, 27.30], [-8.02, -6.70, -7.80], [5.32, 6.12, 6.06], 
    [-10.41, -11.05, -9.47], [-14.24, -13.02, -14.51], [-22.01, -19.10, -20.14], 
    [-16.74, -17.30, -18.41], [12.40, 11.80, 12.76], [0.67, 0.70, 0.75],
    [-2.10, -2.26, -2.44], [-4.90, -4.71, -4.28], [-1.37, -1.43, -1.64], 
    [76.04, 85.23, 91.92]
])

# Средние значения y для каждого эксперимента
y_mean = np.mean(y_observations, axis=1)

# Полный факторный эксперимент с парными взаимодействиями
X_full = np.hstack([z_factors, z_factors[:, 0:1] * z_factors[:, 1:2],
                    z_factors[:, 0:1] * z_factors[:, 2:3], z_factors[:, 0:1] * z_factors[:, 3:4],
                    z_factors[:, 1:2] * z_factors[:, 2:3], z_factors[:, 1:2] * z_factors[:, 3:4],
                    z_factors[:, 2:3] * z_factors[:, 3:4], 
                    z_factors[:, 0:1] * z_factors[:, 1:2] * z_factors[:, 2:3] * z_factors[:, 3:4]])

# Добавляем столбец единиц для свободного члена
X_full = np.hstack([np.ones((16, 1)), X_full])

# Функция для расчета коэффициентов методом наименьших квадратов
def calculate_regression_coefficients(X, y):
    model = LinearRegression(fit_intercept=True)
    model.fit(X, y)
    return model.coef_, model.intercept_

# Функция для проверки значимости коэффициентов через критерий Стьюдента
def check_significance(b, X, y_variance, n, m, alpha):
    # Стандартные ошибки коэффициентов
    s2_b = np.sum(y_variance) / (n * m)
    s_b = np.sqrt(s2_b / np.sum(X**2, axis=0))

    # Расчет t-статистики
    t_values = np.abs(b) / s_b

    # Критическое значение t-критерия
    t_critical = stats.t.ppf(1 - alpha / 2, df=(n * (m - 1)))

    # Выбираем значимые коэффициенты
    significant_b = b[np.where(t_values > t_critical)]
    return t_values, t_critical, significant_b

# Функция для проверки адекватности модели через критерий Фишера
def check_model_adequacy(y_real, y_pred, y_variance, n, m, r):
    # Остаточная дисперсия
    residual_dispersion = np.sum((y_real - y_pred) ** 2) / (n - r)

    # Дисперсия воспроизводимости
    reproduction_dispersion = np.sum(y_variance) / n

    # Критерий Фишера
    F = residual_dispersion / reproduction_dispersion
    F_critical = stats.f.ppf(1 - alpha, dfn=n - r, dfd=n * (m - 1))

    return F, F_critical

# Рассчитываем коэффициенты
b, intercept = calculate_regression_coefficients(X_full, y_mean)

# Дисперсия по экспериментам
y_variance = np.var(y_observations, axis=1, ddof=1)

# Параметры для тестов
n = 16  # количество экспериментов
m = 3   # количество повторов
alpha = 0.05  # уровень значимости

# Проверяем значимость коэффициентов
t_values, t_critical, significant_b = check_significance(b, X_full, y_variance, n, m, alpha)

# Прогнозируем значения на основе модели
y_pred = np.dot(X_full, b) + intercept

# Проверяем адекватность модели
F_value, F_critical = check_model_adequacy(y_mean, y_pred, y_variance, n, m, len(significant_b))

# Выводим результаты
print("Коэффициенты регрессии:", b)
print("Значимые коэффициенты:", significant_b)
print("t-значения:", t_values)
print("Критическое значение t-критерия:", t_critical)
print("F-значение:", F_value)
print("Критическое значение F-критерия:", F_critical)
