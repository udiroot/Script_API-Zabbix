# Script_API-Zabbix

Esse Script obtem via API do Zabbix informações do HOST ID,	HOSTNAME, VISABLE NAME, IP, PROXYID, PROXY NAME, STATUS, GRUPOS, GRUPO ID, TAGS, TEMPLATES,TAMPLATES ID.

As informações são armazenadas em uma lista de dicionários, onde cada dicionário representa um host.

O código exporta um novo arquivo XLSX para um local escolhido usando a biblioteca openpyxl e adiciona uma planilha à pasta de trabalho. 

Ao finalizar ele mostra uma barra de progresso e depois a conclusão da coleta.

Para URL´s Zabbix que possuem SSL, já esta com uma função que ignora a verificação. Para URL´s que não possui, ele roda do mesmo jeito.

## REQUISITOS PARA RODAR NO VSCODE OU NO PYTHON VIA CLI ##
Python 3.6 ou superior
Importar o módulo openpyxl<br>
Importar o módulo pyzabbix<br>
Importar o módulo ZabbixAPI<br>
Importar o módulo tqdm<br>
