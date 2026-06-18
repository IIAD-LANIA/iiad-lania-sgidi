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

# ---- Helpers: fecha de inicio del proyecto ----
def get_start_date():
    raw = st.session_state.state.get('project_start_date', '')
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
    k1.metric('Avance General', str(pct_all)+'%', str(done_all)+'/'+str(appl_all)+' actividades')
    k2.metric('Documentos', str(pct_docs)+'%', str(done_docs)+'/'+str(tot_docs)+' elaborados')
    k3.metric('Fases completadas', str(phases_done)+'/4')
    k4.metric('Docs adicionales', extra_count, 'incorporados al sistema')
    st.divider()
    st.markdown('### Progreso por Fase')
    cols = st.columns(4)
    for i, pk in enumerate(PHASES):
        ph = PHASES[pk]
        total,done,wip,na,pct = phase_progress(pk)
        pend = total-done-wip-na
        # Calcular atrasados de esta fase
        n_late = sum(1 for d in delayed if d['fase'] == pk)
        late_html = (''
            if not n_late else
            '<div class="late-badge" style="margin-top:6px">⚠️ '+str(n_late)+' atrasada(s)</div>')
        card = ('<div class="kcard" style="border-left-color:'+ph['color']+'">'
                '<div style="font-weight:700">'+pk+'</div>'
                '<div style="font-size:.8rem;color:#777">'+ph['name']+'</div>'
                '<div class="kpct" style="color:'+ph['color']+'">'+str(pct)+'%</div>'
                '<div style="font-size:.8rem;color:#777">'+ph['months']+'</div>'
                '<div style="margin-top:8px;font-size:.82rem">'
                'OK '+str(done)+' | ~ '+str(wip)+' | P '+str(pend)+' | N/A '+str(na)
                +'</div>'+late_html+'</div>')
        with cols[i]: st.markdown(card, unsafe_allow_html=True); st.progress(pct/100)
    st.divider()
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('#### Estado por fase')
        cr = []
        for pk in PHASES:
            total,done,wip,na,_ = phase_progress(pk)
            cr += [{'Fase':pk,'Estado':'Completo','n':done},
                   {'Fase':pk,'Estado':'En proceso','n':wip},
                   {'Fase':pk,'Estado':'Pendiente','n':total-done-wip-na},
                   {'Fase':pk,'Estado':'No aplica','n':na}]
        fig = px.bar(pd.DataFrame(cr),x='Fase',y='n',color='Estado',barmode='stack',height=300,
                     color_discrete_map={'Completo':'#4CAF50','En proceso':'#2196F3','Pendiente':'#CFD8DC','No aplica':'#FF7043'})
        fig.update_layout(plot_bgcolor='white',legend=dict(orientation='h',y=-0.3))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('#### Radar de avance')
        lbls=['F'+str(i+1)+': '+PHASES[pk]['name'][:14] for i,pk in enumerate(PHASES)]
        vals=[phase_progress(pk)[4] for pk in PHASES]
        fig_r=go.Figure(go.Scatterpolar(r=vals+[vals[0]],theta=lbls+[lbls[0]],
            fill='toself',fillcolor='rgba(21,101,192,0.15)',line=dict(color='#1565C0',width=2)))
        fig_r.update_layout(polar=dict(radialaxis=dict(range=[0,100])),height=300,margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig_r,use_container_width=True)
    st.divider()
    st.markdown('### Hitos de Cierre')
    mc = st.columns(4)
    for i,pk in enumerate(PHASES):
        ph=PHASES[pk]; _,done,_,_,pct=phase_progress(pk)
        ico='✅' if pct==100 else ('⏳' if done>0 else '…')
        hito=('<div style="background:'+ph['color']+'12;border:1px solid '+ph['color']+'40;'
              'border-radius:10px;padding:14px;text-align:center">'
              '<div style="color:'+ph['color']+';font-weight:700">'+MES_HITO[pk]+'</div>'
              '<div style="font-size:1.3rem;margin:6px 0">'+ico+'</div>'
              '<div style="font-size:.8rem;color:#444">'+ph['hito']+'</div></div>')
        with mc[i]: st.markdown(hito,unsafe_allow_html=True)

