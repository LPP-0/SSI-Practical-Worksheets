#!/bin/bash
# Secção 4 – Listas Estendidas de Controlo de Acesso

# Exercício 1
getfacl porto.txt

# Exercício 2
setfacl -m g:grupo-ssi:w porto.txt

# Exercício 3
getfacl porto.txt
# Após a execução do comando setfacl, podemos notar nas seguintes diferenças
# no output deste comando:

# Foi adicionada a linha "group:grupo-ssi:-w-", que indica que o grupo grupo-ssi 
# tem permissão de escrita (w) no ficheiro porto.txt, mas não tem permissão de 
# leitura nem de execução.

# Foi também adicionada a linha "mask::-w-", que define o limite máximo de permissões
# atribuídas através das ACLs, indicando que a permissão de escrita (w) é a única 
# permissão efetivamente concedida aos grupos através das ACLs.


# Exercício 4
su - membro1
cd /home/user/ssi-semana3/
echo "Texto novo" >> porto.txt
cat porto.txt

# Output do comando 'cat porto.txt':
# cat: porto.txt: Permission denied 

# Foi possível escrever no ficheiro porto.txt, porque o utilizador membro1 
# pertence ao grupo grupo-ssi, que tem permissão de escrita (w) no ficheiro,
# conforme definido na ACL, no exercício 2.

# No entanto, não foi possível ler o conteúdo do ficheiro porto.txt, 
# uma vez que o grupo grupo-ssi não tem permissão de leitura (r) no ficheiro.

# Com isto, podemos concluir que as ACLs permitem uma gestão de permissões mais detalhada
# e flexível, comparativamente ao modelo tradicional de controlo de acesso do Linux.