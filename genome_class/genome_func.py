


def self_get_next_index_of_bias(bot, step, len_of_number):
    """
    Функция получения смещения.
    Используется для получения условия на основе числа смещения
    [...33,43,24,...]
    [... 5, 6, 7,...]
    Пример self.ptr = 5
           step = 1
           index = 6
    Так как мы к self.ptr прибавили step и получили индекс смешение по гену
    len_of_number число ограничитель (К примеру если len_of_number является len(cfg.move_directions)
    то мы получим значение ограниченное количеством направлений от числа в гене
    43 % 8 - кол-во направлений = 3 - Вправо и низ)
    """
    ptr = bot[4]
    dna = bot[6:]
    index = (ptr + step) % len(dna)  # Индекс смещения
    index_of_bias = dna[index] % len_of_number
    return index_of_bias


def self_get_next_index(bot, step):
    """
    Функция получения следующего индекса смешения
    используется для увеличения УТК на число полученное в смешении
    [...33,43,24,...]
    [... 5, 6, 7,...]
    Пример self.ptr = 5
           step = 1
           index = 6
    В данном примере УТК переместится на 43 (и остановится на 48) от позиции где он находился (Это self.ptr = 5)
    """
    ptr = bot[4]
    dna = bot[6:]
    index = (ptr + step) % len(dna)
    ptr = (ptr + dna[index]) % len(dna)
    return ptr


def self_get_bias(bot, step):
    ptr = bot[4]
    dna = bot[6:]
    index = (ptr + step) % len(dna)
    bias = dna[index]
    return bias


def move_ptr_to(bot):
    ptr = bot[4]
    dna = bot[6:]
    # Перемещение УТК к следующей команде на основе числа безусловного перехода
    bot[4] = (ptr + dna[ptr]) % len(dna)


# Функция перемещения указателя текущей команды

def move_ptr(bot):
    ptr = bot[4]
    dna = bot[6:]
    # Перемещения УТК к следующей команде
    bot[4] = (ptr + 1) % len(dna)