import streamlit as st

st.set_page_config(page_title='SGI I+D+I - IIAD', page_icon=':microscope:', layout='wide')

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json, os, base64
from datetime import datetime, date, timedelta

try:
    import requests
    _REQ = True
except ImportError:
    _REQ = False

def _s(k, d=''):
    try: return st.secrets[k]
    except: return d

GH_TOKEN  = _s('GITHUB_TOKEN')
GH_REPO   = _s('GITHUB_REPO')
GH_PATH   = _s('GITHUB_FILE_PATH', 'sgi_state.json')
GH_BRANCH = _s('GITHUB_BRANCH', 'main')
GH_ON     = bool(GH_TOKEN and GH_REPO and _REQ)

def gh_load():
    if not GH_ON: return None, None
    try:
        url = 'https://api.github.com/repos/' + GH_REPO + '/contents/' + GH_PATH + '?ref=' + GH_BRANCH
        h = {'Authorization': 'token ' + GH_TOKEN, 'Accept': 'application/vnd.github.v3+json'}
        r = requests.get(url, headers=h, timeout=8)
        if r.status_code == 200:
            d = r.json()
            raw = base64.b64decode(d['content']).decode().strip()
            return (json.loads(raw) if raw else {}), d['sha']
    except: pass
    return None, None

def gh_save(state, sha=None):
    if not GH_ON: return False, 'GitHub no configurado.', None
    try:
        b64 = base64.b64encode(json.dumps(state, ensure_ascii=False, indent=2).encode()).decode()
        url = 'https://api.github.com/repos/' + GH_REPO + '/contents/' + GH_PATH
        h   = {'Authorization': 'token ' + GH_TOKEN, 'Accept': 'application/vnd.github.v3+json'}
        p   = {'message': 'chore: SGI ' + datetime.now().strftime('%Y-%m-%d %H:%M'),
               'content': b64, 'branch': GH_BRANCH}
        if sha: p['sha'] = sha
        r = requests.put(url, headers=h, json=p, timeout=12)
        if r.status_code in (200, 201): return True, 'Guardado en GitHub.', r.json()['content']['sha']
        return False, r.json().get('message', 'HTTP ' + str(r.status_code)), None
    except Exception as e: return False, str(e), None

