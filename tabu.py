import random

import data_pre_processing
import astar


def tabu_search(graph, start, stops):
    # Inicjalizacja listy tabu
    tabu_list = []
    # Inicjalizacja najlepszego rozwiązania
    best_solution = None
    # Inicjalizacja najlepszego kosztu
    best_cost = float('inf')
    # Inicjalizacja aktualnego rozwiązania
    current_solution = [start[0]] + [[i[0] for i in stops]] + [start[0]]
    # Inicjalizacja aktualnego kosztu
    current_cost = calculate_cost(graph, current_solution)
    # Pętla główna
    while len(tabu_list) < 20:
        # Wygenerowanie sąsiedniego rozwiązania
        neighbor_solution = generate_neighbor(current_solution)
        # Obliczenie kosztu sąsiedniego rozwiązania
        neighbor_cost = calculate_cost(graph, neighbor_solution)
        # Sprawdzenie czy sąsiednie rozwiązanie jest lepsze niż aktualne rozwiązanie
        if neighbor_cost < current_cost:
            # Aktualizacja najlepszego rozwiązania, jeśli to możliwe
            if neighbor_cost < best_cost:
                best_solution = neighbor_solution
                best_cost = neighbor_cost
            # Aktualizacja aktualnego rozwiązania
            current_solution = neighbor_solution
            current_cost = neighbor_cost
        else:
            # Dodanie ruchu do listy tabu, jeśli to możliwe
            if neighbor_solution not in tabu_list:
                tabu_list.append(neighbor_solution)
            # Losowe wybranie rozwiązania spośród ruchów tabu
            current_solution = random.choice(tabu_list)
            current_cost = calculate_cost(graph, current_solution)
    # Zwrócenie najlepszego rozwiązania
    return best_solution

def generate_neighbor(solution):
    # Wygenerowanie sąsiedniego rozwiązania przez zamianę dwóch węzłów
    neighbor = solution[:]
    i, j = random.sample(range(1, len(solution) - 1), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def calculate_cost(graph, solution,):
    return random.randrange(1,100)


# Przykładowe użycie
graph = data_pre_processing.create_graph('connection_graph.csv')
start = astar.get_nodes_by_name(graph,"Kościuszki","11:55:00")

most = astar.get_nodes_by_name(graph,"pl. Wróblewskiego","11:55:00")
kliniki = astar.get_nodes_by_name(graph,"Kliniki - Politechnika Wrocławska","11:55:00")

stops = [most,kliniki]
print(tabu_search(graph, start, stops))  # ['A', 'D', 'C', 'B', 'A']