# ============================================================
# FASES
# ============================================================
elif page in PHASE_PAGES:
    pk=PHASE_PAGES[page]; ph=PHASES[pk]
    total,done,wip,na,pct=phase_progress(pk)
    st.title(pk+': '+ph['name'])
    st.markdown('**'+ph['months']+'** | '+ph['chapters'])
    st.divider()
    kc=st.columns(5)
    kc[0].metric('Avance',str(pct)+'%'); kc[1].metric('Completas',done)
    kc[2].metric('En proceso',wip); kc[3].metric('Pendientes',total-done-wip-na); kc[4].metric('No aplica',na)
    st.progress(pct/100)
    # Mini-panel alertas de esta fase
    delayed_fase = [d for d in get_delayed_items() if d['fase'] == pk]
    if delayed_fase:
        with st.expander(f'⚠️ {len(delayed_fase)} actividad(es) atrasada(s) en esta fase', expanded=True):
            for d in delayed_fase:
                st.markdown(
                    f'<div class="alert-row">'
                    f'<b>{d["id"]}</b> &nbsp;|&nbsp; {d["activity"]}<br>'
                    f'Plazo: <b>{d["deadline"]}</b> ({d["deadline_date"].strftime("%d/%m/%Y")}) &nbsp;'
                    f'<span class="late-badge">{d["days_late"]} días de atraso</span> &nbsp;'
                    f'Estado actual: <i>{d["status"]}</i> &nbsp;| Responsable: {d["responsible"]}'
                    f'</div>', unsafe_allow_html=True)
    st.divider()
    fc1,fc2,fc3=st.columns(3)
    with fc1: f_st=st.multiselect('Estado:',STATUS_OPTIONS,default=STATUS_OPTIONS,key='fs_'+pk)
    with fc2: f_tx=st.text_input('Buscar:',key='ft_'+pk)
    with fc3:
        resps=sorted(set(i['responsible'] for i in ph['items']))
        f_rp=st.multiselect('Responsable:',resps,default=resps,key='fr_'+pk)
    st.divider()
    hdr=st.columns([0.4,0.6,4.0,0.9,1.6,0.5])
    for col,lbl in zip(hdr,['**#**','**Ref.**','**Actividad**','**Plazo**','**Estado**','']): col.markdown(lbl)
    st.markdown('<hr style="margin:4px 0">',unsafe_allow_html=True)
    delayed_ids = {d['id'] for d in delayed_fase}
    for item in ph['items']:
        k=ikey(pk,item['id']); ist=get_istate(k); cur=ist['status']
        if cur not in f_st: continue
        if f_tx and f_tx.lower() not in item['activity'].lower(): continue
        if item['responsible'] not in f_rp: continue
        is_late = item['id'] in delayed_ids
        row=st.columns([0.4,0.6,4.0,0.9,1.6,0.5])
        row[0].markdown('**'+item['id']+'**')
        row[1].markdown('`'+item['ref']+'`')
        badges=''
        if ist['responsable_nombre']: badges+=' | '+ist['responsable_nombre']
        if ist['fecha_inicio']:       badges+=' | '+ist['fecha_inicio']
        if ist['fecha_fin']:          badges+=' -> '+ist['fecha_fin']
        row[2].markdown(item['activity']+'<br><small style="color:#888">'+badges+'</small>',unsafe_allow_html=True)
        row[3].markdown('<small>'+item['deadline']+'</small>',unsafe_allow_html=True)
        new_st=row[4].selectbox('',STATUS_OPTIONS,index=STATUS_OPTIONS.index(cur),
                                 key='sel_'+pk+'_'+item['id'],label_visibility='collapsed')
        if new_st!=cur: ist['status']=new_st; save_istate(k,ist); st.rerun()
        row[5].markdown('<span title="Atrasado">⚠️</span>' if is_late else '', unsafe_allow_html=True)
        with st.expander('Detalles  '+item['id']+': '+item['activity'][:55]):
            d1,d2,d3,d4=st.columns(4)
            try:    fi_v=date.fromisoformat(ist['fecha_inicio']) if ist['fecha_inicio'] else None
            except: fi_v=None
            try:    ff_v=date.fromisoformat(ist['fecha_fin']) if ist['fecha_fin'] else None
            except: ff_v=None
            new_fi  =d1.date_input('Fecha inicio',value=fi_v,key='fi_'+pk+'_'+item['id'])
            new_ff  =d2.date_input('Fecha fin',value=ff_v,key='ff_'+pk+'_'+item['id'])
            new_resp=d3.text_input('Responsable',value=ist['responsable_nombre'],key='rn_'+pk+'_'+item['id'])
            new_rol =d4.text_input('Rol',value=ist['rol'],key='rl_'+pk+'_'+item['id'])
            new_cmt =st.text_area('Comentario / Enlace',value=ist['comentario'],key='cm_'+pk+'_'+item['id'],height=70)
            if ist['comentario'] and ist['comentario'].startswith('http'):
                st.markdown('<a href="'+ist['comentario']+'" target="_blank">Ver evidencia</a>',unsafe_allow_html=True)
            st.caption('Evidencia esperada: '+item['evidence'])
            if is_late:
                late_info = next((d for d in delayed_fase if d['id']==item['id']),None)
                if late_info: st.warning(f'⚠️ Esta actividad lleva **{late_info["days_late"]} días de atraso** (plazo: {late_info["deadline_date"].strftime("%d/%m/%Y")})')
            if st.button('Guardar',key='sv_'+pk+'_'+item['id'],type='primary'):
                save_istate(k,{'status':cur,'fecha_inicio':str(new_fi) if new_fi else '',
                    'fecha_fin':str(new_ff) if new_ff else '','responsable_nombre':new_resp,
                    'rol':new_rol,'comentario':new_cmt})
                st.success('Guardado.')
        st.markdown('<hr style="margin:3px 0;opacity:.2">',unsafe_allow_html=True)

