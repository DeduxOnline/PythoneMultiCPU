import time  # Імпорт модуля для роботи з часом
from multiprocessing import Pool, cpu_count  # Імпорт необхідних класів для мультипроцесингу та визначення кількості ядер CPU
import sys  # Імпорт модуля для доступу до системних функцій
sys.setrecursionlimit(10**6)  # Встановлення максимальної глибини рекурсії

def multiply_even_numbers_recursive(n):
    """Функція для обчислення парного факторіалу рекурсивно."""
    if n < 2:
        return 1
    elif n % 2 == 0:
        return n * multiply_even_numbers_recursive(n - 2)
    else:
        return multiply_even_numbers_recursive(n - 1)

def multiply_even_numbers_multiprocess(user_input, max_processes):
    """Функція для обчислення парного факторіалу з використанням паралельного обчислення."""
    with Pool(processes=max_processes) as pool:
        results = pool.map(multiply_even_numbers_recursive, range(2, user_input + 1, 2))
    return results

if __name__ == "__main__":
    print("Рекурсивне обчислення парного факторіалу з паралельним алгоритмом")

    user_input = input("Введіть початкове число (за замовчуванням = 1000): ").strip()
    if user_input == '': user_input = 1000
    else: user_input = int(user_input)

    num_test = input("Кількість тестів (за замовчуванням = 10): ").strip()
    if num_test == '': num_test = 10
    else: num_test = int(num_test)

    step = input("Крок (за замовчуванням = 1000): ").strip()
    if step == '': step = 1000
    else: step = int(step)

    cpu = input("Кількість ядер (за замовчуванням = кількість ядер в ПК): ").strip()
    if cpu == '':  cpu = cpu_count()
    else: cpu = int(cpu)
 
    print(f"Налаштування ==> Число = {user_input} | Кількість тестів = {num_test} | Крок = {step} | Кількість ядер = {cpu} ")
    for t in range(num_test):
        if t > 0: user_input += step
        print(f"Тест №{t+1} => Число = {user_input}")
        for max_processes in range(1, cpu + 1):
            start_time = time.time()
            result = multiply_even_numbers_multiprocess(int(user_input), max_processes)
            end_time = time.time()
            print(f"--> {max_processes} кількість процесів -> Час виконання: {end_time - start_time:.3f} секунд")
            # print(f"--> Відповідь: {result[-1]}")
    input("Тест ЗАВЕРШЕНО. Натисніть клавішу, щоб вийти")
