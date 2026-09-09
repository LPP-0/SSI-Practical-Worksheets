#!/bin/bash
# Secção 3 – Utilizador Real vs. Efetivo e Elevação de Privilégio

# Exercício 1
nano readfile.c

# #include <stdio.h>
# #include <stdlib.h>

# int main(int argc, char *argv[]){
#
#     if(argc != 2){
#         fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
#         return 1;
#     }

#     FILE *f = fopen(argv[1], "r");
#     if (f == NULL){
#         perror("Error opening file");
#         return 1;
#     }

#     char c;
#     while ((c = fgetc(f)) != EOF){
#         putchar(c);
#     }

#     fclose(f);
#     return 0;
# }

gcc readfile.c -o readfile


# Exercício 2
sudo adduser userssi

# Exercício 3
sudo chown userssi readfile
sudo chown userssi braga.txt

# Exercício 4
./readfile braga.txt
# Output obtido:
# Error opening file: Permission denied

# Exercício 5
sudo chmod u+s readfile

# Exercício 6
./readfile braga.txt
# Output: Braga
# Ao contrário do que aconteceu no exercício 4, o programa executa com sucesso.
# Isto acontece porque a permissão de setuid (s) permite que o programa seja executado 
# com o UID efetivo do dono do ficheiro (userssi), em vez do UID do utilizador que 
# o executa, embora o UID real continue a ser do utilizador user. Desta forma, o programa
# é executado com os privilégios do utilizador userssi, que tem permissão para ler o 
# ficheiro braga.txt, permitindo assim executar o programa com sucesso e ler o conteúdo do ficheiro.