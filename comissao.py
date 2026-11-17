"""Desafio 1 - Cálculo de comissão por vendedor."""

import json
from pathlib import Path

ARQUIVO_VENDAS = Path(__file__).parent / "dados" / "vendas.json"


def calcular_comissao(valor):
    """Retorna a comissão de uma única venda."""
    if valor < 100:
        return 0.0
    if valor < 500:
        return valor * 0.01
    return valor * 0.05


def comissao_por_vendedor(vendas):
    """Soma a comissão de todas as vendas de cada vendedor."""
    totais = {}
    for venda in vendas:
        nome = venda["vendedor"]
        totais[nome] = totais.get(nome, 0) + calcular_comissao(venda["valor"])

    # Arredonda só no final para não acumular erro de arredondamento
    return {nome: round(total, 2) for nome, total in totais.items()}


def formatar_reais(valor):
    # Formato brasileiro: 1.234,56
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    with open(ARQUIVO_VENDAS, encoding="utf-8") as arquivo:
        vendas = json.load(arquivo)["vendas"]

    print("Comissão por vendedor")
    print("-" * 35)
    for nome, total in comissao_por_vendedor(vendas).items():
        print(f"{nome:<20} {formatar_reais(total):>14}")


if __name__ == "__main__":
    main()