PHASES = {
    'Fase 1': {
        'name': 'Fundamentos y Diagnostico', 'months': 'Meses 1-3',
        'month_start': 1, 'month_end': 3,
        'chapters': 'Cap. 4-5 NTC 5801', 'color': '#1565C0',
        'hito': 'Politica de I+D+I aprobada',
        'items': [
            {'id':'1.1','activity':'Equipo de implementacion conformado','ref':'S5.3','responsible':'Direccion','deadline':'Mes 1','evidence':'Acta designacion'},
            {'id':'1.2','activity':'Capacitacion equipo NTC 5801 e ISO 56002','ref':'S7.2','responsible':'Lider SGI','deadline':'Mes 1','evidence':'Registro asistencia'},
            {'id':'1.3','activity':'Analisis PESTEL elaborado','ref':'S4.1.2','responsible':'Lider SGI','deadline':'Mes 1','evidence':'DOC-01'},
            {'id':'1.4','activity':'Auditoria de capacidades internas','ref':'S4.1.3','responsible':'Lider SGI','deadline':'Mes 2','evidence':'DOC-01'},
            {'id':'1.5','activity':'Analisis de contexto documentado','ref':'S4.1','responsible':'Lider SGI','deadline':'Mes 2','evidence':'DOC-01 aprobado'},
            {'id':'1.6','activity':'Partes interesadas identificadas','ref':'S4.2','responsible':'Equipo','deadline':'Mes 2','evidence':'DOC-02'},
            {'id':'1.7','activity':'Necesidades y expectativas documentadas','ref':'S4.2.1','responsible':'Equipo','deadline':'Mes 2','evidence':'DOC-02'},
            {'id':'1.8','activity':'Mecanismos de interaccion definidos','ref':'S4.2.1c','responsible':'Equipo','deadline':'Mes 2','evidence':'DOC-02'},
            {'id':'1.9','activity':'Alcance del SGI documentado','ref':'S4.3','responsible':'Direccion','deadline':'Mes 2','evidence':'DOC-03'},
            {'id':'1.10','activity':'Interacciones ISO 17034 y 17043 en alcance','ref':'S4.3c','responsible':'Lider SGI','deadline':'Mes 2','evidence':'DOC-03'},
            {'id':'1.11','activity':'DOFA elaborado','ref':'S4.1','responsible':'Equipo','deadline':'Mes 3','evidence':'DOC-04'},
            {'id':'1.12','activity':'DOFA cruzado construido','ref':'S4.1','responsible':'Equipo','deadline':'Mes 3','evidence':'DOC-04'},
            {'id':'1.13','activity':'Vision de innovacion redactada','ref':'S5.1.3','responsible':'Direccion','deadline':'Mes 3','evidence':'DOC-05'},
            {'id':'1.14','activity':'Politica de I+D+I firmada','ref':'S5.2.1','responsible':'Alta direccion','deadline':'Mes 3','evidence':'DOC-06'},
            {'id':'1.15','activity':'Politica comunicada al personal','ref':'S5.2.2','responsible':'Comunicaciones','deadline':'Mes 3','evidence':'Registro difusion'},
            {'id':'1.16','activity':'Estrategia de innovacion documentada','ref':'S5.1.4','responsible':'Direccion','deadline':'Mes 3','evidence':'DOC-07'},
            {'id':'1.17','activity':'Roles y responsabilidades RACI definidos','ref':'S5.3','responsible':'Direccion','deadline':'Mes 3','evidence':'DOC-08'},
            {'id':'1.18','activity':'FTO-01 al FTO-05 aprobados','ref':'S7.5','responsible':'Lider SGI','deadline':'Mes 3','evidence':'Listado maestro'},
        ],
    },
    'Fase 2': {
        'name': 'Doc Estrategica y Apoyo', 'months': 'Meses 4-6',
        'month_start': 4, 'month_end': 6,
        'chapters': 'Cap. 6-7 NTC 5801', 'color': '#2E7D32',
        'hito': 'Sistema documental base aprobado',
        'items': [
            {'id':'2.1','activity':'Riesgos y oportunidades identificados','ref':'S6.1','responsible':'Lider SGI','deadline':'Mes 4','evidence':'DOC-09'},
            {'id':'2.2','activity':'Matriz de riesgos valorada','ref':'S6.1','responsible':'Equipo','deadline':'Mes 4','evidence':'DOC-09'},
            {'id':'2.3','activity':'Planes de tratamiento de riesgos','ref':'S6.1','responsible':'Equipo','deadline':'Mes 4','evidence':'DOC-09'},
            {'id':'2.4','activity':'Objetivos de innovacion SMART definidos','ref':'S6.2.1','responsible':'Direccion','deadline':'Mes 4','evidence':'DOC-10'},
            {'id':'2.5','activity':'Planes de accion por objetivo','ref':'S6.2.2','responsible':'Lider SGI','deadline':'Mes 4','evidence':'DOC-10'},
            {'id':'2.6','activity':'Estructura organizacional I+D+I definida','ref':'S6.3','responsible':'Direccion','deadline':'Mes 4','evidence':'DOC-11'},
            {'id':'2.7','activity':'Portafolio inicial de proyectos','ref':'S6.4','responsible':'Lider SGI','deadline':'Mes 5','evidence':'DOC-12'},
            {'id':'2.8','activity':'Procedimiento gestion de recursos','ref':'S7.1','responsible':'Lider SGI','deadline':'Mes 5','evidence':'DOC-13'},
            {'id':'2.9','activity':'Presupuesto anual I+D+I aprobado','ref':'S7.1.5','responsible':'Finanzas','deadline':'Mes 5','evidence':'DOC-14'},
            {'id':'2.10','activity':'Inventario infraestructura habilitadora','ref':'S7.1.6','responsible':'Lider SGI','deadline':'Mes 5','evidence':'DOC-15'},
            {'id':'2.11','activity':'Plan gestion del conocimiento','ref':'S7.1.4','responsible':'Lider SGI','deadline':'Mes 5','evidence':'DOC-16'},
            {'id':'2.12','activity':'Matriz de competencias diligenciada','ref':'S7.2','responsible':'RRHH','deadline':'Mes 5','evidence':'DOC-17'},
            {'id':'2.13','activity':'Brechas de competencia identificadas','ref':'S7.2','responsible':'RRHH','deadline':'Mes 5','evidence':'DOC-17'},
            {'id':'2.14','activity':'Plan de capacitacion elaborado','ref':'S7.2','responsible':'RRHH','deadline':'Mes 5','evidence':'DOC-18'},
            {'id':'2.15','activity':'Plan de comunicacion aprobado','ref':'S7.4','responsible':'Comunicaciones','deadline':'Mes 6','evidence':'DOC-19'},
            {'id':'2.16','activity':'Procedimiento control de documentos','ref':'S7.5','responsible':'Lider SGI','deadline':'Mes 6','evidence':'DOC-20'},
            {'id':'2.17','activity':'Sistema de codificacion documental','ref':'S7.5','responsible':'Lider SGI','deadline':'Mes 6','evidence':'DOC-21'},
            {'id':'2.18','activity':'Listado maestro de documentos','ref':'S7.5.3','responsible':'Lider SGI','deadline':'Mes 6','evidence':'DOC-21'},
            {'id':'2.19','activity':'Catalogo de herramientas de innovacion','ref':'S7.6','responsible':'Equipo','deadline':'Mes 6','evidence':'DOC-22'},
            {'id':'2.20','activity':'Procedimiento vigilancia tecnologica','ref':'S7.7','responsible':'Lider SGI','deadline':'Mes 6','evidence':'DOC-23'},
            {'id':'2.21','activity':'Primera vigilancia tecnologica ejecutada','ref':'S7.7','responsible':'Lider SGI','deadline':'Mes 6','evidence':'VT-001'},
            {'id':'2.22','activity':'Procedimiento propiedad intelectual','ref':'S7.8','responsible':'Asesor juridico','deadline':'Mes 6','evidence':'DOC-24'},
            {'id':'2.23','activity':'FTO-06 al FTO-14 aprobados','ref':'S7.5','responsible':'Lider SGI','deadline':'Mes 6','evidence':'Listado maestro'},
        ],
    },
    'Fase 3': {
        'name': 'Doc Operativa e Implementacion', 'months': 'Meses 7-9',
        'month_start': 7, 'month_end': 9,
        'chapters': 'Cap. 8 NTC 5801', 'color': '#E65100',
        'hito': 'Proyecto piloto en ejecucion',
        'items': [
            {'id':'3.1','activity':'Manual planificacion y control operacional','ref':'S8.1','responsible':'Lider SGI','deadline':'Mes 7','evidence':'DOC-25'},
            {'id':'3.2','activity':'Procedimiento gestion de iniciativas','ref':'S8.2','responsible':'Lider SGI','deadline':'Mes 7','evidence':'DOC-26'},
            {'id':'3.3','activity':'Procedimiento identificacion oportunidades','ref':'S8.3.2','responsible':'Lider SGI','deadline':'Mes 7','evidence':'DOC-27'},
            {'id':'3.4','activity':'Procedimiento creacion de conceptos','ref':'S8.3.3','responsible':'Lider SGI','deadline':'Mes 7','evidence':'DOC-28'},
            {'id':'3.5','activity':'Procedimiento validacion de conceptos','ref':'S8.3.4','responsible':'Lider SGI','deadline':'Mes 8','evidence':'DOC-29'},
            {'id':'3.6','activity':'Procedimiento desarrollo de soluciones','ref':'S8.3.5','responsible':'Lider SGI','deadline':'Mes 8','evidence':'DOC-30'},
            {'id':'3.7','activity':'Procedimiento despliegue de soluciones','ref':'S8.3.6','responsible':'Lider SGI','deadline':'Mes 8','evidence':'DOC-31'},
            {'id':'3.8','activity':'Manual gestion proyectos NTC 5802','ref':'NTC5802','responsible':'Lider SGI','deadline':'Mes 8','evidence':'DOC-32'},
            {'id':'3.9','activity':'Formato formulacion de proyecto MinCiencias','ref':'NTC5802','responsible':'Lider SGI','deadline':'Mes 8','evidence':'FTO-19'},
            {'id':'3.10','activity':'Al menos 1 proyecto piloto en ejecucion','ref':'S8.3','responsible':'Investigador','deadline':'Mes 9','evidence':'Ficha proyecto'},
            {'id':'3.11','activity':'Primera acta comite de innovacion','ref':'S8.2','responsible':'Lider SGI','deadline':'Mes 9','evidence':'FTO-23'},
            {'id':'3.12','activity':'FTO-15 al FTO-24 aprobados','ref':'S7.5','responsible':'Lider SGI','deadline':'Mes 9','evidence':'Listado maestro'},
            {'id':'3.13','activity':'Laboratorio en InstituLAC MinCiencias','ref':'Ext.','responsible':'Direccion','deadline':'Mes 7','evidence':'Constancia registro'},
            {'id':'3.14','activity':'Grupos registrados en GrupLAC','ref':'Ext.','responsible':'Investigador lider','deadline':'Mes 8','evidence':'Ficha GrupLAC'},
            {'id':'3.15','activity':'CvLAC del personal actualizado','ref':'Ext.','responsible':'Investigadores','deadline':'Mes 8','evidence':'Perfiles activos'},
            {'id':'3.16','activity':'Productos de investigacion clasificados','ref':'Ext.','responsible':'Lider SGI','deadline':'Mes 9','evidence':'Listado clasificado'},
        ],
    },
    'Fase 4': {
        'name': 'Evaluacion Auditoria y Mejora', 'months': 'Meses 10-12',
        'month_start': 10, 'month_end': 12,
        'chapters': 'Cap. 9-10 NTC 5801', 'color': '#6A1B9A',
        'hito': 'Primera auditoria interna realizada',
        'items': [
            {'id':'4.1','activity':'Procedimiento seguimiento y medicion','ref':'S9.1.1','responsible':'Lider SGI','deadline':'Mes 10','evidence':'DOC-34'},
            {'id':'4.2','activity':'Indicadores de I+D+I definidos','ref':'S9.1.2','responsible':'Lider SGI','deadline':'Mes 10','evidence':'DOC-35'},
            {'id':'4.3','activity':'Linea base de indicadores establecida','ref':'S9.1.2','responsible':'Lider SGI','deadline':'Mes 10','evidence':'Registro inicial'},
            {'id':'4.4','activity':'Dashboard de seguimiento implementado','ref':'S9.1','responsible':'Lider SGI','deadline':'Mes 10','evidence':'Base datos activa'},
            {'id':'4.5','activity':'Programa anual de auditorias','ref':'S9.2','responsible':'Auditor interno','deadline':'Mes 10','evidence':'DOC-38'},
            {'id':'4.6','activity':'Auditor interno capacitado NTC 5801','ref':'S9.2','responsible':'Direccion','deadline':'Mes 10','evidence':'Certificado'},
            {'id':'4.7','activity':'Lista verificacion auditoria elaborada','ref':'S9.2','responsible':'Auditor interno','deadline':'Mes 10','evidence':'DOC-39'},
            {'id':'4.8','activity':'Primera auditoria interna realizada','ref':'S9.2','responsible':'Auditor interno','deadline':'Mes 11','evidence':'DOC-40'},
            {'id':'4.9','activity':'No conformidades identificadas','ref':'S10.2','responsible':'Auditor interno','deadline':'Mes 11','evidence':'FTO-26'},
            {'id':'4.10','activity':'Planes de accion correctiva elaborados','ref':'S10.2','responsible':'Responsables','deadline':'Mes 11','evidence':'FTO-27'},
            {'id':'4.11','activity':'Procedimiento revision por la direccion','ref':'S9.3','responsible':'Direccion','deadline':'Mes 11','evidence':'DOC-41'},
            {'id':'4.12','activity':'Primera revision por la direccion realizada','ref':'S9.3','responsible':'Alta direccion','deadline':'Mes 12','evidence':'DOC-42'},
            {'id':'4.13','activity':'Informe anual desempeno del SGI','ref':'S9.1.2','responsible':'Lider SGI','deadline':'Mes 12','evidence':'DOC-36'},
            {'id':'4.14','activity':'Plan mejora continua anio 2','ref':'S10.3','responsible':'Equipo','deadline':'Mes 12','evidence':'DOC-45'},
            {'id':'4.15','activity':'FTO-25 al FTO-30 en uso','ref':'S7.5','responsible':'Lider SGI','deadline':'Mes 12','evidence':'Listado maestro'},
            {'id':'4.16','activity':'Sistema listo para evaluacion ICONTEC','ref':'S4-10','responsible':'Lider SGI','deadline':'Mes 12','evidence':'45 documentos base'},
        ],
    },
}

