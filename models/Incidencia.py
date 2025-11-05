from odoo import fields, models


class Incidencia(models.Model):
    _name = "incidencias.incidencia"
    _description = "Guarda las incidencias"

    # Campos simples
    titulo = fields.Char(string="Título", required=True)
    descripcion = fields.Char(string="Descripción")
    fecha_creacion = fields.Datetime(string="Fecha de creación", default=fields.Datetime.now)
    estado_actual = fields.Selection([
        ('abierta', 'Abierta'),
        ('en_progreso', 'En Progreso'),
        ('resuelta', 'Resuelta'),
        ('cerrada', 'Cerrada')
    ], string='Estado Actual', default='abierta')

    # Relaciones N-1
    departamento_id = fields.Many2one(
        comodel_name="hr.department",
        string="Departamento",
        required=True,
        ondelete="cascade"
    )

    empleado_origen_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Empleado Origen",
        required=True,
        ondelete="cascade"
    )

    # Relaciones 1-N (correctas)
    comentario_ids = fields.One2many(
        comodel_name='incidencias.comentario',
        inverse_name='incidencia_id',
        string='Comentarios'
    )

    encuesta_ids = fields.One2many(
        comodel_name='incidencias.encuesta',
        inverse_name='incidencia_id',
        string='Encuestas'
    )