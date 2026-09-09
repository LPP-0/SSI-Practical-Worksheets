#!/bin/bash
# Secção 5 – Capabilities do Linux

# Exercício 1
capsh --print

# Exercício 2
gcc webserver.c -o webserver
./webserver 4050

# Exercício 3
./webserver 80
# Output obtido:
# Errr on bind: Permission denied

# O programa falha ao tentar ligar à porta 80, porque em Linux, as portas inferiores a 1024
# são consideradas privilegiadas, logo apenas processos com privilégios adequados (como root
# ou CAP_NET_BIND_SERVICE) podem efetuar bind a estas portas. O utilizador user não tem esses
# privilégios, resultando no erro "Permission denied".

# Com recurso às capabilities, podemos tornar a execução do programa "webserver" possível, 
# utilizando a capability CAP_NET_BIND_SERVICE, que permite a um processo fazer bind a portas
# privilegiadas, sem ser necessário executar o programa como root.

# O seguinte comando atribui a capability CAP_NET_BIND_SERVICE ao programa webserver:
sudo setcap cap_net_bind_service=+ep webserver

# Agora, a execução do programa webserver deverá ser bem-sucedida.
./webserver 80
# Output obtido:
# Success: binded to port 80

# Pode-se concluir que as capabilities permitem atribuir privilégios específicos 
# a processos ou executáveis, evitando a necessidade de executar programas com 
# os privilégios totais de root.
