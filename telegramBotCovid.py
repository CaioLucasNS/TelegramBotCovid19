import requests, telepot, schedule
from time import sleep


def casos_por_pais(pais='countries'):
    """
    Função para filtrar dados dos países ao redor do mundo ou os dados de um único país,
    se o mesmo for passado como parâmetro.
    :param pais: Pais do qual se quer extrair os dados (em inglês).
    :return: Dicionário contendo os casos de COVID-19
    """
    response = requests.get(f'https://covid19-brazil-api.now.sh/api/report/v1/{str(pais)}')
    dados = response.json().get('data')

    if response.status_code == 200:
        if pais != 'countries':
            return f"País: {dados.get('country')}\n" \
                   f"Casos: {dados.get('cases')}\n" \
                   f"Confirmados: {dados.get('confirmed')}\n" \
                   f"Mortes: {dados.get('deaths')}\n" \
                   f"Recuperados: {dados.get('recovered')} \n" \
                   f"updated at: {dados.get('updated_at')}\n"
        return dados
    else:
        return f'{response.status_code}\n'


def casos_estados_brasil(estado):
    """
    Função para filtrar as informações de COVID-19 por estado brasileiro.
    :param estado: Sigla do estado do qual deseja ver as informações [XX].
    :return: Retorna as informações sobre o corona vírus do estado passado como parâmetro.
    """
    response = requests.get(f'https://covid19-brazil-api.now.sh/api/report/v1/brazil/uf/{estado}')
    dados = response.json()
    if response.status_code == 200:
        return f"UF: {dados.get('uf')}\n" \
               f"Estado: {dados.get('state')}\n" \
               f"Casos: {dados.get('cases')}\n" \
               f"Mortes: {dados.get('deaths')}\n" \
               f"Suspeitas: {dados.get('suspects')}\n" \
               f"Data: {dados.get('datetime')}\n"
    if response.status_code == 200:
        return dados


def verificar_status_api():
    """
    Função de verificação de funcionamento da API
    :return: retorna o status da API, se está disponível ou indisponível
    """
    response = requests.get('https://covid19-brazil-api.now.sh/api/status/v1')
    if response.status_code == 200:
        return f'API Disponível! \n' \
               f'Relatório: {response.json()}\n'
    else:
        return f'API Indisponível! \n' \
               f'CODE: {response.status_code}\n'


print(verificar_status_api())
print(casos_por_pais())
print(casos_por_pais('brazil'))
print(casos_estados_brasil("pe"))

# Bot do telegram
bot = telepot.Bot("COLOQUE AQUI SEU TOKEN")
id_do_chat = 0000000000  # COLOQUE AQUI O ID DO SEU CHAT


def enviar_mensagens():
    # .sendMessage( id_do_chat, texto )
    bot.sendMessage(id_do_chat, 'Informações sobre o COVID-19 \U0001F52C')
    bot.sendMessage(id_do_chat, casos_por_pais('brazil'))
    bot.sendMessage(id_do_chat, casos_estados_brasil('pe'))


try:
    schedule.every().day.at("08:40").do(enviar_mensagens)
    while True:
        schedule.run_pending()
        sleep(1)

except Exception as exc:
    bot.sendMessage(id_do_chat, f'Erro: {exc}')
    print(f'ERRO! {exc}')
