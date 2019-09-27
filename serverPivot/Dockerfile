#=======================================================
# Antes de ejecutar este Dockerfile, se debe copiar el archivo dogKey.json desde el computador del administrador por medio de scp
# scp -P 9022 sergioeabarcaf@146.83.190.248:/media/Datos/proyectosSergio/github/InvernaderoIOT/pyhon/dogKey.json .
#=======================================================

# Dockerfile Desarrollado por sergioeabarcaf
# https://github.com/sergioeabarcaf

# Usar imagen base de ubuntu
FROM ubuntu

# Instalación de componentes necesarios
RUN apt install software-properties-common
RUN apt-add-repository ppa:nilarimogard/webupd8
RUN apt update && apt upgrade -y
RUN apt install git python python-pip -y firebase-admin grive
# Clonar repositorio del proyecto
RUN git clone https://github.com/Sergioeabarcaf/CoopeumoZigbeeTest.git

# Copiar archivos necesarios para la ejecución
COPY dogKey.json /CoopeumoZigbeeTest/serverPivot
COPY dogKey.json .
