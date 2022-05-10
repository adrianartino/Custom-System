#Librerías
from email.mime import text
from logging import info
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
from appCS.models import Areas, Empleados, Equipos, Carta, Impresoras, Cartuchos, CalendarioMantenimiento, Programas, ProgramasArea, EquipoPrograma, Bitacora, Renovacion_Equipos, Renovacion_Impresoras, Preguntas, Encuestas, Respuestas, EncuestaEmpleadoResuelta, Mouses, Teclados, Monitores, HerramientasAlmacen, InstrumentosAlmacen, HerramientasAlmacenInactivas, PrestamosAlmacen, RequisicionCompraAlmacen

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
        
        solicitudesPendientes = PrestamosAlmacen.objects.filter(estatus="Pendiente")
        empleadosSolicitantes = []
        
        if solicitudesPendientes:
            for solicitud in solicitudesPendientes:
                
                #Herramientas
                herramientas = solicitud.id_herramientaInstrumento #Lista de herramientas 1,2
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
                
                idEmpleadoSolicitante = solicitud.id_empleado_solicitante_id
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
                for dato in consultaEmpleado:
                    nombreEmpleadoSolicitante = dato.nombre
                    apellidosEmpleadoSolicitante = dato.apellidos
                    
                    nombreCompletoEmpleadoSolicitante = nombreEmpleadoSolicitante + " " + apellidosEmpleadoSolicitante
                    empleadosSolicitantes.append(nombreCompletoEmpleadoSolicitante)
                
                
            arregloHerramientas = zip(codigos,nombres,descripciones, arregloIndividualCantidades)
            
            listaSolicitudesPendientes = zip(solicitudesPendientes,empleadosSolicitantes)
            

            if "prestamoEntregado" in request.session:
                prestamoEntregado = request.session["prestamoEntregado"]
                del request.session["prestamoEntregado"]
                return render(request, "empleadosCustom/almacen/solicitudesPendientes.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesPendientes":estaEnSolicitudesPendientes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "arregloHerramientas":arregloHerramientas, "solicitudesPendientes":solicitudesPendientes, "listaSolicitudesPendientes":listaSolicitudesPendientes, "prestamoEntregado":prestamoEntregado})

            return render(request, "empleadosCustom/almacen/solicitudesPendientes.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesPendientes":estaEnSolicitudesPendientes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "arregloHerramientas":arregloHerramientas, "solicitudesPendientes":solicitudesPendientes, "listaSolicitudesPendientes":listaSolicitudesPendientes})
        else:
            sinPendientes = True
            if "prestamoEntregado" in request.session:
                prestamoEntregado = request.session["prestamoEntregado"]
                del request.session["prestamoEntregado"]    
                return render(request, "empleadosCustom/almacen/solicitudesPendientes.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesPendientes":estaEnSolicitudesPendientes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "sinPendientes":sinPendientes,"prestamoEntregado":prestamoEntregado})
                
            return render(request, "empleadosCustom/almacen/solicitudesPendientes.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesPendientes":estaEnSolicitudesPendientes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "sinPendientes":sinPendientes})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def firmarPrestamo(request):
    
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
        
        if request.method == "POST":
            idPrestamoRecibido = request.POST['idPrestamo']
            
            infoPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoRecibido)
            
            for dato in infoPrestamo:
                idEmpleadoSolicitante = dato.id_empleado_solicitante_id
                herramientasSolicitadas = dato.id_herramientaInstrumento
                cantidadesSolicitadas = dato.cantidades_solicitadas
                otro = dato.otro
            
            #Información de empleado
            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
            for datoEmpleado in consultaEmpleado:
                nombre = datoEmpleado.nombre
                apellidos = datoEmpleado.apellidos
                nombreCompletoEmpleadoSolicitante = nombre + " " + apellidos
                
                idArea = datoEmpleado.id_area_id
                consultaArea = Areas.objects.filter(id_area = idArea)
                for datoArea in consultaArea:
                    nombreDepartamento = datoArea.nombre
                    colorDepartamento = datoArea.color
                    
            #Información de herramientas
            arregloCantidadesHerramientas = cantidadesSolicitadas.split(",")
            herramientasAPrestar = []
            
            arregloIdsHerramientasAPrestar = herramientasSolicitadas.split(",")
            for idHerramienta in arregloIdsHerramientasAPrestar:
                consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                
                for datoHerramienta in consultaHerramienta:
                    id_herramienta = datoHerramienta.id_herramienta
                    codigo_herramienta = datoHerramienta.codigo_herramienta
                    tipo_herramienta = datoHerramienta.tipo_herramienta
                    nombre_herramienta = datoHerramienta.nombre_herramienta
                    marca = datoHerramienta.marca
                    imagen = datoHerramienta.imagen_herramienta
                    descripcion_herramienta = datoHerramienta.descripcion_herramienta
                    unidad_herramienta = datoHerramienta.unidad
                    sku_herramienta = datoHerramienta.sku
                    cantidad_existencia = datoHerramienta.cantidad_existencia
                    
                herramientasAPrestar.append([id_herramienta, codigo_herramienta, tipo_herramienta,
                                             nombre_herramienta, marca, imagen, descripcion_herramienta,
                                             unidad_herramienta, sku_herramienta, cantidad_existencia])
            
            
            listaHerramientas = zip(herramientasAPrestar, arregloCantidadesHerramientas)
            
            return render(request, "empleadosCustom/almacen/firmarPrestamo.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesPendientes":estaEnSolicitudesPendientes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, 
                                                                                   "infoPrestamo":infoPrestamo, "nombreCompletoEmpleadoSolicitante":nombreCompletoEmpleadoSolicitante,
                                                                                   "nombreDepartamento":nombreDepartamento, "colorDepartamento":colorDepartamento, "listaHerramientas":listaHerramientas, "otro":otro})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def firmarDevolucion(request):
    
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
        
        
        if request.method == "POST":
            idPrestamoRecibido = request.POST['idPrestamo']
            herramientaBaja = False
        
        elif "idPrestamoActualizado" in request.session:
            idPrestamoRecibido =  request.session['idPrestamoActualizado']
            herramientaBaja =  request.session['herramientaActualizada']
            
        infoPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoRecibido)
            
        for dato in infoPrestamo:
            idEmpleadoSolicitante = dato.id_empleado_solicitante_id
            herramientasSolicitadas = dato.id_herramientaInstrumento
            cantidadesSolicitadas = dato.cantidades_solicitadas
            otro = dato.otro
            
        #Información de empleado
        consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
        for datoEmpleado in consultaEmpleado:
            nombre = datoEmpleado.nombre
            apellidos = datoEmpleado.apellidos
            nombreCompletoEmpleadoSolicitante = nombre + " " + apellidos
                
            idArea = datoEmpleado.id_area_id
            consultaArea = Areas.objects.filter(id_area = idArea)
            for datoArea in consultaArea:
                nombreDepartamento = datoArea.nombre
                colorDepartamento = datoArea.color
                    
        #Información de herramientas
        arregloCantidadesHerramientas = cantidadesSolicitadas.split(",")
        herramientasPrestadas = []
        herramientasPrestadasModalsBaja = []
            
        arregloIdsHerramientasAPrestar = herramientasSolicitadas.split(",")
        for idHerramienta in arregloIdsHerramientasAPrestar:
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                
            for datoHerramienta in consultaHerramienta:
                id_herramienta = datoHerramienta.id_herramienta
                codigo_herramienta = datoHerramienta.codigo_herramienta
                tipo_herramienta = datoHerramienta.tipo_herramienta
                nombre_herramienta = datoHerramienta.nombre_herramienta
                marca = datoHerramienta.marca
                imagen = datoHerramienta.imagen_herramienta
                descripcion_herramienta = datoHerramienta.descripcion_herramienta
                unidad_herramienta = datoHerramienta.unidad
                sku_herramienta = datoHerramienta.sku
                cantidad_existencia = datoHerramienta.cantidad_existencia
                    
            herramientasPrestadas.append([id_herramienta, codigo_herramienta, tipo_herramienta,
                                             nombre_herramienta, marca, imagen, descripcion_herramienta,
                                             unidad_herramienta, sku_herramienta, cantidad_existencia])
            herramientasPrestadasModalsBaja.append([id_herramienta, codigo_herramienta, tipo_herramienta,
                                             nombre_herramienta, marca, imagen, descripcion_herramienta,
                                             unidad_herramienta, sku_herramienta, cantidad_existencia])
            
            
        listaHerramientas = zip(herramientasPrestadas, arregloCantidadesHerramientas)
            
        return render(request, "empleadosCustom/almacen/firmarDevolucion.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, 
                                                                                   "infoPrestamo":infoPrestamo, "nombreCompletoEmpleadoSolicitante":nombreCompletoEmpleadoSolicitante,
                                                                                   "nombreDepartamento":nombreDepartamento, "colorDepartamento":colorDepartamento, "listaHerramientas":listaHerramientas, "otro":otro, "herramientasPrestadasModalsBaja":herramientasPrestadasModalsBaja, "herramientaBaja":herramientaBaja})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    
    
