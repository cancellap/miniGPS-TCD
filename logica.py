import heapq

from dados import grafo_base


def dijkstra(grafo, inicio, fim):
    """Calcula o menor caminho entre dois nos usando o algoritmo de Dijkstra."""
    fila = [(0, inicio, [])]
    visitados = set()

    while fila:
        custo, atual, caminho = heapq.heappop(fila)

        if atual in visitados:
            continue

        caminho = caminho + [atual]
        visitados.add(atual)

        if atual == fim:
            return custo, caminho

        for vizinho, peso in grafo[atual].items():
            if vizinho not in visitados:
                heapq.heappush(fila, (custo + peso, vizinho, caminho))

    return float("inf"), []


def ajustar_grafo(clima, horario, alagada):
    """Aplica fatores de clima, horario e bloqueio por alagamento no grafo base."""
    novo = {}

    for no in grafo_base:
        novo[no] = {}
        for vizinho, peso in grafo_base[no].items():
            novo_peso = peso

            if clima == "Chuva":
                novo_peso *= 1.3

            if horario == "Pico":
                novo_peso *= 1.5

            if alagada == f"{no}-{vizinho}" or alagada == f"{vizinho}-{no}":
                continue

            novo[no][vizinho] = novo_peso

    return novo
