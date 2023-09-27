import numpy as np

def score_game(random_predict) -> int:
    """За какое количество попыток в среднем за 10000 подходов угадывает наш алгоритм

    Args:
        random_predict ([type]): функция угадывания

    Returns:
        int: среднее количество попыток
    """
    count_ls = []
    #np.random.seed(1)  # фиксируем сид для воспроизводимости
    random_array = np.random.randint(1, 101, size=(10000))  # загадали список чисел

    for number in random_array:
        count_ls.append(random_predict(number))

    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за: {score} попытки")


def game_core_v3(number: int = 1) -> int:
    """Сначала устанавливаем любое random число, а потом уменьшаем пределы 
    его генерации в зависимости от того больше или меньше это число, искомого
       
       Функция принимает загаданное число и возвращает число попыток
       
    Args:
        number (int, optional): Загаданное число. Defaults to 1.

    Returns:
        int: Число попыток
    """
    count = 0
    left, right = 1, 101 # устанавливаем пределы для генерации случайного числа
    predict = np.random.randint(left, right)

    while predict != number:
      count += 1
      if predict < number: 
        left = predict # сдвигаем нижний предел генерации
      elif predict > number: 
        right = predict # сдвигаем верхний предел генерации
      predict = np.random.randint(left, right) # генерируем новое случайное число

    return count

#RUN
print('Run benchmarking for game_core_v3: ', end='')
score_game(game_core_v3)