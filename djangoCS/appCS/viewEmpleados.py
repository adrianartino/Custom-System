
#Librerías
from email.mime import text
import mimetypes
import os
import base64
from io  import BytesIO
from io import StringIO

#Renderizado
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

#Importación de modelos
from appCS.models import Areas, Empleados, Equipos, Carta, Impresoras, Cartuchos, CalendarioMantenimiento, Programas, ProgramasArea, EquipoPrograma, Bitacora, Renovacion_Equipos, Renovacion_Impresoras, Preguntas, Encuestas, Respuestas, EncuestaEmpleadoResuelta

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

#libreria iconos fontawesome



def fotoAdmin(request):
    idadministrador=request.session["idSesion"]
    datosEmpleado = Empleados.objects.filter(id_empleado=idadministrador)
        
    for dato in datosEmpleado:
        foto = dato.imagen_empleado
        
    return foto

def accesoEmpleado(request):

    #Si ya existe una sesión
    if "idSesion" in request.session:
        if request.session['correoSesion'] == "adminSistemas0817":
                    
            return redirect('/inicio/') #redirecciona a url de inicio
        else:
            return redirect('/principal/') #redirecciona a la pagina normal del empleado

    #Si no hay una sesión iniciada
    else:

        #si se apretó el botón.
        if request.method == "POST":
            
            correousuario = request.POST['usernameEmpleado']
            

            datosUsuario = Empleados.objects.filter(correo=correousuario)

            #Si encontro a un usuario con ese correo...
            if datosUsuario:

                for dato in datosUsuario:
                    id = dato.id_empleado
                    nombres = dato.nombre
                    apellidos = dato.apellidos
                    correo = dato.correo
                    contraReal = dato.contraseña
                    
                #mandar correo...
                asunto = "CS | Solicitud de acceso de " + nombres + " " + apellidos
                plantilla = "empleadosCustom/solicitudAcceso/correo.html"
                html_mensaje = render_to_string(plantilla, {"nombre": nombres, "apellidos": apellidos, "correo": correo, "contraseña": contraReal})
                email_remitente = settings.EMAIL_HOST_USER
                email_destino = [correo]
                mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                mensaje.content_subtype = 'html'
                mensaje.send()
                
                textoCorreo = "Se ha enviado un correo con tus datos de acceso."
                request.session['textoCorreo'] = textoCorreo #variable global.. 
                return redirect('/login/')
                    

            #Si no se encuentra a nadie con ese correo...
            else:
                hayError = True
                error = "No se ha encontrado al usuario"
                return render(request, "Login/accesoEmpleado.html", {"hayError":hayError, "textoError":error})

        #se carga la pagina por primera vez.
        return render(request, "Login/accesoEmpleado.html")


    
            

