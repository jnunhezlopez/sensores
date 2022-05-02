import ssl
import sys
import paho.mqtt.client as suscriptor
import paho.mqtt.publish as publicador
import sqlite
import time
broker = "192.168.0.18"
dicSensor = {"CC:50:E3:C7:16:91":1, "84:F3:EB:2F:D1:F0":2, "80:7D:3A:7D:58:4B":3, "60:01:94:14:48:7D":4}

def on_connect(client, userdata, flags, rc):
	print('Conectado (%s)' % client._client_id.decode())
	client.subscribe(topic='RFID', qos=2)
	client.subscribe(topic='TEMPERATURA', qos=2)
	client.subscribe(topic='HUMEDAD', qos=2)
def on_message(client, userdata, message):
	print('-------------------')
	print('topic: %s' % message.topic)
	print('payload: %s' % message.payload)
	print('qos: %d' % message.qos)
	print('hora: %s' % time.asctime(time.localtime()))
	if message.topic == 'TEMPERATURA':
		bd = sqlite.conexion("../sensores.db")
		campos = ["Valor", "IdSensor", "Fecha"]
		payload =message.payload.rpartition('-')
		valores= [payload[2], dicSensor[payload[0]], "DateTime('now','localtime')"]
		bd.insert("Lecturas", campos, valores)
		bd.cerrarConn()
	auth = {'username':"SCADA_LOLIN_UP", 'password':"SCADA_LOLIN_UP"}
	publicador.single("RFID_UP", message.payload, auth=auth, hostname=broker)

def main():
	client = suscriptor.Client(client_id='SCADA_LOLIN_UP', clean_session=False)
	client.username_pw_set('SCADA_LOLIN_UP', 'SCADA_LOLIN_UP')
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host=broker)
	client.loop_forever()
if __name__ == '__main__':
	main()
sys.exit(0)

