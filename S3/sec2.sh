#!/bin/bash
# Secção 2 – Gestão de Utilizadores e Grupos

# Exercício 0
cat /etc/passwd
cat /etc/group

# Exercício 1
sudo adduser membro1
sudo adduser membro2
sudo adduser membro3

# Exercício 2
sudo groupadd grupo-ssi
sudo usermod -aG grupo-ssi membro1
sudo usermod -aG grupo-ssi membro2
sudo usermod -aG grupo-ssi membro3

sudo groupadd par-ssi
sudo usermod -aG par-ssi membro1
sudo usermod -aG par-ssi membro2

# Exercício 3
cat /etc/passwd
cat /etc/group
# Sim, observam-se diferenças. No ficheiro /etc/passwd, foram adicionadas novas linhas no final, 
# uma para cada utilizador criado (membro1, membro2, membro3), com informações como o seu UID,
# GID principal, diretoria home e shell associada.
# No ficheiro /etc/group, foram adicionadas entradas para os novos grupos criados
# (grupo-ssi, par-ssi), em como a associação dos utilizadores a esses grupos.

# Exercício 4
sudo chown membro1 braga.txt

# Exercício 5
cat braga.txt
# O acesso é negado porque o utilizador atual não é o dono do ficheiro,
# e não existem permissões atribuídas a grupo ou outros, tal como foi definido 
# no exercício 5 da secção 1 (chmod u=r,go= braga.txt), o que significa que apenas 
# o dono do ficheiro tem permissão de leitura, e os outros utilizadores não têm 
# permissão de leitura, escrita ou execução.

# Exercício 6
su - membro1

# Exercício 7

# Output do comando 'id':
# uid=1001(membro1) gid=1001(membro1) groups=1001(membro1),100(users),1004(grupo-ssi),1005(par-ssi)

# Output do comando 'groups':
# membro1 users grupo-ssi par-ssi 

# O comando 'id' mostra o UID (user id), GID (group id) principal e os grupos
# a que o utilizador pertence.
# O comando 'groups' lista apenas os nomes dos grupos aos quais o utilizador pertence.


# Exercício 8
# O ficheiro encontra-se na diretoria /home/user/ssi-semana3/braga.txt
# É necessário que os utilizadores tenham permissão de execução na diretoria /home/user 
# para poderem acessar os ficheiros dentro dela, mesmo que tenham permissão de leitura no ficheiro em si.
# Para isso, foi executado o seguinte comando pelo utilizador user (dono da diretoria):
chmod o+x /home/user

# Voltando ao utilizador membro1, agora é possível ler o conteúdo do ficheiro braga.txt, 
# usando o comando 
cat /home/user/ssi-semana3/braga.txt

# Isto demonstra que, em Linux, o acesso a um ficheiro depende das permissões
# ao longo de todo o caminho até ele.

# Exercício 9
# O comando cd /home/user/ssi-semana3/dir2 falha, com uma mensagem de "Permission denied".
# Isto ocorre porque, no exercício 7 da secção 1, removemos a permissão de execução (x)
# da diretoria 'dir2' para o grupo e para outros. Para entrar numa diretoria, um
# utilizador precisa da permissão de execução sobre ela. Como 'membro1' não é o dono
# nem tem essa permissão, o acesso é negado.