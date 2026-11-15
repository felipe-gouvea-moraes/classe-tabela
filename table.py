from typing import Any

class Tabela:
    def __init__(self, cabecalhos: list[str], dados: list[list[Any]]) -> None:
        self.cabecalhos: list[str] = cabecalhos
        self.dados: list[list[Any]] = dados
        self.linhas: int = len(self.dados)
        self.colunas: int = len(self.dados[0]) if self.dados else 0
        self.dados_por_coluna: list[list[Any]] = linha_para_coluna(self.dados)

    def somar_coluna_numerica(self, nome_cabecalho: str) -> float | int:
        '''Recebe o nome de um cabeçalho, soma todos os valores da coluna dele e retorna este valor.\n
        **Retorna *False* caso algum valor não seja um int ou float (como list, str, bool etc.)**'''
        indice_coluna: int = self.cabecalhos.index(nome_cabecalho)
        soma: float | int = 0
        for valor in self.dados_por_coluna[indice_coluna]:
            tipo_valor = str(type(valor))
            if tipo_valor != "<class 'int'>" and tipo_valor != "<class 'float'>":
                return False
            soma += valor
        return soma

    def pegar_tabela(self, tipo_de_dado: str = 'list') -> list[list[any]] | list[dict] | list[tuple]:
        '''Retorna a tabela total em diferentes tipos de dado, pode ser mudado alterando o parâmetro tipo_de_dado para:
        - **'list'**: Padrão de chamada, retorna a matriz bidimensional com os cabeçalhos.
        - **'dict'**: Retorna uma lista de dicionários, com a chave sendo igual a o cabeçalho da coluna.
        - **'tuple'**: Retorna uma lista de tuplas, útil para desempacotamento, cada tupla tem os valores de uma lista.'''
        base_de_dados: list = []
        match tipo_de_dado:
            case 'list':
                base_de_dados = [self.cabecalhos].extend(self.dados)
            case 'dict':
                base_de_dados = []
                for linha in self.dados:
                    dicio = dict()
                    dicio.update(zip(self.cabecalhos, linha))
                    base_de_dados.append(dicio)
            case 'tuple':
                for linha in self.dados:
                    base_de_dados.append(tuple(linha))
        return base_de_dados


    def renderizar_tabela(self, tipo_borda: str = 'none', fundo_cabecalhos=' ') -> None:
        larguras: list[int] = largura_por_coluna(self.dados_por_coluna, self.cabecalhos)
        cantos, conectores, linhas = obter_caracteres(tipo_borda)

        if not cantos or not conectores or not linhas:
            linha_valores: str = '\033[1m'.join(f'{str(v):^{larguras[i]}}' for i, v in enumerate(self.cabecalhos))
            print(linha_valores, '\033[0m')
            for linha in self.dados:
                linha_valores: str = ''.join(f'{str(v):<{larguras[i]}}' for i, v in enumerate(linha))
                print(linha_valores)
            return

        texto_por_bordas: list[str] = gerar_linhas_borda(larguras, cantos, conectores, linhas)
        texto_por_linha: list[str] = []
        
        texto_por_linha.append(texto_por_bordas[0])
        
        linha_cabecalhos = linhas[1]
        for id_coluna, cabecalho in enumerate(self.cabecalhos):
            linha_cabecalhos += f'{str(cabecalho):{fundo_cabecalhos}^{larguras[id_coluna]}}'
            linha_cabecalhos += linhas [1]

        texto_por_linha.append(linha_cabecalhos)
        texto_por_linha.append(texto_por_bordas[1])

        for id_linha, linha in enumerate(self.dados):
            linha_valores = linhas[1]
            
            for id_coluna, valor in enumerate(linha):
                linha_valores += f'{str(valor):<{larguras[id_coluna]}}'
                linha_valores += linhas[1]
            
            texto_por_linha.append(linha_valores)
            
            if id_linha < len(self.dados) - 1:
                texto_por_linha.append(texto_por_bordas[1])
                
        texto_por_linha.append(texto_por_bordas[2])
        
        for linha_pronta in texto_por_linha:
            print(linha_pronta)


def gerar_linhas_borda(
    tamanhos: list[int], 
    cantos: list[str], 
    conectores: list[str], 
    linhas: list[str]
) -> list[str]:
    linhas_tabela: list[str] = [cantos[0], conectores[1], cantos[2]]
    
    for tamanho in tamanhos:
        for indice in range(len(linhas_tabela)):
            linhas_tabela[indice] += linhas[0] * tamanho
            match indice:
                case 0:
                    adicao: str = conectores[0]
                case 1:
                    adicao: str = conectores[3]
                case 2:
                    adicao: str = conectores[4]
            linhas_tabela[indice] += adicao
            
    for indice in range(len(linhas_tabela)):
        match indice:
            case 0:
                adicao = cantos[1]
            case 1:
                adicao = conectores[2]
            case 2:
                adicao = cantos[3]
        linhas_tabela[indice] = linhas_tabela[indice][:-1] + adicao
        
    return linhas_tabela


def obter_caracteres(tipo_borda: str) -> tuple[list[str], list[str], list[str]] | tuple[None, None, None]:
    match tipo_borda:
        case 'none':
            return (None, None, None)
        case 'basic':
            cantos: list[str] = ['┌', '┐', '└', '┘']
            conectores: list[str] = ['┬', '├', '┤', '┼', '┴']
            linhas: list[str] = ['─', '│']
        case 'sketch':
            cantos = ['+', '+', '+', '+']
            conectores = ['+', '+', '+', '+', '+']
            linhas = ['-', '|']
        case 'bold':
            cantos = ['┏', '┓', '┗', '┛']
            conectores = ['┳', '┣', '┫', '╋', '┻']
            linhas = ['━', '┃']
        case 'double':
            cantos = ['╔', '╗', '╚', '╝']
            conectores = ['╦', '╠', '╣', '╬', '╩']
            linhas = ['═', '║']
        case _:
            return (None, None, None)
            
    return (cantos, conectores, linhas)


def linha_para_coluna(matriz: list[list[Any]]) -> list[list[Any]]:
    if not matriz:
        return []
    quant_colunas: int = len(matriz[0])
    nova_matriz: list[list[Any]] = []
    for indice_coluna in range(quant_colunas):
        coluna: list[Any] = [linha[indice_coluna] for linha in matriz]
        nova_matriz.append(coluna)
    return nova_matriz


def largura_por_coluna(dados_coluna: list[list[Any]], cabecalhos: list[str]) -> list[int]:
    larguras: list[int] = []
    for indice, coluna in enumerate(dados_coluna):
        maior_largura: int = len(str(cabecalhos[indice])) if cabecalhos and indice < len(cabecalhos) else 0
        for valor in coluna:
            if len(str(valor)) > maior_largura:
                maior_largura = len(str(valor))
        larguras.append(maior_largura)
    return larguras