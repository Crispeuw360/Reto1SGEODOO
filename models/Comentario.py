from pkg_resources import require

from odoo import fields,models
from odoo.api import ondelete


class Comentario(models.Model):
    _name = "incidencias.comentario"
    _description = "guarda los comentarios"

    #campos simples
    contenido = fields.Char(str="Introduce el contenido", required = True)
    fecha = fields.Datetime(str="Introduce la fecha", required=True)

    #campor relacionales(foranea)
    #id_incidencia = fields.Integer(comodel_name="Incidencias.incidencia",str="incidencia",require=True,ondelete="cascade",onupdate="cascade")
    id_empleado = fields.Integer(comodel_name="hr.employee",str="empleado",require=True,ondelete="cascade")