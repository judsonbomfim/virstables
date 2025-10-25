import datetime
from apps.leilao.models import Leilao

def exibirLance(leilao):
    hoje_date = datetime.date.today()
    leilao = Leilao.objects.get(id=leilao)
    exibir_lance = 'n'
    
    # Converter as datas do leilão para date
    data_inicio = leilao.data_inicio.date() if hasattr(leilao.data_inicio, 'date') else leilao.data_inicio
    data_fim = leilao.data_fim.date() if hasattr(leilao.data_fim, 'date') else leilao.data_fim
    
    if data_inicio <= hoje_date <= data_fim:
        exibir_lance = 's'
        
    return exibir_lance