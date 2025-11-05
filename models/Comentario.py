from odoo import fields, models


class Comentario(models.Model):
    _name = "incidencias.comentario"
    _description = "Guarda los comentarios"

    # Campos simples
    contenido = fields.Char(string="Contenido", required=True)
    fecha = fields.Datetime(string="Fecha", default=fields.Datetime.now)

    # Relaciones N-1
    incidencia_id = fields.Many2one(
        comodel_name='incidencias.incidencia',
        string='Incidencia',
        required=True,
        ondelete="cascade"
    )

    empleado_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Empleado',
        required=True,
        ondelete="cascade"
    )