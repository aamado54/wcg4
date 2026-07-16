from django.conf import settings
from django.db import models
from core.models import TimeStampedModel, UNE


class UserProfile(TimeStampedModel):
    ROLE_ADMIN = 'ADMIN'
    ROLE_GERENCIA = 'GERENCIA'
    ROLE_USUARIO = 'USUARIO'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Administrador'),
        (ROLE_GERENCIA, 'Gerencia'),
        (ROLE_USUARIO, 'Usuario'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    display_name = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    role_label = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USUARIO)
    default_all_une_access = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'

    def __str__(self):
        return self.display_name or self.user.get_full_name() or self.user.username


class UserUNEPermission(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='une_permissions'
    )
    une = models.ForeignKey(
        UNE,
        on_delete=models.CASCADE,
        related_name='user_permissions'
    )
    can_view_summary = models.BooleanField(default=False)
    can_view_detail = models.BooleanField(default=False)
    granted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='granted_une_permissions'
    )
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'une')
        verbose_name = 'Permiso por UNE'
        verbose_name_plural = 'Permisos por UNE'
        ordering = ['user__username', 'une__sort_order']

    def __str__(self):
        return f'{self.user.username} - {self.une.code}'