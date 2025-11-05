from odoo import fields, models

class Estadisticas(models.Model):
    _name = "incidencias.estadisticas"
    _description = "Guarda las estadísticas de las incidencias"

    # Campos simples
    fecha = fields.Date(string="Fecha",default=fields.Date.context_today,required=True)
    total_incidencias = fields.Integer(string="Total de Incidencias",required=True )
    incidencias_finalizadas = fields.Integer( string="Incidencias Finalizadas",required=True)
    tiempo_promedio_resolucion = fields.Float(string="Tiempo Promedio de Resolución (horas)")