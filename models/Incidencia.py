from pkg_resources import require

from odoo import fields,models
from odoo.api import ondelete


class Incidencia(models.Model):
    _name = "incidencias.incidencia"
    _description = "guarda las incidencias"

    #campos simples
    titulo = fields.Char(str="Introduce el titulo", required = True)
    descripcion = fields.Char(str="Introduce una descripcion")
    fecha_creacion = fields.Datetime(str="Introduce la fecha", required=True)
    estado_actual =  fields.Boolean(str="True = resuelto, False = sin Resolver", required = True)

    #campor relacionales(foranea)
    id_departamento = fields.Integer(comodel_name="hr.department",str="departamento",require=True,ondelete="cascade",)
    id_empleado = fields.Integer(comodel_name="hr.employee",str="empleado",require=True,ondelete="cascade",)