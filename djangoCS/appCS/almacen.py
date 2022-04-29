#Librerías
from email.mime import text
import mimetypes
import os
import base64
from io  import BytesIO
from io import StringIO
from typing import List

#Renderizado
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from reportlab import cmp
from django.views.generic import ListView
import json

#Importación de modelos
from appCS.models import Areas, Empleados, Equipos, Carta, Impresoras, Cartuchos, CalendarioMantenimiento, Programas, ProgramasArea, EquipoPrograma, Bitacora, Renovacion_Equipos, Renovacion_Impresoras, Preguntas, Encuestas, Respuestas, EncuestaEmpleadoResuelta, Mouses, Teclados, Monitores, HerramientasAlmacen, InstrumentosAlmacen, HerramientasAlmacenInactivas, PrestamosAlmacen

#Librería para manejar archivos en Python
from django.core.files.base import ContentFile

#Librerías de fecha
from datetime import date, datetime
from datetime import timedelta
from calendar import calendar
from dateutil.relativedelta import relativedelta

#Archivo configuración Django
from django.conf import settings

#Correo
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#Librerias reportes pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.graphics.shapes import Drawing 
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import BarChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF

#Libreria excel.
import xlwt

def fotoAdmin(request):
    idadministrador=request.session["idSesion"]
    datosEmpleado = Empleados.objects.filter(id_empleado=idadministrador)
        
    for dato in datosEmpleado:
        foto = dato.imagen_empleado
        
    return foto

