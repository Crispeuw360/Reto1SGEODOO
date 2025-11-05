# -*- coding: utf-8 -*-
from odoo import fields, models

class Encuesta(models.Model):
    _name = 'incidencias.encuesta'
    _description = 'Guarda las encuestas realizadas por los empleados'

    # Campos simples
    titulo = fields.Char(string="Título de la encuesta", required=True)
    puntuacion = fields.Integer(string="Puntuación", required=True)
    comentario = fields.Text(string="Comentario")
    fecha_respuesta = fields.Datetime(string="Fecha de Respuesta", default=fields.Datetime.now)

    # Relaciones - CAMBIO IMPORTANTE: Usa Many2one en lugar de One2many
    incidencia_id = fields.Many2one(
        comodel_name='incidencias.incidencia',
        string='Incidencia asociada',
        ondelete='cascade'
    )

    empleado_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Empleado que responde',
        required=True,
        ondelete='cascade',
        help='Empleado que completa la encuesta'
    )