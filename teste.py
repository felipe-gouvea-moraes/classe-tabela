import table as tb

if __name__ == "__main__":
    tabela = tb.Tabela(
        ['Fruta', 'Preço'],
        [
            ['Maçãzona gigantesca', 'algum valor extremamente grande por algum motivo ae'],
            ['Banana', 4.50]
        ]
    )
    tabela.renderizar_tabela(tipo_borda='basic', fundo_cabecalhos='~')