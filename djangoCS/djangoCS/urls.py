"""djangoCS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path
from appCS import views
from appCS import viewEmpleados
from django.conf import settings
from appCS import almacen
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login),
    path('login/', views.login),
    path('inicio/', views.inicio),
    path('verAreas/', views.verAreas),
    path('agregarAreas/',views.agregarAreas),
    path('verEmpleados/', views.verEmpleados),
    path('agregarEmpleados/', views.agregarEmpleados),
    path('verEquipos/',views.verEquipos),
    path('agregarEquipos/', views.agregarEquipos),
    path('renovacionEquipos/', views.renovacionEquipos),
    path('infoEquipo/', views.infoEquipo),
    path('verImpresoras/', views.verImpresoras),
    path('agregarImpresoras/', views.agregarImpresoras),
    path('renovacionImpresoras/', views.renovacionImpresoras),
    path('infoImpresora/', views.infoImpresora),
    path('verInsumos/', views.verInsumos),
    path('agregarInsumos/', views.agregarInsumos),
    path('actualizarInsumos/', views.actualizarInsumos),
    path('verProgramas/', views.verProgramas),
    path('agregarProgramas/', views.agregarProgramas),
    path('actualizarProgramasArea/', views.actualizarProgramasArea),
    path('calendarioMant/',views.calendarioMant),
    path('formularioMant/', views.formularioMant),
    path('verCarta/', views.verCarta),
    path('agregarCarta/', views.agregarCarta),
    path('imprimirCarta/', views.imprimirCarta),
    path("BitacorasEquipos/", views.BitacorasEquipos),
    path("BitacorasImpresoras/", views.BitacorasImpresoras),
    path("BitacorasEmpleados/", views.BitacorasEmpleados),
    path("BitacorasCartuchos/", views.BitacorasCartuchos),
    path("DescargarPDF/", views.descargarPDF),
    path("DescargarPDF2/", views.descargarPDF2),
    path("ProgramaPorArea/",views.ProgramasporArea),
    path("verProgramasPorArea/", views.verProgramasPorArea),
    path("guardarImagen/", views.guardarImagen),
    path("editarEquipo/", views.editarEquipo),
    path("editarEquipoBd/", views.editarEquipoBd),
    path("editarEmpleado/", views.editarEmpleado),
    path("editarEmpleadoBd/", views.editarEmpleadoBd),
    path("editarImpresora/", views.editarImpresora),
    path("editarImpresoraBd/", views.editarImpresoraBd),
    path("editarMouse/", views.editarMouse),
    path("editarMouseBd/", views.editarMouseBd),
    path("editarTeclado/", views.editarTeclado),
    path("editarTecladoBd/", views.editarTecladoBd),
    path("editarMonitor/", views.editarMonitor),
    path("editarMonitorBd/", views.editarMonitorBd),
    path("editarTelefono/", views.editarTelefono),
    
    path("editarTelefonoBd/", views.editarTelefonoBd),
    path("editarDisco/", views.editarDisco),
    path("editarDiscoBd/", views.editarDiscoBd),
    path("firmarCarta/", views.firmarCarta),
    path("salir/", views.salir, name="salir"),
    path("altaEmpleado/", views.altaEmpleado),
    path("bajaEmpleado/", views.bajaEmpleado),
    path("altaEquipo/", views.altaEquipo),
    path("bajaEquipo/", views.bajaEquipo),
    path("altaImpresora/", views.altaImpresora),
    path("bajaImpresora/", views.bajaImpresora),
    path("bajaMouse/", views.bajaMouse),
    path("altaMouse/", views.altaMouse),
    path("bajaTeclado/", views.bajaTeclado),
    path("altaTeclado/", views.altaTeclado),
    path("bajaMonitor/", views.bajaMonitor),
    path("altaMonitor/", views.altaMonitor),
    path("bajaTelefono/", views.bajaTelefono),
    path("altaTelefono/", views.altaTelefono),
    
    path("qrEquipo/", views.qrEquipo),
     path("qrImpresora/", views.qrImpresora),
    
    path("reporteDepartamentos/",views.reporteDepartamentos),
    path("reporteEmpleadosActivos/",views.reporteEmpleadosActivos),
    path("reporteEquiposActivos/",views.reporteEquiposActivos),
    path("reporteImpresoras/", views.reporteImpresoras),
    path("reporteInsumos/", views.reporteInsumos),
    path("reporteInsumosRequisicion/", views.reporteInsumosRequisicion),
    path("reporteRenovacionEq/", views.reporteRenovacionEq),
    path("reporteRenovacionImp/", views.reporteRenovacionImp),
    path("reporteMousesActivos/", views.reporteMousesActivos),
    
    path("pdfInfoEquipo/", views.pdfInfoEquipo),
    path("pdfInfoImpresora/", views.pdfInfoImpresora),
    
    path("xlDepartamentos/", views.xlDepartamentos),
    path("xlEmpleados/", views.xlEmpleados),
    path("xlEquipos/", views.xlEquipos),
    path("xlRenovacionEquipos/", views.xlRenovacionEquipos),
    path("xlImpresoras/",views.xlImpresoras),
    path("xlRenovacionImpresoras/", views.xlRenovacionImpresoras),
    path("xlInsumos/", views.xlInsumos),
    path("xlMouses/", views.xlMouses),
    path("xlTeclados/", views.xlTeclados),
    path("xlMonitores/", views.xlMonitores),
    path("xlTelefonos/", views.xlTelefonos),
    
    path("correoContra/", views.correoContra),
    
    #Equipos de sistemas
    path("verMouses/", views.verMouses),
    path("agregarMouses/", views.agregarMouses),
    path("verTeclados/", views.verTeclados),
    path("agregarTeclados/", views.agregarTeclados),
    path("verMonitores/", views.verMonitores),
    path("agregarMonitores/",views.agregarMonitores),
    path("verTelefonos/", views.verTelefonos),
    path("agregarTelefonos/", views.agregarTelefonos),
    path("extensionesTel/", views.extensionesTel),
    
    path("agregarDiscosDuros/", views.agregarDiscosDuros),
    path("verDiscosDuros/", views.verDiscosDuros),
    
    path("agregarUSB/", views.agregarUSB),
    path("verUSB/", views.verUSB),
    path('actualizarUSB/', views.actualizarUSB),
    
    path("agregarPrestamos/", views.agregarPrestamos),
    path("verPrestamos/", views.verPrestamos),
    path("actualizarPrestamos/", views.actualizarPrestamos),
    path("firmarPrestamoDevolucion/", views.firmarPrestamoDevolucion),
    
    path("agregarEncuestas/", views.agregarEncuestas),
    path("verEncuestas/", views.verEncuestas),
    path("preguntas/", views.preguntas),

    path("principal/", viewEmpleados.principal),
    path("encuestas/", viewEmpleados.encuestas),
    
    path("equipo/", viewEmpleados.equipo),
    path("carta/", viewEmpleados.carta),
    path("directorio/", viewEmpleados.directorio),
    path("documentosAplicablesATodos/", viewEmpleados.documentosAplicablesATodos),

    #descarga de archivos aplicables a todas las areas

    path("aplicable1/", viewEmpleados.aplicable1),
    path("aplicable2/", viewEmpleados.aplicable2),
    path("aplicable3/", viewEmpleados.aplicable3),

    path("guardarRespuesta/", viewEmpleados.guardarRespuesta),
    path("guardarRespuestaTextbox/", viewEmpleados.guardarRespuestaTextbox),

    #acceso a empleado
    path("accesoEmpleado/", viewEmpleados.accesoEmpleado),

    #resultados rh
    path("resultadosEncuestas/", viewEmpleados.resultadosEncuestas),
    path("verRespuestasAbiertas/", viewEmpleados.verRespuestasAbiertas),

    #Reportes de resultados
    path("pruebaPDF/",viewEmpleados.pruebaPDF),
    path("resultadosMultiples/",viewEmpleados.resultadosMultiples),
    path("resultadosAbiertas/",viewEmpleados.resultadosAbiertas),
    
    #Almacen
    path("solicitudesPendientesALM/",almacen.solicitudesPendientesALM),
    path("historialSolicitudesALM/",almacen.historialSolicitudesALM),
    path("solicitudesMarcadasALM/",almacen.solicitudesMarcadasALM),
    path("verHerramientasALM/",almacen.verHerramientasALM),
    path('actualizarCantidadesHerramientasAlmacen/', almacen.actualizarCantidadesHerramientasAlmacen),
    path('bajaHerramientaAlmacen/', almacen.bajaHerramientaAlmacen),
    path('bajaHerramientaAlmacenPrestamo/', almacen.bajaHerramientaAlmacenPrestamo),
    path("agregarHerramientasALM/",almacen.agregarHerramientasALM),
    path("solicitarHerramientas/",almacen.solicitarHerramientas),
    path("verMisPrestamos/",almacen.verMisPrestamos),
    path("firmarPrestamo/", almacen.firmarPrestamo),
    path("guardarEntrega/", almacen.guardarEntrega),
    path("guardarDevolucion/", almacen.guardarDevolucion),
    path("firmarDevolucion/", almacen.firmarDevolucion),
    path("excelInventario/", almacen.excelInventario),
    path("excelInventarioHerramientas/", almacen.excelInventarioHerramientas),
    path("devolucionParcial/", almacen.devolucionParcial),
    path("guardarDevolucionParcial/", almacen.guardarDevolucionParcial),
    path("verRequisicionesHerramientas/", almacen.verRequisicionesHerramientas),
    path("entradaHerramientaPorRequi/", almacen.entradaHerramientaPorRequi),
    path("descontarDeInventario/", almacen.descontarDeInventario),
    path("pdfCostosAlmac??n/", almacen.pdfCostosAlmac??n),
    path("listaAltasAlmacen/", almacen.listaAltasAlmacen),
    path("excelInventarioHerramientasCategoria/", almacen.excelInventarioHerramientasCategoria),
    path("quitarPerdida/", almacen.quitarPerdida),
    #soportes tecnicos
    path("verSoportes/",views.verSoportes),
    path("agregarSoporteEquipoComputo/",views.agregarSoporteEquipoComputo),
    path("agregarSoporteImpresora/",views.agregarSoporteImpresora),
    path("agregarSoporteOtros/",views.agregarSoporteOtros),
    
    #Implementacion de soluciones
    path("verImplementaciones/", views.verImplementaciones),
    path("agregarImplementacion/", views.agregarImplementacion),
    
    path("implementacionesSistemas/", viewEmpleados.implementacionesSistemas),
    path("revisarImplementacion/", viewEmpleados.revisarImplementacion),
    path("firmarImplementacion/", viewEmpleados.firmarImplementacion),
    path("excelImplementacion/", viewEmpleados.excelImplementacion),
    
    
    #Mochilas
    path("verMochilas/", views.verMochilas),
    path("agregarMochila/", views.agregarMochila),
    path("altaMochila/", views.altaMochila),
    path("bajaMochila/", views.bajaMochila),
    path("xlMochilas/", views.xlMochilas),
    path("editarMochila/", views.editarMochila),
    
    #Celulares
    path("agregarCelulares/", views.agregarCelulares),
    path("verCelulares/", views.verCelulares),
    path("bajaCelular/", views.bajaCelular),
    path("altaCelular/", views.altaCelular),
    path("editarCelular/", views.editarCelular),
    path("xlCelulares/", views.xlCelulares),
    path("agregarCartaCelulares/", views.agregarCartaCelulares),
    path("guardarFirmaCelularSinQR/", views.guardarFirmaCelularSinQR),
    path("firmarCartaCelularQR/", views.firmarCartaCelularQR),
    path("cartasCelulares/", views.cartasCelulares),
    path("imprimirCartaCelular/", views.imprimirCartaCelular)


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