def principal(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        estaEnInicio = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        
        
            return render(request, "empleadosCustom/inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, 
            "rh": rh})
    
        return render(request, "empleadosCustom/inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def encuestas(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        enAño = True
        estaEnEncuesta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        if correo  == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh= False


        preguntas = Preguntas.objects.filter(id_encuesta = 1)

        preguntasMultiples = []
        preguntasAbiertas = []
        contadorPreguntas = 0
        for pregunta in preguntas:
            id_pregunta = pregunta.id_pregunta
            texto_pregunta = pregunta.pregunta
            tipo = pregunta.tipo
            clasificacionPregunta = pregunta.clasificacion

            if tipo== "M":
                preguntasMultiples.append([id_pregunta, texto_pregunta, clasificacionPregunta])
                contadorPreguntas = contadorPreguntas +1 
            else:
                preguntasAbiertas.append([id_pregunta, texto_pregunta])
                contadorPreguntas = contadorPreguntas +1 



        #Condicion para saber si el empleado ya contesto algo..

        empleadoTieneRespuestas = Respuestas.objects.filter(id_empleado = id_admin) #Consulta a la tabla de respuestas para ver si alguna tiene el id del empleado

        #Si el empleado ya tiene aunque sea una pregunta resuelta..
        if empleadoTieneRespuestas:
            aunqueseaunapregunta = True
            contadorRespuestas = 0
            for respuesta in empleadoTieneRespuestas:
                contadorRespuestas = contadorRespuestas + 1
            return render(request, "empleadosCustom/encuestas/año2022/encuestaEnero.html", {"enAño":enAño, "estaEnEncuesta": estaEnEncuesta, "preguntasMultiples":preguntasMultiples,"preguntasAbiertas":preguntasAbiertas, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
            "aunqueseaunapregunta":aunqueseaunapregunta, "contadorPreguntas": contadorPreguntas, "contadorRespuestas":contadorRespuestas, "rh": rh})

        #Si el empleado no tiene ninguna pregunta resuelta
        else:
            #Mostrar solo la introducción.
            aunqueseaunapregunta = False
            introduccion = True
        
        
            return render(request, "empleadosCustom/encuestas/año2022/encuestaEnero.html", {"enAño":enAño, "estaEnEncuesta": estaEnEncuesta, "preguntasMultiples":preguntasMultiples,"preguntasAbiertas":preguntasAbiertas, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
            "aunqueseaunapregunta":aunqueseaunapregunta, "contadorPreguntas": contadorPreguntas, "introduccion":introduccion, "rh": rh})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def resultadosEncuestas(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        enAño = True
        estaEnReseultados = True
        rh= True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

        empleadosActivos = Empleados.objects.filter(activo = "A", correo__icontains="@customco.com.mx")
        contadorEmpleadosActivos = 0

        for activos in empleadosActivos:
            contadorEmpleadosActivos = contadorEmpleadosActivos + 1

        empleadosContestados = EncuestaEmpleadoResuelta.objects.filter(id_encuesta = 1)
        contadorEmpleadoscontestados = 0

        for contestado in empleadosContestados:
            contadorEmpleadoscontestados = contadorEmpleadoscontestados + 1

        empleadosFaltantes = contadorEmpleadosActivos - contadorEmpleadoscontestados

        br = " <br> "
        empleadosIrresponsables = ""

        idsActivos = []
        idsContestados = []

        for empleadosTotales in empleadosActivos:

            idEmpleado = empleadosTotales.id_empleado
            idsActivos.append(str(idEmpleado))



        for empleadosResueltos in empleadosContestados:

            id_empleado = empleadosResueltos.id_empleado_id
            idsContestados.append(str(id_empleado))

        for activos in idsActivos:
            if activos in idsContestados:
                yaContesto = True
            else:
                datosEmpleadoSinContestar = Empleados.objects.filter(id_empleado = activos)

                for datos in datosEmpleadoSinContestar:
                    nombres = datos.nombre
                    apellidos = datos.apellidos
                
                nombreCompleto= nombres + " " + apellidos

                empleadosIrresponsables += nombreCompleto + br
                


        porcentaje = (contadorEmpleadoscontestados * 100) / contadorEmpleadosActivos

        pregMultiples = []
        pregAbiertas =[]
        porcentajesPreguntasMultiples = []
        contadorSiNo = []

        preguntas = Preguntas.objects.filter(id_encuesta = 1)

        for pregunta in preguntas:
            id_pregunta = pregunta.id_pregunta
            texto = pregunta.pregunta
            tipo = pregunta.tipo
            clasificacion = pregunta.clasificacion

            if tipo == "M":
                pregMultiples.append([id_pregunta, texto, clasificacion])

            elif tipo == "A":
                pregAbiertas.append([id_pregunta, texto])
        

        for multiple in pregMultiples:
            idPregunta = multiple[0]

            respuestas = Respuestas.objects.filter(id_pregunta =idPregunta) #en este caso devuelve dos respuestas de dos diferentes empleados
            contadorSI = 0
            contadorNO = 0
            for respuesta in respuestas:
                res = respuesta.respuesta #SI o NO
                
                if res == "SI":
                    contadorSI = contadorSI + 1
                elif res == "NO":
                    contadorNO = contadorNO +1
                
            contadorSiNo.append([contadorSI, contadorNO])
            
            porcentajePregunta = (contadorSI * 100)/ contadorEmpleadoscontestados
            
            criterio = ""
            if porcentajePregunta >= 90 and porcentajePregunta <= 100:
                criterio = "EXCELENTE"
            elif porcentajePregunta >= 80 and porcentajePregunta <= 89:
                criterio = "MUY BUENO"
            elif porcentajePregunta >= 70 and porcentajePregunta <= 79:
                criterio = "BUENO"
            elif porcentajePregunta >= 60 and porcentajePregunta <= 69:
                criterio = "REGULAR"
            elif porcentajePregunta >= 0 and porcentajePregunta <= 59:
                criterio = "DEFICIENTE"

            porcentajesPreguntasMultiples.append([porcentajePregunta,criterio])

        listaMultiples = zip(pregMultiples,porcentajesPreguntasMultiples, contadorSiNo)
        listaMultiples2 = zip(pregMultiples,porcentajesPreguntasMultiples, contadorSiNo)

        suma = 0

        for porcentajesMultiples in porcentajesPreguntasMultiples:
            porcentajeSuma = porcentajesMultiples[0]
            suma = suma + porcentajeSuma

        contadorPreguntasMultiples = 0

        for m in pregMultiples:

            contadorPreguntasMultiples = contadorPreguntasMultiples + 1

        promedio = suma / contadorPreguntasMultiples

        criterioPromedio = ""
        if promedio >= 90 and promedio <= 100:
            criterioPromedio = "EXCELENTE"
        elif promedio >= 80 and promedio <= 89:
            criterioPromedio = "MUY BUENO"
        elif promedio >= 70 and promedio <= 79:
            criterioPromedio = "BUENO"
        elif promedio >= 60 and promedio <= 69:
            criterioPromedio = "REGULAR"
        elif promedio >= 0 and promedio <= 59:
            criterioPromedio = "DEFICIENTE"

        numeros =[1,2]


        return render(request, "empleadosCustom/encuestas/año2022/resultadosEnero.html", {"enAño":enAño, "estaEnReseultados": estaEnReseultados, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
              "rh":rh, "contadorEmpleadosActivos":contadorEmpleadosActivos, "contadorEmpleadoscontestados":contadorEmpleadoscontestados, "porcentaje":porcentaje, "pregMultiples":pregMultiples, "pregAbiertas":pregAbiertas,
              "porcentajesPreguntasMultiples":porcentajesPreguntasMultiples,"listaMultiples":listaMultiples, "promedio":promedio, "criterioPromedio": criterioPromedio, "numeros":numeros, "listaMultiples2":listaMultiples2, "empleadosFaltantes":empleadosFaltantes
              , "empleadosIrresponsables":empleadosIrresponsables, "idsActivos":idsActivos, "idsContestados":idsContestados })
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def guardarRespuesta(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        enAño = True
        estaEnEncuesta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

        if request.method == "POST":
            
            empleadoID = request.POST['empleadoEncuesta']
            id_pregunta = request.POST['preguntaID']
            respuesta = ""
            nameInput = "respuesta"

            if request.POST.get(nameInput, False): #Checkeado
                respuesta = "SI"
            elif request.POST.get(nameInput, True): #No checkeado
                respuesta = "NO"

         

            registroRespuesta = Respuestas(id_pregunta = Preguntas.objects.get(id_pregunta = id_pregunta), id_empleado = Empleados.objects.get(id_empleado = empleadoID), respuesta = respuesta)
            registroRespuesta.save()

        
        return redirect('/encuestas/') #redirecciona a url de inicio
   
        

        
        

    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def guardarRespuestaTextbox(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        enAño = True
        estaEnEncuesta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

        if request.method == "POST":
            
            empleadoID = request.POST['empleadoEncuesta']
            id_pregunta = request.POST['preguntaID']
            respuesta = request.POST['respuestaText']

            registroRespuesta = Respuestas(id_pregunta = Preguntas.objects.get(id_pregunta = id_pregunta), id_empleado = Empleados.objects.get(id_empleado = empleadoID), respuesta = respuesta)
            registroRespuesta.save()

            numeroPreguntas = Preguntas.objects.filter(id_encuesta = 1)
            contadorPreguntas = 0
            for pregunta in numeroPreguntas:
                contadorPreguntas = contadorPreguntas +1

            respuestasEmpleado = Respuestas.objects.filter(id_empleado = id_admin) #4 registros

            contadorRespuestas = 0
            for respuesta in respuestasEmpleado:
                contadorRespuestas = contadorRespuestas +1

            if (contadorRespuestas == contadorPreguntas):
                registroEmpleadoCompletoEncuesta = EncuestaEmpleadoResuelta(id_empleado = Empleados.objects.get(id_empleado = id_admin), id_encuesta = Encuestas.objects.get(id_encuesta = 1))
                registroEmpleadoCompletoEncuesta.save()


        
        return redirect('/encuestas/') #redirecciona a url de inicio
   
        

        
        

    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def verRespuestasAbiertas(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        enAño = True
        estaEnReseultados = True
        rh= True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

        if request.method == "POST":
            
            pregunta = request.POST['idPregunta']

            datosPregunta = Preguntas.objects.filter(id_pregunta=pregunta)

            for datos in datosPregunta:
                idPregunta = datos.id_pregunta
                texto = datos.pregunta

            datosRespuestas = Respuestas.objects.filter(id_pregunta = idPregunta)





        


        return render(request, "empleadosCustom/encuestas/año2022/verRespuestasAbiertas.html", {"enAño":enAño, "estaEnReseultados": estaEnReseultados, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
              "rh":rh, "idPregunta": idPregunta, "texto":texto, "datosRespuestas": datosRespuestas})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def equipo(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
      
        estaEnVerEquipo = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        if correo  == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh= False

        #Codigo de info equipos.
        datosEquipo = Equipos.objects.filter(id_empleado =id_admin)
        
        #Si hay un equipo asignado a es empleado...
        if datosEquipo: 
            tieneEquipo = True  

            #Sacar datos del empleado
            datosPropietario= Empleados.objects.filter(id_empleado=id_admin)
            for datos in datosPropietario:
                nombre= datos.nombre
                apellidos=datos.apellidos
                nombreEmpleado= nombre + " " + apellidos
                departamento=datos.id_area_id
                datosDepa= Areas.objects.filter(id_area=departamento)
                for datos in datosDepa:
                    nombreArea= datos.nombre
                    colorArea=datos.color



            #Sacar id de equipo para consultar renovación
            for dato in datosEquipo:
                id_equipo = dato.id_equipo

            #Sacar datos de renovación
            datosRenovacion= Renovacion_Equipos.objects.filter(id_equipo=id_equipo)
            for datos in datosRenovacion:
                compra= datos.fecha_compra
                renovar=  datos.fecha_renov
                        
                    
            #Verificar si tiene mantenimientos.      
            mantenimientos= CalendarioMantenimiento.objects.filter(id_equipo_id__id_equipo=id_equipo)
            if mantenimientos:
                return render(request, "empleadosCustom/miEquipo/verInfoEquipo.html", { "estaEnVerEquipo": estaEnVerEquipo, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                "tieneEquipo":tieneEquipo, "datosPropietario":datosPropietario, "nombreEmpleado":nombreEmpleado, "nombreArea":nombreArea, "colorArea":colorArea, "compra":compra, "renovar":renovar, "mantenimientos":mantenimientos, "datosEquipo": datosEquipo,  "rh":rh})
            else:
                return render(request, "empleadosCustom/miEquipo/verInfoEquipo.html", { "estaEnVerEquipo": estaEnVerEquipo, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                "tieneEquipo":tieneEquipo, "datosPropietario":datosPropietario, "nombreEmpleado":nombreEmpleado,"nombreArea":nombreArea, "colorArea":colorArea, "compra":compra, "renovar":renovar, "datosEquipo": datosEquipo,  "rh":rh})
                    
        else:
            noTieneEquipo = True
            return render(request, "empleadosCustom/miEquipo/verInfoEquipo.html", { "estaEnVerEquipo": estaEnVerEquipo, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
            "noTieneEquipo":noTieneEquipo,  "rh":rh})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def carta(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
      
        estaEnVerCarta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        if correo  == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh= False
        
        datosRegistro = Carta.objects.filter(id_empleado = id_admin)
        
        empleados=[]
        equipos=[]
        
        for registros in datosRegistro:
            empleado= registros.id_empleado_id
            equipo = registros.id_equipo_id
            
            datosEmpleado = Empleados.objects.filter(id_empleado=empleado)
            for datos in datosEmpleado:
                nombres= datos.nombre
                apellido= datos.apellidos
                
            datosEquipos =Equipos.objects.filter(id_equipo=equipo)
            for datos in datosEquipos:
                marca=datos.marca
                modelo=datos.modelo
                
            empleados.append([nombres,apellido])
            equipos.append([marca, modelo])
        
        lista1=zip(datosRegistro,empleados,equipos)
        
        
        return render(request, "empleadosCustom/miEquipo/verCartaResponsiva.html", { "estaEnVerCarta": estaEnVerCarta, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "lista1":lista1,  "rh":rh})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def directorio(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
      
        estaEnVerCorreos = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        if correo  == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh= False

        empleadosActivos = Empleados.objects.filter(activo__icontains= "A", correo__icontains = "customco.com.mx")
        
        #empleados Actvos
        areasEnActivos = []
        datosAreasEnActivos = []
        
        for empleado in empleadosActivos:
            areasEnActivos.append(empleado.id_area_id)
            
        for id in areasEnActivos:
            datosArea = Areas.objects.filter(id_area = id) 
            
            if datosArea:
                for dato in datosArea:
                    nombreArea = dato.nombre
                    colorArea = dato.color
            
            datosAreasEnActivos.append([nombreArea, colorArea])
            
        lista = zip(empleadosActivos, datosAreasEnActivos)
        
        
        return render(request, "empleadosCustom/directorioCorreos/verDirectorio.html", { "estaEnVerCorreos": estaEnVerCorreos, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "lista":lista,  "rh":rh})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    

def documentosAplicablesATodos(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        estaEnVerDocumentos = True
        estaEnEncuesta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        if correo  == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh= False
        
        
        return render(request, "empleadosCustom/documentos/aplicablesatodos.html", {"estaEnVerDocumentos":estaEnVerDocumentos, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,  "rh":rh})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def aplicable1(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
     
        
        if request.method == "POST":
            
            formato = request.POST['fto1']


            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            nombreArchivo = formato+".xlsx"
            ubicacionArchivo = BASE_DIR + '/media/documentosAreas/'+ nombreArchivo

            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
            return response


            
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def aplicable2(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
     
        
        if request.method == "POST":
            
            formato = request.POST['fto1']


            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            nombreArchivo = formato+".docx"
            ubicacionArchivo = BASE_DIR + '/media/documentosAreas/'+ nombreArchivo

            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
            return response


           
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def aplicable3(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
     
        
        if request.method == "POST":
            
            formato = request.POST['fto1']


            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            nombreArchivo = formato+".pdf"
            ubicacionArchivo = BASE_DIR + '/media/documentosAreas/'+ nombreArchivo

            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
            return response


           
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def pruebaPDF(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:

       #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Resultados Encuesta Clima Laboral - Enero 2022.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        base_dir = str(settings.BASE_DIR) #C:\Users\AuxSistemas\Desktop\CS Escritorio\Custom-System\djangoCS
        #nombre de empresa
        logo = base_dir+'/static/images/logoCustom.PNG'   
        c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
        c.setFont('Helvetica-Bold', 14)
        c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,720, 'RFC: CAC070116IS9')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,705, 'Tel: 8717147716')
        #fecha
        hoy=datetime.now()
        fecha = str(hoy.date())
        color_guinda="#B03A2E"
        color_azul = "#cf1515"
        c.setFillColor(color_guinda)
        
            
        c.setFont('Helvetica-Bold', 12)
        c.drawString(425,750, "CLIMA LABORAL 2022")
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(405,730, "Fecha de impresión: " +fecha)
        #linea guinda
            
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,695,560,695)
        #nombre departamento
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica', 12)
        c.drawString(405,710, 'Departamento de Sistemas')
        #titulo
        c.setFont('Helvetica-Bold', 22)
            
        c.drawString(55,660, 'Resultados Encuesta Clima Laboral Enero 2022')


        #tabla1
        c.setFont('Helvetica-Bold', 18)
        c.drawString(215,620, 'Criterios de Evaluación')


        #header de tabla
        styles = getSampleStyleSheet()
        styleBH =styles["Normal"]
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10
        
        
        rango = Paragraph('''Rango Porcentaje''', styleBH)
        criterio = Paragraph('''Criterio''', styleBH)
       
      
        filasTabla=[]
        filasTabla.append([rango, criterio])
        #Tabla
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7
        
        high = 590
        porcentajes = ["100% - 90%", "89% - 80%", "79% - 70%","69% - 60%", "59% - 0%" ]
        criterios = ["Excelente", "Muy bueno", "Bueno", "Regular", "Deficiente"]
        
        contador = 0
        for x in porcentajes:
            if contador == 0:
                fila = [porcentajes[contador], criterios[contador]]
                contador= 1

            elif contador != 0:
                fila = [porcentajes[contador], criterios[contador]]
                contador= contador+1
            filasTabla.append(fila)
            high= high - 18 
            
        #escribir tabla
        width, height = letter
        tabla = Table(filasTabla, colWidths=[4 * cm, 4 * cm])
        
        tabla.setStyle(TableStyle([
           
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), '#e9c7ae'),
            
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (1,1), (-1,-5), '#4CAF50'),
            ('BACKGROUND', (1,2), (-1,-4), '#2196F3'),
            ('BACKGROUND', (1,3), (-1,-3), '#FFC107'),
            ('BACKGROUND', (1,4), (-1,-2), '#FF5722'),
            ('BACKGROUND', (1,5), (-1,-1), '#F44336'),
        ]))

        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, 200, high)

        #tabla2

        c.setFont('Helvetica-Bold', 18)
        c.drawString(215,475, 'Encuestas contestadas')

        empleadosActivos = Empleados.objects.filter(activo = "A", correo__icontains="@customco.com.mx")
        contadorEmpleadosActivos = 0

        for activos in empleadosActivos:
            contadorEmpleadosActivos = contadorEmpleadosActivos + 1

        contadorEmpleadosActivos = str(contadorEmpleadosActivos)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(80,440, 'Número de empleados')
        c.drawString(85,415, 'activos en la empresa:')
        c.setFont('Helvetica-Bold', 36)
        c.setFillColor(color_azul)
        c.drawString(140,375, contadorEmpleadosActivos)


        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 16)
        c.drawString(360,440, 'Número de encuestas')
        c.drawString(365,415, 'resueltas esperadas:')
        c.setFont('Helvetica-Bold', 36)
        c.setFillColor(color_azul)
        c.drawString(425,375, contadorEmpleadosActivos)
        c.setFillColor(color_negro)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(80,340, 'Relación contestadas/')
        c.drawString(85,320, 'no contestadas:')

        empleadosContestados = EncuestaEmpleadoResuelta.objects.filter(id_encuesta = 1)
        contadorEmpleadoscontestados = 0

        for contestado in empleadosContestados:
            contadorEmpleadoscontestados = contadorEmpleadoscontestados + 1
        
        

        empleadosFaltantes = int(contadorEmpleadosActivos) - int(contadorEmpleadoscontestados)

        empleadosFaltantes = int(empleadosFaltantes)

      

       

        

        #grafico de pastel
        b = Drawing()
        pie = Pie()
        pie.x = 0
        pie.y = 0
        pie.height = 160
        pie.width = 160
        pie.data = [contadorEmpleadoscontestados, empleadosFaltantes ]
        pie.labels = ['Contestadas', 'No contestadas']
        pie.slices.strokeWidth = 0.5
        pie.slices[1].popout = 20
        pie.slices[0].fillColor= colors.HexColor("#e91e63")
        pie.slices[1].fillColor=colors.HexColor("#009688")
        b.add(pie)
        x,y = 100,130 
        renderPDF.draw(b, c, x, y, showBoundary=False)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(360,340, 'Porcentaje total')
        c.drawString(365,320, 'resuelto:')

        porcentajeTotal = 100
        porcentaje = int(contadorEmpleadoscontestados * 100) / int(contadorEmpleadosActivos)

        porcentaje = str(porcentaje)

        porcentajeDigitos = ("{0:.4f}".format(float(porcentaje))) + "%"

        porcentajeBarra = ("{0:.0f}".format(float(porcentaje)))

        porcentajeBarraa = int(porcentajeBarra)

        c.setStrokeColorRGB(0.7, 0, 0.7) #color de contorno
        c.setFillColorRGB(255, 255, 255) #color de relleno
        c.rect(360, 275, 200, 25, fill=True)

        c.setStrokeColorRGB(0.7, 0, 0.7) #color de contorno

        if porcentajeBarraa >= 0 and porcentajeBarraa <= 33:
            c.setFillColorRGB(255, 0, 0) #color de relleno
            c.rect(360, 275, porcentajeBarra, 25, fill=True)
        elif porcentajeBarraa >= 34 and porcentajeBarraa <= 66:
            c.setFillColorRGB(255, 165, 0) #color de relleno
            c.rect(360, 275, porcentajeBarra, 25, fill=True)
        elif porcentajeBarraa >= 67 and porcentajeBarraa <= 100:
            c.setFillColorRGB(0, 128, 0) #color de relleno
            c.rect(360, 275, porcentajeBarra, 25, fill=True)

        c.setFont('Helvetica-Bold', 30)
        c.setFillColor(color_azul)
        c.drawString(360,230, porcentajeDigitos)
        c.setFont('Helvetica-Bold', 18)
        c.setFillColor(color_negro)
        c.drawString(360,200, "del 100% de empleados")
       



  

        
        
        f = Drawing()
        barra = VerticalBarChart()
        barra.x = 0
        barra.y = 0
        barra.height = 100
        barra.width = 50
        data = [(10,2)]
        barra.valueAxis.valueMin = 0
        barra.valueAxis.valueMax = 20 
        barra.data = data
        barra.categoryAxis.categoryNames = ['SI', 'NO']
        barra.bars[(0,0)].fillColor = colors.HexColor("#E91E63")
        barra.bars[(0,1)].fillColor = colors.red
        f.add(barra)
        x,y = 60, 300
        #renderPDF.draw(f, c, x, y, showBoundary=False)  


        #linea guinda
        color_guinda="#B03A2E"
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,60,560,60)
        
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(170,48, '2021 - Administrador de Custom System. - Versión: 1.0.0 ')
        
        
        c.showPage()
        
        
        
        #guardar pdf
        c.save()
        #obtener valores de bytesIO y esribirlos en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        respuesta.write(pdf)
        return respuesta


        
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def resultadosMultiples(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:

       #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Resultados Preguntas Multiples Encuesta Clima Laboral - Enero 2022.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        base_dir = str(settings.BASE_DIR) #C:\Users\AuxSistemas\Desktop\CS Escritorio\Custom-System\djangoCS
        #nombre de empresa
        logo = base_dir+'/static/images/logoCustom.PNG'   
        c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
        c.setFont('Helvetica-Bold', 14)
        c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,720, 'RFC: CAC070116IS9')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,705, 'Tel: 8717147716')
        #fecha
        hoy=datetime.now()
        fecha = str(hoy.date())
        color_guinda="#B03A2E"
        color_azul = "#cf1515"
        c.setFillColor(color_guinda)
        
            
        c.setFont('Helvetica-Bold', 12)
        c.drawString(425,750, "CLIMA LABORAL 2022")
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(405,730, "Fecha de impresión: " +fecha)
        #linea guinda
            
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,695,560,695)
        #nombre departamento
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica', 12)
        c.drawString(405,710, 'Departamento de Sistemas')
        #titulo
        c.setFont('Helvetica-Bold', 22)
            
        c.drawString(55,660, 'Resultados Encuesta Clima Laboral Enero 2022')


        #tabla1
        c.setFont('Helvetica-Bold', 18)
        c.drawString(215,620, 'Criterios de Evaluación')


        #header de tabla
        styles = getSampleStyleSheet()
        styleBH =styles["Normal"]
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10
        
        
        rango = Paragraph('''Rango Porcentaje''', styleBH)
        criterio = Paragraph('''Criterio''', styleBH)
       
      
        filasTabla=[]
        filasTabla.append([rango, criterio])
        #Tabla
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7
        
        high = 590
        porcentajes = ["100% - 90%", "89% - 80%", "79% - 70%","69% - 60%", "59% - 0%" ]
        criterios = ["Excelente", "Muy bueno", "Bueno", "Regular", "Deficiente"]
        
        contador = 0
        for x in porcentajes:
            if contador == 0:
                fila = [porcentajes[contador], criterios[contador]]
                contador= 1

            elif contador != 0:
                fila = [porcentajes[contador], criterios[contador]]
                contador= contador+1
            filasTabla.append(fila)
            high= high - 18 
            
        #escribir tabla
        width, height = letter
        tabla = Table(filasTabla, colWidths=[4 * cm, 4 * cm])
        
        tabla.setStyle(TableStyle([
           
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), '#e9c7ae'),
            
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (1,1), (-1,-5), '#4CAF50'),
            ('BACKGROUND', (1,2), (-1,-4), '#2196F3'),
            ('BACKGROUND', (1,3), (-1,-3), '#FFC107'),
            ('BACKGROUND', (1,4), (-1,-2), '#FF5722'),
            ('BACKGROUND', (1,5), (-1,-1), '#F44336'),
        ]))

        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, 200, high)

        #tabla2

        c.setFont('Helvetica-Bold', 18)
        c.drawString(215,475, 'Encuestas contestadas')

        empleadosActivos = Empleados.objects.filter(activo = "A", correo__icontains="@customco.com.mx")
        contadorEmpleadosActivos = 0

        for activos in empleadosActivos:
            contadorEmpleadosActivos = contadorEmpleadosActivos + 1

        contadorEmpleadosActivos = str(contadorEmpleadosActivos)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(80,440, 'Número de empleados')
        c.drawString(85,415, 'activos en la empresa:')
        c.setFont('Helvetica-Bold', 36)
        c.setFillColor(color_azul)
        c.drawString(140,375, contadorEmpleadosActivos)


        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 16)
        c.drawString(360,440, 'Número de encuestas')
        c.drawString(365,415, 'resueltas esperadas:')
        c.setFont('Helvetica-Bold', 36)
        c.setFillColor(color_azul)
        c.drawString(425,375, contadorEmpleadosActivos)
        c.setFillColor(color_negro)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(80,340, 'Relación contestadas/')
        c.drawString(85,320, 'no contestadas:')

        empleadosContestados = EncuestaEmpleadoResuelta.objects.filter(id_encuesta = 1)
        contadorEmpleadoscontestados = 0

        for contestado in empleadosContestados:
            contadorEmpleadoscontestados = contadorEmpleadoscontestados + 1
        
        

        empleadosFaltantes = int(contadorEmpleadosActivos) - int(contadorEmpleadoscontestados)

        empleadosFaltantes = int(empleadosFaltantes)

      

       

        

        #grafico de pastel
        b = Drawing()
        pie = Pie()
        pie.x = 0
        pie.y = 0
        pie.height = 160
        pie.width = 160
        pie.data = [contadorEmpleadoscontestados, empleadosFaltantes ]
        pie.labels = ['Contestadas', 'No contestadas']
        pie.slices.strokeWidth = 0.5
        pie.slices[1].popout = 20
        pie.slices[0].fillColor= colors.HexColor("#e91e63")
        pie.slices[1].fillColor=colors.HexColor("#009688")
        b.add(pie)
        x,y = 100,130 
        renderPDF.draw(b, c, x, y, showBoundary=False)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(360,340, 'Porcentaje total')
        c.drawString(365,320, 'resuelto:')

        porcentajeTotal = 100
        porcentaje = int(contadorEmpleadoscontestados * 100) / int(contadorEmpleadosActivos)

        porcentaje = str(porcentaje)

        porcentajeDigitos = ("{0:.4f}".format(float(porcentaje))) + "%"

        porcentajeBarra = ("{0:.0f}".format(float(porcentaje)))

        porcentajeBarraa = int(porcentajeBarra)

        c.setStrokeColorRGB(0.7, 0, 0.7) #color de contorno
        c.setFillColorRGB(255, 255, 255) #color de relleno
        c.rect(360, 275, 200, 25, fill=True)

        c.setStrokeColorRGB(0.7, 0, 0.7) #color de contorno

        if porcentajeBarraa >= 0 and porcentajeBarraa <= 33:
            c.setFillColorRGB(255, 0, 0) #color de relleno
            c.rect(360, 275, porcentajeBarra, 25, fill=True)
        elif porcentajeBarraa >= 34 and porcentajeBarraa <= 66:
            c.setFillColorRGB(255, 165, 0) #color de relleno
            c.rect(360, 275, porcentajeBarra, 25, fill=True)
        elif porcentajeBarraa >= 67 and porcentajeBarraa <= 100:
            c.setFillColorRGB(0, 128, 0) #color de relleno
            c.rect(360, 275, porcentajeBarra, 25, fill=True)

        c.setFont('Helvetica-Bold', 30)
        c.setFillColor(color_azul)
        c.drawString(360,230, porcentajeDigitos)
        c.setFont('Helvetica-Bold', 18)
        c.setFillColor(color_negro)
        c.drawString(360,200, "del 100% de empleados")
       



  

        
        
        f = Drawing()
        barra = VerticalBarChart()
        barra.x = 0
        barra.y = 0
        barra.height = 100
        barra.width = 50
        data = [(10,2)]
        barra.valueAxis.valueMin = 0
        barra.valueAxis.valueMax = 20 
        barra.data = data
        barra.categoryAxis.categoryNames = ['SI', 'NO']
        barra.bars[(0,0)].fillColor = colors.HexColor("#E91E63")
        barra.bars[(0,1)].fillColor = colors.red
        f.add(barra)
        x,y = 60, 300
        #renderPDF.draw(f, c, x, y, showBoundary=False)  


        #linea guinda
        color_guinda="#B03A2E"
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,60,560,60)
        
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(170,48, '2021 - Administrador de Custom System. - Versión: 1.0.0 ')
        
        
        c.showPage()
        
        
        
        #guardar pdf
        c.save()
        #obtener valores de bytesIO y esribirlos en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        respuesta.write(pdf)
        return respuesta


        
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio



