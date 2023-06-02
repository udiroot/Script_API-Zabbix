# SCRIPT DESENVOLVIDO POR EDSON NUNES EM 01/JUN/2023 - udiroot@outlook.com

import openpyxl
from pyzabbix import ZabbixAPI
from tqdm import tqdm

# URL da API do Zabbix
zapi = ZabbixAPI('http://192.168.0.19:8080/api_jsonrpc.php')

# Credenciais
username = "Admin"
password = "zabbix"

# Enable HTTP auth
zapi.session.auth = (username, password)

# Disable SSL certificate verification
zapi.session.verify = False

# Login (in case of HTTP Auth, only the username is needed, the password, if passed, will be ignored)
zapi.login(username, password)

# Obter informações dos hosts
hosts = zapi.host.get(output=['hostid', 'host', 'name', 'status', 'groups', 'interfaces', 'tags', 'parentTemplates',
                              'proxy_hostid'], selectGroups=['groupid', 'name'],
                      selectInterfaces=['interfaceid', 'ip'], selectTags=['tag', 'value'],
                      selectParentTemplates=['templateid', 'name'])

# Cria um novo arquivo XLSX
wb = openpyxl.Workbook()

# Seleciona a primeira planilha
ws = wb.active

# Define os nomes das colunas
columns = ['HOST ID', 'HOSTNAME', 'VISABLE NAME', 'IP', 'PROXYID', 'PROXY NAME', 'STATUS', 'GRUPOS', 'GRUPO ID', 'TAGS', 'TEMPLATES',
           'TAMPLATES ID']

# Define os nomes das colunas na primeira linha da planilha
ws.append(columns)

# Obtendo nome dos proxys
proxies = zapi.proxy.get(output=['proxyid', 'host'])
proxy_dict = {p['proxyid']: p['host'] for p in proxies}

# Popula as linhas com informações dos hosts
for host in tqdm(hosts): 
    # Extrai as informações de interesse do objeto do host
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
    
    # Cria uma nova linha com as informações do host
    row = [host_id, host_name, host_visible_name, host_ip, host_proxy, host_proxy_name, host_status, host_groups, host_groups_ids,
       host_tags, host_templates, host_templates_ids]
    
    # Adiciona a linha na planilha
    ws.append(row)

# Salva o arquivo XLSX
wb.save('C:\\FOLER\\info-full-hosts-zabbix.xlsx')
