from tkinter import *
from tkinter.simpledialog import Dialog
import tkinter.messagebox
import Pmw
import string

#para el acceso a base de datos
import access
#cambio para Sqlite
import sqlite
import datetime
import winsound
#datos para emitir un sonido del sistema
frecuencia = 500
duracion = 250
#baseDatosAccess ="I:/documents_Virtual/PROGRAMACION Y PROTOTIPOS/python/basedatos/Sensores.mdb" # "//UBAKOYA/Documentos/Sensores.mdb"  
baseDatosSqlite = "I:/documents_Virtual/PROGRAMACION Y PROTOTIPOS/sqlite/sensores.db"#"//RASPBERRYPI/home/sensores.db"#"//CASIN-VIRTUALBO/Documentos/sensores.db"#

def creaListaDeDict(dic,ele):
    lista = []
    for val in dic:
        if type(ele) is tuple:
            cadena = '%s-%s' % (val['%s'%ele[0]],val['%s'%ele[1]])
        else:
            cadena = val['%s' %ele]
        lista.append (cadena)
    return lista

class frmInsert (Dialog):
    def body(self, master):
        self.title("Introducir datos a insertar")
        Label(master, text='Ubicación:').grid(row=0, sticky=W)
        Label(master, text='Sensor:').grid(row=1, sticky=W)
        Label(master, text='Lectura:').grid(row=2, sticky=W)
        Label(master, text='Fecha:').grid(row=3, sticky=W)
        Label(master, text='Hora:').grid(row=4, sticky=W)
        #values= list(self.cargaUbicaciones.keys()),
        self.cmbUbicaciones = Pmw.ComboBox(master,selectioncommand=self.cmbUbicacionesSel)
        self.cmbUbicaciones.setlist(creaListaDeDict(self.cargaUbicaciones(),('Id','Ubicacion')))
        self.cmbSensores = Pmw.ComboBox(master, selectioncommand = self.cmbSensoresSel)
        self.txtLectura = Entry(master, width= 16)
        self.txtFecha = Entry(master, width=16)
        self.txtHora = Entry(master, width=16)
        self.cmbUbicaciones.grid(row=0, column=1, sticky=W)
        self.cmbSensores.grid(row=1, column=1, sticky=W)
        self.txtLectura.grid(row=2, column=1, sticky=W)
        self.txtFecha.grid(row=3, column=1, sticky=W)
        self.txtHora.grid(row=4, column=1, sticky=W)
    def apply(self):
        ub=self.cmbUbicaciones.get(ACTIVE)
        sn=self.cmbSensores.get(ACTIVE)
        lc=self.txtLectura.get()
        fc=self.txtFecha.get()
        hr=self.txtHora.get()
        if fc=='' or hr=='':
            valorFecha = "DateTime('now', 'localtime')"
        else:
            valorFecha = "'%s %s'" % (fc,hr)
        #print("Del formulario:%s,%s,%s,%s" %(ub,sn,lc,fc))
        #bd = access.conexion(baseDatosAccess)
        bd = sqlite.conexion(baseDatosSqlite)
        campos=["Valor","IdSensor","Fecha"]
        valores=[lc,sn.rpartition('-')[0],valorFecha]
        bd.insert("Lecturas",campos,valores)
        bd.cerrarConn()
    def cmbUbicacionesSel(self, value):
        #print("Recibido %s" %value)
        self.cmbSensores.setlist([])
        self.cmbSensores.setlist(creaListaDeDict(self.getSensoresBy("IdUbicacion",value.rpartition('-')[0]),('Id','Sensor')))        
        #winsound.Beep(frecuencia,duracion)
    def cmbSensoresSel(self, value):
        #winsound.Beep(frecuencia,duracion)
        pass
    def cargaUbicaciones(self):
        #bd = access.conexion(baseDatosAccess)
        bd = sqlite.conexion(baseDatosSqlite)
        ubicaciones = bd.getUbicaciones()
        bd.cerrarConn()      
        return ubicaciones  
    def getSensoresBy(self,campo,valor):
        #bd = access.conexion(baseDatosAccess)
        bd = sqlite.conexion(baseDatosSqlite)
        sensores = bd.getSensoresBy(campo=campo,valor=valor)
        bd.cerrarConn()         
        return sensores
