from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


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

    # ========== VALIDACIONES SQL ==========
    _sql_constraints = [
        ('contenido_no_vacio', 'CHECK(contenido IS NOT NULL AND contenido != """")',
         'El contenido del comentario no puede estar vacío'),
    ]

    # ========== VALIDACIONES PYTHON ==========
    @api.constrains('contenido')
    def _check_contenido(self):
        for record in self:
            contenido_limpio = record.contenido.strip()
            if len(contenido_limpio) < 3:
                raise ValidationError(_('El comentario debe tener al menos 3 caracteres'))
            if len(contenido_limpio) > 500:
                raise ValidationError(_('El comentario no puede exceder 500 caracteres'))

    @api.constrains('incidencia_id', 'empleado_id')
    def _check_empleado_puede_comentar(self):
        for record in self:
            if record.incidencia_id and record.empleado_id:
                # Solo empleados del mismo departamento pueden comentar
                if record.empleado_id.department_id != record.incidencia_id.departamento_id:
                    raise ValidationError(
                        _('Solo empleados del departamento %s pueden comentar en esta incidencia') %
                        record.incidencia_id.departamento_id.name
                    )

    @api.constrains('fecha')
    def _check_fecha_comentario(self):
        for record in self:
            if record.fecha > fields.Datetime.now():
                raise ValidationError(_('La fecha del comentario no puede ser futura'))
            if record.incidencia_id and record.fecha < record.incidencia_id.fecha_creacion:
                raise ValidationError(
                    _('El comentario no puede ser anterior a la creación de la incidencia')
                )

    # ========== SOBRECARGA DE MÉTODOS ==========
    @api.model
    def create(self, vals):
        # Validación antes de crear
        if 'contenido' in vals:
            contenido_limpio = vals['contenido'].strip()
            if len(contenido_limpio) < 3:
                raise ValidationError(_('El comentario debe tener al menos 3 caracteres'))
            vals['contenido'] = contenido_limpio

        # Establecer fecha si no viene
        if 'fecha' not in vals:
            vals['fecha'] = fields.Datetime.now()

        # Validar que la incidencia existe y no está cerrada
        if 'incidencia_id' in vals:
            incidencia = self.env['incidencias.incidencia'].browse(vals['incidencia_id'])
            if incidencia.estado_actual == 'cerrada':
                raise ValidationError(
                    _('No se pueden añadir comentarios a incidencias cerradas')
                )

        # Registrar quien crea el comentario
        vals['creado_por'] = self.env.uid

        # Llamar al método original
        result = super(Comentario, self).create(vals)

        # Notificar creación de comentario - CORREGIDO PARA Odoo 16
        result.incidencia_id.message_post(
            body=_('Nuevo comentario: %s') % result.contenido[:100],
            subject=_('Comentario añadido'),
            subtype_xmlid='mail.mt_comment'  # ← CAMBIADO a subtype_xmlid
        )

        return result

    def write(self, vals):
        # No permitir modificar comentarios después de 1 hora
        for record in self:
            tiempo_transcurrido = fields.Datetime.now() - record.fecha
            if tiempo_transcurrido.total_seconds() > 3600:  # 1 hora
                raise ValidationError(
                    _('No se pueden modificar comentarios después de 1 hora')
                )

        # Validar contenido si se modifica
        if 'contenido' in vals:
            contenido_limpio = vals['contenido'].strip()
            if len(contenido_limpio) < 3:
                raise ValidationError(_('El comentario debe tener al menos 3 caracteres'))
            vals['contenido'] = contenido_limpio

        # Registrar modificación
        vals['modificado_por'] = self.env.uid
        vals['fecha_modificacion'] = fields.Datetime.now()

        return super(Comentario, self).write(vals)

    def unlink(self):
        # Validar antes de eliminar
        for record in self:
            tiempo_transcurrido = fields.Datetime.now() - record.fecha
            if tiempo_transcurrido.total_seconds() > 3600:  # 1 hora
                raise ValidationError(
                    _('No se pueden eliminar comentarios después de 1 hora')
                )

            # Solo el creador puede eliminar
            if record.creado_por != self.env.user:
                raise ValidationError(
                    _('Solo el creador del comentario puede eliminarlo')
                )

        return super(Comentario, self).unlink()

    # En Comentario.py, añade este método para el botón
    def save_comment(self):
        """Método para el botón Guardar en comentarios"""
        # Odoo guarda automáticamente, pero el método debe existir
        return True

    # ========== CAMPOS ADICIONALES PARA SEGUIMIENTO ==========
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