# ============================================================
# LINEA DE TIEMPO (GANTT)
# ============================================================
elif page == 'Linea de Tiempo':
    st.title('Linea de Tiempo — Gantt de Implementacion')
    start = get_start_date()
    if not start:
        st.warning('ℹ️ Para ver el Gantt, primero configura la **fecha de inicio del proyecto** en la página **Configuración**.')
        st.stop()
    st.markdown(f'Inicio del proyecto: **{start.strftime("%d/%m/%Y")}** | '
                f'Fin estimado: **{(start + timedelta(days=30*12)).strftime("%d/%m/%Y")}**')
    st.divider()
    view = st.radio('Vista:', ['Por Fase', 'Actividades detalladas'], horizontal=True)
    filter_phase = st.multiselect('Filtrar fases:', list(PHASES.keys()), default=list(PHASES.keys()))
    st.divider()
    df_gantt = build_gantt_df(start)
    df_gantt = df_gantt[df_gantt['Fase'].isin(filter_phase)]
    today_line = date.today()
    if view == 'Por Fase':
        df_plot = df_gantt[df_gantt['Tipo'] == 'Fase'].copy()
    else:
        df_plot = df_gantt[df_gantt['Tipo'] == 'Actividad'].copy()
    # Marcar atrasados
    delayed_ids_all = {(d['fase'], d['id']) for d in get_delayed_items()}
    def estado_color(row):
        if row['Tipo'] == 'Actividad':
            iid = row['Tarea'].split(':')[0].strip()
            if (row['Fase'], iid) in delayed_ids_all and row['Estado'] not in ('Completo','No aplica'):
                return 'Atrasado'
        return row['Estado']
    df_plot['Estado_color'] = df_plot.apply(estado_color, axis=1)
    color_map = {'Completo':'#43A047','En proceso':'#1E88E5','Pendiente':'#90A4AE',
                 'No aplica':'#FF7043','Atrasado':'#E53935'}
    fig_g = px.timeline(
        df_plot, x_start='Inicio', x_end='Fin', y='Tarea',
        color='Estado_color', color_discrete_map=color_map,
        hover_data=['Fase','Avance','Estado'],
        height=max(400, len(df_plot) * 28)
    )
    fig_g.add_vline(x=str(today_line), line_dash='dash', line_color='#F44336',
                    annotation_text='Hoy', annotation_position='top right',
                    annotation_font_color='#F44336')
    fig_g.update_yaxes(autorange='reversed')
    fig_g.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(orientation='h', y=-0.08),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title='', yaxis_title=''
    )
    st.plotly_chart(fig_g, use_container_width=True)
    st.caption('La línea roja vertical indica la fecha de hoy. Las barras rojas indican actividades atrasadas.')

