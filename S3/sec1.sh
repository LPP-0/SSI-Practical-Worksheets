#!/bin/bash
# Secção 1 – Utilizador, Grupo e Permissão

# Exercício 1
mkdir ssi-semana3
cd ssi-semana3
echo "Lisboa" > lisboa.txt
echo "Porto" > porto.txt
echo "Braga" > braga.txt

# Exercício 2
ls -l lisboa.txt

# Exercício 3
chmod 666 lisboa.txt

# Exercício 4
chmod u=rx porto.txt

# Exercício 5
chmod u=r,go= braga.txt


# Exercício 6
mkdir dir1 dir2
ls -ld dir1 dir2

# Exercício 7
chmod g-x,o-x dir2