def resultadosAbiertas(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:

       #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Resultados Preguntas Abiertas Encuesta Clima Laboral - Enero 2022.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        base_dir = str(settings.BASE_DIR) #C:\Users\AuxSistemas\Desktop\CS Escritorio\Custom-System\djangoCS
        #nombre de empresa
        logo = base_dir+'/static/images/logoCustom.PNG'   
        c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
        c.setFont('Helvetica-Bold', 14)
        c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,720, 'RFC: CAC070116IS9')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,705, 'Tel: 8717147716')
        #fecha
        hoy=datetime.now()
        fecha = str(hoy.date())
        color_guinda="#B03A2E"
        color_azul = "#cf1515"
        c.setFillColor(color_guinda)
        
            
        c.setFont('Helvetica-Bold', 12)
        c.drawString(425,750, "CLIMA LABORAL 2022")
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(405,730, "Fecha de impresión: " +fecha)
        #linea guinda
            
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,695,560,695)
        #nombre departamento
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica', 12)
        c.drawString(405,710, 'Departamento de Sistemas')
        #titulo
        c.setFont('Helvetica-Bold', 22)
            
        c.drawString(55,660, 'Resultados Encuesta Clima Laboral Enero 2022')


        #tabla1
        c.setFont('Helvetica-Bold', 18)
        c.drawString(215,620, 'Criterios de Evaluación')


        #header de tabla
        styles = getSampleStyleSheet()
        styleBH =styles["Normal"]
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10
        
        
        rango = Paragraph('''Rango Porcentaje''', styleBH)
        criterio = Paragraph('''Criterio''', styleBH)
       
      
        filasTabla=[]
        filasTabla.append([rango, criterio])
        #Tabla
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7
        
        high = 590
        porcentajes = ["100% - 90%", "89% - 80%", "79% - 70%","69% - 60%", "59% - 0%" ]
        criterios = ["Excelente", "Muy bueno", "Bueno", "Regular", "Deficiente"]
        
        contador = 0
        for x in porcentajes:
            if contador == 0:
                fila = [porcentajes[contador], criterios[contador]]
                contador= 1

            elif contador != 0:
                fila = [porcentajes[contador], criterios[contador]]
                contador= contador+1
            filasTabla.append(fila)
            high= high - 18 
            
        #escribir tabla
        width, height = letter
        tabla = Table(filasTabla, colWidths=[4 * cm, 4 * cm])
        
        tabla.setStyle(TableStyle([
           
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), '#e9c7ae'),
            
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (1,1), (-1,-5), '#4CAF50'),
            ('BACKGROUND', (1,2), (-1,-4), '#2196F3'),
            ('BACKGROUND', (1,3), (-1,-3), '#FFC107'),
            ('BACKGROUND', (1,4), (-1,-2), '#FF5722'),
            ('BACKGROUND', (1,5), (-1,-1), '#F44336'),
        ]))

        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, 200, high)

        #tabla2

        c.setFont('Helvetica-Bold', 18)
        c.drawString(215,475, 'Encuestas contestadas')

        empleadosActivos = Empleados.objects.filter(activo = "A", correo__icontains="@customco.com.mx")
        contadorEmpleadosActivos = 0

        for activos in empleadosActivos:
            contadorEmpleadosActivos = contadorEmpleadosActivos + 1

        contadorEmpleadosActivos = str(contadorEmpleadosActivos)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(80,440, 'Número de empleados')
        c.drawString(85,415, 'activos en la empresa:')
        c.setFont('Helvetica-Bold', 36)
        c.setFillColor(color_azul)
        c.drawString(140,375, contadorEmpleadosActivos)


        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 16)
        c.drawString(360,440, 'Número de encuestas')
        c.drawString(365,415, 'resueltas esperadas:')
        c.setFont('Helvetica-Bold', 36)
        c.setFillColor(color_azul)
        c.drawString(425,375, contadorEmpleadosActivos)
        c.setFillColor(color_negro)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(80,340, 'Relación contestadas/')
        c.drawString(85,320, 'no contestadas:')

        empleadosContestados = EncuestaEmpleadoResuelta.objects.filter(id_encuesta = 1)
        contadorEmpleadoscontestados = 0

        for contestado in empleadosContestados:
            contadorEmpleadoscontestados = contadorEmpleadoscontestados + 1
        
        

        empleadosFaltantes = int(contadorEmpleadosActivos) - int(contadorEmpleadoscontestados)

        empleadosFaltantes = int(empleadosFaltantes)

      

       

        

        #grafico de pastel
        b = Drawing()
        pie = Pie()
        pie.x = 0
        pie.y = 0
        pie.height = 160
        pie.width = 160
        pie.data = [contadorEmpleadoscontestados, empleadosFaltantes ]
        pie.labels = ['Contestadas', 'No contestadas']
        pie.slices.strokeWidth = 0.5
        pie.slices[1].popout = 20
        pie.slices[0].fillColor= colors.HexColor("#e91e63")
        pie.slices[1].fillColor=colors.HexColor("#009688")
        b.add(pie)
        x,y = 100,130 
        renderPDF.draw(b, c, x, y, showBoundary=False)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(360,340, 'Porcentaje total')
        c.drawString(365,320, 'resuelto:')

        porcentajeTotal = 100
        porcentaje = int(contadorEmpleadoscontestados * 100) / int(contadorEmpleadosActivos)

        porcentaje = str(porcentaje)

        porcentajeDigitos = ("{0:.4f}".format(float(porcentaje))) + "%"

        porcentajeBarra = ("{0:.0f}".format(float(porcentaje)))

        porcentajeBarraa = int(porcentajeBarra)

        c.setStrokeColorRGB(0.7, 0, 0.7) #color de contorno
        c.setFillColorRGB(255, 255, 255) #color de relleno
        c.rect(360, 275, 200, 25, fill=True)

        c.setStrokeColorRGB(0.7, 0, 0.7) #color de contorno

        if porcentajeBarraa >= 0 and porcentajeBarraa <= 33:
            c.setFillColorRGB(255, 0, 0) #color de relleno
            c.rect(360, 275, porcentajeBarra, 25, fill=True)
        elif porcentajeBarraa >= 34 and porcentajeBarraa <= 66:
            c.setFillColorRGB(255, 165, 0) #color de relleno
            c.rect(360, 275, porcentajeBarra, 25, fill=True)
        elif porcentajeBarraa >= 67 and porcentajeBarraa <= 100:
            c.setFillColorRGB(0, 128, 0) #color de relleno
            c.rect(360, 275, porcentajeBarra, 25, fill=True)

        c.setFont('Helvetica-Bold', 30)
        c.setFillColor(color_azul)
        c.drawString(360,230, porcentajeDigitos)
        c.setFont('Helvetica-Bold', 18)
        c.setFillColor(color_negro)
        c.drawString(360,200, "del 100% de empleados")
       



  

        
        
        f = Drawing()
        barra = VerticalBarChart()
        barra.x = 0
        barra.y = 0
        barra.height = 100
        barra.width = 50
        data = [(10,2)]
        barra.valueAxis.valueMin = 0
        barra.valueAxis.valueMax = 20 
        barra.data = data
        barra.categoryAxis.categoryNames = ['SI', 'NO']
        barra.bars[(0,0)].fillColor = colors.HexColor("#E91E63")
        barra.bars[(0,1)].fillColor = colors.red
        f.add(barra)
        x,y = 60, 300
        #renderPDF.draw(f, c, x, y, showBoundary=False)  


        #linea guinda
        color_guinda="#B03A2E"
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,60,560,60)
        
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(170,48, '2021 - Administrador de Custom System. - Versión: 1.0.0 ')
        
        
        c.showPage()
        
        
        
        #guardar pdf
        c.save()
        #obtener valores de bytesIO y esribirlos en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        respuesta.write(pdf)
        return respuesta


        
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio