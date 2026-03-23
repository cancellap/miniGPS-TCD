from interface import criar_app


def main():
    """Inicializa a interface principal e inicia o loop da aplicacao."""
    app = criar_app()
    app.mainloop()


if __name__ == "__main__":
    main()