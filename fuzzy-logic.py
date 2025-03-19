# Required packages:
# pip install numpy scikit-fuzzy matplotlib tabulate

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from tabulate import tabulate


# Generate rule matrix
def generate_rule_matrix():
    """Generate rule matrix based on fuzzy logic patterns for traffic light control"""
    rule_matrix = []
    # Define rules based on the provided table
    rules = [
        ("small", "very_small", "very_small", "increase"),
        ("small", "very_small", "small", "increase"),
        ("small", "very_small", "medium", "increase"),
        ("small", "very_small", "large", "no_change"),
        ("small", "very_small", "very_large", "no_change"),
        ("small", "small", "very_small", "increase"),
        ("small", "small", "small", "increase"),
        ("small", "small", "medium", "increase"),
        ("small", "small", "large", "no_change"),
        ("small", "small", "very_large", "no_change"),
        ("small", "medium", "very_small", "increase"),
        ("small", "medium", "small", "increase"),
        ("small", "medium", "medium", "increase"),
        ("small", "medium", "large", "increase"),
        ("small", "medium", "very_large", "no_change"),
        ("small", "large", "very_small", "increase"),
        ("small", "large", "small", "increase"),
        ("small", "large", "medium", "increase"),
        ("small", "large", "large", "increase"),
        ("small", "large", "very_large", "increase"),
        ("small", "very_large", "very_small", "increase"),
        ("small", "very_large", "small", "increase"),
        ("small", "very_large", "medium", "increase"),
        ("small", "very_large", "large", "increase"),
        ("small", "very_large", "very_large", "increase"),
        ("medium", "very_small", "very_small", "no_change"),
        ("medium", "very_small", "small", "no_change"),
        ("medium", "very_small", "medium", "decrease"),
        ("medium", "very_small", "large", "decrease"),
        ("medium", "very_small", "very_large", "decrease"),
        ("medium", "small", "very_small", "increase"),
        ("medium", "small", "small", "no_change"),
        ("medium", "small", "medium", "decrease"),
        ("medium", "small", "large", "decrease"),
        ("medium", "small", "very_large", "decrease"),
        ("medium", "medium", "very_small", "increase"),
        ("medium", "medium", "small", "increase"),
        ("medium", "medium", "medium", "no_change"),
        ("medium", "medium", "large", "decrease"),
        ("medium", "medium", "very_large", "decrease"),
        ("medium", "large", "very_small", "increase"),
        ("medium", "large", "small", "increase"),
        ("medium", "large", "medium", "increase"),
        ("medium", "large", "large", "no_change"),
        ("medium", "large", "very_large", "decrease"),
        ("medium", "very_large", "very_small", "increase"),
        ("medium", "very_large", "small", "increase"),
        ("medium", "very_large", "medium", "increase"),
        ("medium", "very_large", "large", "increase"),
        ("medium", "very_large", "very_large", "no_change"),
        ("large", "very_small", "very_small", "decrease"),
        ("large", "very_small", "small", "decrease"),
        ("large", "very_small", "medium", "decrease"),
        ("large", "very_small", "large", "decrease"),
        ("large", "very_small", "very_large", "decrease"),
        ("large", "small", "very_small", "decrease"),
        ("large", "small", "small", "decrease"),
        ("large", "small", "medium", "decrease"),
        ("large", "small", "large", "decrease"),
        ("large", "small", "very_large", "decrease"),
        ("large", "medium", "very_small", "no_change"),
        ("large", "medium", "small", "decrease"),
        ("large", "medium", "medium", "decrease"),
        ("large", "medium", "large", "decrease"),
        ("large", "medium", "very_large", "decrease"),
        ("large", "large", "very_small", "no_change"),
        ("large", "large", "small", "no_change"),
        ("large", "large", "medium", "no_change"),
        ("large", "large", "large", "decrease"),
        ("large", "large", "very_large", "decrease"),
        ("large", "very_large", "very_small", "no_change"),
        ("large", "very_large", "small", "no_change"),
        ("large", "very_large", "medium", "no_change"),
        ("large", "very_large", "large", "decrease"),
        ("large", "very_large", "very_large", "decrease"),
    ]

    for rule in rules:
        rule_matrix.append(
            {
                "green_time": rule[0],
                "cars_ns": rule[1],
                "cars_ew": rule[2],
                "time_change": rule[3],
            }
        )

    return rule_matrix


# Creating fuzzy variables
# Input variables
green_time = ctrl.Antecedent(np.arange(10, 51, 1), "green_time")
cars_ns = ctrl.Antecedent(np.arange(0, 91, 1), "cars_ns")  # North-South
cars_ew = ctrl.Antecedent(np.arange(0, 91, 1), "cars_ew")  # East-West