DOCUMENTS = [
    {'code':'DOC-01','name':'Analisis cuestiones externas e internas','phase':'Fase 1','chapter':'S4.1','type':'Procedimiento + Registro'},
    {'code':'DOC-02','name':'Matriz de partes interesadas','phase':'Fase 1','chapter':'S4.2','type':'Registro vivo'},
    {'code':'DOC-03','name':'Alcance del SGI','phase':'Fase 1','chapter':'S4.3','type':'Declaracion formal'},
    {'code':'DOC-04','name':'Analisis DOFA del laboratorio','phase':'Fase 1','chapter':'S4.1','type':'Registro interno'},
    {'code':'DOC-05','name':'Vision de innovacion','phase':'Fase 1','chapter':'S5.1.3','type':'Declaracion estrategica'},
    {'code':'DOC-06','name':'Politica de I+D+I','phase':'Fase 1','chapter':'S5.2.1','type':'Documento oficial'},
    {'code':'DOC-07','name':'Estrategia de innovacion','phase':'Fase 1','chapter':'S5.1.4','type':'Documento estrategico'},
    {'code':'DOC-08','name':'Matriz RACI roles y responsabilidades','phase':'Fase 1','chapter':'S5.3','type':'Organigrama + RACI'},
    {'code':'DOC-09','name':'Matriz de riesgos y oportunidades','phase':'Fase 2','chapter':'S6.1','type':'Registro vivo'},
    {'code':'DOC-10','name':'Objetivos SMART y planes de accion','phase':'Fase 2','chapter':'S6.2','type':'Plan formal'},
    {'code':'DOC-11','name':'Estructura organizacional I+D+I','phase':'Fase 2','chapter':'S6.3','type':'Organigrama'},
    {'code':'DOC-12','name':'Portafolio de iniciativas','phase':'Fase 2','chapter':'S6.4','type':'Base de datos'},
    {'code':'DOC-13','name':'Procedimiento gestion de recursos','phase':'Fase 2','chapter':'S7.1','type':'Procedimiento'},
    {'code':'DOC-14','name':'Presupuesto anual I+D+I','phase':'Fase 2','chapter':'S7.1.5','type':'Plan financiero'},
    {'code':'DOC-15','name':'Inventario infraestructura habilitadora','phase':'Fase 2','chapter':'S7.1.6','type':'Registro'},
    {'code':'DOC-16','name':'Plan gestion del conocimiento','phase':'Fase 2','chapter':'S7.1.4','type':'Plan'},
    {'code':'DOC-17','name':'Matriz de competencias del personal','phase':'Fase 2','chapter':'S7.2','type':'Registro'},
    {'code':'DOC-18','name':'Plan anual de capacitacion','phase':'Fase 2','chapter':'S7.2','type':'Plan'},
    {'code':'DOC-19','name':'Plan de comunicacion del SGI','phase':'Fase 2','chapter':'S7.4','type':'Plan'},
    {'code':'DOC-20','name':'Procedimiento control de documentos','phase':'Fase 2','chapter':'S7.5','type':'Procedimiento maestro'},
    {'code':'DOC-21','name':'Listado maestro de documentos','phase':'Fase 2','chapter':'S7.5.3','type':'Registro vivo'},
    {'code':'DOC-22','name':'Catalogo herramientas de innovacion','phase':'Fase 2','chapter':'S7.6','type':'Catalogo'},
    {'code':'DOC-23','name':'Procedimiento vigilancia tecnologica','phase':'Fase 2','chapter':'S7.7','type':'Procedimiento'},
    {'code':'DOC-24','name':'Procedimiento propiedad intelectual','phase':'Fase 2','chapter':'S7.8','type':'Procedimiento'},
    {'code':'DOC-25','name':'Manual planificacion y control operacional','phase':'Fase 3','chapter':'S8.1','type':'Manual'},
    {'code':'DOC-26','name':'Procedimiento gestion de iniciativas','phase':'Fase 3','chapter':'S8.2','type':'Procedimiento'},
    {'code':'DOC-27','name':'Procedimiento identificacion oportunidades','phase':'Fase 3','chapter':'S8.3.2','type':'Procedimiento'},
    {'code':'DOC-28','name':'Procedimiento creacion de conceptos','phase':'Fase 3','chapter':'S8.3.3','type':'Procedimiento'},
    {'code':'DOC-29','name':'Procedimiento validacion de conceptos','phase':'Fase 3','chapter':'S8.3.4','type':'Procedimiento'},
    {'code':'DOC-30','name':'Procedimiento desarrollo de soluciones','phase':'Fase 3','chapter':'S8.3.5','type':'Procedimiento'},
    {'code':'DOC-31','name':'Procedimiento despliegue de soluciones','phase':'Fase 3','chapter':'S8.3.6','type':'Procedimiento'},
    {'code':'DOC-32','name':'Manual gestion proyectos NTC 5802','phase':'Fase 3','chapter':'S8+5802','type':'Manual'},
    {'code':'DOC-33','name':'Formato formulacion proyecto MinCiencias','phase':'Fase 3','chapter':'NTC5802','type':'Formato estandar'},
    {'code':'DOC-34','name':'Procedimiento seguimiento y medicion','phase':'Fase 4','chapter':'S9.1.1','type':'Procedimiento'},
    {'code':'DOC-35','name':'Tablero de indicadores KPIs','phase':'Fase 4','chapter':'S9.1.2','type':'Dashboard'},
    {'code':'DOC-36','name':'Informe anual desempeno SGI','phase':'Fase 4','chapter':'S9.1.2','type':'Informe'},
    {'code':'DOC-37','name':'Procedimiento auditoria interna','phase':'Fase 4','chapter':'S9.2','type':'Procedimiento'},
    {'code':'DOC-38','name':'Programa anual de auditorias','phase':'Fase 4','chapter':'S9.2','type':'Plan'},
    {'code':'DOC-39','name':'Lista verificacion auditoria','phase':'Fase 4','chapter':'S9.2','type':'Instrumento'},
    {'code':'DOC-40','name':'Informe de auditoria interna','phase':'Fase 4','chapter':'S9.2','type':'Registro'},
    {'code':'DOC-41','name':'Procedimiento revision por la direccion','phase':'Fase 4','chapter':'S9.3','type':'Procedimiento'},
    {'code':'DOC-42','name':'Informe revision por la direccion','phase':'Fase 4','chapter':'S9.3','type':'Registro'},
    {'code':'DOC-43','name':'Procedimiento no conformidades','phase':'Fase 4','chapter':'S10.2','type':'Procedimiento'},
    {'code':'DOC-44','name':'Registro no conformidades y mejoras','phase':'Fase 4','chapter':'S10.2','type':'Registro vivo'},
    {'code':'DOC-45','name':'Plan de mejora continua del SGI','phase':'Fase 4','chapter':'S10.3','type':'Plan anual'},
]

