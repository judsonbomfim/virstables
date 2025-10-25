import datetime
from apps.leilao.models import Leilao

def exibirLance(leilao):
    hoje_date = datetime.date.today()
    leilao = Leilao.objects.get(id=leilao)
    exibir_lance = 'n'   
    if leilao.data_inicio <= hoje_date <= leilao.data_fim:
        exibir_lance = 's'    
    return exibir_lance