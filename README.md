# idle-hdd

### ***What is it?***

Small script designed to shutdown all unmounted hard disk drive installed.  
Intended to be run automatically by the Linux sudo cron daemon.

### ***Dependences (tested in)***

- Python3 (v3.10.7)
  - subprocess
  - sys
  - time
  - json
- hdparm (v9.60)
- lsblk (2.38)

------

### Suspende los Discos Duros ***desmontados*** e inactivos en *Linux*.

Herramienta diseñada para ser ejecutado en Linux con el único objetivo de apagar
los discos duros que se encuentran desmontados y, por tanto, inactivos generando 
ruido innecesario y reduciendo la vida útil de los mismos.  
El script está destinado a ser ejecutado mediante cron daemon como sudo, 
automatizando el proceso de apagar los discos cuando sea necesario.

### ¿Porqué se creó este script?

Si se tiene un ordenador con más de un disco duro mecánico puede resultar 
innecesario mantener encendidos esos discos secundarios, haciendo ruido y 
reduciendo su tiempo de vida de funcionamiento.  
Los sistemas operativos Windows automáticamente apagan los discos mecánicos 
si no se están utilizando pasado un tiempo, pero parece ser que Ubuntu y Arch
Linux (y quizás otros también) siempre mantienen encendido todos los discos,
por lo menos en mi ordenador personal.  
Existen herramientas y algunas soluciones en la red, pero no me convenciaron
por lo que se ha diseñado un pequeño script Python para apagar todos los discos
duros que se encuentren desmontados en el sistema.  