# ============================================================
# ALERTAS DE ATRASO
# ============================================================
elif page == 'Alertas de Atraso':
    st.title('Alertas de Atraso')
    start = get_start_date()
    if not start:
        st.warning('ℹ️ Para usar las alertas, configura la **fecha de inicio del proyecto** en **Configuración**.')
        st.stop()
    st.markdown(f'Fecha de inicio configurada: **{start.strftime("%d/%m/%Y")}** | Hoy: **{date.today().strftime("%d/%m/%Y")}**')
    delayed = get_delayed_items()
    st.divider()
    if not delayed:
        st.success('✅ ¡Excelente! No hay actividades atrasadas a la fecha. El proyecto va al día.')
    else:
        st.error(f'⚠️ Se detectaron **{len(delayed)} actividades atrasadas** que requieren atención.')
        # Resumen por fase
        st.markdown('### Resumen por fase')
        fase_counts = {}
        for d in delayed:
            fase_counts[d['fase']] = fase_counts.get(d['fase'], 0) + 1
        cols_f = st.columns(len(fase_counts))
        for i, (fk, cnt) in enumerate(fase_counts.items()):
            color = PHASES[fk]['color']
            with cols_f[i]:
                st.markdown(f'<div class="kcard" style="border-left-color:{color};text-align:center">'
                            f'<div style="font-weight:700">{fk}</div>'
                            f'<div style="font-size:1.8rem;font-weight:800;color:{color}">{cnt}</div>'
                            f'<div style="font-size:.8rem;color:#777">atrasada(s)</div></div>',
                            unsafe_allow_html=True)
        st.divider()
        # Filtros
        c1f, c2f = st.columns(2)
        f_fase = c1f.multiselect('Filtrar por fase:', list(PHASES.keys()), default=list(PHASES.keys()), key='al_fase')
        umbral = c2f.slider('Mostrar con mas de N dias de atraso:', 0, 90, 0, key='al_umbral')
        filtered = [d for d in delayed if d['fase'] in f_fase and d['days_late'] >= umbral]
        st.markdown(f'### Detalle ({len(filtered)} actividades)')
        for d in filtered:
            color = PHASES[d['fase']]['color']
            urgency = '🔴 Critico' if d['days_late'] > 14 else ('🟡 Moderado' if d['days_late'] > 7 else '🟢 Leve')
            st.markdown(
                f'<div class="alert-row" style="border-left-color:{color}">'
                f'<div style="display:flex;justify-content:space-between;align-items:center">'
                f'<span><b>{d["fase"]} &nbsp;|&nbsp; {d["id"]}</b> &mdash; {d["activity"]}</span>'
                f'<span class="late-badge">{d["days_late"]} días</span></div>'
                f'<div style="margin-top:4px;color:#555">'
                f'Ref: <code>{d["ref"]}</code> &nbsp;|&nbsp; '
                f'Plazo: <b>{d["deadline"]}</b> ({d["deadline_date"].strftime("%d/%m/%Y")}) &nbsp;|&nbsp; '
                f'Estado: <i>{d["status"]}</i> &nbsp;|&nbsp; '
                f'Responsable: {d["responsible"]} &nbsp;|&nbsp; {urgency}'
                f'</div></div>', unsafe_allow_html=True)
        st.divider()
        # Exportar
        df_late = pd.DataFrame([{
            'Fase': d['fase'], 'ID': d['id'], 'Actividad': d['activity'],
            'Ref NTC': d['ref'], 'Plazo': d['deadline'],
            'Fecha limite': d['deadline_date'].strftime('%d/%m/%Y'),
            'Dias de atraso': d['days_late'], 'Estado actual': d['status'],
            'Responsable': d['responsible']
        } for d in delayed])
        st.download_button('Descargar informe de atraso (CSV)',
            data=df_late.to_csv(index=False).encode(),
            file_name='SGI_Alertas_'+datetime.now().strftime('%Y%m%d')+'.csv',
            mime='text/csv', use_container_width=True)

# ============================================================
# REGISTRO DOCUMENTAL
# ============================================================
elif page == 'Registro Documental':
    extra_docs = get_extra_docs()
    extra_fmts = get_extra_fmts()
    n_docs = len(DOCUMENTS) + len(extra_docs)
    n_fmts = len(FORMATS) + len(extra_fmts)
    st.title('Registro Documental del SGI')
    st.markdown(f'**{n_docs} documentos base** y **{n_fmts} formatos operativos**  '
                f'*(incluye {len(extra_docs)} doc. y {len(extra_fmts)} form. adicionales)*')
    edit_codes = st.checkbox('Editar codigos SGC', value=False)
    st.divider()
    tab_labels = [f'Documentos Base ({n_docs})', f'Formatos ({n_fmts})', 'Agregar Documento', 'Agregar Formato']
    t1, t2, t3, t4 = st.tabs(tab_labels)

    def render_doc_list(tab, items_list, tid):
        with tab:
            pf = st.multiselect('Fase:', ['Fase 1','Fase 2','Fase 3','Fase 4'],
                                default=['Fase 1','Fase 2','Fase 3','Fase 4'], key='df_'+tid)
            hdr = st.columns([0.5,1.1,0.9,3.6,1.6,0.4])
            for col, lbl in zip(hdr, ['**Fase**','**Codigo**','**Ref.**','**Nombre**','**Estado**','']):
                col.markdown(lbl)
            st.markdown('<hr style="margin:4px 0">', unsafe_allow_html=True)
            for d in items_list:
                if d['phase'] not in pf: continue
                cur_s = get_doc_status(d['code'])
                cc    = get_custom_code(d['code'])
                color = PHASES[d['phase']]['color']
                tag   = '<span class="tag" style="background:'+color+'20;color:'+color+'">'+d['phase']+'</span>'
                extra_mark = ' <span class="extra-badge">+extra</span>' if d.get('extra') else ''
                row = st.columns([0.5,1.1,0.9,3.6,1.6,0.4])
                row[0].markdown(tag, unsafe_allow_html=True)
                if edit_codes:
                    nc = row[1].text_input('', value=cc, key='cedit_'+d['code'], label_visibility='collapsed')
                    if nc != cc: set_custom_code(d['code'], nc)
                else:
                    row[1].markdown(('**`'+cc+'`**' if cc != d['code'] else '`'+cc+'`'), unsafe_allow_html=True)
                row[2].markdown('<small>`'+d.get('chapter','-')+'`</small>', unsafe_allow_html=True)
                row[3].markdown(d['name']+extra_mark+'<br><small style="color:#999">'+d.get('type','-')+'</small>',
                                unsafe_allow_html=True)
                new_s = row[4].selectbox('', STATUS_OPTIONS, index=STATUS_OPTIONS.index(cur_s),
                                         key='dsel_'+d['code'], label_visibility='collapsed')
                if new_s != cur_s: set_doc_status(d['code'], new_s); st.rerun()
                if d.get('extra'):
                    if row[5].button('🗑', key='del_doc_'+d['code'], help='Eliminar documento adicional'):
                        remove_extra_doc(d['code']); st.rerun()
                else:
                    row[5].markdown('')
                st.markdown('<hr style="margin:3px 0;opacity:.18">', unsafe_allow_html=True)

    render_doc_list(t1, all_docs(), 'docs')
    with t2:
        pf2 = st.multiselect('Fase:', ['Fase 1','Fase 2','Fase 3','Fase 4'],
                             default=['Fase 1','Fase 2','Fase 3','Fase 4'], key='df_fmts')
        hdr2 = st.columns([0.5,1.1,3.8,1.6,0.4])
        for col, lbl in zip(hdr2, ['**Fase**','**Codigo**','**Nombre**','**Estado**','']):
            col.markdown(lbl)
        st.markdown('<hr style="margin:4px 0">', unsafe_allow_html=True)
        for d in all_fmts():
            if d['phase'] not in pf2: continue
            cur_s = get_doc_status(d['code'])
            cc    = get_custom_code(d['code'])
            color = PHASES[d['phase']]['color']
            tag   = '<span class="tag" style="background:'+color+'20;color:'+color+'">'+d['phase']+'</span>'
            extra_mark = ' <span class="extra-badge">+extra</span>' if d.get('extra') else ''
            row2 = st.columns([0.5,1.1,3.8,1.6,0.4])
            row2[0].markdown(tag, unsafe_allow_html=True)
            if edit_codes:
                nc2 = row2[1].text_input('', value=cc, key='cedit_'+d['code'], label_visibility='collapsed')
                if nc2 != cc: set_custom_code(d['code'], nc2)
            else:
                row2[1].markdown(('**`'+cc+'`**' if cc != d['code'] else '`'+cc+'`'), unsafe_allow_html=True)
            row2[2].markdown(d['name']+extra_mark, unsafe_allow_html=True)
            new_s2 = row2[3].selectbox('', STATUS_OPTIONS, index=STATUS_OPTIONS.index(cur_s),
                                       key='dsel_'+d['code'], label_visibility='collapsed')
            if new_s2 != cur_s: set_doc_status(d['code'], new_s2); st.rerun()
            if d.get('extra'):
                if row2[4].button('🗑', key='del_fmt_'+d['code'], help='Eliminar formato adicional'):
                    remove_extra_fmt(d['code']); st.rerun()
            else:
                row2[4].markdown('')
            st.markdown('<hr style="margin:3px 0;opacity:.18">', unsafe_allow_html=True)
    with t3:
        st.markdown('### Agregar documento adicional al SGI')
        st.caption('Los documentos agregados aquí se guardan en el JSON del sistema y se muestran '
                   'en la lista principal marcados con la etiqueta **+extra**.')
        st.divider()
        with st.form('form_add_doc', clear_on_submit=True):
            fa1, fa2 = st.columns(2)
            new_code  = fa1.text_input('Código del documento *', placeholder='Ej: DOC-46 o IIAD-PRC-001')
            new_phase = fa2.selectbox('Fase de implementación *', ['Fase 1','Fase 2','Fase 3','Fase 4'])
            new_name  = st.text_input('Nombre del documento *', placeholder='Ej: Protocolo gestión de muestras')
            fb1, fb2 = st.columns(2)
            new_chap  = fb1.text_input('Referencia normativa', placeholder='Ej: S7.5 / S8.1 / ISO17034-S5')
            new_type  = fb2.selectbox('Tipo de documento', DOC_TYPES)
            new_obs   = st.text_area('Justificación / Observación', height=70)
            submitted = st.form_submit_button('Agregar documento', type='primary', use_container_width=True)
            if submitted:
                code_clean = new_code.strip().upper()
                if not code_clean or not new_name.strip():
                    st.error('El código y el nombre son obligatorios.')
                elif code_exists(code_clean):
                    st.error(f'El código **{code_clean}** ya existe.')
                else:
                    add_extra_doc({'code':code_clean,'name':new_name.strip(),'phase':new_phase,
                                   'chapter':new_chap.strip(),'type':new_type,'obs':new_obs.strip(),
                                   'extra':True,'added':datetime.now().strftime('%Y-%m-%d %H:%M')})
                    st.success(f'✅ Documento **{code_clean}** agregado a {new_phase}.'); st.rerun()
    with t4:
        st.markdown('### Agregar formato operativo adicional')
        st.caption('Los formatos agregados aquí se guardan en el JSON del sistema.')
        st.divider()
        with st.form('form_add_fmt', clear_on_submit=True):
            fc1, fc2 = st.columns(2)
            new_fcode = fc1.text_input('Código del formato *', placeholder='Ej: FTO-31 o IIAD-FTO-001')
            new_fphase= fc2.selectbox('Fase de implementación *', ['Fase 1','Fase 2','Fase 3','Fase 4'])
            new_fname = st.text_input('Nombre del formato *', placeholder='Ej: Registro cadena de custodia')
            fd1, fd2 = st.columns(2)
            new_fchap = fd1.text_input('Referencia normativa', placeholder='Ej: S7.5 / ISO17043-S5')
            new_ftype = fd2.selectbox('Tipo', ['Formato','Plantilla','Registro','Acta','Ficha','Protocolo','Otro'])
            new_fobs  = st.text_area('Justificación / Observación', height=70)
            fsubmitted = st.form_submit_button('Agregar formato', type='primary', use_container_width=True)
            if fsubmitted:
                fcode_clean = new_fcode.strip().upper()
                if not fcode_clean or not new_fname.strip():
                    st.error('El código y el nombre son obligatorios.')
                elif code_exists(fcode_clean):
                    st.error(f'El código **{fcode_clean}** ya existe.')
                else:
                    add_extra_fmt({'code':fcode_clean,'name':new_fname.strip(),'phase':new_fphase,
                                   'chapter':new_fchap.strip(),'type':new_ftype,'obs':new_fobs.strip(),
                                   'extra':True,'added':datetime.now().strftime('%Y-%m-%d %H:%M')})
                    st.success(f'✅ Formato **{fcode_clean}** agregado a {new_fphase}.'); st.rerun()

