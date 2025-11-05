from odoo import fields, models

class IncidenciaTecnica(models.Model):
    _name = 'incidencias.tecnica'
    _inherit = 'incidencias.incidencia'  # Hereda de IncidenciaBase
    _description = 'Incidencia técnica especializada'

    # Campos adicionales específicos para incidencias técnicas
    tipo_equipo = fields.Selection([
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('red', 'Red')
    ], string="Tipo de equipo")
    prioridad = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica')
    ], string="Prioridad", default='media')

    # Many2many con usuarios (modelo existente de Odoo)
    tecnicos_asignados = fields.Many2many(
        comodel_name='res.users',
        string='Técnicos asignados',
        help='Técnicos responsables de esta incidencia'
    )