FORMATS = [
    {'code':'FTO-01','name':'Formato analisis PESTEL','phase':'Fase 1'},
    {'code':'FTO-02','name':'Plantilla matriz partes interesadas','phase':'Fase 1'},
    {'code':'FTO-03','name':'Plantilla DOFA cruzada','phase':'Fase 1'},
    {'code':'FTO-04','name':'Acta reunion alta direccion','phase':'Fase 1'},
    {'code':'FTO-05','name':'Acta conformacion equipo implementacion','phase':'Fase 1'},
    {'code':'FTO-06','name':'Formato identificacion y evaluacion riesgos','phase':'Fase 2'},
    {'code':'FTO-07','name':'Ficha objetivo de innovacion','phase':'Fase 2'},
    {'code':'FTO-08','name':'Formato solicitud y asignacion recursos','phase':'Fase 2'},
    {'code':'FTO-09','name':'Perfil competencias por cargo','phase':'Fase 2'},
    {'code':'FTO-10','name':'Formato evaluacion de competencias','phase':'Fase 2'},
    {'code':'FTO-11','name':'Formato solicitud de capacitacion','phase':'Fase 2'},
    {'code':'FTO-12','name':'Registro asistencia capacitaciones','phase':'Fase 2'},
    {'code':'FTO-13','name':'Solicitud proteccion propiedad intelectual','phase':'Fase 2'},
    {'code':'FTO-14','name':'Informe vigilancia tecnologica','phase':'Fase 2'},
    {'code':'FTO-15','name':'Formato captacion ideas y oportunidades','phase':'Fase 3'},
    {'code':'FTO-16','name':'Ficha evaluacion preliminar de ideas','phase':'Fase 3'},
    {'code':'FTO-17','name':'Formato desarrollo de concepto','phase':'Fase 3'},
    {'code':'FTO-18','name':'Protocolo prueba o validacion experimental','phase':'Fase 3'},
    {'code':'FTO-19','name':'Ficha de proyecto I+D+I','phase':'Fase 3'},
    {'code':'FTO-20','name':'Cronograma de proyecto Gantt','phase':'Fase 3'},
    {'code':'FTO-21','name':'Informe de avance de proyecto','phase':'Fase 3'},
    {'code':'FTO-22','name':'Informe final de proyecto','phase':'Fase 3'},
    {'code':'FTO-23','name':'Acta comite de innovacion','phase':'Fase 3'},
    {'code':'FTO-24','name':'Registro lecciones aprendidas','phase':'Fase 3'},
    {'code':'FTO-25','name':'Ficha de indicador KPI','phase':'Fase 4'},
    {'code':'FTO-26','name':'Formato reporte no conformidad','phase':'Fase 4'},
    {'code':'FTO-27','name':'Formato accion correctiva y preventiva','phase':'Fase 4'},
    {'code':'FTO-28','name':'Lista chequeo auditoria interna','phase':'Fase 4'},
    {'code':'FTO-29','name':'Acta revision por la direccion','phase':'Fase 4'},
    {'code':'FTO-30','name':'Encuesta satisfaccion partes interesadas','phase':'Fase 4'},
]