def solicitudesPendientesALM(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnSolicitudesPendientes = True
        almacen = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes


        return render(request, "empleadosCustom/almacen/solicitudesPendientes.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesPendientes":estaEnSolicitudesPendientes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def historialSolicitudesALM(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnHistorialSolicitudes = True
        almacen = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes


        return render(request, "empleadosCustom/almacen/historialSolicitudes.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnHistorialSolicitudes":estaEnHistorialSolicitudes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def solicitudesMarcadasALM(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnSolicitudesMarcadas = True
        almacen = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes


        return render(request, "empleadosCustom/almacen/solicitudesMarcadas.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

    
def verHerramientasALM(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnVerHerramientas = True
        almacen = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        registrosHerramientas = HerramientasAlmacen.objects.all()
        registrosHerramientasModal = HerramientasAlmacen.objects.all()
        registrosHerramientasModalBaja = HerramientasAlmacen.objects.all()
        
        registrosHerramientasDañadas = HerramientasAlmacenInactivas.objects.all()
        datosHerramientasDañadas = []
        for herramientaDañada in registrosHerramientasDañadas:
            id_herramienta = herramientaDañada.id_herramienta_id
            
            #consulta a herramienta
            datosHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = id_herramienta)
            
            for herramienta in datosHerramienta:
            
                tipo = herramienta.tipo_herramienta
                codigo = herramienta.codigo_herramienta
                nombre = herramienta.nombre_herramienta
                marca = herramienta.marca
                descripcion = herramienta.descripcion_herramienta
            
            datosHerramientasDañadas.append([id_herramienta, tipo, codigo, nombre, marca, descripcion])
        
        listaDañadas = zip(registrosHerramientasDañadas, datosHerramientasDañadas)    
    
        if "herramientaActualizada" in request.session:
            herramientaAct = request.session['herramientaActualizada']
            del request.session['herramientaActualizada']
            return render(request, "empleadosCustom/almacen/verHerramientas.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnVerHerramientas":estaEnVerHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "registrosHerramientas":registrosHerramientas, "registrosHerramientasModal":registrosHerramientasModal, "registrosHerramientasModalBaja":registrosHerramientasModalBaja, "listaDañadas":listaDañadas, "herramientaAct":herramientaAct})
            


        return render(request, "empleadosCustom/almacen/verHerramientas.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnVerHerramientas":estaEnVerHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "registrosHerramientas":registrosHerramientas, "registrosHerramientasModalBaja":registrosHerramientasModalBaja, "registrosHerramientasModal":registrosHerramientasModal, "listaDañadas":listaDañadas})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def agregarHerramientasALM(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnAgregarHerramientas = True
        almacen = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes


        if request.method == "POST":
            tipoHerramienta = request.POST['tipoHerramienta']
            nombreHerramienta = request.POST['nombreHerramienta']
            marcaHerramienta = request.POST['marcaHerramienta']
            unidadMedida = request.POST['unidadMedida']
            descripcion = request.POST['descripcion']
            imagenHerramienta = request.FILES.get('imagenHerramienta')
            skuHerramienta = request.POST['skuHerramienta']
            cantidadHerramienta = request.POST['cantidadHerramienta']
            
            
            #Codigo de herramienta
            consultaHerramientas = HerramientasAlmacen.objects.all()
                
            #Si hay, sumar codigo
            if consultaHerramientas:
                for herramienta in consultaHerramientas:
                    codigo = herramienta.codigo_herramienta
                    
                    #el ultimo código
                primerDigito = codigo[2]
                segundoDigito = codigo[3]
                tercerDigito = codigo[4]
                cuartoDigito = codigo[5]
                    
                numero = primerDigito+segundoDigito+tercerDigito+cuartoDigito
                intNumero = int(numero)
                codigoInt = intNumero + 1
                codigo = "HA"+str(codigoInt)
            else:
                codigo = "HA1000"
                
                # Registro de herramienta
            fechaAlta =  datetime.now()
                
            if imagenHerramienta:
                registroHerramienta = HerramientasAlmacen(codigo_herramienta = codigo,
                                                          tipo_herramienta = tipoHerramienta,
                                                          nombre_herramienta = nombreHerramienta,
                                                          descripcion_herramienta = descripcion,
                                                          marca = marcaHerramienta,
                                                          unidad = unidadMedida,
                                                          sku = skuHerramienta,
                                                          imagen_herramienta = imagenHerramienta,
                                                          estado_herramienta = "F",
                                                          motivo_estado = "Es funcional, disponible para prestamo",
                                                          fecha_alta = fechaAlta, 
                                                          cantidad_existencia = cantidadHerramienta)
            else:
                registroHerramienta = HerramientasAlmacen(codigo_herramienta = codigo,
                                                          tipo_herramienta = tipoHerramienta,
                                                          nombre_herramienta = nombreHerramienta,
                                                          descripcion_herramienta = descripcion,
                                                          marca = marcaHerramienta,
                                                          unidad = unidadMedida,
                                                          sku = skuHerramienta,
                                                          estado_herramienta = "F",
                                                          motivo_estado = "Es funcional, disponible para prestamo",
                                                          fecha_alta = fechaAlta, 
                                                          cantidad_existencia = cantidadHerramienta)
                
            registroHerramienta.save()
            if registroHerramienta:
                herramientaGuardada = "La herramienta " + nombreHerramienta + " ha sido guardada satisfactoriamente!"
                return render(request, "empleadosCustom/almacen/agregarHerramientas.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnAgregarHerramientas":estaEnAgregarHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "herramientaGuardada":herramientaGuardada})
        return render(request, "empleadosCustom/almacen/agregarHerramientas.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnAgregarHerramientas":estaEnAgregarHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio







#Herramientas
def solicitarHerramientas(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnSolicitarHerramienta = True
        solicitantePrestamo = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        fechaHoy = datetime.now()
        
        
        data = [i.json() for i in HerramientasAlmacen.objects.all()]
        consulta = HerramientasAlmacen.objects.all()
        consulta2 = HerramientasAlmacen.objects.all()
        consultaFunciones = HerramientasAlmacen.objects.all()
        
        if request.method == "POST":
            
            fecha_solicitud = datetime.now()
            fecha_requerido = request.POST['fecha_requerido']
            fecha_separada = fecha_requerido.split("/") #29   06    2018            2018     29   06
            fecha_normal_requerido = fecha_separada[2] + "-" + fecha_separada[0] + "-" + fecha_separada[1]
            
            proyecto = request.POST['proyecto']
            notas = request.POST['notas']
            cantidadHerramientasSolicitadas = request.POST['cantidadHerramientasSolicitadas']
            otrasHerramientas = request.POST['otrasHerramientas']
            
            if otrasHerramientas == "":
                otrasHerramientas = "No se solicitan otras herramientas"
            
            arregloCantidades = []
            
            arregloIdsHerramientas = cantidadHerramientasSolicitadas.split(",")
            contadorHerramienta = 0
            for h in arregloIdsHerramientas:
                contadorHerramienta = contadorHerramienta + 1
            
            
            idPregunta = "id"
            cantidadSolicitar = "cantidadSolicitar"
            herramienta = 0
            for idherramienta in range(contadorHerramienta):
                herramienta= herramienta + 1
                nameIdDeHerramienta = idPregunta + str(herramienta)
                nameCantidadASolicitar = cantidadSolicitar + str(herramienta)
                
                #Obtener valores que se mandaron
                idHerramientaMandado = request.POST[nameIdDeHerramienta]
                cantidadSolicitadaMandada = request.POST[nameCantidadASolicitar]
                arregloCantidades.append(cantidadSolicitadaMandada)

            stringCantidadesAGuardarEnBD = ""
            contadorCantidades = 0
            for cantidad in arregloCantidades:
                contadorCantidades = contadorCantidades + 1
                if contadorCantidades == 1:
                    stringCantidadesAGuardarEnBD = str(cantidad)
                else:
                    stringCantidadesAGuardarEnBD += "," + str(cantidad)
                    
            
            registroSolicitudPrestamo = PrestamosAlmacen(fecha_solicitud = fecha_solicitud,
                                                         fecha_requerimiento = fecha_normal_requerido,
                                                         id_empleado_solicitante = Empleados.objects.get(id_empleado = id_admin),
                                                         proyecto_tarea = proyecto,
                                                         otro = otrasHerramientas,
                                                         observaciones = notas,
                                                         id_herramientaInstrumento = cantidadHerramientasSolicitadas,
                                                         cantidades_solicitadas = stringCantidadesAGuardarEnBD,
                                                         estatus = "Pendiente")
            registroSolicitudPrestamo.save()
            solicitudGuardada = "La solicitud ha sigo guardada con exito!"
            return render(request, "empleadosCustom/almacen/empleados/solicitudHerramientas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnSolicitarHerramienta":estaEnSolicitarHerramienta,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                                "fechaHoy":fechaHoy, "context":json.dumps(data), "HerramientasAlmacen":consulta, "consulta2":consulta2, "consultaFunciones":consultaFunciones, "solicitudGuardada":solicitudGuardada, "contadorHerramienta":contadorHerramienta})

        return render(request, "empleadosCustom/almacen/empleados/solicitudHerramientas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnSolicitarHerramienta":estaEnSolicitarHerramienta,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                                "fechaHoy":fechaHoy, "context":json.dumps(data), "HerramientasAlmacen":consulta, "consulta2":consulta2, "consultaFunciones":consultaFunciones})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def verMisPrestamos(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnVerMisPrestamos = True
        solicitantePrestamo = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        solicitudesPendientes = PrestamosAlmacen.objects.filter(id_empleado_solicitante_id__id_empleado = id_admin)
        
        arregloHerramientas = []
        for solicitud in solicitudesPendientes:
            
            #Herramientas
            herramientas = solicitud.id_herramientaInstrumento
            arregloIndividualHerramientas = herramientas.split(",") #[1,2]
            
            codigos = []
            nombres = []
            descripciones = []
            for herramientaIndividual in arregloIndividualHerramientas:
                
                idHerramienta = int(herramientaIndividual)
                
                consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                
                for dato in consultaHerramienta:
                    codigo = dato.codigo_herramienta
                    nombre = dato.nombre_herramienta
                    descripcion = dato.descripcion_herramienta
                codigos.append(codigo)
                nombres.append(nombre)
                descripciones.append(descripciones)
                    
            
            # Cantidades
            cantidades = solicitud.cantidades_solicitadas
            arregloIndividualCantidades = cantidades.split(",")
            
        arregloHerramientas = zip(codigos,nombres,descripciones, arregloIndividualCantidades)
        
        


        return render(request, "empleadosCustom/almacen/empleados/verMisPrestamos.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnVerMisPrestamos":estaEnVerMisPrestamos,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                          "solicitudesPendientes":solicitudesPendientes, "arregloHerramientas":arregloHerramientas})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def actualizarCantidadesHerramientasAlmacen(request):
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        if request.method == "POST":
            idHerramientaActualizar = request.POST['idHerramientaActualizar']
            cantidadHerramientaActualizar = request.POST['cantidadHerramientaActualizar']
            intCantidadHerramientaActualizar = int(cantidadHerramientaActualizar)
            
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaActualizar)
            
            for dato in consultaHerramienta:
                cantidadExistenteActual = dato.cantidad_existencia
                nombreHerramienta = dato.nombre_herramienta
                
            intCantidadExistenciaActual = int(cantidadExistenteActual)
            
            sumaCantidad = intCantidadExistenciaActual + intCantidadHerramientaActualizar
            
            #Actualizar cantidad
            actualizacion = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaActualizar).update(cantidad_existencia = sumaCantidad)
            
            if actualizacion:
                request.session['herramientaActualizada'] = "La herramienta " + nombreHerramienta + " ha sido actualizada satisfactoriamente!"
                
                return redirect('/verHerramientasALM/')
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def bajaHerramientaAlmacen(request):
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        if request.method == "POST":
            idHerramientaBaja = request.POST['idHerramientaBaja']
            motivoBaja = request.POST['motivoBaja']
            explicacion = request.POST['explicacion']
            
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaBaja)
            
            for dato in consultaHerramienta:
                cantidadExistenteActual = dato.cantidad_existencia
                nombreHerramienta = dato.nombre_herramienta
                
            intCantidadExistenciaActual = int(cantidadExistenteActual)
            
            
            restaCantidad = intCantidadExistenciaActual - 1
            fechaBaja = datetime.now()
            #Actualizar cantidad
            actualizacion = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaBaja).update(cantidad_existencia = restaCantidad)
            
            #Registro de baja 
            registroDeBaja = HerramientasAlmacenInactivas(id_herramienta = HerramientasAlmacen.objects.get(id_herramienta = idHerramientaBaja), motivo_baja = motivoBaja, explicacion_baja = explicacion, 
                                                          cantidad_baja = "1", fecha_baja = fechaBaja)
            registroDeBaja.save()
            if actualizacion and registroDeBaja:
                request.session['herramientaActualizada'] = "La herramienta " + nombreHerramienta + " ha sido dada de baja satisfactoriamente!"
                
                return redirect('/verHerramientasALM/')
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    

