from pkg_resources import require

from odoo import fields,models
from odoo.api import ondelete


class Comentario(models.Model):
    _name = "incidencias.comentario"
    _description = "Guarda los comentarios"

    # Campos simples
    contenido = fields.Char(string="Introduce el contenido", required=True)
    fecha = fields.Datetime(string="Introduce la fecha", required=True, default=fields.Datetime.now)

    # Relaciones N-1
    incidencia_id = fields.Many2one(
        comodel_name='incidencias.incidencia',
        string='Incidencia',
        required=True,
        ondelete="cascade",
        help="Id de la Incidencia"
    )
    empleado_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Empleado',
        required=True,
        ondelete="cascade",
        help="Id del empleado"
    )