# Output variable
time_change = ctrl.Consequent(np.arange(-20, 21, 1), "time_change")

# Membership functions for green light time
x_green = np.arange(10, 51, 1)
green_time["small"] = fuzz.trapmf(x_green, [10, 10, 20, 25])
green_time["medium"] = fuzz.trapmf(x_green, [20, 25, 35, 40])
green_time["large"] = fuzz.trapmf(x_green, [35, 40, 50, 50])

# Membership functions for number of cars on both streets
x_cars = np.arange(0, 91, 1)
for car_var in [cars_ns, cars_ew]:
    car_var["very_small"] = fuzz.trapmf(x_cars, [0, 0, 13, 18])
    car_var["small"] = fuzz.trapmf(x_cars, [16, 21, 31, 36])
    car_var["medium"] = fuzz.trapmf(x_cars, [34, 40, 50, 56])
    car_var["large"] = fuzz.trapmf(x_cars, [54, 59, 69, 76])
    car_var["very_large"] = fuzz.trapmf(x_cars, [72, 77, 90, 90])

# Membership functions for time change
x_change = np.arange(-20, 21, 1)
time_change["decrease"] = fuzz.gaussmf(x_change, -20, 7)
time_change["no_change"] = fuzz.gaussmf(x_change, 0, 7)
time_change["increase"] = fuzz.gaussmf(x_change, 20, 7)

# Generate rule matrix called rule_matrix
rule_matrix = generate_rule_matrix()

# Print all rules with their numbers in a table format
table = [["Rule", "Green Time", "Cars NS", "Cars EW", "Time Change"]]
for i, rule in enumerate(rule_matrix, 1):
    table.append(
        [i, rule["green_time"], rule["cars_ns"], rule["cars_ew"], rule["time_change"]]
    )
print("Таблиця правил для нечіткої системи:")
print(tabulate(table, headers="firstrow", tablefmt="grid"))

# Create rules from the matrix for fuzzy system
rules = [
    ctrl.Rule(
        green_time[rule["green_time"]]
        & cars_ns[rule["cars_ns"]]
        & cars_ew[rule["cars_ew"]],
        time_change[rule["time_change"]],
    )
    for rule in rule_matrix
]

# Create control system
traffic_light_ctrl = ctrl.ControlSystem(rules)
traffic_light = ctrl.ControlSystemSimulation(traffic_light_ctrl)


def simulate_traffic_light():
    """Run a single simulation of the traffic light system"""
    # Get input values from user
    print("\nВведіть дані для моделювання роботи світлофора:")
    current_green_time = float(
        input("Час зеленого світла на вулиці ПнПв (секунди, 10-50): ")
    )
    current_cars_ns = float(input("Число машин на вулиці ПнПв (0-90): "))
    current_cars_ew = float(input("Число машин на вулиці ЗС (0-90): "))

    # Set input values
    traffic_light.input["green_time"] = current_green_time
    traffic_light.input["cars_ns"] = current_cars_ns
    traffic_light.input["cars_ew"] = current_cars_ew

    # Calculate output
    try:
        traffic_light.compute()

        # Get results
        green_time_change = traffic_light.output["time_change"]
        new_green_time = current_green_time + green_time_change

        # Ensure time stays in valid range
        new_green_time = max(10, min(50, new_green_time))

        # Display results
        print("\nРезультати моделювання:")
        print(f"Поточний час зеленого світла: {current_green_time} секунд")
        print(f"Зміна часу зеленого світла: {green_time_change:.2f} секунд")
        print(f"Новий час зеленого світла: {new_green_time:.2f} секунд")

        # Calculate red light time (assuming 60 second cycle)
        red_time = 60 - new_green_time
        print(f"Час червоного світла: {red_time:.2f} секунд")

        return True

    except Exception as e:
        print(f"Помилка обчислення: {e}. Перевірте вхідні значення.")
        return False


def run_simulation():
    """Run the simulation with option to repeat"""
    while True:
        simulate_traffic_light()

        repeat = input("\nБажаєте провести ще одну симуляцію? (так/ні): ")
        if repeat.lower() not in ["так", "yes", "y", "т"]:
            print("Моделювання завершено.")
            break


def plot_membership_functions():
    """Plot membership functions for all variables"""
    green_time.view()
    cars_ns.view()
    time_change.view()
    plt.show()


if __name__ == "__main__":
    print("=" * 70)
    print("Моделювання роботи світлофора на базі нечіткої логіки")
    print("=" * 70)
    print("Цикл світлофора: 60 секунд")
    print("Діапазон часу зеленого світла: 10-50 секунд")
    plot_membership_functions()
    run_simulation()
