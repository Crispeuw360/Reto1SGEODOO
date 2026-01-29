from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class Incidencia(models.Model):
    _name = "incidencias.incidencia"
    _description = "Guarda las incidencias"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # =====================
    # CAMPOS
    # =====================
    titulo = fields.Char(string="Título", required=True, tracking=True)
    descripcion = fields.Text(string="Descripción")
    fecha_creacion = fields.Datetime(
        string="Fecha de creación",
        default=fields.Datetime.now,
        readonly=True
    )

    estado_actual = fields.Selection(
        [
            ('abierta', 'Abierta'),
            ('en_progreso', 'En Progreso'),
            ('resuelta', 'Resuelta'),
            ('cerrada', 'Cerrada')
        ],
        string='Estado Actual',
        default='abierta',
        tracking=True
    )

    proyecto = fields.Many2one(comodel_name= "project.task", string="Tarea de Proyecto", required = False, ondelete="cascade")

    departamento_id = fields.Many2one(
        'hr.department',
        string="Departamento",
        required=True,
        ondelete="restrict"
    )

    empleado_origen_id = fields.Many2one(
        'hr.employee',
        string="Empleado Origen",
        required=True,
        ondelete="restrict"
    )

    comentario_ids = fields.One2many(
        'incidencias.comentario',
        'incidencia_id',
        string='Comentarios'
    )

    encuesta_ids = fields.One2many(
        'incidencias.encuesta',
        'incidencia_id',
        string='Encuestas'
    )

    creado_por = fields.Many2one(
        'res.users',
        string='Creado por',
        default=lambda self: self.env.user,
        readonly=True
    )

    modificado_por = fields.Many2one(
        'res.users',
        string='Modificado por',
        readonly=True
    )

    fecha_modificacion = fields.Datetime(
        string='Última modificación',
        readonly=True
    )

    total_comentarios = fields.Integer(
        compute='_compute_totales',
        store=True
    )

    ultimo_comentario = fields.Datetime(
        compute='_compute_totales',
        store=True
    )

    # =====================
    # COMPUTADOS
    # =====================
    @api.depends('comentario_ids', 'comentario_ids.fecha')
    def _compute_totales(self):
        for record in self:
            record.total_comentarios = len(record.comentario_ids)
            record.ultimo_comentario = (
                max(record.comentario_ids.mapped('fecha'))
                if record.comentario_ids else False
            )

    # =====================
    # BOTONES (ACCIONES)
    # =====================
    def set_en_progreso(self):
        self._validar_cambio_estado('en_progreso')
        self.write({'estado_actual': 'en_progreso'})

    def set_resuelta(self):
        self._validar_cambio_estado('resuelta')
        self.write({'estado_actual': 'resuelta'})

    def set_cerrada(self):
        self._validar_cambio_estado('cerrada')
        self.write({'estado_actual': 'cerrada'})

    def reabrir(self):
        self._validar_cambio_estado('abierta')
        self.write({'estado_actual': 'abierta'})

    # =====================
    # VALIDACIONES
    # =====================
    _sql_constraints = [
        ('titulo_unico', 'unique(titulo)', 'El título debe ser único.')
    ]

    @api.constrains('titulo')
    def _check_titulo(self):
        for record in self:
            if record.titulo and not 5 <= len(record.titulo) <= 100:
                raise ValidationError(
                    _('El título debe tener entre 5 y 100 caracteres')
                )

    @api.constrains('departamento_id', 'empleado_origen_id')
    def _check_departamento_empleado(self):
        for record in self:
            if record.empleado_origen_id.department_id != record.departamento_id:
                raise ValidationError(
                    _('El empleado no pertenece al departamento seleccionado')
                )

    # =====================
    # WRITE / CREATE
    # =====================
    def write(self, vals):
        if 'estado_actual' in vals:
            self._validar_cambio_estado(vals['estado_actual'])

        vals['modificado_por'] = self.env.user.id
        vals['fecha_modificacion'] = fields.Datetime.now()

        return super().write(vals)

    # =====================
    # METODO PRIVADO
    # =====================
    def _validar_cambio_estado(self, nuevo_estado):
        reglas = {
            'abierta': ['en_progreso'],
            'en_progreso': ['resuelta', 'abierta'],
            'resuelta': ['cerrada', 'en_progreso'],
            'cerrada': ['abierta'],
        }

        for record in self:
            permitido = reglas.get(record.estado_actual, [])
            if nuevo_estado not in permitido:
                raise ValidationError(
                    _('No se puede pasar de %s a %s')
                    % (record.estado_actual, nuevo_estado)
                )
