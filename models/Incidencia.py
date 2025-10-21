from odoo import fields, models

class Incidencia(models.Model):
    _name = "incidencias.incidencia"
    _description = "Guarda las incidencias"

    # Campos simples
    titulo = fields.Char(string="Introduce el título", required=True)
    descripcion = fields.Char(string="Introduce una descripción")
    fecha_creacion = fields.Datetime(string="Fecha de creación", default=fields.Datetime.now)
    estado_actual = fields.Selection([
        ('abierta', 'Abierta'),
        ('en_progreso', 'En Progreso'),
        ('resuelta', 'Resuelta'),
        ('cerrada', 'Cerrada')
    ], string='Estado Actual', default='abierta')

    # Relaciones N-1
    id_departamento = fields.Many2one(
        comodel_name="hr.department",
        string="Departamento",
        required=True,  # ✅ CORREGIDO: required (no require)
        ondelete="cascade",
        help="Departamento asociado a la incidencia"
    )
    empleado_origen_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Empleado Origen",
        required=True,  # ✅ CORREGIDO: required (no require)
        ondelete="cascade",
        help="Empleado que creó la incidencia"
    )

    # Relaciones 1-N
    comentario_ids = fields.One2many(
        comodel_name='incidencias.comentario',  # ✅ CORREGIDO: nombre completo
        inverse_name='incidencia_id',
        string='Comentarios',
        help="Comentarios de la incidencia"
    )

    encuesta_id = fields.Many2one(
        comodel_name='incidencias.encuesta',
        string='Encuestas asociadas',
        unique=True,
        ondelete='set null'
    )
