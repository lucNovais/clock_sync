"""
Modulo de constantes utilizadas no projeto.
"""

# Servidor e porta NTP
NTP_SERVER = 'br.pool.ntp.org'
NTP_PORT = 123

# Tamanho do buffer das mensagens trocadas
BUFFER_SIZE = 1024

# Endereco e porta do servidor de tempo
SERVER_ADDRESS = '192.168.100.4'
SERVER_PORT = 2000

# Mensagem que um cliente manda para solicitar atualizacao de tempo
TIME_REQUEST = 'UPDATED_TIME'

# Tempo que os clientes conectados ao servidor de tempo realizam solicitacao de atualizacao
TIME_TO_UPDATE = 10

# Constante da divisao do incremento gradual do tempo local do cliente
DIVISION_CONSTANT = 10
