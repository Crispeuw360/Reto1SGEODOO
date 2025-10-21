# -*- coding: utf-8 -*-
from odoo import fields, models

class Encuesta(models.Model):
    _name = 'incidencias.encuesta'
    _description = 'Guarda las encuestas realizadas por los empleados'

    # Campos simples
    puntuacion = fields.Integer(string="Puntuación", required=True)
    comentario = fields.Text(string="Comentario")
    fecha_respuesta = fields.Datetime(string="Fecha de Respuesta", default=fields.Datetime.now)

    # Relaciones
    id_incidencia = fields.One2many(
        comodel_name='incidencias.incidencia',
        inverse_name='encuesta_id',
        string='Incidencia asociada'
    )

    id_empleado = fields.Many2one(
        comodel_name='hr.employee',
        string='Empleado que responde',
        required=True,
        ondelete='cascade',
        help='Empleado que completa la encuesta'
    )
