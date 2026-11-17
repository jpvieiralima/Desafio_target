"""Desafio 2 - Movimentação de estoque (entrada e saída)."""

import json
from pathlib import Path

ARQUIVO_ESTOQUE = Path(__file__).parent / "dados" / "estoque.json"


class Estoque:
    def __init__(self, produtos):
        # Guarda os produtos pelo código para achar mais fácil
        self.produtos = {p["codigoProduto"]: p for p in produtos}
        self.movimentacoes = []
        self.proximo_id = 1

    def movimentar(self, codigo, tipo, quantidade, descricao):
        """Registra uma entrada ou saída e devolve o estoque final do produto."""
        if codigo not in self.produtos:
            raise ValueError(f"Produto {codigo} não encontrado.")
        if tipo not in ("entrada", "saida"):
            raise ValueError("Tipo deve ser 'entrada' ou 'saida'.")
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        produto = self.produtos[codigo]
        if tipo == "saida" and quantidade > produto["estoque"]:
            raise ValueError(
                f"Estoque insuficiente. Disponível: {produto['estoque']}."
            )

        if tipo == "entrada":
            produto["estoque"] += quantidade
        else:
            produto["estoque"] -= quantidade

        self.movimentacoes.append({
            "id": self.proximo_id,
            "codigoProduto": codigo,
            "tipo": tipo,
            "quantidade": quantidade,
            "descricao": descricao,
        })
        self.proximo_id += 1

        return produto["estoque"]


def carregar_estoque():
    with open(ARQUIVO_ESTOQUE, encoding="utf-8") as arquivo:
        return Estoque(json.load(arquivo)["estoque"])


def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro válido.")


def listar_produtos(estoque):
    print("\nProdutos:")
    for p in estoque.produtos.values():
        print(f"  {p['codigoProduto']} - {p['descricaoProduto']:<28} estoque: {p['estoque']}")


def listar_movimentacoes(estoque):
    if not estoque.movimentacoes:
        print("\nNenhuma movimentação lançada ainda.")
        return
    print("\nMovimentações:")
    for m in estoque.movimentacoes:
        print(f"  #{m['id']} | produto {m['codigoProduto']} | {m['tipo']:<7} | "
              f"qtde {m['quantidade']} | {m['descricao']}")


def lancar_movimentacao(estoque, tipo):
    codigo = ler_inteiro("Código do produto: ")
    quantidade = ler_inteiro("Quantidade: ")
    descricao = input("Descrição da movimentação: ").strip() or tipo.capitalize()

    try:
        saldo = estoque.movimentar(codigo, tipo, quantidade, descricao)
    except ValueError as erro:
        print(f"Erro: {erro}")
        return

    produto = estoque.produtos[codigo]
    movimento = estoque.movimentacoes[-1]
    print(f"Movimentação #{movimento['id']} registrada.")
    print(f"Estoque final de {produto['descricaoProduto']}: {saldo}")


def main():
    estoque = carregar_estoque()

    while True:
        print("\n=== Controle de Estoque ===")
        print("1 - Listar produtos")
        print("2 - Lançar entrada")
        print("3 - Lançar saída")
        print("4 - Ver movimentações")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            listar_produtos(estoque)
        elif opcao == "2":
            lancar_movimentacao(estoque, "entrada")
        elif opcao == "3":
            lancar_movimentacao(estoque, "saida")
        elif opcao == "4":
            listar_movimentacoes(estoque)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