STATUS_OPTIONS = ['Pendiente', 'En proceso', 'Completo', 'No aplica']
STATE_FILE     = 'sgi_state.json'
PHASE_PAGES    = {'Fase 1 - Fundamentos': 'Fase 1', 'Fase 2 - Apoyo Estrategico': 'Fase 2',
                  'Fase 3 - Operacion': 'Fase 3', 'Fase 4 - Evaluacion y Mejora': 'Fase 4'}
MES_HITO       = {'Fase 1':'Mes 3','Fase 2':'Mes 6','Fase 3':'Mes 9','Fase 4':'Mes 12'}
DOC_TYPES = ['Procedimiento','Manual','Registro','Plan','Declaracion formal','Instrumento',
             'Informe','Catalogo','Organigrama','Base de datos','Formato estandar','Otro']

# ---- DEFAULT_CONFIG: valores por defecto para la seccion Configuracion ----
DEFAULT_CONFIG = {
    'fecha_inicio_proyecto': '',
    'responsable_principal': '',
}

# ---- Helpers: fecha de inicio del proyecto ----
def get_start_date():
    # Primero busca en _config (nueva estructura), luego en project_start_date (legado)
    cfg = st.session_state.state.get('_config', {})
    raw = cfg.get('fecha_inicio_proyecto', '') or st.session_state.state.get('project_start_date', '')
    if raw:
        try: return date.fromisoformat(raw)
        except: pass
    return None

