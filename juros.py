"""Desafio 3 - Juros por atraso (2,5% ao dia sobre o valor original)."""

from datetime import date, datetime

from comissao import formatar_reais

TAXA_DIARIA = 0.025


def calcular_juros(valor, vencimento, hoje=None):
    """Retorna (dias de atraso, valor dos juros). Sem atraso, juros é zero."""
    hoje = hoje or date.today()
    dias_atraso = max((hoje - vencimento).days, 0)
    juros = round(valor * TAXA_DIARIA * dias_atraso, 2)
    return dias_atraso, juros


def main():
    try:
        valor = float(input("Valor (ex: 150.00): ").replace(",", "."))
        vencimento = datetime.strptime(
            input("Data de vencimento (dd/mm/aaaa): ").strip(), "%d/%m/%Y"
        ).date()
    except ValueError:
        print("Valor ou data inválidos.")
        return

    if valor <= 0:
        print("O valor deve ser maior que zero.")
        return

    dias, juros = calcular_juros(valor, vencimento)

    print(f"\nData de hoje: {date.today():%d/%m/%Y}")
    print(f"Dias em atraso: {dias}")
    print(f"Juros: {formatar_reais(juros)}")
    print(f"Valor total a pagar: {formatar_reais(valor + juros)}")


if __name__ == "__main__":
    main()
