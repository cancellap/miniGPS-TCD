import tkinter as tk
from tkinter import ttk

from dados import grafo_base, posicoes
from logica import ajustar_grafo, dijkstra


def listar_arestas(grafo):
    """Retorna as arestas unicas do grafo no formato No1-No2."""
    arestas = []
    vistos = set()

    for no in grafo:
        for vizinho in grafo[no]:
            chave = tuple(sorted((no, vizinho)))
            if chave in vistos:
                continue
            vistos.add(chave)
            arestas.append(f"{chave[0]}-{chave[1]}")

    return arestas


def desenhar_grafo(canvas, caminho=None):
    """Desenha o grafo no canvas e destaca, em vermelho, o caminho informado."""
    if caminho is None:
        caminho = []

    canvas.delete("all")

    for no in grafo_base:
        for vizinho in grafo_base[no]:
            x1, y1 = posicoes[no]
            x2, y2 = posicoes[vizinho]

            cor = "black"
            largura = 1

            for i in range(len(caminho) - 1):
                if (no == caminho[i] and vizinho == caminho[i + 1]) or (
                    vizinho == caminho[i] and no == caminho[i + 1]
                ):
                    cor = "red"
                    largura = 3

            canvas.create_line(x1, y1, x2, y2, fill=cor, width=largura)

    for no, (x, y) in posicoes.items():
        canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="lightblue")
        canvas.create_text(x, y - 15, text=no)


def criar_app():
    """Cria e configura a janela principal com controles e area de desenho."""
    root = tk.Tk()
    root.title("Mini GPS com Dijkstra")

    canvas = tk.Canvas(root, width=480, height=280, bg="white")
    canvas.grid(row=0, column=0, rowspan=6)

    origem_var = tk.StringVar(value="A")
    destino_var = tk.StringVar(value="H")
    clima_var = tk.StringVar(value="Normal")
    horario_var = tk.StringVar(value="Normal")
    alagamento_var = tk.StringVar(value="Nenhum")
    opcoes_alagamento = ["Nenhum", *listar_arestas(grafo_base)]

    ttk.Label(root, text="Origem").grid(row=0, column=1)
    ttk.Combobox(root, textvariable=origem_var, values=list(grafo_base.keys())).grid(
        row=0, column=2
    )

    ttk.Label(root, text="Destino").grid(row=1, column=1)
    ttk.Combobox(root, textvariable=destino_var, values=list(grafo_base.keys())).grid(
        row=1, column=2
    )

    ttk.Label(root, text="Clima").grid(row=2, column=1)
    ttk.Combobox(root, textvariable=clima_var, values=["Normal", "Chuva"]).grid(
        row=2, column=2
    )

    ttk.Label(root, text="Horário").grid(row=3, column=1)
    ttk.Combobox(root, textvariable=horario_var, values=["Normal", "Pico"]).grid(
        row=3, column=2
    )

    ttk.Label(root, text="Alagamento").grid(row=4, column=1)
    ttk.Combobox(
        root,
        textvariable=alagamento_var,
        values=opcoes_alagamento,
    ).grid(row=4, column=2)

    resultado_label = ttk.Label(root, text="Resultado aparecerá aqui")
    resultado_label.grid(row=6, column=0, columnspan=3)

    def calcular_rota():
        """Le valores da interface, calcula rota e atualiza resultado e desenho."""
        origem = origem_var.get()
        destino = destino_var.get()
        clima = clima_var.get()
        horario = horario_var.get()
        alagada = alagamento_var.get()

        grafo = ajustar_grafo(clima, horario, alagada)
        custo, caminho = dijkstra(grafo, origem, destino)

        resultado_label.config(
            text=f"Caminho: {' → '.join(caminho)} | Custo: {round(custo, 2)}"
        )

        desenhar_grafo(canvas, caminho)

    ttk.Button(root, text="Calcular rota", command=calcular_rota).grid(
        row=5, column=1, columnspan=2
    )

    desenhar_grafo(canvas)

    return root