def guardarEntrega(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        if request.method == "POST":
            idPrestamoGuardar = request.POST['idPrestamoGuardar']
            condicionesEntrega = request.POST['condicionesEntrega']
            canvasLargo = request.POST['canvasData']
            format, imgstr = canvasLargo.split(';base64,')
            ext = format.split('/')[-1]
            archivo = ContentFile(base64.b64decode(imgstr), name= "Prestamo"+str(idPrestamoGuardar) + '.' + ext)    
            
            fechaPrestamo = datetime.now()
            #actualizarRegistro
            
            actualizacionPrestamo = PrestamosAlmacen.objects.get(id_prestamo = idPrestamoGuardar)
            actualizacionPrestamo.fecha_prestamo = fechaPrestamo
            actualizacionPrestamo.firma_prestamo = archivo
            actualizacionPrestamo.condiciones = condicionesEntrega
            actualizacionPrestamo.estatus = "En prestamo"
            actualizacionPrestamo.save()
            
            if actualizacionPrestamo:
                #AQUI SE DEBEN DE DAR DE BAJA LAS CANTIDADES SELECCIONADAS
                consultaPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoGuardar)
                for datos in consultaPrestamo:
                    idsHerramientas = datos.id_herramientaInstrumento
                    cantidadesHerramientas = datos.cantidades_solicitadas
                    idEmpleadoSolicitante = datos.id_empleado_solicitante_id
                    fecha_solicitud = datos.fecha_solicitud
                    proyecto = datos.proyecto_tarea
                    imagenFirmaEntrega = datos.firma_prestamo
                    
                arregloCantidadesHerramientas = cantidadesHerramientas.split(",")
                arregloIdsHerramientas = idsHerramientas.split(",")
                
                listaHerramientas = zip(arregloIdsHerramientas, arregloCantidadesHerramientas)
                
                arregloTablaHerramientasCorreo = []
                
                for herramienta, cantidad in listaHerramientas:
                    consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = herramienta)
                    for datoHerramienta in consultaHerramienta:
                        cantidadActualEnExistencia = datoHerramienta.cantidad_existencia
                        idHerramienta = datoHerramienta.id_herramienta
                        codigoHerramienta = datoHerramienta.codigo_herramienta
                        skuHerramienta = datoHerramienta.sku
                        nombreHerramienta = datoHerramienta.nombre_herramienta
                        marcaHerramienta = datoHerramienta.marca
                        if datoHerramienta.imagen_herramienta == None:
                            imagenHerramienta = "Sin imagen"
                        else: 
                            imagenHerramienta = datoHerramienta.imagen_herramienta
                        cantidadPrestada = str(cantidad)
                    
                    cantidadActualizada = cantidadActualEnExistencia - int(cantidad)
                    
                    actualizarExistenciaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = herramienta).update(cantidad_existencia = cantidadActualizada)
                    
                    arregloTablaHerramientasCorreo.append([idHerramienta,codigoHerramienta,skuHerramienta,nombreHerramienta,marcaHerramienta,imagenHerramienta,cantidadActualizada,cantidadPrestada])
                    
                if actualizarExistenciaHerramienta:
                
            
                    request.session['prestamoEntregado'] = "El prestamo "+ str(idPrestamoGuardar)+" ha sido entregado satisfactoriamente!"
                    
                    #Madar correo
                    datosEmpleadoSolicitante = Empleados.objects.filter(id_empleado=idEmpleadoSolicitante)
                    for dato in datosEmpleadoSolicitante:
                        nombreSolicitante= dato.nombre
                        apellidosSolicitante=dato.apellidos
                        correoSolicitante=dato.correo
                    
                    
                    asunto = "CS | Nueva entrega de préstamo a empleado."
                    plantilla = "empleadosCustom/almacen/correos/correoEntregaHerramienta.html"
                    
                    
                   
                    html_mensaje = render_to_string(plantilla, {"nombreSolicitante": nombreSolicitante, "apellidosSolicitante": apellidosSolicitante, "correoSolicitante": correoSolicitante,
                                                                "fecha_solicitud":fecha_solicitud,
                                                                "fecha_entrega":fechaPrestamo,
                                                                "proyecto":proyecto,
                                                                "imagenFirmaEntrega":imagenFirmaEntrega,
                                                                "idPrestamoEntregado":idPrestamoGuardar,
                                                                "arregloTablaHerramientasCorreo":arregloTablaHerramientasCorreo})
                    email_remitente = settings.EMAIL_HOST_USER
                    email_destino = ['sistemas@customco.com.mx']
                    mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                    mensaje.content_subtype = 'html'
                    mensaje.send()

                    return redirect("/solicitudesPendientesALM/")
            
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def guardarDevolucion(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        if request.method == "POST":
            idPrestamoGuardar = request.POST['idPrestamoGuardar']
            condicionesDevolucion = request.POST['condicionesEntrega']
            canvasLargo = request.POST['canvasData']
            format, imgstr = canvasLargo.split(';base64,')
            ext = format.split('/')[-1]
            archivo = ContentFile(base64.b64decode(imgstr), name= "Prestamo"+str(idPrestamoGuardar) + '.' + ext)    
            
            fechaDevolucion = datetime.now()
            #actualizarRegistro
            
            actualizacionPrestamo = PrestamosAlmacen.objects.get(id_prestamo = idPrestamoGuardar)
            actualizacionPrestamo.fecha_devolucion = fechaDevolucion
            actualizacionPrestamo.firma_devolucion = archivo
            actualizacionPrestamo.condiciones = condicionesDevolucion
            actualizacionPrestamo.estatus = "Devuelto"
            actualizacionPrestamo.save()
            
            if actualizacionPrestamo:
                #AQUI SE DEBEN DE DAR DE ALTA LAS CANTIDADES SELECCIONADAS
                consultaPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoGuardar)
                for datos in consultaPrestamo:
                    idsHerramientas = datos.id_herramientaInstrumento
                    cantidadesHerramientas = datos.cantidades_solicitadas
                    idEmpleadoSolicitante = datos.id_empleado_solicitante_id
                    fecha_solicitud = datos.fecha_solicitud
                    fechaPrestamo = datos.fecha_prestamo
                    proyecto = datos.proyecto_tarea
                    imagenFirmaDevolucion = datos.fecha_devolucion
                    
                arregloCantidadesHerramientas = cantidadesHerramientas.split(",")
                arregloIdsHerramientas = idsHerramientas.split(",")
                
                listaHerramientas = zip(arregloIdsHerramientas, arregloCantidadesHerramientas)
                
                arregloTablaHerramientasCorreo = []
                
                for herramienta, cantidad in listaHerramientas:
                    consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = herramienta)
                    for datoHerramienta in consultaHerramienta:
                        cantidadActualEnExistencia = datoHerramienta.cantidad_existencia
                        idHerramienta = datoHerramienta.id_herramienta
                        codigoHerramienta = datoHerramienta.codigo_herramienta
                        skuHerramienta = datoHerramienta.sku
                        nombreHerramienta = datoHerramienta.nombre_herramienta
                        marcaHerramienta = datoHerramienta.marca
                        if datoHerramienta.imagen_herramienta == None:
                            imagenHerramienta = "Sin imagen"
                        else: 
                            imagenHerramienta = datoHerramienta.imagen_herramienta
                        cantidadDevuelta = str(cantidad)
                    
                    cantidadActualizada = cantidadActualEnExistencia + int(cantidad)
                    
                    actualizarExistenciaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = herramienta).update(cantidad_existencia = cantidadActualizada)
                    arregloTablaHerramientasCorreo.append([idHerramienta,codigoHerramienta,skuHerramienta,nombreHerramienta,marcaHerramienta,imagenHerramienta,cantidadActualizada,cantidadDevuelta])
                    
                if actualizarExistenciaHerramienta:
                
            
                    request.session['prestamoDevuelto'] = "El prestamo "+ str(idPrestamoGuardar)+" ha sido devuelto satisfactoriamente!"

                    datosEmpleadoSolicitante = Empleados.objects.filter(id_empleado=idEmpleadoSolicitante)
                    for dato in datosEmpleadoSolicitante:
                        nombreSolicitante= dato.nombre
                        apellidosSolicitante=dato.apellidos
                        correoSolicitante=dato.correo
                    
                    
                    asunto = "CS | Nueva devolución de préstamo a almacén."
                    plantilla = "empleadosCustom/almacen/correos/correoDevolucionHerramienta.html"
                    
                    
                   
                    html_mensaje = render_to_string(plantilla, {"nombreSolicitante": nombreSolicitante, "apellidosSolicitante": apellidosSolicitante, "correoSolicitante": correoSolicitante,
                                                                "fecha_solicitud":fecha_solicitud,
                                                                "fecha_entrega":fechaPrestamo,
                                                                "fecha_devolucion":fechaDevolucion,
                                                                "proyecto":proyecto,
                                                                "imagenFirmaEntrega":imagenFirmaDevolucion,
                                                                "idPrestamoEntregado":idPrestamoGuardar,
                                                                "arregloTablaHerramientasCorreo":arregloTablaHerramientasCorreo})
                    email_remitente = settings.EMAIL_HOST_USER
                    email_destino = ['sistemas@customco.com.mx']
                    mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                    mensaje.content_subtype = 'html'
                    mensaje.send()
                    
                    return redirect("/solicitudesMarcadasALM/")
            
    
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
        
        prestamosDevueltos = PrestamosAlmacen.objects.filter(estatus="Devuelto")
        empleadosSolicitantes = []
        conDaño = []
        
        if prestamosDevueltos:
            for prestamoDevuelto in prestamosDevueltos:
                
                idPrestamoDevuelto = prestamoDevuelto.id_prestamo
                
                consultaPrestamoConDaño = HerramientasAlmacenInactivas.objects.filter(id_prestamo_id__id_prestamo = idPrestamoDevuelto)
                conDaños = ""
                #Si ese prestamo se entregó con algun daño..
                nombresHerramientasDañadas = []
                motivosDañados = []
                idsHerramientasDañadas = []
                if consultaPrestamoConDaño:
                    conDaños = "SI"
                    for daño in consultaPrestamoConDaño:
                        
                        idHerramientaDañada = daño.id_herramienta_id
                        motivo = daño.motivo_baja
                        
                        
                        idsHerramientasDañadas.append(idHerramientaDañada)
                        motivosDañados.append(motivo)
                        
                        consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaDañada)
                        for datoH in consultaHerramienta:
                            nombreHerramientaDañada = datoH.nombre_herramienta
                            
                        nombresHerramientasDañadas.append(nombreHerramientaDañada)
                    
                else: 
                    conDaños = "NO"
                    idsHerramientasDañadas.append("jijija")
                
                herramientasDañadas = zip(idsHerramientasDañadas, nombresHerramientasDañadas, motivosDañados)
                
                conDaño.append(conDaños)
                    
                
                #Herramientas
                herramientasDevueltas = prestamoDevuelto.id_herramientaInstrumento #Lista de herramientas 1,2
                arregloIndividualHerramientas = herramientasDevueltas.split(",") #[1,2]
                
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
                    descripciones.append(descripcion)
                        
                
                # Cantidades
                cantidades = prestamoDevuelto.cantidades_solicitadas
                arregloIndividualCantidades = cantidades.split(",")
                
                idEmpleadoSolicitante = prestamoDevuelto.id_empleado_solicitante_id
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
                for dato in consultaEmpleado:
                    nombreEmpleadoSolicitante = dato.nombre
                    apellidosEmpleadoSolicitante = dato.apellidos
                    
                    nombreCompletoEmpleadoSolicitante = nombreEmpleadoSolicitante + " " + apellidosEmpleadoSolicitante
                    empleadosSolicitantes.append(nombreCompletoEmpleadoSolicitante)
                
                
            arregloHerramientas = zip(codigos,nombres,descripciones, arregloIndividualCantidades)
            
            listaSolicitudesPendientes = zip(prestamosDevueltos,empleadosSolicitantes, conDaño)
            

            
            return render(request, "empleadosCustom/almacen/historialSolicitudes.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnHistorialSolicitudes":estaEnHistorialSolicitudes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "arregloHerramientas":arregloHerramientas, "solicitudesPendientes":prestamosDevueltos, "listaSolicitudesPendientes":listaSolicitudesPendientes, "herramientasDañadas":herramientasDañadas})
        else:
            sinPendientes = True
                
            return render(request, "empleadosCustom/almacen/historialSolicitudes.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnHistorialSolicitudes":estaEnHistorialSolicitudes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "sinPendientes":sinPendientes})
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
        
        prestamosRealizados = PrestamosAlmacen.objects.filter(estatus="En prestamo")
        empleadosPrestados = []
        
        if prestamosRealizados:
            for prestamo in prestamosRealizados:
                
                #Herramientas
                herramientas = prestamo.id_herramientaInstrumento #Lista de herramientas 1,2
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
                    descripciones.append(descripcion)
                        
                
                # Cantidades
                cantidades = prestamo.cantidades_solicitadas
                arregloIndividualCantidades = cantidades.split(",")
                
                idEmpleadoSolicitante = prestamo.id_empleado_solicitante_id
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
                for dato in consultaEmpleado:
                    nombreEmpleadoSolicitante = dato.nombre
                    apellidosEmpleadoSolicitante = dato.apellidos
                    
                    nombreCompletoEmpleadoSolicitante = nombreEmpleadoSolicitante + " " + apellidosEmpleadoSolicitante
                    empleadosPrestados.append(nombreCompletoEmpleadoSolicitante)
                
                
            arregloHerramientas = zip(codigos,nombres,descripciones, arregloIndividualCantidades)
            
            listaPrestamosRealizados = zip(prestamosRealizados,empleadosPrestados)
            

            if "prestamoDevuelto" in request.session:
                prestamoEntregado = request.session["prestamoDevuelto"]
                del request.session["prestamoDevuelto"]
                return render(request, "empleadosCustom/almacen/solicitudesMarcadas.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "arregloHerramientas":arregloHerramientas, "prestamosRealizados":prestamosRealizados, "listaPrestamosRealizados":listaPrestamosRealizados, "prestamoEntregado":prestamoEntregado})

            return render(request, "empleadosCustom/almacen/solicitudesMarcadas.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "arregloHerramientas":arregloHerramientas, "prestamosRealizados":prestamosRealizados, "listaPrestamosRealizados":listaPrestamosRealizados})
        else:
            sinPrestamos = True
            if "prestamoDevuelto" in request.session:
                prestamoEntregado = request.session["prestamoDevuelto"]
                del request.session["prestamoDevuelto"]    
                return render(request, "empleadosCustom/almacen/solicitudesMarcadas.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "sinPrestamos":sinPrestamos,"prestamoEntregado":prestamoEntregado})
                
            return render(request, "empleadosCustom/almacen/solicitudesMarcadas.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "sinPrestamos":sinPrestamos})
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
        
        #Herramientas dañadas
        registrosHerramientasDañadas = HerramientasAlmacenInactivas.objects.filter(enInventario = "Si")
        datosHerramientasDañadas = []
        for herramientaDañada in registrosHerramientasDañadas:
            id_herramienta = herramientaDañada.id_herramienta_id
            id_prestamo = herramientaDañada.id_prestamo
            #consulta a herramienta
            datosHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = id_herramienta)
            
            for herramienta in datosHerramienta:
            
                tipo = herramienta.tipo_herramienta
                codigo = herramienta.codigo_herramienta
                nombre = herramienta.nombre_herramienta
                marca = herramienta.marca
                descripcion = herramienta.descripcion_herramienta
                
                if id_prestamo == None:
                    id_prestamo = "Sin prestamo"
                    nombreEmpleadoResponsable = "Dado de baja por almacén"
                else:
                    consultaPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = id_prestamo)
                    for dato in consultaPrestamo:
                        idEmpleadoResponsable = dato.id_empleado_solicitante_id
                            
                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoResponsable)
                    for datoEmpleado in consultaEmpleado:
                        nombreEmpleadoResponsable = datoEmpleado.nombre
                    
            
            datosHerramientasDañadas.append([id_herramienta, tipo, codigo, nombre, marca, descripcion, id_prestamo, nombreEmpleadoResponsable])
        
        listaDañadas = zip(registrosHerramientasDañadas, datosHerramientasDañadas)    
    
        #Costos de herramientas
        costoTotalHerramienta = []
        herramientasDañadasXHerramienta = []
        herramientasEnPrestamo = []
        costoTotalDañoHerramienta = []
        prestamosDeHerramienta = []
        for herramienta in registrosHerramientas:
            cantidadExistencia = herramienta.cantidad_existencia
            costo = herramienta.costo
            
            idHerramienta = herramienta.id_herramienta
            consultaHerramientasDañadas = HerramientasAlmacenInactivas.objects.filter(id_herramienta_id__id_herramienta = idHerramienta, enInventario="Si")
            
            contadorHerramientasDañadas = 0
            for dañada in consultaHerramientasDañadas:
                contadorHerramientasDañadas = contadorHerramientasDañadas + 1
            
            totalExistenciaConDaños = cantidadExistencia + contadorHerramientasDañadas
            
            costoTotalDaño = costo * contadorHerramientasDañadas
            
           
            
            consultaPrestamos = PrestamosAlmacen.objects.filter(estatus = "En prestamo")
            contadorHerramientaEnPrestamo = 0
            for prestamo in consultaPrestamos:
                idsHerramientasPrestadas = prestamo.id_herramientaInstrumento
                cantidadesHerramientasPrestadas = prestamo.cantidades_solicitadas
                
                arregloIdsHerramientasPrestadas = idsHerramientasPrestadas.split(",")
                arregloCantidadesHerramientas = cantidadesHerramientasPrestadas.split(",")
                
                listaHerramientasEnPrestamo = zip(arregloIdsHerramientasPrestadas, arregloCantidadesHerramientas)
                
                for idH, cantidad in listaHerramientasEnPrestamo:
                    intidH = int(idH)
                    if intidH == idHerramienta:
                        contadorHerramientaEnPrestamo = contadorHerramientaEnPrestamo + int(cantidad)
                        
            if contadorHerramientaEnPrestamo == 0:
                costoTotalInventarioHerramienta = costo*totalExistenciaConDaños
            else:
                costoPrestados = costo*contadorHerramientaEnPrestamo
                costosTodos = costo*totalExistenciaConDaños
                costoTotalInventarioHerramienta = costoPrestados + costosTodos
            
            
            herramientasEnPrestamo.append(contadorHerramientaEnPrestamo)
            costoTotalHerramienta.append(costoTotalInventarioHerramienta)
            herramientasDañadasXHerramienta.append(contadorHerramientasDañadas)
            costoTotalDañoHerramienta.append(costoTotalDaño)
            
        
            #Prestamos de herramientas
            prestamosAlmacen = PrestamosAlmacen.objects.filter(estatus="En prestamo")
            prestamosHerramientaIndividual = []
            for prestamo in prestamosAlmacen:
                idsHerramientasPrestamo = prestamo.id_herramientaInstrumento
                idPrestamo = prestamo.id_prestamo
                idEmpleadoSolicitante = prestamo.id_empleado_solicitante_id
                
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
                for dato in consultaEmpleado:
                    nombreEmpleado = dato.nombre
                
                arregloIdsHerramientasPrestamo = idsHerramientasPrestamo.split(",")
                for idf in arregloIdsHerramientasPrestamo:
                    intId = int(idf)
                    if intId == idHerramienta:
                        prestamosHerramientaIndividual.append([idPrestamo, nombreEmpleado])
                  
            
            prestamosDeHerramienta.append(prestamosHerramientaIndividual)
            
            
        
            
        listaHerramientas = zip(registrosHerramientas, costoTotalHerramienta, herramientasDañadasXHerramienta, herramientasEnPrestamo, costoTotalDañoHerramienta, prestamosDeHerramienta)

        registrosHerramientasModal = zip(registrosHerramientas,herramientasEnPrestamo)
        registrosHerramientasModalBaja = zip(registrosHerramientas,herramientasEnPrestamo)
        
        costoTotalTotal = 0
        for costototal in costoTotalHerramienta:
            costoTotalTotal = costoTotalTotal + costototal
        
        #Si una herramienta fue actualizada..
        if "herramientaActualizada" in request.session:
            herramientaAct = request.session['herramientaActualizada']
            del request.session['herramientaActualizada']
            return render(request, "empleadosCustom/almacen/verHerramientas.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnVerHerramientas":estaEnVerHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "registrosHerramientas":registrosHerramientas, "registrosHerramientasModal":registrosHerramientasModal, "registrosHerramientasModalBaja":registrosHerramientasModalBaja, "listaDañadas":listaDañadas, "herramientaAct":herramientaAct, "listaHerramientas":listaHerramientas, "costoTotalTotal":costoTotalTotal})
            


        return render(request, "empleadosCustom/almacen/verHerramientas.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnVerHerramientas":estaEnVerHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "registrosHerramientas":registrosHerramientas, "registrosHerramientasModalBaja":registrosHerramientasModalBaja, "registrosHerramientasModal":registrosHerramientasModal, "listaDañadas":listaDañadas, "listaHerramientas":listaHerramientas, "costoTotalTotal":costoTotalTotal})
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
            costoHerramienta = request.POST['costoHerramienta']
            
            proveedorHerramienta = request.POST['proveedorHerramienta']
            odcHerramienta = request.POST['odcHerramienta']
            
            if proveedorHerramienta == "":
                proveedorHerramienta = "Sin proveedor"
            
            if odcHerramienta == "":
                odcHerramienta == "Sin orden de compra"
                
            
            
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
                                                          cantidad_existencia = cantidadHerramienta,
                                                          costo = costoHerramienta,
                                                          stock = cantidadHerramienta,
                                                          orden_compra_evidence = odcHerramienta,
                                                          proveedor = proveedorHerramienta)
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
                                                          cantidad_existencia = cantidadHerramienta,
                                                          costo = costoHerramienta,
                                                          stock = cantidadHerramienta,
                                                          orden_compra_evidence = odcHerramienta,
                                                          proveedor = proveedorHerramienta)
                
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
        
        #Mandar prestamos de cada herramienta
        
        consulta2 = HerramientasAlmacen.objects.all()
        datosPrestamosPorHerramienta = []
        datosHerramientasRequisicion = []
        
        for herramienta in consulta2:
            idHerramienta = herramienta.id_herramienta
            
            prestamos = PrestamosAlmacen.objects.filter(estatus = "En prestamo")
            prestamosHerramientaIndividual = []
            for prestamo in prestamos:
                idPrestamito = prestamo.id_prestamo
                idsHerramientas = prestamo.id_herramientaInstrumento
                cantidadesHerramientas = prestamo.cantidades_solicitadas
                solicitante = prestamo.id_empleado_solicitante_id 
                consultaSolicitante = Empleados.objects.filter(id_empleado = solicitante)
                for datoEmpleado in consultaSolicitante:
                    nombreSolicitante = datoEmpleado.nombre
                
                arregloIds = idsHerramientas.split(",")
                arregloCantidades = cantidadesHerramientas.split(",")
                
                listaHerramientasEnPrestamo = zip(arregloIds, arregloCantidades)
                
                for idH, cantidad in listaHerramientasEnPrestamo:
                    
                    intidh = int(idH)
                    if idHerramienta == intidh:
                        prestamosHerramientaIndividual.append([idPrestamito, nombreSolicitante, cantidad ])
            
            datosPrestamosPorHerramienta.append(prestamosHerramientaIndividual)
                
        consultaHerramientasTabla = zip(consulta2, datosPrestamosPorHerramienta)
            
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
            arregloCantidadesRequi = []
            names = []
            names2 = []
            
            arregloIdsHerramientas = cantidadHerramientasSolicitadas.split(",")
            
            idPregunta = "id"
            cantidadSolicitar = "cantidadSolicitar"
            cantidadSolicitarRequi = "cantidadSolicitarRequi"
            for idherramienta in arregloIdsHerramientas:      # 1 2
                stringHerramienta = str(idherramienta)
                nameIdDeHerramienta = idPregunta + stringHerramienta
                nameCantidadASolicitar = cantidadSolicitar + stringHerramienta
                nameCantidadSolicitarRequi = cantidadSolicitarRequi + stringHerramienta #cantidadSolicitarRequi1   #cantidadSolicitarRequi2
                
                #Obtener valores que se mandaron
                idHerramientaMandado = request.POST[nameIdDeHerramienta]
                cantidadSolicitadaMandada = request.POST[nameCantidadASolicitar]
                arregloCantidades.append(cantidadSolicitadaMandada)
                
                cantidadSolicitadaRequiMandada = request.POST[nameCantidadSolicitarRequi]
                arregloCantidadesRequi.append(cantidadSolicitadaRequiMandada)

            stringCantidadesAGuardarEnBD = ""
            contadorCantidades = 0
            for cantidad in arregloCantidades:
                contadorCantidades = contadorCantidades + 1
                if contadorCantidades == 1:
                    stringCantidadesAGuardarEnBD = str(cantidad)
                else:
                    stringCantidadesAGuardarEnBD += "," + str(cantidad)
                    
            
            listaHerramientasRequi = zip(arregloIdsHerramientas, arregloCantidadesRequi)
            
            
                    
            
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
            
            registrosPrestamos = PrestamosAlmacen.objects.filter(estatus="Pendiente")
            arrayIdsPrestamos = []
            
            for prest in registrosPrestamos:
                idPrestPendiente = prest.id_prestamo
                arrayIdsPrestamos.append(idPrestPendiente)
                
            ultimoID = 0
            for idd in arrayIdsPrestamos:
                idInt = int(idd)
                ultimoID = idInt
            
            
            for herramientaRequi, cantidadRequi in listaHerramientasRequi:
                
                #Si es 0, no guarda la requi!
                if cantidadRequi == "0":
                    nada = True
                else: #Se guarda la requi
                    nada = False
                    registroRequi = RequisicionCompraAlmacen(id_empleado_solicitante = Empleados.objects.get(id_empleado = id_admin),
                                                             id_herramienta = HerramientasAlmacen.objects.get(id_herramienta = herramientaRequi),
                                                             id_prestamo = PrestamosAlmacen.objects.get(id_prestamo = ultimoID),
                                                             cantidad_requerida = cantidadRequi,
                                                             fehca_requi = fecha_solicitud,
                                                             estatus_requi = "Pendiente")
                    registroRequi.save()
                    
                    consultaHerramientaRequerida = HerramientasAlmacen.objects.filter(id_herramienta = herramientaRequi)
                    for dato in consultaHerramientaRequerida:
                        nombreHerramientaRequerida = dato.nombre_herramienta
                        sku_herramientaRequerida = dato.sku
                        codigo = dato.codigo_herramienta
                        if dato.imagen_herramienta == None:
                            imagen = "sin imagen"
                        else:
                            imagen = dato.imagen_herramienta
                        marca = dato.marca
                        proveedor = dato.proveedor
                        ordenCompra = dato.orden_compra_evidence
                    
                    datosHerramientasRequisicion.append([herramientaRequi,nombreHerramientaRequerida,codigo,sku_herramientaRequerida,imagen, cantidadRequi, marca, proveedor,ordenCompra])
                    
                    
                    
            if nada == False:         
                request.session['solicitudGuardada'] = "La solicitud ha sigo guardada con exito! Se ha mandado la requisición de herramientas por correo!"
            else:
                request.session['solicitudGuardada'] = "La solicitud ha sigo guardada con exito!"
            
            #CORREO ELECTRÓNICO
            datosEmpleadoSolicitante = Empleados.objects.filter(id_empleado=id_admin)
            strUltimoPrestamo = PrestamosAlmacen.objects.count()
            ultimoPrestamo = str(strUltimoPrestamo)
            for dato in datosEmpleadoSolicitante:
                nombreSolicitante= dato.nombre
                apellidosSolicitante=dato.apellidos
                correoSolicitante=dato.correo
            
            if nada == False:    
                asunto = "CS | Nueva solicitud de préstamo de herramienta con Requisición de compra."
            else:
                asunto = "CS | Nueva solicitud de préstamo de herramienta."
            plantilla = "empleadosCustom/almacen/correos/correoSolicitud.html"
            
            if nada == False:
                html_mensaje = render_to_string(plantilla, {"nombreSolicitante": nombreSolicitante, "apellidosSolicitante": apellidosSolicitante, "correoSolicitante": correoSolicitante,
                                                        "fecha_solicitud":fecha_solicitud,
                                                        "fecha_normal_requerido":fecha_normal_requerido,
                                                        "proyecto":proyecto,
                                                        "ultimoPrestamo":ultimoPrestamo, "datosHerramientasRequisicion":datosHerramientasRequisicion })
            else:
                html_mensaje = render_to_string(plantilla, {"nombreSolicitante": nombreSolicitante, "apellidosSolicitante": apellidosSolicitante, "correoSolicitante": correoSolicitante,
                                                        "fecha_solicitud":fecha_solicitud,
                                                        "fecha_normal_requerido":fecha_normal_requerido,
                                                        "proyecto":proyecto,
                                                        "ultimoPrestamo":ultimoPrestamo})
            email_remitente = settings.EMAIL_HOST_USER
            email_destino = ['sistemas@customco.com.mx']
            mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
            mensaje.content_subtype = 'html'
            mensaje.send()
            
            
            
            return redirect('/verMisPrestamos/')

        return render(request, "empleadosCustom/almacen/empleados/solicitudHerramientas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnSolicitarHerramienta":estaEnSolicitarHerramienta,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                                "fechaHoy":fechaHoy, "context":json.dumps(data), "HerramientasAlmacen":consulta, "consulta2":consultaHerramientasTabla, "consultaFunciones":consultaFunciones})
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
        
        
        
        # PRESTAMOS PENDIENTES- ----------------------------------------------------------------------------------------------------------------------------
        solicitudesPendientes = PrestamosAlmacen.objects.filter(id_empleado_solicitante_id__id_empleado = id_admin, estatus="Pendiente")
        prestamosEntregados = PrestamosAlmacen.objects.filter(id_empleado_solicitante_id__id_empleado = id_admin, estatus="En prestamo")
        prestamosDevueltos = PrestamosAlmacen.objects.filter(id_empleado_solicitante_id__id_empleado = id_admin, estatus="Devuelto")
        
            
        
        #Pendientes
        arregloHerramientas = []
        codigos = []
        nombres = []
        descripciones = []
        
        #Entregados 
        arregloHerramientasEntregadas = []
        codigosHerramientasEntregadas = []
        nombresHerramientasEntregadas = []
        descripcionesHerramientasEntregadas = []
        
        #Pendientes
        conDaño = []
        nombresHerramientasDañadas = []
        motivosDañados = []
        idsHerramientasDañadas = []
        codigosDevueltos = []
        nombresDevueltos = []
        descripcionesDevueltos = []
        
        listaPrestamosDevueltos = ""
        herramientasDañadas = ""
        arregloHerramientasDevueltas = []
        
        
        if solicitudesPendientes:
            
            for solicitud in solicitudesPendientes:
                
                #Herramientas
                herramientas = solicitud.id_herramientaInstrumento
                arregloIndividualHerramientas = herramientas.split(",") #[1,2]
                
                
                for herramientaIndividual in arregloIndividualHerramientas:
                    
                    idHerramienta = int(herramientaIndividual)
                    
                    consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                    
                    for dato in consultaHerramienta:
                        codigo = dato.codigo_herramienta
                        nombre = dato.nombre_herramienta
                        descripcion = dato.descripcion_herramienta
                    codigos.append(codigo)
                    nombres.append(nombre)
                    descripciones.append(descripcion)
                        
                
                # Cantidades
                cantidades = solicitud.cantidades_solicitadas
                arregloIndividualCantidades = cantidades.split(",")
                
            arregloHerramientas = zip(codigos,nombres,descripciones, arregloIndividualCantidades)
        
        
            
        
        if prestamosEntregados:
            
            for entrega in prestamosEntregados:
                
                #Herramientas
                herramientasEntregadas = entrega.id_herramientaInstrumento
                arregloIndividualHerramientasEntregadas = herramientasEntregadas.split(",") #[1,2]
                
                
                for herramientaIndividualEntregada in arregloIndividualHerramientasEntregadas:
                    
                    idHerramientaEntregada = int(herramientaIndividualEntregada)
                    
                    consultaHerramientaEntregada = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaEntregada)
                    
                    for datoE in consultaHerramientaEntregada:
                        codigoE = datoE.codigo_herramienta
                        nombreE = datoE.nombre_herramienta
                        descripcionE = datoE.descripcion_herramienta
                    codigosHerramientasEntregadas.append(codigoE)
                    nombresHerramientasEntregadas.append(nombreE)
                    descripcionesHerramientasEntregadas.append(descripcionE)
                        
                
                # Cantidades
                cantidadesEntregadas = entrega.cantidades_solicitadas
                arregloIndividualCantidadesEntregadas = cantidadesEntregadas.split(",")
                
            arregloHerramientasEntregadas = zip(codigosHerramientasEntregadas,nombresHerramientasEntregadas,descripcionesHerramientasEntregadas, arregloIndividualCantidadesEntregadas)
        
        
        
        
        
        if prestamosDevueltos:
            for prestamoDevuelto in prestamosDevueltos:
                
                idPrestamoDevuelto = prestamoDevuelto.id_prestamo
                
                consultaPrestamoConDaño = HerramientasAlmacenInactivas.objects.filter(id_prestamo_id__id_prestamo = idPrestamoDevuelto)
                conDaños = ""
                #Si ese prestamo se entregó con algun daño..
                
                if consultaPrestamoConDaño:
                    conDaños = "SI"
                    for daño in consultaPrestamoConDaño:
                        
                        idHerramientaDañada = daño.id_herramienta_id
                        motivo = daño.motivo_baja
                        
                        
                        idsHerramientasDañadas.append(idHerramientaDañada)
                        motivosDañados.append(motivo)
                        
                        consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaDañada)
                        for datoH in consultaHerramienta:
                            nombreHerramientaDañada = datoH.nombre_herramienta
                            
                        nombresHerramientasDañadas.append(nombreHerramientaDañada)
                    
                else: 
                    conDaños = "NO"
                    idsHerramientasDañadas.append("jijija")
                
                
                
                conDaño.append(conDaños)
                    
                
                #Herramientas
                herramientasDevueltas = prestamoDevuelto.id_herramientaInstrumento #Lista de herramientas 1,2
                arregloIndividualHerramientas = herramientasDevueltas.split(",") #[1,2]
                
                for herramientaIndividual in arregloIndividualHerramientas:
                    
                    idHerramienta = int(herramientaIndividual)
                    
                    consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                    
                    for dato in consultaHerramienta:
                        codigo = dato.codigo_herramienta
                        nombre = dato.nombre_herramienta
                        descripcion = dato.descripcion_herramienta
                    codigosDevueltos.append(codigo)
                    nombresDevueltos.append(nombre)
                    descripcionesDevueltos.append(descripcion)
                        
                
                # Cantidades
                cantidades = prestamoDevuelto.cantidades_solicitadas
                arregloIndividualCantidades = cantidades.split(",")
                
                
                
                arregloHerramientasDevueltas = zip(codigosDevueltos,nombresDevueltos,descripcionesDevueltos, arregloIndividualCantidades)
            
            listaPrestamosDevueltos = zip(prestamosDevueltos, conDaño)
            
            herramientasDañadas = zip(idsHerramientasDañadas, nombresHerramientasDañadas, motivosDañados)
            
            

        if 'solicitudGuardada' in request.session:
            solicitudGuardada = request.session['solicitudGuardada']
            del request.session['solicitudGuardada']
            return render(request, "empleadosCustom/almacen/empleados/verMisPrestamos.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnVerMisPrestamos":estaEnVerMisPrestamos,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                      "solicitudesPendientes":solicitudesPendientes, "arregloHerramientas":arregloHerramientas,
                                                                                      "prestamosEntregados":prestamosEntregados, "arregloHerramientasEntregadas":arregloHerramientasEntregadas,
                                                                                      "listaPrestamosDevueltos":listaPrestamosDevueltos, "herramientasDañadas":herramientasDañadas, "arregloHerramientasDevueltas":arregloHerramientasDevueltas, "solicitudGuardada":solicitudGuardada})
        
        return render(request, "empleadosCustom/almacen/empleados/verMisPrestamos.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnVerMisPrestamos":estaEnVerMisPrestamos,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                      "solicitudesPendientes":solicitudesPendientes, "arregloHerramientas":arregloHerramientas,
                                                                                      "prestamosEntregados":prestamosEntregados, "arregloHerramientasEntregadas":arregloHerramientasEntregadas,
                                                                                      "listaPrestamosDevueltos":listaPrestamosDevueltos, "herramientasDañadas":herramientasDañadas, "arregloHerramientasDevueltas":arregloHerramientasDevueltas})
        
        
            
            
        
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
                stockActual = dato.stock
                
            intCantidadExistenciaActual = int(cantidadExistenteActual)
            
            sumaCantidad = intCantidadExistenciaActual + intCantidadHerramientaActualizar
            
            if sumaCantidad > stockActual:
                stockActual = sumaCantidad
            
            #Actualizar cantidad
            actualizacion = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaActualizar).update(cantidad_existencia = sumaCantidad, stock = stockActual)
            
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
            
            bajita = ""
            if motivoBaja == "E":
                bajita = "Extravío"
            elif motivoBaja == "D":
                bajita = "Dañado"
            
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaBaja)
            
            for dato in consultaHerramienta:
                cantidadExistenteActual = dato.cantidad_existencia
                nombreHerramienta = dato.nombre_herramienta
                codigoInternoSistema = dato.codigo_herramienta
                tipo = dato.tipo_herramienta
                marca = dato.marca
                descripcion = dato.descripcion_herramienta
                sku = dato.sku
                imagenHerramienta = dato.imagen_herramienta
                
            intCantidadExistenciaActual = int(cantidadExistenteActual)
            
            
            restaCantidad = intCantidadExistenciaActual - 1
            fechaBaja = datetime.now()
            #Actualizar cantidad
            actualizacion = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaBaja).update(cantidad_existencia = restaCantidad)
            
            #Registro de baja 
            if bajita == "Extravío":
                registroDeBaja = HerramientasAlmacenInactivas(id_herramienta = HerramientasAlmacen.objects.get(id_herramienta = idHerramientaBaja), motivo_baja = motivoBaja, explicacion_baja = explicacion, 
                                                          cantidad_baja = "1", fecha_baja = fechaBaja, enInventario = "No")
            else:
                registroDeBaja = HerramientasAlmacenInactivas(id_herramienta = HerramientasAlmacen.objects.get(id_herramienta = idHerramientaBaja), motivo_baja = motivoBaja, explicacion_baja = explicacion, 
                                                          cantidad_baja = "1", fecha_baja = fechaBaja, enInventario = "Si")
            registroDeBaja.save()
            if actualizacion and registroDeBaja:
                request.session['herramientaActualizada'] = "La herramienta " + nombreHerramienta + " ha sido dada de baja satisfactoriamente! Se ha mandado un correo con la solicitud de requisición de compra!"
                
                #MANDAR CORREO DE SOLICITUD DE REQUISICIÓN DE COMPRA
                
                    
                asunto = "CS | Solicitud de requisición de compra de herramienta"
                plantilla = "empleadosCustom/almacen/correos/correoBajaHerramienta.html"
                html_mensaje = render_to_string(plantilla, {"idHerramientaDañada":idHerramientaBaja,
                                                            "codigoHerramientaDañada":codigoInternoSistema,
                                                            "skuHerramientaDañada":sku,
                                                            "tipoHerramientaDañada":tipo,
                                                            "nombreHerramientaDañada":nombreHerramienta,
                                                            "marcaHerramientaDañada":marca,
                                                            "descripcionHerramientaDañada":descripcion,
                                                            "restaCantidad":restaCantidad,
                                                            "motivoDañoHerramientaDañada":bajita,
                                                            "explicacionDañoHerramientaDañada":explicacion,
                                                            "imagenHerramientaDañada":imagenHerramienta
                                                            })
                email_remitente = settings.EMAIL_HOST_USER
                email_destino = ['sistemas@customco.com.mx']
                mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                mensaje.content_subtype = 'html'
                mensaje.send()
            
                
                
                return redirect('/verHerramientasALM/')
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def bajaHerramientaAlmacenPrestamo(request):
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        if request.method == "POST":
            idPrestamoConDaño = request.POST['idPrestamo']
            idHerramientaBaja = request.POST['idHerramientaBaja']
            intIdHerramientaBaja = int(idHerramientaBaja)
            motivoBaja = request.POST['motivoBaja']
            explicacion = request.POST['explicacion']
            
            fechaBaja = datetime.now()
            
            #Sacar nombre de herramienta
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaBaja)
            for datoH in consultaHerramienta:
                nombreHerramienta = datoH.nombre_herramienta
            
            #Restar cantidad del prestamo, no de la existencia actual en almacén, ya que aun no se devuelve
            consultaPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoConDaño)
            
            for dato in consultaPrestamo:
                idsHerramientas = dato.id_herramientaInstrumento
                cantidadesHerramientas = dato.cantidades_solicitadas
                
            #Arreglos ya separados
            arregloCantidades = cantidadesHerramientas.split(",")
            arregloIdsHerramientas = idsHerramientas.split(",")
            listaHerramientasCantidades = zip(arregloIdsHerramientas, arregloCantidades)
            
            posicionArreglo = 0
            for herramienta,cantidad in listaHerramientasCantidades:
                posicionArreglo = posicionArreglo + 1
                if herramienta == idHerramientaBaja:  #No entra a esta condicion ???
                    nuevaCantidadPrestada = int(cantidad) - 1
                    arregloCantidades[posicionArreglo-1] = nuevaCantidadPrestada
                    #Ya esta actualizado en el arreglo.. falta actualizar en la BD
                    
            stringCantidadesActualizar = ""
            contadorCantidades = 0
            for cantidad in arregloCantidades:
                contadorCantidades = contadorCantidades + 1
                if contadorCantidades == 1:
                    stringCantidadesActualizar = str(cantidad)
                else:
                    stringCantidadesActualizar += ","+str(cantidad)
                    
            #String de cantidades realizado
            
            #Actualizar string de cantidades
            actualizacionPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoConDaño).update(cantidades_solicitadas = stringCantidadesActualizar)
            
            
            #Registro de baja 
            registroDeBaja = HerramientasAlmacenInactivas(id_herramienta = HerramientasAlmacen.objects.get(id_herramienta = idHerramientaBaja), motivo_baja = motivoBaja, explicacion_baja = explicacion, 
                                                          cantidad_baja = "1", fecha_baja = fechaBaja, id_prestamo = PrestamosAlmacen.objects.get(id_prestamo = idPrestamoConDaño))
            registroDeBaja.save()
            
            if actualizacionPrestamo and registroDeBaja:
                
                #MANDAR CORREO PARA REQUISICIOOON DE ESE EQUIPO QUE SE DIO DE BAJAAAAAA..
                
                
                request.session['idPrestamoActualizado'] = idPrestamoConDaño
                request.session['herramientaActualizada'] = "La herramienta " + nombreHerramienta + " ha sido dada de baja satisfactoriamente!"
                
                return redirect('/firmarDevolucion/')
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    

