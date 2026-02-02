# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Encuesta(models.Model):
    _name = 'incidencias.encuesta'
    _description = 'Guarda las encuestas realizadas por los empleados'

    # Campos simples
    titulo = fields.Char(string="Título de la encuesta", required=True)
    puntuacion = fields.Integer(string="Puntuación", required=True)
    comentario = fields.Text(string="Comentario")
    fecha_respuesta = fields.Datetime(
        string="Fecha de Respuesta",
        default=fields.Datetime.now
    )

    # Relaciones
    incidencia_id = fields.Many2one(
        comodel_name='incidencias.incidencia',
        string='Incidencia asociada',
        ondelete='cascade'
    )

    empleado_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Empleado que responde',
        required=True,
        ondelete='cascade'
    )

    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('enviada', 'Enviada'),
        ('validada', 'Validada'),
    ], string="Estado", default='borrador', required=True)

    usuario_creador = fields.Many2one(
        'res.users',
        string="Creada por",
        readonly=True
    )

    @api.model
    def create(self, vals):
        # Forzamos usuario creador
        if not vals.get('usuario_creador'):
            vals['usuario_creador'] = self.env.user.id

        # Forzamos estado inicial
        vals['estado'] = 'borrador'

        return super(Encuesta, self).create(vals)

    # ====== VALIDACIÓN ======
    @api.constrains('puntuacion')
    def _check_puntuacion_rango(self):
        for rec in self:
            if rec.puntuacion is None:
                continue
            if rec.puntuacion < 0 or rec.puntuacion > 10:
                raise ValidationError("La puntuación debe estar entre 0 y 10.")

    # == RESTRICCIÓN DE EDICIÓN ==
    def write(self, vals):
        # Admin técnico puede editar siempre
        if self.env.user.has_group('base.group_system'):
            return super().write(vals)

        solo_cambia_estado = set(vals.keys()).issubset({'estado'})
        if not solo_cambia_estado:
            for rec in self:
                if rec.estado == 'validada':
                    raise ValidationError(
                        "No puedes modificar una encuesta que ya está VALIDADA."
                    )

        return super().write(vals)

    def action_enviar(self):
        for rec in self:
            rec.write({'estado': 'enviada'})

    def action_validar(self):
        for rec in self:
            rec.write({'estado': 'validada'})

    def action_volver_borrador(self):
        for rec in self:
            rec.write({'estado': 'borrador'})