def mes_to_date(mes_str, start):
    """Convierte 'Mes N' a fecha real dado el start del proyecto."""
    try:
        n = int(mes_str.replace('Mes ', '').strip())
        return start + timedelta(days=30 * n)
    except:
        return None

def get_delayed_items():
    """Devuelve lista de items atrasados (plazo vencido y no Completo/No aplica)."""
    start = get_start_date()
    if not start: return []
    today = date.today()
    delayed = []
    for pk, ph in PHASES.items():
        for item in ph['items']:
            k   = ikey(pk, item['id'])
            ist = get_istate(k)
            if ist['status'] in ('Completo', 'No aplica'): continue
            deadline_date = mes_to_date(item['deadline'], start)
            if deadline_date and today > deadline_date:
                days_late = (today - deadline_date).days
                delayed.append({
                    'fase': pk, 'id': item['id'], 'activity': item['activity'],
                    'ref': item['ref'], 'deadline': item['deadline'],
                    'deadline_date': deadline_date, 'days_late': days_late,
                    'status': ist['status'], 'responsible': item['responsible'],
                })
    return sorted(delayed, key=lambda x: x['days_late'], reverse=True)

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                txt = f.read().strip()
            return json.loads(txt) if txt else {}
        except Exception:
            return {}
    return {}

def save_state(s):
    """Guarda localmente y marca cambios pendientes para sincronizar con GitHub."""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(s, f, ensure_ascii=False, indent=2)
    # Marcar que hay cambios pendientes de subir a GitHub
    st.session_state.pending_save = True

def ikey(pk, iid): return 'chk_' + pk + '_' + iid
def dkey(code):    return 'doc_' + code

def get_istate(key):
    v = st.session_state.state.get(key, {})
    if isinstance(v, str): v = {'status': v}
    return {'status': v.get('status','Pendiente'), 'fecha_inicio': v.get('fecha_inicio',''),
            'fecha_fin': v.get('fecha_fin',''), 'responsable_nombre': v.get('responsable_nombre',''),
            'rol': v.get('rol',''), 'comentario': v.get('comentario','')}

def save_istate(key, data):
    st.session_state.state[key] = data
    save_state(st.session_state.state)

def get_custom_code(orig):
    return st.session_state.state.get('custom_codes', {}).get(orig, orig)

def set_custom_code(orig, new):
    st.session_state.state.setdefault('custom_codes', {})[orig] = new.strip() or orig
    save_state(st.session_state.state)

def get_doc_status(code):
    v = st.session_state.state.get(dkey(code), 'Pendiente')
    return v if isinstance(v, str) else v.get('status', 'Pendiente')

def set_doc_status(code, status):
    v = st.session_state.state.get(dkey(code), {})
    if isinstance(v, str): v = {'status': v}
    v['status'] = status
    st.session_state.state[dkey(code)] = v
    save_state(st.session_state.state)

def get_extra_docs():
    return st.session_state.state.get('extra_documents', [])

def get_extra_fmts():
    return st.session_state.state.get('extra_formats', [])

def add_extra_doc(entry):
    st.session_state.state.setdefault('extra_documents', []).append(entry)
    save_state(st.session_state.state)

def add_extra_fmt(entry):
    st.session_state.state.setdefault('extra_formats', []).append(entry)
    save_state(st.session_state.state)

def remove_extra_doc(code):
    lst = st.session_state.state.get('extra_documents', [])
    st.session_state.state['extra_documents'] = [d for d in lst if d['code'] != code]
    save_state(st.session_state.state)

def remove_extra_fmt(code):
    lst = st.session_state.state.get('extra_formats', [])
    st.session_state.state['extra_formats'] = [d for d in lst if d['code'] != code]
    save_state(st.session_state.state)

