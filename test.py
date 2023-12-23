import math

def temp(cycle):
    min_temp = -15
    max_temp = 15
    t_change_rate = 10000
    # Рассчитываем угол для синусоиды в пределах от 0 до 2π
    deegres = (cycle / t_change_rate) * (2 * math.pi)
    # Используем синусоиду для моделирования изменения температуры
    t_sin = math.sin(deegres)
    # Масштабируем синусоиду к диапазону от минимальной до максимальной температуры
    temp = min_temp + (t_sin + 1) * (max_temp - min_temp) / 2
    return int(temp)

cycle = 1 
while True:
    cycle += 1
    print(cycle)
    temperature = temp(cycle)
    print(f"Текущая температура: {temperature}")