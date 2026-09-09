#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

int main() {
    
    // Exercício 5 - Correção da vulnerabilidade
    int fd = open("/etc/passwd", O_WRONLY | O_APPEND | O_CLOEXEC);
    

    if (fd < 0) {
        perror("open /etc/passwd");
        exit(1);
    }

    printf("Passwd FD leaked: %d\n", fd);
    setuid(getuid());
    execl("/bin/sh", "sh", NULL);
}