def all_docs():
    return DOCUMENTS + get_extra_docs()

def all_fmts():
    return FORMATS + get_extra_fmts()

def code_exists(code):
    all_codes = [d['code'] for d in all_docs()] + [d['code'] for d in all_fmts()]
    return code.strip().upper() in [c.upper() for c in all_codes]

# ---- Inicializar session_state ----
if 'state' not in st.session_state:
    st.session_state.state        = load_state()
    st.session_state.gh_sha       = None
    st.session_state.gh_source    = 'local'
    st.session_state.gh_loaded    = False
    st.session_state.pending_save = False  # FIX: flag de auto-guardado

def phase_progress(pk):
    items = PHASES[pk]['items']
    total = len(items)
    done  = sum(1 for i in items if get_istate(ikey(pk, i['id']))['status'] == 'Completo')
    wip   = sum(1 for i in items if get_istate(ikey(pk, i['id']))['status'] == 'En proceso')
    na    = sum(1 for i in items if get_istate(ikey(pk, i['id']))['status'] == 'No aplica')
    appl  = total - na
    return total, done, wip, na, (round(done / appl * 100) if appl > 0 else 0)

def overall_progress():
    ai = sum(len(PHASES[pk]['items']) for pk in PHASES)
    ad = sum(phase_progress(pk)[1] for pk in PHASES)
    an = sum(phase_progress(pk)[3] for pk in PHASES)
    ap = ai - an
    return ai, ad, ap, (round(ad / ap * 100) if ap > 0 else 0)

def doc_progress():
    all_d = all_docs() + all_fmts()
    tot   = len(all_d)
    done  = sum(1 for d in all_d if get_doc_status(d['code']) == 'Completo')
    return tot, done, (round(done / tot * 100) if tot > 0 else 0)

# ---- Gantt builder ----
def build_gantt_df(start_date):
    rows = []
    for pk, ph in PHASES.items():
        # Barra de fase completa
        fs = start_date + timedelta(days=30 * (ph['month_start'] - 1))
        fe = start_date + timedelta(days=30 * ph['month_end'])
        _,done,wip,na,pct = phase_progress(pk)
        rows.append({'Tarea': pk + ': ' + ph['name'], 'Inicio': fs, 'Fin': fe,
                     'Fase': pk, 'Tipo': 'Fase', 'Avance': str(pct)+'%',
                     'Estado': 'Completo' if pct==100 else ('En proceso' if done+wip>0 else 'Pendiente')})
        # Barras por actividad
        for item in ph['items']:
            n = int(item['deadline'].replace('Mes ', ''))
            act_start = start_date + timedelta(days=30 * (n - 1))
            act_end   = start_date + timedelta(days=30 * n)
            ist = get_istate(ikey(pk, item['id']))
            rows.append({'Tarea': item['id'] + ': ' + item['activity'][:50],
                         'Inicio': act_start, 'Fin': act_end,
                         'Fase': pk, 'Tipo': 'Actividad',
                         'Avance': item['deadline'], 'Estado': ist['status']})
    return pd.DataFrame(rows)

COLOR_STATUS = {'Completo':'#43A047','En proceso':'#1E88E5','Pendiente':'#B0BEC5',
                'No aplica':'#FF7043','Atrasado':'#E53935'}

st.markdown('''<style>
[data-testid="stSidebar"]{background-color:#0D1B2A}
[data-testid="stSidebar"] *{color:#E8EDF3!important}
[data-testid="stSidebar"] hr{border-color:#2a3f5a!important}
.kcard{background:white;border-radius:12px;padding:16px;border-left:5px solid;
       box-shadow:0 2px 8px rgba(0,0,0,.07);margin-bottom:10px}
.kpct{font-size:2rem;font-weight:800;margin:4px 0}
.tag{display:inline-block;padding:2px 9px;border-radius:20px;font-size:.74rem;font-weight:600}
.extra-badge{display:inline-block;padding:1px 7px;border-radius:10px;font-size:.70rem;
             font-weight:600;background:#FFF3E0;color:#E65100;border:1px solid #FFCC02}
.alert-row{background:#FFF8E1;border-left:4px solid #F9A825;border-radius:6px;
           padding:8px 12px;margin-bottom:6px;font-size:.83rem}
.late-badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:.72rem;
            font-weight:700;background:#FFEBEE;color:#C62828;border:1px solid #EF9A9A}
</style>''', unsafe_allow_html=True)