class Shell:
    def __init__(self, title = ''):
        self.root = Tk()
        Pmw.initialise(self.root)
        self.root.title(title)

    def doBaseForm(self, master):
        self.balloon = Pmw.Balloon(master)
        self.menuBar = Pmw.MenuBar(master, hull_borderwidth=2,
        hull_relief = RAISED, hotkeys = 1, balloon=self.balloon)

        self.menuBar.pack(fill=X)
        self.menuBar.addmenu('Archivo','Salir')
        self.menuBar.addmenuitem('Archivo','command','Gestión de ubicaciones',label='Ubicaciones',command=self.maestroUbicaciones)
        self.menuBar.addmenuitem('Archivo','command','Gestión de sensores',label='Sensores',command=self.maestroSensores)
        self.menuBar.addmenuitem('Archivo','command','Gestión de lecturas',label='Lecturas',command=self.getLecturas)        
        self.menuBar.addmenuitem('Archivo','command','Salir de la aplicación',label='Salir',command=self.exit)

        self.menuBar.addmenu('Ver','Ver información')
        self.menuBar.addmenuitem('Ver','command','Cargar datos de sensores',label='Datos sensores',command=self.getInformacion)
        self.menuBar.addmenu('Ayuda','Acerca de formulario', side=RIGHT)
        self.menuBar.addmenuitem('Ayuda','command','Información de la aplicación',
            label='Acerca de...', command=self.help)
        
        #self.dataFrame=Frame(master)
        #self.dataFrame.pack(fill=BOTH, expand=1)
        
        #self.infoFrame=Frame(self.root, bd=1, relief='groove')
        self.infoFrame=Frame(master, bd=1, relief='groove')
        self.infoFrame.pack(fill=BOTH, expand=1, padx=10)

        self.statusBar = Pmw.MessageBar(master, entry_width=40,
            entry_relief='groove', labelpos = W, label_text = '')
        self.statusBar.pack(fill=X, padx=10, pady=10)
        #se añade un balloon text a la barra de estado
        self.balloon.configure(statuscommand=self.statusBar.helpmessage)
        #se crea el menú acerca de
        Pmw.aboutversion('V.1 Sensores')
        Pmw.aboutcopyright('Copyright mr Casiano')
        Pmw.aboutcontact('Empezada: 03/01/2022\n'+
            'Casiano Automatics SI\n')
        self.about = Pmw.AboutDialog(master, applicationname='formulario')
        self.about.withdraw()
    def exit(self):
        self.root.destroy()
        #import sys
        #sys.exit(0)
    def getInformacion(self):
        self.getUbicaciones()
    def getUbicaciones(self):
        #bd = access.conexion(baseDatosAccess)
        bd = sqlite.conexion(baseDatosSqlite)
        ubicaciones = bd.getUbicaciones()
        self.listaUbicaciones.delete(0,'end')
        for ub in ubicaciones:
            print(ub['Ubicacion'])
            self.listaUbicaciones.insert(ub['Id'],'%s-%s' %(ub['Id'], ub['Ubicacion']))
        bd.cerrarConn()
    def help(self):
        self.about.show()
    def doInfoForm(self):
        #self.pictureID=Label(self.infoFrame, bd=0)
        #self.pictureID.pack(side=LEFT, expand=1)
        self.etiquetaUbicaciones = Label(self.infoFrame, text='Ubicaciones')
        self.etiquetaUbicaciones.place(relx=.05, rely=.05)
        self.listaUbicaciones = Listbox(self.infoFrame)
        #self.listaUbicaciones.pack(side=LEFT, expand=1)
        self.listaUbicaciones.place(relx = 0.05, rely=.1)
        self.listaUbicaciones.bind('<%s>' % "Double-Button-1", self.eventoCargaSensores)

        self.etiquetaSensores = Label(self.infoFrame)
        self.etiquetaSensores.place(relx=.05, rely=.45)
        self.listaSensores = Listbox(self.infoFrame)
        self.listaSensores.place(relx = 0.05, rely=.50)        
        #self.listaSensores.pack(side=LEFT, expand=1)
        self.listaSensores.bind('<%s>' % "Double-Button-1", self.eventoCargaLecturas)

        self.etiquetaLecturas = Label(self.infoFrame)
        self.etiquetaLecturas.place(relx=0.25, rely=.05)
        self.listaLecturas = Listbox(self.infoFrame,width=40)
        self.listaLecturas.place(relx = 0.25, rely=.1)        
        #self.listaLecturas.pack(side=LEFT, expand=1)
        self.listaLecturas.bind('<%s>' % "Double-Button-1", self.eventoRepresentaGrafica)
        self.btnBorraLectura = Button(self.infoFrame, text='Borrar Lectura', command=self.btnclkBorraLectura,
        bg='red', fg='yellow').place(relx = 0.55, rely=.50, anchor=SE)
        #Comentada la parte de visualizar gráficas en un "Canvas" ya que no
        #permite actualizar el gráfico con nuevos datos
        #self.contenedorGrafica = Canvas(self.infoFrame, width=450, height=300, bg= 'white')
        #self.contenedorGrafica.place(relx = .25, rely = .05)
    def btnclkBorraLectura(self):
        bd = sqlite.conexion(baseDatosSqlite)
        bd.ejecutaSql("delete from Lecturas where id =%s" %self.listaLecturas.get(ACTIVE).rpartition('-')[0])
        bd.cerrarConn
    def eventoCargaSensores(self, event):
        #print("Click en %s" % self.listaUbicaciones.get(ACTIVE))
        self.getSensoresBy("idUbicacion",self.listaUbicaciones.get(ACTIVE).rpartition('-')[0])
        #print("Índice de ubicaciones: %s" % self.listaUbicaciones.get(ACTIVE).rpartition('-')[0])
    def getSensoresBy(self,campo,valor):
        #bd = access.conexion(baseDatosAccess)
        bd = sqlite.conexion(baseDatosSqlite)
        sensores = bd.getSensoresBy(campo=campo,valor=valor)
        self.listaSensores.delete(0,'end')
        self.listaLecturas.delete(0, 'end')
        self.etiquetaSensores.configure(text=self.listaUbicaciones.get(ACTIVE))
        for sensor in sensores:
            self.listaSensores.insert(sensor['Id'],'%s-%s' %(sensor['Id'],sensor['Sensor']))
        return sensores
        bd.cerrarConn()        
    def eventoCargaLecturas(self, event):
        self.getLecturasBy("idSensor",self.listaSensores.get(ACTIVE).rpartition('-')[0])
        print("Índice de sensores: %s" %self.listaSensores.get(ACTIVE).rpartition('-')[0])        
    def getLecturasBy(self,campo,valor):
        #bd = access.conexion(baseDatosAccess)
        bd = sqlite.conexion(baseDatosSqlite)
        lecturas = bd.getLecturasBy(campo=campo,valor=valor)
        self.listaLecturas.delete(0,'end')
        self.etiquetaLecturas.configure(text=self.listaSensores.get(ACTIVE))
        for lectura in lecturas:
            texto = "%s-Tª:%s, Fecha:%s" % (lectura['Id'], lectura['Valor'], lectura['Fecha'])
            self.listaLecturas.insert(lectura['Id'],texto)
        bd.cerrarConn()        
    def eventoRepresentaGrafica(self, event):
        #gestión del cursor, no funciona, tampoco con root en vez de infoFrame
        #self.infoFrame.config(cursor="wait")
        #self.infoFrame.update()
        from pandas import DataFrame
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        #print("Índice de sensores: %s", self.listaSensores.get(ACTIVE).rpartition('-')[0])                
        #data1 = {'Horas': ['01\n9','01\n10','01\n10','01\n11','01\n12','01\n13'],
        #     'Temperaturas': [17,18,19,20,19,20] }
        #bd = access.conexion(baseDatosAccess)
        bd = sqlite.conexion(baseDatosSqlite)        
        data1={}
        data1 =bd.selectgrafica("select * from lecturas where idsensor=%s and fecha between '2022-01-20' and '2022-01-21' order by fecha" 
            % str(self.listaSensores.get(ACTIVE).rpartition('-')[0]))
        print(data1)
        df1 = DataFrame(data1,columns=['Horas','Temperaturas'])
        figure1 = plt.figure(figsize=(6,4), dpi=100)

        ax1 = figure1.add_subplot(111)
        #bar1 = FigureCanvasTkAgg(figure1, self.contenedorGrafica)
        #bar1.get_tk_widget().pack(side=LEFT, fill=BOTH)
        df1 = df1[['Horas','Temperaturas']].groupby('Horas').mean()
        #rot=0 pone las etiquetas del eje x en horizontal, por defecto las pone verticales
        #ver cómo queda con mucho datos
        df1.plot(kind='bar', legend=True, ax=ax1)#, rot=0)
        figure1.show()
        ax1.set_title('Evolución temperatura por horas\n Sensor:%s-%s' 
        % (self.listaUbicaciones.get(ACTIVE), self.listaSensores.get(ACTIVE)))
        bd.cerrarConn()
        #gestión del cursor(cambio del icono), no funciona
        #self.infoFrame.config(cursor="")
    def getUbicacionesBy(self, valor):
        #bd = access.conexion(baseDatosAccess)
        bd = sqlite.conexion(baseDatosSqlite)
        return bd.getUbicacionesBy("Id",valor)
    def getLecturas(self):
        frm=frmInsert(self.root)
    def maestroUbicaciones(self):
        wUbicaciones = Toplevel(self.root,bg='light blue')
        wUbicaciones.geometry('200x200+150+150')
        lbl = Label(wUbicaciones, text="MaestroUbicaciones")
        lbl.pack(padx=10,pady=10)
        self.idUbicacion=Pmw.EntryField(wUbicaciones, entry_width=8,
            value='', modifiedcommand=self.upd_IdUbicacion,
            label_text='Id:',
            labelpos=W, labelmargin=1)
        self.idUbicacion.place(relx=.20, rely=.325, anchor=W)
        self.nombreUbicacion=Pmw.EntryField(wUbicaciones, entry_width=8,
            value='', modifiedcommand=self.upd_nombreUbicacion,
            label_text='Ubicación: ',
            labelpos=W, labelmargin=1)
        self.nombreUbicacion.place(relx=.20, rely=.70, anchor = W)   
        self.btnguardarUbicacion=Button(wUbicaciones,text='Guardar',bg='dark gray')  
        self.btnguardarUbicacion.pack(side= BOTTOM, anchor=W, fill=X)   
        self.btnguardarUbicacion.bind('<%s>' % "Button-1", self.guardarUbicacion)
    def guardarUbicacion(self, event):
        #print("En el horno: guardarUbicacion")
        if self.idUbicacion.get()!='':
            print("No se puede guardar con un id dado, probar modificar")
        else:
            if self.nombreUbicacion.get()!='':
                bd = sqlite.conexion(baseDatosSqlite)
                id =bd.insert("Ubicaciones",["Ubicacion"],["'%s'" %self.nombreUbicacion.get()])
                if id != -1:#devuelve -1 cuando se produce un error
                    self.idUbicacion.setentry(id)
            else:
                print("Debe indicarse un nombre de ubicación")
    def upd_IdUbicacion(self):
        if self.idUbicacion.get()!='':
            Ubicacion = self.getUbicacionesBy(self.idUbicacion.get())
            if Ubicacion:
                self.nombreUbicacion.setentry(Ubicacion[0]['Ubicacion'])
            else:
                self.nombreUbicacion.clear()
        else:
                self.nombreUbicacion.clear()
        #self.idUbicacion.setentry()
    def upd_nombreUbicacion(self):
        valid = self.nombreUbicacion.get()
        if valid:
            self.nombreUbicacion.setentry(valid)
    def maestroSensores(self):
        wSensores = Toplevel(self.root,bg='light blue')
        wSensores.geometry('200x200+100+100')
        lbl = Label(wSensores, text="MaestroSensores")
        lbl.pack(padx=10,pady=10)
        self.idSensor=Pmw.EntryField(wSensores, entry_width=8,
            value='', modifiedcommand=self.upd_IdSensor,
            label_text='Id:',
            labelpos=W, labelmargin=1)
        self.idSensor.place(relx=.20, rely=.225, anchor=W)
        self.nombreSensor=Pmw.EntryField(wSensores, entry_width=8,
            value='', modifiedcommand=self.upd_nombreSensor,
            label_text='Sensor: ',
            labelpos=W, labelmargin=1)
        self.nombreSensor.place(relx=.20, rely=.40, anchor = W, width=150)   
        self.MACSensor=Pmw.EntryField(wSensores, entry_width=8,
            value='', modifiedcommand=self.upd_MACSensor,
            label_text='MAC: ',
            labelpos=W, labelmargin=1)
        self.MACSensor.place(relx=.20, rely=.575, anchor = W, width=150)           
        self.lblUbicaciones = Label(wSensores, text='Ubicacion:')
        self.lblUbicaciones.place(relx=.20, rely=.725, anchor=W)        
        self.cmbUbicaciones = Pmw.ComboBox(wSensores)
        self.cmbUbicaciones.setlist(creaListaDeDict(self.cargaUbicaciones(),('Id','Ubicacion')))    
        self.cmbUbicaciones.place(relx=.20, rely=.825, anchor = W)  
        self.cmbUbicaciones.selectitem(0)
        self.btnguardarSensor=Button(wSensores,text='Guardar',bg='dark gray')  
        self.btnguardarSensor.pack(side= BOTTOM, anchor=W, fill=X)   
        self.btnguardarSensor.bind('<%s>' % "Button-1", self.guardarSensor)
    def guardarSensor(self, event):
        #print("En el horno: guardarUbicacion")
        if self.idSensor.get()!='':
            print("No se puede guardar con un id dado, probar modificar")
        else:
            if self.nombreSensor.get()!='':
                bd = sqlite.conexion(baseDatosSqlite)
                id =bd.insert("Sensores",["Sensor","IdUbicacion","MAC"],
                ["'%s'" % self.nombreSensor.get(),
                "%s" % self.cmbUbicaciones.get(ACTIVE).rpartition('-')[0],
                "'%s'" % self.MACSensor.get()])
                if id != -1:#devuelve -1 cuando se produce un error
                    self.idSensor.setentry(id)
            else:
                print("Debe indicarse un identificador del sensor")
    def upd_IdSensor(self):
        if self.idSensor.get()!='':
            Sensor = self.getSensoresBy("Id", self.idSensor.get())
            if Sensor:
                self.nombreSensor.setentry(Sensor[0]['Sensor'])
                self.MACSensor.setentry(Sensor[0]['MAC'])
            else:
                self.nombreSensor.clear()
        else:
                self.nombreSensor.clear()
        #self.idUbicacion.setentry()
    def upd_nombreSensor(self):
        valid = self.nombreSensor.get()
        if valid:
            self.nombreSensor.setentry(valid)
    def upd_MACSensor(self):
        valid = self.MACSensor.get()
        if valid:
            self.MACSensor.setentry(valid)            
    def cargaUbicaciones(self):
        #bd = access.conexion(baseDatosAccess)
        bd = sqlite.conexion(baseDatosSqlite)
        ubicaciones = bd.getUbicaciones()
        bd.cerrarConn()      
        return ubicaciones              
if __name__=='__main__':
    shell=Shell(title='formulario')
    shell.root.geometry("%dx%d" %(800,600))
    shell.doBaseForm(shell.root)
    #el formulario con el nombre de usuario y código se eliminará
    #shell.doDataForm()
    shell.doInfoForm()
    shell.root.mainloop()