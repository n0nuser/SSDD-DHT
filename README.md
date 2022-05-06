# SSDD - Chord DHT (Tabla Hash Distribuida)

## Un poco sobre CHORD 
Chord es un protocolo y algoritmo para una tabla hash distribuida punto a punto que se puede utilizar para compartir archivos entre pares (p2p). El algoritmo de chord es el encargado de distribuir objetos en un red dinámica y es el quien implementa un protocolo para encontrar esos objetos en la red. Además la ubicación de los datos se implemnta en la parte superior de Chord al asociar una clave con cada elemento de datos y alamcenar el par clave/elemento de datos en el nodo al que asigna la clave.
El protocolo Chord admite solo una operación: dad una clave, determinara el nodo responsable de almacenar el valor de la clave.

Cada clave (basada en el nombre del archivo) insertada en el DHT se codifica para encajar en el espacio de teclas admitido por la implementación particular de Chord. El espacio de claves (el rango de hashes posibles), en esta implementación reside entre 0 y 2 m -1 inclusive donde m = 10 (indicado por MAX_BITS en el código). Así que el espacio de claves está entre 0 y 1023.

Los nodos así como las claves también tienen un valor hash en la DHT que es el que hemos construido a traves de la combinación de su IP y su PUERTO usando el algoritmo hash SHA1. Tenemos que tener en cuenta los hashes porque CHORD ordena los ndos en función de quien es el siguiente hash más alto, y como la red es circular, el nodo sucesor del nodo con el hash más alto será el nodo con el hash más pequeño.

Otro aspecto clave sobre CHORD es que es capaz de autoestabilizarse, es decir, si tenemos dos nodos conectados en una red circular y uno de repente se desconecta, como los nodos estan haciendo continuamente ping a su nodo sucesor, los nodos se estabilizarán. Y si pensabamos que los archivos que tenía el nodo que se ha desconectado se pierden, esto no es asñi ya que antes de desconectarse se replican en su nodo sucesor.

## Programa

Dado que CHORD es un sistema descentralizado no hay un fichero para el servidor y otro diferente para el cliente, nuestro fichero peer.py ya actua como cliente y servidor al mismo tiempo.

Para que nuestro programa funcione correctamente debemos indicarle los argumentos por línea de comando de la siguiente forma:

```
poetry run python main.py <IP> <PUERTO>
```

Este programa ha sido implentado a partir del código de github de EXAMPLE y se ha implmentado un servicio API REST mediante Flask por ver realmente su correcto funcionamiento hay que realizar las peticiones a los endpoints des de un buscador para ver los resultados.

**Atención:** Un nodo puede tener la misma IP que otro pero no el mismo PUERTO

## Ejemplo de como utilizar el programa

Lo primero que tenemos que hacer para poder ejecutar el programa es lanzar el comando `poetry run python main.py <IP> <PUERTO>` tantas veces como nodos queramos que tenga nuestra red CHORD.

Entonces para hacer la prueba lanzariamos en 3 terminales de 3 máquinas distintas lo siguientes comandos:

```
poetry run python main.py 192.168.1.12 2000
```


```
poetry run python main.py 192.168.1.13 3000
```


```
poetry run python main.py 192.168.1.14 4000
```

Las peticiones a los endpoints son las siguientes:

Si quieres añadir un nodo tan solo tienes que utilizar esta petición:
```
http://YOUR_IP:PORT/server/REST/DHT/addNode?ip=IP
```

YOUR_IP = 192.168.1.12 
PORT = 2000
IP = La IP de la red donde te quieres conectar

Para eliminar un nodo de la red solo tienes que enviar esta petición:
```
http://YOUR_IP:PORT/server/REST/DHT/removeNode
```

Si quieres usbir un archivo a la red DHT sería la siguiente petición:
```
http://YOUR_IP:PORT/server/REST/DHT/uploadContent?filename=NombreFichero&data=Datos
```

FILENAME = NombreDeTuFichero (notas.txt)
DATA = Un string ("Esto es una nota de texto")

Para descargar el archivo tan solo tienes que enviar esta petición con el nombre del fichero a descargar:
```
http://YOUR_IP:PORT/server/REST/DHT/downloadContent?filename=NombreFichero
```
FILENAME = NombreDelFicheroSubido

Si quieres imprimir la FingerTable que muestra todos los nodos que hay conectados en la red CHORD y cada una de sus claves:
```
http://YOUR_IP:PORT/server/REST/DHT/imprimirFingerTable
```

Y para imprimir quien es tu sucesor y predecesor en la red se hace de la siguiente forma:
```
http://YOUR_IP:PORT/server/REST/DHT/imprimirSucPred
```