with st.sidebar:
    lb = st.session_state.state.get('logo_b64')
    if lb:
        st.markdown('<img src="' + lb + '" style="width:100%;border-radius:8px;margin-bottom:10px">',
                    unsafe_allow_html=True)
    st.markdown('## Seguimiento de implementación sistema de gestión de la investigación')
    st.markdown('### Laboratorio Nacional de Insumos Agrícolas - LANIA - Área IIAD')
    st.markdown('*basado en las normas NTC 5801 / ISO 56002*')

    # FIX: Carga inicial desde GitHub (solo una vez por sesión)
    if GH_ON and not st.session_state.gh_loaded:
        st.session_state.gh_loaded = True
        with st.spinner('Sincronizando...'):
            gh_state, gh_sha = gh_load()
        if gh_state is not None:
            st.session_state.state        = gh_state
            st.session_state.gh_sha       = gh_sha
            st.session_state.gh_source    = 'github'
            st.session_state.pending_save = False
            save_state(gh_state)
            st.rerun()

    # FIX: Auto-guardado en GitHub cuando hay cambios pendientes
    if GH_ON and st.session_state.get('pending_save', False):
        ok, msg, new_sha = gh_save(
            st.session_state.state,
            st.session_state.get('gh_sha')
        )
        if ok:
            st.session_state.gh_sha       = new_sha
            st.session_state.gh_source    = 'github'
            st.session_state.pending_save = False

    if GH_ON:
        src   = st.session_state.get('gh_source', 'local')
        color = '#238636' if src == 'github' else '#6e7681'
        label = 'GitHub activo' if src == 'github' else 'Sin sincronizar'
        st.markdown('<span style="background:' + color + ';color:white;padding:3px 10px;'
                    'border-radius:10px;font-size:.74rem;font-weight:600">' + label + '</span>',
                    unsafe_allow_html=True)
    st.markdown('---')
    page = st.radio('', ['Dashboard','Fase 1 - Fundamentos','Fase 2 - Apoyo Estrategico',
                          'Fase 3 - Operacion','Fase 4 - Evaluacion y Mejora',
                          'Linea de Tiempo','Alertas de Atraso',
                          'Registro Documental','Reportes y Exportar','Configuracion'],
                     label_visibility='collapsed')
    st.markdown('---')
    _, done_all, appl_all, pct_all = overall_progress()
    st.markdown('### Avance: **' + str(pct_all) + '%**')
    st.progress(pct_all / 100)
    st.caption(str(done_all) + ' de ' + str(appl_all) + ' completadas')
    # Mini alerta en sidebar si hay atrasados
    delayed = get_delayed_items()
    if delayed:
        st.markdown('<div style="background:#FFEBEE;border-radius:8px;padding:8px 10px;margin-top:6px">'
                    '<span style="color:#C62828;font-weight:700">⚠️ '+str(len(delayed))+' actividades atrasadas</span>'
                    '</div>', unsafe_allow_html=True)
    st.markdown('---')
    if GH_ON:
        st.markdown('##### Sync GitHub')
        c1, c2 = st.columns(2)
        with c1:
            if st.button('Recargar', use_container_width=True):
                with st.spinner('...'): s, sha = gh_load()
                if s:
                    st.session_state.state        = s
                    st.session_state.gh_sha       = sha
                    st.session_state.gh_source    = 'github'
                    st.session_state.pending_save = False
                    save_state(s)
                    st.rerun()
                else: st.error('Error al conectar.')
        with c2:
            if st.button('Guardar', use_container_width=True, type='primary'):
                with st.spinner('...'): ok, msg, sha2 = gh_save(st.session_state.state, st.session_state.gh_sha)
                if ok:
                    st.session_state.gh_sha       = sha2
                    st.session_state.gh_source    = 'github'
                    st.session_state.pending_save = False
                    st.success(msg)
                else: st.error(msg)
        st.markdown('---')
    st.download_button('Descargar JSON',
        data=json.dumps(st.session_state.state, ensure_ascii=False, indent=2).encode(),
        file_name='sgi_' + datetime.now().strftime('%Y%m%d_%H%M') + '.json',
        mime='application/json', use_container_width=True)
    if not GH_ON:
        st.markdown('---')
        uf = st.file_uploader('Cargar sgi_state.json', type=['json'])
        if uf:
            try:
                loaded = json.load(uf); st.session_state.state = loaded
                save_state(loaded); st.rerun()
            except Exception as e: st.error(str(e))

# ============================================================
# DASHBOARD
# ============================================================
if page == 'Dashboard':
    st.title('Sistema de Gestion I+D+I - Área de Investigación e Innovación (IIAD)')
    st.markdown('**Laboratorio LANIA** | NTC 5801 / ISO 56002 | ' + datetime.now().strftime('%d/%m/%Y'))
    if GH_ON:
        src = st.session_state.get('gh_source','local')
        sha_s = (st.session_state.gh_sha or '')[:7]
        if src == 'github': st.info('Sincronizado con GitHub  SHA: ' + sha_s)
        else: st.warning('Estado local. Presiona Guardar para sincronizar.')
    # Banner de alertas
    delayed = get_delayed_items()
    if delayed:
        st.error(f'⚠️ **{len(delayed)} actividades atrasadas** detectadas. '
                 'Ve a **Alertas de Atraso** para el detalle completo.')
    elif get_start_date():
        st.success('✅ Sin actividades atrasadas a la fecha.')
    else:
        st.info('ℹ️ Configura la **fecha de inicio del proyecto** en Configuración para activar alertas de atraso.')
    st.divider()
    _, done_all, appl_all, pct_all = overall_progress()
    tot_docs, done_docs, pct_docs  = doc_progress()
    phases_done = sum(1 for pk in PHASES if phase_progress(pk)[4] == 100)
    extra_count = len(get_extra_docs()) + len(get_extra_fmts())
    k1,k2,k3,k4 = st.columns(4)
    k1.metric('Avance General',   str(pct_all)+'%',   str(done_all)+'/'+str(appl_all)+' actividades')
    k2.metric('Avance Docs',      str(pct_docs)+'%',  str(done_docs)+'/'+str(tot_docs)+' documentos')
    k3.metric('Fases Completas',  str(phases_done),   'de '+str(len(PHASES))+' fases')
    k4.metric('Extras Añadidos',  str(extra_count),   'docs/formatos adicionales')