# ============================================================
# REPORTES Y EXPORTAR
# ============================================================
elif page == 'Reportes y Exportar':
    st.title('Reportes de Avance'); st.divider()
    rows=[]
    for pk,ph in PHASES.items():
        for item in ph['items']:
            ist=get_istate(ikey(pk,item['id']))
            rows.append({'Fase':pk,'ID':item['id'],'Actividad':item['activity'],
                         'Ref. NTC':item['ref'],'Plazo':item['deadline'],
                         'Responsable':ist['responsable_nombre'],'Estado':ist['status'],'Comentario':ist['comentario']})
    df=pd.DataFrame(rows)
    st.markdown('### Resumen por Fase')
    summary=[]
    for pk in PHASES:
        total,done,wip,na,pct=phase_progress(pk)
        n_late_f = sum(1 for d in get_delayed_items() if d['fase']==pk)
        summary.append({'Fase':pk+': '+PHASES[pk]['name'],'Total':total,'Completas':done,
                         'En proceso':wip,'Pendientes':total-done-wip-na,'N/A':na,
                         '% Avance':str(pct)+'%','Atrasadas':n_late_f})
    st.dataframe(pd.DataFrame(summary),use_container_width=True,hide_index=True)
    st.divider()
    dfp=df[df['Estado'].isin(['En proceso','Pendiente'])]
    st.markdown('### Pendientes / En proceso ('+str(len(dfp))+')')
    if dfp.empty: st.success('Todas completadas.')
    else: st.dataframe(dfp,use_container_width=True,hide_index=True)
    st.divider()
    doc_rows = []
    for d in all_docs():
        doc_rows.append({'Tipo':'Documento','Cod. Original':d['code'],'Cod. SGC':get_custom_code(d['code']),
                         'Nombre':d['name'],'Fase':d['phase'],'Ref. Normativa':d.get('chapter','-'),
                         'Tipo doc':d.get('type','-'),'Estado':get_doc_status(d['code']),
                         'Extra':'Si' if d.get('extra') else 'No','Observacion':d.get('obs','')})
    for d in all_fmts():
        doc_rows.append({'Tipo':'Formato','Cod. Original':d['code'],'Cod. SGC':get_custom_code(d['code']),
                         'Nombre':d['name'],'Fase':d['phase'],'Ref. Normativa':d.get('chapter','-'),
                         'Tipo doc':d.get('type','-'),'Estado':get_doc_status(d['code']),
                         'Extra':'Si' if d.get('extra') else 'No','Observacion':d.get('obs','')})
    df_docs = pd.DataFrame(doc_rows)
    c1e, c2e = st.columns(2)
    with c1e:
        st.download_button('Descargar CSV Actividades',
            data=df.to_csv(index=False).encode(),
            file_name='SGI_Actividades_'+datetime.now().strftime('%Y%m%d')+'.csv',
            mime='text/csv', use_container_width=True)
    with c2e:
        st.download_button('Descargar CSV Documentos',
            data=df_docs.to_csv(index=False).encode(),
            file_name='SGI_Documentos_'+datetime.now().strftime('%Y%m%d')+'.csv',
            mime='text/csv', use_container_width=True)

