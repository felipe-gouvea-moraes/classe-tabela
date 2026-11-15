import table as tb

if __name__ == "__main__":
    tabela = tb.Tabela(
        ['Fruta', 'Preço'],
        [
            ['Maçãzona gigantesca', 14],
            ['Banana', 4.50]
        ]
    )
    tabela.renderizar_tabela(tipo_borda='basic', fundo_cabecalhos='~')
    print(tabela.pegar_tabela(tipo_de_dado='tuple'))
    print('Soma', tabela.somar_coluna_numerica('Preço'))
