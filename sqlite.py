#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sqlite3
import datetime
import sys
#from six import string_types
def row_tuple(item):#convierte un dato fecha hora a un formato tipo string
    #pendiente ver como manipular el dato fecha hora en python
    return tuple(map(lambda part:str(part)if isinstance(part,datetime.datetime) else part , item))
    #if isinstance(part, string_types) or isinstance(part, datetime)else part, item))
def main(argv):
    bdsqlite = argv[0] if len(argv) > 0 else 'sensores.db'
    bd = conexion(bdsqlite)
    bd.select("Lecturas")
    bd.cerrarConn
class conexion():
    def __init__(self, basedatos):
        DRIVER_NAME = "Microsoft Access Driver (*.mdb, *.accdb)"
        #self.database = "I:/documents_Virtual/PROGRAMACION Y PROTOTIPOS/python/basedatos/Sensores.mdb"
        self.basedatos=basedatos
        self.conn = sqlite3.connect('%s' %self.basedatos)
        self.cur = self.conn.cursor()
    def cerrarConn(self):
        self.conn.close()
    def getSensores(self):
        return self.select("sensores")
    def getSensoresBy(self,campo,valor):
        sql = "select * from %s where %s = %s" % ("sensores",campo,valor)
        return self.select("sensores",sql)
    def getUbicaciones(self):
        return self.select("ubicaciones")
    def getUbicacionesBy(self,campo,valor):
        sql = "select * from %s where %s = %s" % ("Ubicaciones",campo,valor)
        return self.select("ubicaciones",sql)
    def getLecturasBy(self,campo,valor):
        sql = "select * from %s where %s = %s" % ("Lecturas",campo,valor)
        return self.select("Lecturas",sql)        
    def select(self, tabla, sql=""):
        if sql == "":
            sql = "select * from %s" %tabla
        self.cur.execute(sql)
        campos = [column[0] for column in self.cur.description]
        datos=[]
        result = self.cur.fetchall()
        for row in result:
            #datos.append(dict(zip(campos, row_tuple(row))))
            datos.append(dict(zip(campos, row)))
    #print (row_tuple(row))
        #print(datos)
        #print('Hora:Minuto(%s:%s)' % (datos[0]['Fecha'].hour,datos[0]['Fecha'].minute))
        #self.cur.close()
        return datos
    def ejecutaSql(self,sql):
        try:
            self.cur.execute(sql)
            if sql.find('select')!=-1:
                pass
            else:#si es una sql de eliminación o de actualización
                self.conn.commit()
            print('Ejecutado %s' %sql)
        except sqlite3.Error as err:
            print(err)    
    def execute(self,sql):
        try:
            rows = self.cur.execute(sql)
            if sql.find('select')!=-1:
                pass
            else:#si es una sql de eliminación o de actualización
                self.conn.commit()
            return rows
        except sqlite3.Error as err:
            print(err)                        
    def selectgrafica(self,sql=""):
        if sql == "":
            sql = "select * from Lecturas"
        #la siguiente instrucción es para poder acceder al valor
        #de un campo por nombre (si no solo se puede hacer por índice)
        self.cur.row_factory=sqlite3.Row
        self.cur.execute(sql)
        #campos = [column[0] for column in self.cur.description]
        datosgrafica={}
        fechas=[]
        temperaturas=[]
        result = self.cur.fetchall()
        
        for row in result:
            fecha = datetime.datetime.strptime (row['Fecha'], '%Y-%m-%d %H:%M:%S')
            fechas.append('%s/%s-%s' % (fecha.month,fecha.day,fecha.hour))
            temperaturas.append(row['Valor'])
        datosgrafica['Horas']=fechas
        datosgrafica['Temperaturas']=temperaturas

        #print('Hora:Minuto(%s:%s)' % (datos[0]['Fecha'].hour,datos[0]['Fecha'].minute))
        #self.cur.close()
        #print (datosgrafica)
        return datosgrafica

    def insert(self,tabla,campos,valores):
        scampos=','.join(str(s) for s in campos)
        svalores=','.join(str(s)for s in valores)
        sql = "insert into %s (%s)values(%s)" %(tabla,scampos,svalores)
        print("Insert: %s" %sql)
        try:
            self.cur.execute(sql)
            #en Sqlite el commit está en la conexión no en el cursor
            #self.cur.commit()
            self.conn.commit()
            #se obtiene el id del nuevo registro grabado        
            id = self.cur.lastrowid
            print("Id el campo recién insertado: %s" % id)            
        except sqlite3.Error as err:
            print(err)
            id = -1
        return id
        #self.cur.close()
    def SensoresADict(self):
        #HACER, pasar varios campos y añadirlos a la SQL
        #de momento esta función es solamente para sensores
        sql = "select Id, MAC from sensores" 
        self.cur.execute(sql)
        ids=[]
        MACs=[]
        result = self.cur.fetchall()
        for row in result:
            ids.append(row[0])
            MACs.append(row[1])
        return dict(zip(MACs, ids))
if __name__=='__main__':
    main(sys.argv[1:])