# ============================================================
# CONFIGURACION
# ============================================================
elif page == 'Configuracion':
    st.title('Configuración del Proyecto')
    st.divider()

    # Cargar config actual desde session_state
    config = st.session_state.get("estado", {}).get("_config", DEFAULT_CONFIG)

    st.subheader("📅 Parámetros Generales")

    col1, col2 = st.columns(2)

    with col1:
        fecha_actual = (
            datetime.strptime(config["fecha_inicio_proyecto"], "%Y-%m-%d").date()
            if config.get("fecha_inicio_proyecto")
            else datetime.today().date()
        )
        nueva_fecha = st.date_input(
            "Fecha de inicio del proyecto",
            value=fecha_actual,
            help="Fecha oficial de inicio del SG-IDI"
        )

    with col2:
        nuevo_responsable = st.text_input(
            "Responsable principal",
            value=config.get("responsable_principal", ""),
            help="Nombre del líder del proyecto"
        )

    st.divider()

    if st.button("💾 Guardar configuración", type="primary"):
        # Actualizar en session_state
        st.session_state["estado"]["_config"]["fecha_inicio_proyecto"] = str(nueva_fecha)
        st.session_state["estado"]["_config"]["responsable_principal"] = nuevo_responsable

        # Persistir en el JSON
        guardar_estado(st.session_state["estado"])
        st.success("✅ Configuración guardada correctamente.")
        st.rerun()

    # Vista previa de los valores guardados
    st.subheader("📋 Valores actuales")
    st.json(st.session_state["estado"]["_config"])
