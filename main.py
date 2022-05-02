import socket
from peer import Peer
from flask import Flask, request

# Valores por defecto si no se pasan por argumentos o fichero de configuración
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]
FICHERO = "config.json"
PORT = 2000
BUFFER = 4096
MAX_BITS = 10
api = Flask(__name__)
peer = Peer(IP, PORT, BUFFER, MAX_BITS)
peer.start()


@api.route("/server/rest/DHT/addNode")
def anadirNodo():
    global peer, IP
    ip = request.args.get("ip")
    if ip:
        peer.sendJoinRequest(ip, PORT)
        return (
            "Se ha unido el nodo ("
            + str(IP)
            + ":"
            + str(PORT)
            + ") con ID "
            + str(peer.id)
            + " a la red "
            + str(ip)
        )
    else:
        return "No se ha podido unir al nodo a la red. Falta la IP."


@api.route("/server/rest/DHT/removeNode")
def apagarNodo():
    global peer
    if peer:
        peer.leaveNetwork()
        text = "Cerrando nodo con id: " + str(peer.id)
        return text
    else:
        return "El nodo ya se encuentra apagado."


@api.route("/server/rest/DHT/uploadContent")
def subirArchivo():
    global peer
    if peer:
        filename = request.args.get("filename")
        data = request.args.get("data")
        if filename and data:
            fileID = peer._getHash(filename)
            recvIPport = peer.getSuccessor(peer.succ, fileID)
            peer.uploadFile(filename, data, recvIPport, True)
            return (
                "Se ha subido el archivo " + str(filename) + " con el id " + str(fileID)
            )
        else:
            return "Faltan parámetros de URL: filename, data."
    else:
        return "No se ha iniciado el nodo."


@api.route("/server/rest/DHT/downloadContent")
def descargarArchivo():
    global peer
    if peer:
        filename = request.args.get("filename")
        if filename:
            peer.downloadFile(filename)
            text = "Archivo " + filename + " descargado.<br>"
            with open(filename, "r") as f:
                data = f.readlines()
            for line in data:
                text += line + "<br>"
            return text
        else:
            return "Faltan párametros de URL: filename."
    else:
        return "No se ha iniciado el nodo."


@api.route("/server/rest/DHT/imprimirFingerTable")
def imprimirFingerTable():
    global peer
    if peer:
        return peer.printFTable()
    else:
        return "No se ha iniciado el nodo."


@api.route("/server/rest/DHT/imprimirSucPred")
def imprimirSucPred():
    global peer
    if peer:
        text = "ID: " + str(peer.id) + "<br>"
        text = text + "Suc: " + str(peer.succID) + "<br>"
        text = text + "Pred: " + str(peer.predID) + "<br>"
        return text
    else:
        return "No se ha iniciado el nodo."


try:
    api.run(host="0.0.0.0", port=8080)
except Exception as e:
    peer.ServerSocket.close()
