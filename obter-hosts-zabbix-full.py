# SCRIPT DESENVOLVIDO POR EDSON NUNES EM 01/JUN/2023 - udiroot@outlook.com

import openpyxl
from pyzabbix import ZabbixAPI
from tqdm import tqdm

# API ZABBIX
zapi = ZabbixAPI('http://192.168.0.19:8080/api_jsonrpc.php')

# CREDENCIAIS
username = "Admin"
password = "zabbix"

# ATIVA O HTTP
zapi.session.auth = (username, password)

# IGNORA O SSL DA URL
zapi.session.verify = False

# INÍCIO DE SESSÃO (NO CASO DE AUTENTICAÇÃO HTTP, SÓ É NECESSÁRIO O NOME DE UTILIZADOR; A PALAVRA-PASSE, SE FOR PASSADA, SERÁ IGNORADA)
zapi.login(username, password)

# OBTER INFORMAÇÃOS DOS HOSTS
hosts = zapi.host.get(output=['hostid', 'host', 'name', 'status', 'groups', 'interfaces', 'tags', 'parentTemplates',
                              'proxy_hostid'], selectGroups=['groupid', 'name'],
                      selectInterfaces=['interfaceid', 'ip'], selectTags=['tag', 'value'],
                      selectParentTemplates=['templateid', 'name'])

# CRIA UM ARQUIVO XLSX
wb = openpyxl.Workbook()

# SELECIONA A PLANILHA
ws = wb.active

# DEFINE O NOME DAS COLUNAS
columns = ['HOST ID', 'HOSTNAME', 'VISABLE NAME', 'IP', 'PROXYID', 'PROXY NAME', 'STATUS', 'GRUPOS', 'GRUPO ID', 'TAGS', 'TEMPLATES',
           'TAMPLATES ID']

# DEFINE O NOME DAS COLUNAS NA PRIMEIRA LINHA DA PLANILHA
ws.append(columns)

# OBTER NOME DOS PROXYS (CASO TENHA, SE NÃO TIVER O CAMPO FICA VAZIO)
proxies = zapi.proxy.get(output=['proxyid', 'host'])
proxy_dict = {p['proxyid']: p['host'] for p in proxies}

# POPULA AS INFORMAÇÕES NAS COLUNAS
for host in tqdm(hosts): 
    # EXTRAI AS INFORMAÇÕES
    host_id = host['hostid']
    host_name = host['host']
    host_visible_name = host['name']
    host_status = host['status']
    host_ip = host['interfaces'][0]['ip']
    host_proxy = host['proxy_hostid'] if host['proxy_hostid'] else ''
    host_proxy_name = proxy_dict.get(host_proxy, '')
    host_groups = ', '.join([g['name'] for g in host['groups']])
    host_groups_ids = ', '.join([g['groupid'] for g in host['groups']])
    host_tags = ', '.join([f"{t['tag']}: {t['value']}" for t in host['tags']])
    host_templates = ', '.join([t['name'] for t in host['parentTemplates']])
    host_templates_ids = ', '.join([t['templateid'] for t in host['parentTemplates']])
    
    # CRIA UMA NOVA LINHA COM AS INFORMAÇÕES
    row = [host_id, host_name, host_visible_name, host_ip, host_proxy, host_proxy_name, host_status, host_groups, host_groups_ids,
       host_tags, host_templates, host_templates_ids]
    
    # ADICIONA A LINHA NA PLANILHA
    ws.append(row)

# EXPORTA O XLSX
wb.save('C:\\FOLDER\\info-full-hosts-zabbix.xlsx')
