# CONCATENATED .PY FILES

PART_NUMBER=1
TOTAL_PARTS=10

DOCUMENT_MODE=LITERAL_CODE_ARCHIVE
PARSING_PRIORITY=PATH_LITERAL->CONTENT_NUMBERED_BEGIN->CONTENT_BASE64_BEGIN->CONTENT_BEGIN
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
RECORD_SEPARATOR=BEGIN_LITERAL_FILE_RECORD|END_LITERAL_FILE_RECORD
RECORD_BOUNDARY=========== RECORD_BOUNDARY ==========
CONTENT_POLICY=PRESERVE_EXACT_TEXT_WITH_METADATA_AND_NUMBERED_FALLBACK
READING_HINT=Prefer PATH_LITERAL first for file identity. Prefer CONTENT_NUMBERED_BEGIN for faithful line-by-line reading. Use CONTENT_BASE64_BEGIN for exact reconstruction when available. Use CONTENT_BEGIN only as a convenience view. If CONTENT_BEGIN looks compacted, flattened, or visually altered, do not use it to infer exact identifiers, variable names, paths, punctuation grouping, or spacing.
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=accounts/__init__.py
PATH_JSON="accounts/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=accounts/admin.py
PATH_JSON="accounts/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=17
SIZE_BYTES_UTF8=717
CONTENT_SHA256=0f0798c127467778373c6527f2fbdfec527a677bb52d91744db4b3708e131a04
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.contrib import admin
from .models import UserProfile, UserUNEPermission


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'role_label', 'default_all_une_access')
    list_filter = ('role_label', 'default_all_une_access')
    search_fields = ('user__username', 'user__email', 'display_name', 'job_title')


@admin.register(UserUNEPermission)
class UserUNEPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'une', 'can_view_summary', 'can_view_detail', 'granted_by', 'granted_at')
    list_filter = ('une', 'can_view_summary', 'can_view_detail')
    search_fields = ('user__username', 'user__email', 'une__code', 'une__name_es')
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import admin
00002|from .models import UserProfile, UserUNEPermission
00003|
00004|
00005|@admin.register(UserProfile)
00006|class UserProfileAdmin(admin.ModelAdmin):
00007|    list_display = ('user', 'display_name', 'role_label', 'default_all_une_access')
00008|    list_filter = ('role_label', 'default_all_une_access')
00009|    search_fields = ('user__username', 'user__email', 'display_name', 'job_title')
00010|
00011|
00012|@admin.register(UserUNEPermission)
00013|class UserUNEPermissionAdmin(admin.ModelAdmin):
00014|    list_display = ('user', 'une', 'can_view_summary', 'can_view_detail', 'granted_by', 'granted_at')
00015|    list_filter = ('une', 'can_view_summary', 'can_view_detail')
00016|    search_fields = ('user__username', 'user__email', 'une__code', 'une__name_es')
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgYWRtaW4KZnJvbSAubW9kZWxzIGltcG9ydCBVc2VyUHJvZmlsZSwgVXNlclVORVBlcm1pc3Npb24KCgpAYWRtaW4ucmVnaXN0ZXIoVXNlclByb2ZpbGUpCmNsYXNzIFVzZXJQcm9maWxlQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoJ3VzZXInLCAnZGlzcGxheV9uYW1lJywgJ3JvbGVfbGFiZWwnLCAnZGVmYXVsdF9hbGxfdW5lX2FjY2VzcycpCiAgICBsaXN0X2ZpbHRlciA9ICgncm9sZV9sYWJlbCcsICdkZWZhdWx0X2FsbF91bmVfYWNjZXNzJykKICAgIHNlYXJjaF9maWVsZHMgPSAoJ3VzZXJfX3VzZXJuYW1lJywgJ3VzZXJfX2VtYWlsJywgJ2Rpc3BsYXlfbmFtZScsICdqb2JfdGl0bGUnKQoKCkBhZG1pbi5yZWdpc3RlcihVc2VyVU5FUGVybWlzc2lvbikKY2xhc3MgVXNlclVORVBlcm1pc3Npb25BZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgndXNlcicsICd1bmUnLCAnY2FuX3ZpZXdfc3VtbWFyeScsICdjYW5fdmlld19kZXRhaWwnLCAnZ3JhbnRlZF9ieScsICdncmFudGVkX2F0JykKICAgIGxpc3RfZmlsdGVyID0gKCd1bmUnLCAnY2FuX3ZpZXdfc3VtbWFyeScsICdjYW5fdmlld19kZXRhaWwnKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgndXNlcl9fdXNlcm5hbWUnLCAndXNlcl9fZW1haWwnLCAndW5lX19jb2RlJywgJ3VuZV9fbmFtZV9lcycp
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=accounts/apps.py
PATH_JSON="accounts/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=10
SIZE_BYTES_UTF8=209
CONTENT_SHA256=2fd6deff85e18045b594851f987996cdd0a350c287f00a6e02cb05a9e61313f1
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals  # noqa
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class AccountsConfig(AppConfig):
00005|    default_auto_field = 'django.db.models.BigAutoField'
00006|    name = 'accounts'
00007|
00008|    def ready(self):
00009|        import accounts.signals  # noqa
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgQWNjb3VudHNDb25maWcoQXBwQ29uZmlnKToKICAgIGRlZmF1bHRfYXV0b19maWVsZCA9ICdkamFuZ28uZGIubW9kZWxzLkJpZ0F1dG9GaWVsZCcKICAgIG5hbWUgPSAnYWNjb3VudHMnCgogICAgZGVmIHJlYWR5KHNlbGYpOgogICAgICAgIGltcG9ydCBhY2NvdW50cy5zaWduYWxzICAjIG5vcWE=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=accounts/models.py
PATH_JSON="accounts/models.py"
FILENAME=models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=66
SIZE_BYTES_UTF8=2018
CONTENT_SHA256=005827922a6b83a376fcc5d6377b0c133cd2a2f6f8eb125553f776f3fdaf575e
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
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
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.conf import settings
00002|from django.db import models
00003|from core.models import TimeStampedModel, UNE
00004|
00005|
00006|class UserProfile(TimeStampedModel):
00007|    ROLE_ADMIN = 'ADMIN'
00008|    ROLE_GERENCIA = 'GERENCIA'
00009|    ROLE_USUARIO = 'USUARIO'
00010|
00011|    ROLE_CHOICES = [
00012|        (ROLE_ADMIN, 'Administrador'),
00013|        (ROLE_GERENCIA, 'Gerencia'),
00014|        (ROLE_USUARIO, 'Usuario'),
00015|    ]
00016|
00017|    user = models.OneToOneField(
00018|        settings.AUTH_USER_MODEL,
00019|        on_delete=models.CASCADE,
00020|        related_name='profile'
00021|    )
00022|    display_name = models.CharField(max_length=255, blank=True)
00023|    job_title = models.CharField(max_length=255, blank=True)
00024|    role_label = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USUARIO)
00025|    default_all_une_access = models.BooleanField(default=False)
00026|    notes = models.TextField(blank=True)
00027|
00028|    class Meta:
00029|        verbose_name = 'Perfil de usuario'
00030|        verbose_name_plural = 'Perfiles de usuario'
00031|
00032|    def __str__(self):
00033|        return self.display_name or self.user.get_full_name() or self.user.username
00034|
00035|
00036|class UserUNEPermission(TimeStampedModel):
00037|    user = models.ForeignKey(
00038|        settings.AUTH_USER_MODEL,
00039|        on_delete=models.CASCADE,
00040|        related_name='une_permissions'
00041|    )
00042|    une = models.ForeignKey(
00043|        UNE,
00044|        on_delete=models.CASCADE,
00045|        related_name='user_permissions'
00046|    )
00047|    can_view_summary = models.BooleanField(default=False)
00048|    can_view_detail = models.BooleanField(default=False)
00049|    granted_by = models.ForeignKey(
00050|        settings.AUTH_USER_MODEL,
00051|        on_delete=models.SET_NULL,
00052|        null=True,
00053|        blank=True,
00054|        related_name='granted_une_permissions'
00055|    )
00056|    granted_at = models.DateTimeField(auto_now_add=True)
00057|
00058|    class Meta:
00059|        unique_together = ('user', 'une')
00060|        verbose_name = 'Permiso por UNE'
00061|        verbose_name_plural = 'Permisos por UNE'
00062|        ordering = ['user__username', 'une__sort_order']
00063|
00064|    def __str__(self):
00065|        return f'{self.user.username} - {self.une.code}'
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29uZiBpbXBvcnQgc2V0dGluZ3MKZnJvbSBkamFuZ28uZGIgaW1wb3J0IG1vZGVscwpmcm9tIGNvcmUubW9kZWxzIGltcG9ydCBUaW1lU3RhbXBlZE1vZGVsLCBVTkUKCgpjbGFzcyBVc2VyUHJvZmlsZShUaW1lU3RhbXBlZE1vZGVsKToKICAgIFJPTEVfQURNSU4gPSAnQURNSU4nCiAgICBST0xFX0dFUkVOQ0lBID0gJ0dFUkVOQ0lBJwogICAgUk9MRV9VU1VBUklPID0gJ1VTVUFSSU8nCgogICAgUk9MRV9DSE9JQ0VTID0gWwogICAgICAgIChST0xFX0FETUlOLCAnQWRtaW5pc3RyYWRvcicpLAogICAgICAgIChST0xFX0dFUkVOQ0lBLCAnR2VyZW5jaWEnKSwKICAgICAgICAoUk9MRV9VU1VBUklPLCAnVXN1YXJpbycpLAogICAgXQoKICAgIHVzZXIgPSBtb2RlbHMuT25lVG9PbmVGaWVsZCgKICAgICAgICBzZXR0aW5ncy5BVVRIX1VTRVJfTU9ERUwsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0ncHJvZmlsZScKICAgICkKICAgIGRpc3BsYXlfbmFtZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUsIGJsYW5rPVRydWUpCiAgICBqb2JfdGl0bGUgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjU1LCBibGFuaz1UcnVlKQogICAgcm9sZV9sYWJlbCA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yMCwgY2hvaWNlcz1ST0xFX0NIT0lDRVMsIGRlZmF1bHQ9Uk9MRV9VU1VBUklPKQogICAgZGVmYXVsdF9hbGxfdW5lX2FjY2VzcyA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1GYWxzZSkKICAgIG5vdGVzID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgdmVyYm9zZV9uYW1lID0gJ1BlcmZpbCBkZSB1c3VhcmlvJwogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAnUGVyZmlsZXMgZGUgdXN1YXJpbycKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gc2VsZi5kaXNwbGF5X25hbWUgb3Igc2VsZi51c2VyLmdldF9mdWxsX25hbWUoKSBvciBzZWxmLnVzZXIudXNlcm5hbWUKCgpjbGFzcyBVc2VyVU5FUGVybWlzc2lvbihUaW1lU3RhbXBlZE1vZGVsKToKICAgIHVzZXIgPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICBzZXR0aW5ncy5BVVRIX1VTRVJfTU9ERUwsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0ndW5lX3Blcm1pc3Npb25zJwogICAgKQogICAgdW5lID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgVU5FLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwKICAgICAgICByZWxhdGVkX25hbWU9J3VzZXJfcGVybWlzc2lvbnMnCiAgICApCiAgICBjYW5fdmlld19zdW1tYXJ5ID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PUZhbHNlKQogICAgY2FuX3ZpZXdfZGV0YWlsID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PUZhbHNlKQogICAgZ3JhbnRlZF9ieSA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIHNldHRpbmdzLkFVVEhfVVNFUl9NT0RFTCwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0nZ3JhbnRlZF91bmVfcGVybWlzc2lvbnMnCiAgICApCiAgICBncmFudGVkX2F0ID0gbW9kZWxzLkRhdGVUaW1lRmllbGQoYXV0b19ub3dfYWRkPVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICB1bmlxdWVfdG9nZXRoZXIgPSAoJ3VzZXInLCAndW5lJykKICAgICAgICB2ZXJib3NlX25hbWUgPSAnUGVybWlzbyBwb3IgVU5FJwogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAnUGVybWlzb3MgcG9yIFVORScKICAgICAgICBvcmRlcmluZyA9IFsndXNlcl9fdXNlcm5hbWUnLCAndW5lX19zb3J0X29yZGVyJ10KCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZid7c2VsZi51c2VyLnVzZXJuYW1lfSAtIHtzZWxmLnVuZS5jb2RlfSc=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=accounts/signals.py
PATH_JSON="accounts/signals.py"
FILENAME=signals.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=19
SIZE_BYTES_UTF8=507
CONTENT_SHA256=346aaefe00b1f199828b4eae536ede28a86b5cab404bf34dcd54cafe71d389df
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib.auth import get_user_model
00002|from django.db.models.signals import post_save
00003|from django.dispatch import receiver
00004|from .models import UserProfile
00005|
00006|User = get_user_model()
00007|
00008|
00009|@receiver(post_save, sender=User)
00010|def create_user_profile(sender, instance, created, **kwargs):
00011|    if created:
00012|        UserProfile.objects.create(user=instance)
00013|
00014|
00015|@receiver(post_save, sender=User)
00016|def save_user_profile(sender, instance, **kwargs):
00017|    if hasattr(instance, 'profile'):
00018|        instance.profile.save()
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYi5hdXRoIGltcG9ydCBnZXRfdXNlcl9tb2RlbApmcm9tIGRqYW5nby5kYi5tb2RlbHMuc2lnbmFscyBpbXBvcnQgcG9zdF9zYXZlCmZyb20gZGphbmdvLmRpc3BhdGNoIGltcG9ydCByZWNlaXZlcgpmcm9tIC5tb2RlbHMgaW1wb3J0IFVzZXJQcm9maWxlCgpVc2VyID0gZ2V0X3VzZXJfbW9kZWwoKQoKCkByZWNlaXZlcihwb3N0X3NhdmUsIHNlbmRlcj1Vc2VyKQpkZWYgY3JlYXRlX3VzZXJfcHJvZmlsZShzZW5kZXIsIGluc3RhbmNlLCBjcmVhdGVkLCAqKmt3YXJncyk6CiAgICBpZiBjcmVhdGVkOgogICAgICAgIFVzZXJQcm9maWxlLm9iamVjdHMuY3JlYXRlKHVzZXI9aW5zdGFuY2UpCgoKQHJlY2VpdmVyKHBvc3Rfc2F2ZSwgc2VuZGVyPVVzZXIpCmRlZiBzYXZlX3VzZXJfcHJvZmlsZShzZW5kZXIsIGluc3RhbmNlLCAqKmt3YXJncyk6CiAgICBpZiBoYXNhdHRyKGluc3RhbmNlLCAncHJvZmlsZScpOgogICAgICAgIGluc3RhbmNlLnByb2ZpbGUuc2F2ZSgp
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=accounts/tests.py
PATH_JSON="accounts/tests.py"
FILENAME=tests.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=60
CONTENT_SHA256=9ab6c6191360e63c1b4c9b5659aef348a743c9e078be68190917369e4e9563e8
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.test import TestCase

# Create your tests here.

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.test import TestCase
00002|
00003|# Create your tests here.

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udGVzdCBpbXBvcnQgVGVzdENhc2UKCiMgQ3JlYXRlIHlvdXIgdGVzdHMgaGVyZS4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=accounts/views.py
PATH_JSON="accounts/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=63
CONTENT_SHA256=c5cd48407aec8a3ee3df74d46e8fbfa1ec32defb34de9c3f7ada4159a318265d
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.shortcuts import render

# Create your views here.

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.shortcuts import render
00002|
00003|# Create your views here.

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uc2hvcnRjdXRzIGltcG9ydCByZW5kZXIKCiMgQ3JlYXRlIHlvdXIgdmlld3MgaGVyZS4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/__init__.py
PATH_JSON="apps/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/__init__.py
PATH_JSON="apps/core/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/admin.py
PATH_JSON="apps/core/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=145
SIZE_BYTES_UTF8=4073
CONTENT_SHA256=f0fbabaff3b55bd4eb574c3096398528e827b74c6a7456ac2a427cf0141166f6
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.contrib import admin

from .models import (
    Contacto,
    DataDictionaryField,
    DataImportBatch,
    DataImportError,
    Entidad,
    Producto,
    RelacionEntidadProducto,
    UnidadNegocio,
)


class ContactoInline(admin.TabularInline):
    model = Contacto
    extra = 0
    fields = ("nombre", "cargo", "email", "telefono_movil", "activo")


class RelacionEntidadProductoInline(admin.TabularInline):
    model = RelacionEntidadProducto
    extra = 0
    autocomplete_fields = ("producto", "unidad_negocio")


@admin.register(UnidadNegocio)
class UnidadNegocioAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "activa", "orden")
    list_filter = ("activa",)
    search_fields = ("codigo", "nombre")
    ordering = ("orden", "nombre")


@admin.register(Entidad)
class EntidadAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "nit",
        "tipo_entidad",
        "ciudad",
        "categoria_riesgo",
        "activo",
        "fecha_modificacion",
    )
    list_filter = ("tipo_entidad", "activo", "categoria_riesgo", "pais")
    search_fields = ("nombre", "nombre_comercial", "nit", "email")
    ordering = ("nombre",)
    inlines = [ContactoInline, RelacionEntidadProductoInline]
    readonly_fields = ("fecha_creacion", "fecha_modificacion")


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "entidad",
        "cargo",
        "email",
        "es_contacto_cobranza",
        "activo",
    )
    list_filter = ("activo", "es_decisor_credito", "es_contacto_cobranza", "es_contacto_operativo")
    search_fields = ("nombre", "email", "entidad__nombre", "entidad__nit")
    autocomplete_fields = ("entidad",)
    ordering = ("entidad__nombre", "nombre")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "tipo_producto", "activo")
    list_filter = ("activo", "tipo_producto")
    search_fields = ("codigo", "nombre")
    ordering = ("nombre",)


@admin.register(RelacionEntidadProducto)
class RelacionEntidadProductoAdmin(admin.ModelAdmin):
    list_display = (
        "entidad",
        "producto",
        "unidad_negocio",
        "estado",
        "fecha_inicio",
        "monto_aprobado",
    )
    list_filter = ("estado", "unidad_negocio", "moneda")
    search_fields = (
        "entidad__nombre",
        "entidad__nit",
        "producto__codigo",
        "codigo_operacion_externo",
    )
    autocomplete_fields = ("entidad", "producto", "unidad_negocio")


@admin.register(DataDictionaryField)
class DataDictionaryFieldAdmin(admin.ModelAdmin):
    list_display = (
        "modulo",
        "nombre_logico",
        "tabla_fisica",
        "campo_fisico",
        "tipo_dato",
        "activo",
        "orden",
    )
    list_filter = ("modulo", "activo", "periodicidad")
    search_fields = ("nombre_logico", "tabla_fisica", "campo_fisico", "definicion")
    ordering = ("modulo", "orden", "tabla_fisica")


class DataImportErrorInline(admin.TabularInline):
    model = DataImportError
    extra = 0
    readonly_fields = ("fila_numero", "campo", "valor_original", "mensaje_error")
    can_delete = False


@admin.register(DataImportBatch)
class DataImportBatchAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_carga",
        "modulo",
        "tipo_importacion",
        "archivo_nombre",
        "estado",
        "filas_leidas",
        "filas_validas",
        "filas_error",
        "usuario",
    )
    list_filter = ("modulo", "estado", "tipo_importacion")
    search_fields = ("archivo_nombre", "tipo_importacion", "observaciones")
    date_hierarchy = "fecha_carga"
    readonly_fields = ("fecha_carga",)
    inlines = [DataImportErrorInline]


@admin.register(DataImportError)
class DataImportErrorAdmin(admin.ModelAdmin):
    list_display = ("batch", "fila_numero", "campo", "mensaje_error")
    list_filter = ("batch__modulo",)
    search_fields = ("mensaje_error", "valor_original", "campo")
    ordering = ("-batch__fecha_carga", "fila_numero")

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import admin
00002|
00003|from .models import (
00004|    Contacto,
00005|    DataDictionaryField,
00006|    DataImportBatch,
00007|    DataImportError,
00008|    Entidad,
00009|    Producto,
00010|    RelacionEntidadProducto,
00011|    UnidadNegocio,
00012|)
00013|
00014|
00015|class ContactoInline(admin.TabularInline):
00016|    model = Contacto
00017|    extra = 0
00018|    fields = ("nombre", "cargo", "email", "telefono_movil", "activo")
00019|
00020|
00021|class RelacionEntidadProductoInline(admin.TabularInline):
00022|    model = RelacionEntidadProducto
00023|    extra = 0
00024|    autocomplete_fields = ("producto", "unidad_negocio")
00025|
00026|
00027|@admin.register(UnidadNegocio)
00028|class UnidadNegocioAdmin(admin.ModelAdmin):
00029|    list_display = ("codigo", "nombre", "activa", "orden")
00030|    list_filter = ("activa",)
00031|    search_fields = ("codigo", "nombre")
00032|    ordering = ("orden", "nombre")
00033|
00034|
00035|@admin.register(Entidad)
00036|class EntidadAdmin(admin.ModelAdmin):
00037|    list_display = (
00038|        "nombre",
00039|        "nit",
00040|        "tipo_entidad",
00041|        "ciudad",
00042|        "categoria_riesgo",
00043|        "activo",
00044|        "fecha_modificacion",
00045|    )
00046|    list_filter = ("tipo_entidad", "activo", "categoria_riesgo", "pais")
00047|    search_fields = ("nombre", "nombre_comercial", "nit", "email")
00048|    ordering = ("nombre",)
00049|    inlines = [ContactoInline, RelacionEntidadProductoInline]
00050|    readonly_fields = ("fecha_creacion", "fecha_modificacion")
00051|
00052|
00053|@admin.register(Contacto)
00054|class ContactoAdmin(admin.ModelAdmin):
00055|    list_display = (
00056|        "nombre",
00057|        "entidad",
00058|        "cargo",
00059|        "email",
00060|        "es_contacto_cobranza",
00061|        "activo",
00062|    )
00063|    list_filter = ("activo", "es_decisor_credito", "es_contacto_cobranza", "es_contacto_operativo")
00064|    search_fields = ("nombre", "email", "entidad__nombre", "entidad__nit")
00065|    autocomplete_fields = ("entidad",)
00066|    ordering = ("entidad__nombre", "nombre")
00067|
00068|
00069|@admin.register(Producto)
00070|class ProductoAdmin(admin.ModelAdmin):
00071|    list_display = ("codigo", "nombre", "tipo_producto", "activo")
00072|    list_filter = ("activo", "tipo_producto")
00073|    search_fields = ("codigo", "nombre")
00074|    ordering = ("nombre",)
00075|
00076|
00077|@admin.register(RelacionEntidadProducto)
00078|class RelacionEntidadProductoAdmin(admin.ModelAdmin):
00079|    list_display = (
00080|        "entidad",
00081|        "producto",
00082|        "unidad_negocio",
00083|        "estado",
00084|        "fecha_inicio",
00085|        "monto_aprobado",
00086|    )
00087|    list_filter = ("estado", "unidad_negocio", "moneda")
00088|    search_fields = (
00089|        "entidad__nombre",
00090|        "entidad__nit",
00091|        "producto__codigo",
00092|        "codigo_operacion_externo",
00093|    )
00094|    autocomplete_fields = ("entidad", "producto", "unidad_negocio")
00095|
00096|
00097|@admin.register(DataDictionaryField)
00098|class DataDictionaryFieldAdmin(admin.ModelAdmin):
00099|    list_display = (
00100|        "modulo",
00101|        "nombre_logico",
00102|        "tabla_fisica",
00103|        "campo_fisico",
00104|        "tipo_dato",
00105|        "activo",
00106|        "orden",
00107|    )
00108|    list_filter = ("modulo", "activo", "periodicidad")
00109|    search_fields = ("nombre_logico", "tabla_fisica", "campo_fisico", "definicion")
00110|    ordering = ("modulo", "orden", "tabla_fisica")
00111|
00112|
00113|class DataImportErrorInline(admin.TabularInline):
00114|    model = DataImportError
00115|    extra = 0
00116|    readonly_fields = ("fila_numero", "campo", "valor_original", "mensaje_error")
00117|    can_delete = False
00118|
00119|
00120|@admin.register(DataImportBatch)
00121|class DataImportBatchAdmin(admin.ModelAdmin):
00122|    list_display = (
00123|        "fecha_carga",
00124|        "modulo",
00125|        "tipo_importacion",
00126|        "archivo_nombre",
00127|        "estado",
00128|        "filas_leidas",
00129|        "filas_validas",
00130|        "filas_error",
00131|        "usuario",
00132|    )
00133|    list_filter = ("modulo", "estado", "tipo_importacion")
00134|    search_fields = ("archivo_nombre", "tipo_importacion", "observaciones")
00135|    date_hierarchy = "fecha_carga"
00136|    readonly_fields = ("fecha_carga",)
00137|    inlines = [DataImportErrorInline]
00138|
00139|
00140|@admin.register(DataImportError)
00141|class DataImportErrorAdmin(admin.ModelAdmin):
00142|    list_display = ("batch", "fila_numero", "campo", "mensaje_error")
00143|    list_filter = ("batch__modulo",)
00144|    search_fields = ("mensaje_error", "valor_original", "campo")
00145|    ordering = ("-batch__fecha_carga", "fila_numero")

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgYWRtaW4KCmZyb20gLm1vZGVscyBpbXBvcnQgKAogICAgQ29udGFjdG8sCiAgICBEYXRhRGljdGlvbmFyeUZpZWxkLAogICAgRGF0YUltcG9ydEJhdGNoLAogICAgRGF0YUltcG9ydEVycm9yLAogICAgRW50aWRhZCwKICAgIFByb2R1Y3RvLAogICAgUmVsYWNpb25FbnRpZGFkUHJvZHVjdG8sCiAgICBVbmlkYWROZWdvY2lvLAopCgoKY2xhc3MgQ29udGFjdG9JbmxpbmUoYWRtaW4uVGFidWxhcklubGluZSk6CiAgICBtb2RlbCA9IENvbnRhY3RvCiAgICBleHRyYSA9IDAKICAgIGZpZWxkcyA9ICgibm9tYnJlIiwgImNhcmdvIiwgImVtYWlsIiwgInRlbGVmb25vX21vdmlsIiwgImFjdGl2byIpCgoKY2xhc3MgUmVsYWNpb25FbnRpZGFkUHJvZHVjdG9JbmxpbmUoYWRtaW4uVGFidWxhcklubGluZSk6CiAgICBtb2RlbCA9IFJlbGFjaW9uRW50aWRhZFByb2R1Y3RvCiAgICBleHRyYSA9IDAKICAgIGF1dG9jb21wbGV0ZV9maWVsZHMgPSAoInByb2R1Y3RvIiwgInVuaWRhZF9uZWdvY2lvIikKCgpAYWRtaW4ucmVnaXN0ZXIoVW5pZGFkTmVnb2NpbykKY2xhc3MgVW5pZGFkTmVnb2Npb0FkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKCJjb2RpZ28iLCAibm9tYnJlIiwgImFjdGl2YSIsICJvcmRlbiIpCiAgICBsaXN0X2ZpbHRlciA9ICgiYWN0aXZhIiwpCiAgICBzZWFyY2hfZmllbGRzID0gKCJjb2RpZ28iLCAibm9tYnJlIikKICAgIG9yZGVyaW5nID0gKCJvcmRlbiIsICJub21icmUiKQoKCkBhZG1pbi5yZWdpc3RlcihFbnRpZGFkKQpjbGFzcyBFbnRpZGFkQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoCiAgICAgICAgIm5vbWJyZSIsCiAgICAgICAgIm5pdCIsCiAgICAgICAgInRpcG9fZW50aWRhZCIsCiAgICAgICAgImNpdWRhZCIsCiAgICAgICAgImNhdGVnb3JpYV9yaWVzZ28iLAogICAgICAgICJhY3Rpdm8iLAogICAgICAgICJmZWNoYV9tb2RpZmljYWNpb24iLAogICAgKQogICAgbGlzdF9maWx0ZXIgPSAoInRpcG9fZW50aWRhZCIsICJhY3Rpdm8iLCAiY2F0ZWdvcmlhX3JpZXNnbyIsICJwYWlzIikKICAgIHNlYXJjaF9maWVsZHMgPSAoIm5vbWJyZSIsICJub21icmVfY29tZXJjaWFsIiwgIm5pdCIsICJlbWFpbCIpCiAgICBvcmRlcmluZyA9ICgibm9tYnJlIiwpCiAgICBpbmxpbmVzID0gW0NvbnRhY3RvSW5saW5lLCBSZWxhY2lvbkVudGlkYWRQcm9kdWN0b0lubGluZV0KICAgIHJlYWRvbmx5X2ZpZWxkcyA9ICgiZmVjaGFfY3JlYWNpb24iLCAiZmVjaGFfbW9kaWZpY2FjaW9uIikKCgpAYWRtaW4ucmVnaXN0ZXIoQ29udGFjdG8pCmNsYXNzIENvbnRhY3RvQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoCiAgICAgICAgIm5vbWJyZSIsCiAgICAgICAgImVudGlkYWQiLAogICAgICAgICJjYXJnbyIsCiAgICAgICAgImVtYWlsIiwKICAgICAgICAiZXNfY29udGFjdG9fY29icmFuemEiLAogICAgICAgICJhY3Rpdm8iLAogICAgKQogICAgbGlzdF9maWx0ZXIgPSAoImFjdGl2byIsICJlc19kZWNpc29yX2NyZWRpdG8iLCAiZXNfY29udGFjdG9fY29icmFuemEiLCAiZXNfY29udGFjdG9fb3BlcmF0aXZvIikKICAgIHNlYXJjaF9maWVsZHMgPSAoIm5vbWJyZSIsICJlbWFpbCIsICJlbnRpZGFkX19ub21icmUiLCAiZW50aWRhZF9fbml0IikKICAgIGF1dG9jb21wbGV0ZV9maWVsZHMgPSAoImVudGlkYWQiLCkKICAgIG9yZGVyaW5nID0gKCJlbnRpZGFkX19ub21icmUiLCAibm9tYnJlIikKCgpAYWRtaW4ucmVnaXN0ZXIoUHJvZHVjdG8pCmNsYXNzIFByb2R1Y3RvQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoImNvZGlnbyIsICJub21icmUiLCAidGlwb19wcm9kdWN0byIsICJhY3Rpdm8iKQogICAgbGlzdF9maWx0ZXIgPSAoImFjdGl2byIsICJ0aXBvX3Byb2R1Y3RvIikKICAgIHNlYXJjaF9maWVsZHMgPSAoImNvZGlnbyIsICJub21icmUiKQogICAgb3JkZXJpbmcgPSAoIm5vbWJyZSIsKQoKCkBhZG1pbi5yZWdpc3RlcihSZWxhY2lvbkVudGlkYWRQcm9kdWN0bykKY2xhc3MgUmVsYWNpb25FbnRpZGFkUHJvZHVjdG9BZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAiZW50aWRhZCIsCiAgICAgICAgInByb2R1Y3RvIiwKICAgICAgICAidW5pZGFkX25lZ29jaW8iLAogICAgICAgICJlc3RhZG8iLAogICAgICAgICJmZWNoYV9pbmljaW8iLAogICAgICAgICJtb250b19hcHJvYmFkbyIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgiZXN0YWRvIiwgInVuaWRhZF9uZWdvY2lvIiwgIm1vbmVkYSIpCiAgICBzZWFyY2hfZmllbGRzID0gKAogICAgICAgICJlbnRpZGFkX19ub21icmUiLAogICAgICAgICJlbnRpZGFkX19uaXQiLAogICAgICAgICJwcm9kdWN0b19fY29kaWdvIiwKICAgICAgICAiY29kaWdvX29wZXJhY2lvbl9leHRlcm5vIiwKICAgICkKICAgIGF1dG9jb21wbGV0ZV9maWVsZHMgPSAoImVudGlkYWQiLCAicHJvZHVjdG8iLCAidW5pZGFkX25lZ29jaW8iKQoKCkBhZG1pbi5yZWdpc3RlcihEYXRhRGljdGlvbmFyeUZpZWxkKQpjbGFzcyBEYXRhRGljdGlvbmFyeUZpZWxkQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoCiAgICAgICAgIm1vZHVsbyIsCiAgICAgICAgIm5vbWJyZV9sb2dpY28iLAogICAgICAgICJ0YWJsYV9maXNpY2EiLAogICAgICAgICJjYW1wb19maXNpY28iLAogICAgICAgICJ0aXBvX2RhdG8iLAogICAgICAgICJhY3Rpdm8iLAogICAgICAgICJvcmRlbiIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgibW9kdWxvIiwgImFjdGl2byIsICJwZXJpb2RpY2lkYWQiKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgibm9tYnJlX2xvZ2ljbyIsICJ0YWJsYV9maXNpY2EiLCAiY2FtcG9fZmlzaWNvIiwgImRlZmluaWNpb24iKQogICAgb3JkZXJpbmcgPSAoIm1vZHVsbyIsICJvcmRlbiIsICJ0YWJsYV9maXNpY2EiKQoKCmNsYXNzIERhdGFJbXBvcnRFcnJvcklubGluZShhZG1pbi5UYWJ1bGFySW5saW5lKToKICAgIG1vZGVsID0gRGF0YUltcG9ydEVycm9yCiAgICBleHRyYSA9IDAKICAgIHJlYWRvbmx5X2ZpZWxkcyA9ICgiZmlsYV9udW1lcm8iLCAiY2FtcG8iLCAidmFsb3Jfb3JpZ2luYWwiLCAibWVuc2FqZV9lcnJvciIpCiAgICBjYW5fZGVsZXRlID0gRmFsc2UKCgpAYWRtaW4ucmVnaXN0ZXIoRGF0YUltcG9ydEJhdGNoKQpjbGFzcyBEYXRhSW1wb3J0QmF0Y2hBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAiZmVjaGFfY2FyZ2EiLAogICAgICAgICJtb2R1bG8iLAogICAgICAgICJ0aXBvX2ltcG9ydGFjaW9uIiwKICAgICAgICAiYXJjaGl2b19ub21icmUiLAogICAgICAgICJlc3RhZG8iLAogICAgICAgICJmaWxhc19sZWlkYXMiLAogICAgICAgICJmaWxhc192YWxpZGFzIiwKICAgICAgICAiZmlsYXNfZXJyb3IiLAogICAgICAgICJ1c3VhcmlvIiwKICAgICkKICAgIGxpc3RfZmlsdGVyID0gKCJtb2R1bG8iLCAiZXN0YWRvIiwgInRpcG9faW1wb3J0YWNpb24iKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiYXJjaGl2b19ub21icmUiLCAidGlwb19pbXBvcnRhY2lvbiIsICJvYnNlcnZhY2lvbmVzIikKICAgIGRhdGVfaGllcmFyY2h5ID0gImZlY2hhX2NhcmdhIgogICAgcmVhZG9ubHlfZmllbGRzID0gKCJmZWNoYV9jYXJnYSIsKQogICAgaW5saW5lcyA9IFtEYXRhSW1wb3J0RXJyb3JJbmxpbmVdCgoKQGFkbWluLnJlZ2lzdGVyKERhdGFJbXBvcnRFcnJvcikKY2xhc3MgRGF0YUltcG9ydEVycm9yQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoImJhdGNoIiwgImZpbGFfbnVtZXJvIiwgImNhbXBvIiwgIm1lbnNhamVfZXJyb3IiKQogICAgbGlzdF9maWx0ZXIgPSAoImJhdGNoX19tb2R1bG8iLCkKICAgIHNlYXJjaF9maWVsZHMgPSAoIm1lbnNhamVfZXJyb3IiLCAidmFsb3Jfb3JpZ2luYWwiLCAiY2FtcG8iKQogICAgb3JkZXJpbmcgPSAoIi1iYXRjaF9fZmVjaGFfY2FyZ2EiLCAiZmlsYV9udW1lcm8iKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/apps.py
PATH_JSON="apps/core/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=8
SIZE_BYTES_UTF8=204
CONTENT_SHA256=d09ef745db37e6709e92088b9717f89f827ed4c1a64060063c0e5d32229579de
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    label = "wcgone_core"
    verbose_name = "Núcleo WCG"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class CoreConfig(AppConfig):
00005|    default_auto_field = "django.db.models.BigAutoField"
00006|    name = "apps.core"
00007|    label = "wcgone_core"
00008|    verbose_name = "Núcleo WCG"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgQ29yZUNvbmZpZyhBcHBDb25maWcpOgogICAgZGVmYXVsdF9hdXRvX2ZpZWxkID0gImRqYW5nby5kYi5tb2RlbHMuQmlnQXV0b0ZpZWxkIgogICAgbmFtZSA9ICJhcHBzLmNvcmUiCiAgICBsYWJlbCA9ICJ3Y2dvbmVfY29yZSIKICAgIHZlcmJvc2VfbmFtZSA9ICJOw7pjbGVvIFdDRyIK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/exports.py
PATH_JSON="apps/core/exports.py"
FILENAME=exports.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=19
SIZE_BYTES_UTF8=578
CONTENT_SHA256=0964559d50e990007a4a6a9cc792c51b2e91b46cac7c7ec6275ae9dbf609d1c9
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Exportaciones CSV simples vía HttpResponse."""

from __future__ import annotations

import csv
from io import StringIO

from django.http import HttpResponse


def csv_response(filename: str, headers: list[str], rows: list[list]) -> HttpResponse:
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    response = HttpResponse("\ufeff" + buffer.getvalue(), content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Exportaciones CSV simples vía HttpResponse."""
00002|
00003|from __future__ import annotations
00004|
00005|import csv
00006|from io import StringIO
00007|
00008|from django.http import HttpResponse
00009|
00010|
00011|def csv_response(filename: str, headers: list[str], rows: list[list]) -> HttpResponse:
00012|    buffer = StringIO()
00013|    writer = csv.writer(buffer)
00014|    writer.writerow(headers)
00015|    for row in rows:
00016|        writer.writerow(row)
00017|    response = HttpResponse("\ufeff" + buffer.getvalue(), content_type="text/csv; charset=utf-8")
00018|    response["Content-Disposition"] = f'attachment; filename="{filename}"'
00019|    return response

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiRXhwb3J0YWNpb25lcyBDU1Ygc2ltcGxlcyB2w61hIEh0dHBSZXNwb25zZS4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmltcG9ydCBjc3YKZnJvbSBpbyBpbXBvcnQgU3RyaW5nSU8KCmZyb20gZGphbmdvLmh0dHAgaW1wb3J0IEh0dHBSZXNwb25zZQoKCmRlZiBjc3ZfcmVzcG9uc2UoZmlsZW5hbWU6IHN0ciwgaGVhZGVyczogbGlzdFtzdHJdLCByb3dzOiBsaXN0W2xpc3RdKSAtPiBIdHRwUmVzcG9uc2U6CiAgICBidWZmZXIgPSBTdHJpbmdJTygpCiAgICB3cml0ZXIgPSBjc3Yud3JpdGVyKGJ1ZmZlcikKICAgIHdyaXRlci53cml0ZXJvdyhoZWFkZXJzKQogICAgZm9yIHJvdyBpbiByb3dzOgogICAgICAgIHdyaXRlci53cml0ZXJvdyhyb3cpCiAgICByZXNwb25zZSA9IEh0dHBSZXNwb25zZSgiXHVmZWZmIiArIGJ1ZmZlci5nZXR2YWx1ZSgpLCBjb250ZW50X3R5cGU9InRleHQvY3N2OyBjaGFyc2V0PXV0Zi04IikKICAgIHJlc3BvbnNlWyJDb250ZW50LURpc3Bvc2l0aW9uIl0gPSBmJ2F0dGFjaG1lbnQ7IGZpbGVuYW1lPSJ7ZmlsZW5hbWV9IicKICAgIHJldHVybiByZXNwb25zZQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/forms.py
PATH_JSON="apps/core/forms.py"
FILENAME=forms.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=18
SIZE_BYTES_UTF8=664
CONTENT_SHA256=04e042a7b6559071938e9c32ffe5e88907768ae4f0432d5e89f563417f5151ae
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django import forms


class ImportFileForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo",
        help_text="Formatos aceptados: CSV o XLSX.",
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".csv,.xlsx,.xls"}),
    )

    def clean_archivo(self):
        archivo = self.cleaned_data["archivo"]
        name = (archivo.name or "").lower()
        if not name.endswith((".csv", ".xlsx", ".xls", ".txt", ".tsv")):
            raise forms.ValidationError("Use un archivo CSV o XLSX.")
        if archivo.size == 0:
            raise forms.ValidationError("El archivo está vacío.")
        return archivo

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django import forms
00002|
00003|
00004|class ImportFileForm(forms.Form):
00005|    archivo = forms.FileField(
00006|        label="Archivo",
00007|        help_text="Formatos aceptados: CSV o XLSX.",
00008|        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".csv,.xlsx,.xls"}),
00009|    )
00010|
00011|    def clean_archivo(self):
00012|        archivo = self.cleaned_data["archivo"]
00013|        name = (archivo.name or "").lower()
00014|        if not name.endswith((".csv", ".xlsx", ".xls", ".txt", ".tsv")):
00015|            raise forms.ValidationError("Use un archivo CSV o XLSX.")
00016|        if archivo.size == 0:
00017|            raise forms.ValidationError("El archivo está vacío.")
00018|        return archivo

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28gaW1wb3J0IGZvcm1zCgoKY2xhc3MgSW1wb3J0RmlsZUZvcm0oZm9ybXMuRm9ybSk6CiAgICBhcmNoaXZvID0gZm9ybXMuRmlsZUZpZWxkKAogICAgICAgIGxhYmVsPSJBcmNoaXZvIiwKICAgICAgICBoZWxwX3RleHQ9IkZvcm1hdG9zIGFjZXB0YWRvczogQ1NWIG8gWExTWC4iLAogICAgICAgIHdpZGdldD1mb3Jtcy5DbGVhcmFibGVGaWxlSW5wdXQoYXR0cnM9eyJjbGFzcyI6ICJmb3JtLWNvbnRyb2wiLCAiYWNjZXB0IjogIi5jc3YsLnhsc3gsLnhscyJ9KSwKICAgICkKCiAgICBkZWYgY2xlYW5fYXJjaGl2byhzZWxmKToKICAgICAgICBhcmNoaXZvID0gc2VsZi5jbGVhbmVkX2RhdGFbImFyY2hpdm8iXQogICAgICAgIG5hbWUgPSAoYXJjaGl2by5uYW1lIG9yICIiKS5sb3dlcigpCiAgICAgICAgaWYgbm90IG5hbWUuZW5kc3dpdGgoKCIuY3N2IiwgIi54bHN4IiwgIi54bHMiLCAiLnR4dCIsICIudHN2IikpOgogICAgICAgICAgICByYWlzZSBmb3Jtcy5WYWxpZGF0aW9uRXJyb3IoIlVzZSB1biBhcmNoaXZvIENTViBvIFhMU1guIikKICAgICAgICBpZiBhcmNoaXZvLnNpemUgPT0gMDoKICAgICAgICAgICAgcmFpc2UgZm9ybXMuVmFsaWRhdGlvbkVycm9yKCJFbCBhcmNoaXZvIGVzdMOhIHZhY8Otby4iKQogICAgICAgIHJldHVybiBhcmNoaXZvCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/imports/__init__.py
PATH_JSON="apps/core/imports/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=9
SIZE_BYTES_UTF8=256
CONTENT_SHA256=4042014e1d83b090f8ff902ea0157f128e0c6d952cd583b67ef9c532629e290f
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from apps.core.imports.base import ImportValidationError, run_import_batch
from apps.core.imports.columns import normalize_columns, require_any

__all__ = [
    "ImportValidationError",
    "run_import_batch",
    "normalize_columns",
    "require_any",
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from apps.core.imports.base import ImportValidationError, run_import_batch
00002|from apps.core.imports.columns import normalize_columns, require_any
00003|
00004|__all__ = [
00005|    "ImportValidationError",
00006|    "run_import_batch",
00007|    "normalize_columns",
00008|    "require_any",
00009|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBhcHBzLmNvcmUuaW1wb3J0cy5iYXNlIGltcG9ydCBJbXBvcnRWYWxpZGF0aW9uRXJyb3IsIHJ1bl9pbXBvcnRfYmF0Y2gKZnJvbSBhcHBzLmNvcmUuaW1wb3J0cy5jb2x1bW5zIGltcG9ydCBub3JtYWxpemVfY29sdW1ucywgcmVxdWlyZV9hbnkKCl9fYWxsX18gPSBbCiAgICAiSW1wb3J0VmFsaWRhdGlvbkVycm9yIiwKICAgICJydW5faW1wb3J0X2JhdGNoIiwKICAgICJub3JtYWxpemVfY29sdW1ucyIsCiAgICAicmVxdWlyZV9hbnkiLApdCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/imports/base.py
PATH_JSON="apps/core/imports/base.py"
FILENAME=base.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=174
SIZE_BYTES_UTF8=5992
CONTENT_SHA256=b93dc3f2b283608cacc3ac5541693d5cc5f278886504dfef409a79a68257448f
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Utilidades compartidas de importación CSV/XLSX."""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
from typing import Any, Callable

import pandas as pd
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from apps.core.models import DataImportBatch, DataImportError


class ImportValidationError(Exception):
    pass


def cell_str(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def row_to_json(row: pd.Series) -> dict:
    data = {}
    for key, value in row.items():
        if pd.isna(value):
            data[str(key)] = None
        elif hasattr(value, "isoformat"):
            data[str(key)] = value.isoformat()
        else:
            data[str(key)] = str(value)
    return data


def read_dataframe(uploaded_file: UploadedFile, sheet_name=0) -> pd.DataFrame:
    name = (uploaded_file.name or "").lower()
    raw = uploaded_file.read()
    uploaded_file.seek(0)
    if not raw:
        raise ImportValidationError("El archivo está vacío.")
    if name.endswith((".xlsx", ".xls")):
        if sheet_name is None:
            xls = pd.ExcelFile(io.BytesIO(raw))
            sheet_name = xls.sheet_names[0]
            for candidate in xls.sheet_names:
                low = candidate.lower()
                if any(k in low for k in ("base", "leasing", "datos", "ticket", "hoja")):
                    sheet_name = candidate
                    break
            df = pd.read_excel(xls, sheet_name=sheet_name)
        else:
            df = pd.read_excel(io.BytesIO(raw), sheet_name=sheet_name)
    elif name.endswith((".csv", ".tsv", ".txt")):
        df = pd.read_csv(io.BytesIO(raw))
    else:
        raise ImportValidationError("Formato no soportado. Use CSV o XLSX.")
    if df.empty:
        raise ImportValidationError("El archivo no contiene filas de datos.")
    return df.dropna(how="all")


def save_upload_copy(uploaded_file: UploadedFile) -> tuple[str, str]:
    uploads_root = Path(settings.UPLOADS_ROOT)
    uploads_root.mkdir(parents=True, exist_ok=True)
    raw = uploaded_file.read()
    uploaded_file.seek(0)
    file_hash = hashlib.sha256(raw).hexdigest()
    dest = uploads_root / f"{file_hash[:16]}_{uploaded_file.name}"
    if not dest.exists():
        dest.write_bytes(raw)
    return str(dest.relative_to(settings.BASE_DIR)), file_hash


def run_import_batch(
    *,
    user,
    modulo: str,
    tipo_importacion: str,
    uploaded_file: UploadedFile,
    preprocess: Callable[[pd.DataFrame], pd.DataFrame] | None = None,
    row_handler: Callable[..., tuple[bool, bool] | None],
) -> DataImportBatch:
    """
    Ejecuta importación fila a fila.
    row_handler retorna (creado, actualizado) o None si hubo errores en row_errors.
    """
    archivo_ruta, archivo_hash = save_upload_copy(uploaded_file)
    batch = DataImportBatch.objects.create(
        modulo=modulo,
        tipo_importacion=tipo_importacion,
        archivo_nombre=uploaded_file.name,
        archivo_hash=archivo_hash,
        archivo_ruta=archivo_ruta,
        usuario=user,
        estado=DataImportBatch.ESTADO_PROCESANDO,
    )
    creados = 0
    actualizados = 0
    logs: list[str] = []

    try:
        df = read_dataframe(uploaded_file)
        if preprocess:
            df = preprocess(df)
        batch.filas_leidas = len(df)

        for idx, row in df.iterrows():
            fila_numero = int(idx) + 2
            row_errors: list[str] = []
            try:
                result = row_handler(row, row_errors, batch)
                if row_errors:
                    batch.filas_error += 1
                    for msg in row_errors:
                        DataImportError.objects.create(
                            batch=batch,
                            fila_numero=fila_numero,
                            mensaje_error=msg,
                            payload_json=row_to_json(row),
                        )
                    logs.append(f"Fila {fila_numero}: {'; '.join(row_errors)}")
                elif result is not None:
                    created, updated = result
                    batch.filas_validas += 1
                    if created:
                        creados += 1
                    if updated:
                        actualizados += 1
                else:
                    batch.filas_error += 1
                    DataImportError.objects.create(
                        batch=batch,
                        fila_numero=fila_numero,
                        mensaje_error="Fila omitida sin detalle.",
                        payload_json=row_to_json(row),
                    )
            except Exception as exc:
                batch.filas_error += 1
                DataImportError.objects.create(
                    batch=batch,
                    fila_numero=fila_numero,
                    mensaje_error=str(exc),
                    payload_json=row_to_json(row),
                )
                logs.append(f"Fila {fila_numero}: {exc}")

        if batch.filas_error == 0 and batch.filas_validas > 0:
            batch.estado = DataImportBatch.ESTADO_OK
        elif batch.filas_validas > 0:
            batch.estado = DataImportBatch.ESTADO_PARCIAL
        elif batch.filas_leidas == 0:
            batch.estado = DataImportBatch.ESTADO_ERROR
            logs.append("No se encontraron filas para procesar.")
        else:
            batch.estado = DataImportBatch.ESTADO_ERROR

    except ImportValidationError as exc:
        batch.estado = DataImportBatch.ESTADO_ERROR
        logs.append(str(exc))
    except Exception as exc:
        batch.estado = DataImportBatch.ESTADO_ERROR
        logs.append(f"Error general: {exc}")

    batch.observaciones = (
        f"Creados: {creados}, Actualizados: {actualizados}. "
        + (" | ".join(logs[:20]) if logs else "")
    )[:8000]
    batch.save()
    return batch

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Utilidades compartidas de importación CSV/XLSX."""
00002|
00003|from __future__ import annotations
00004|
00005|import hashlib
00006|import io
00007|import json
00008|from pathlib import Path
00009|from typing import Any, Callable
00010|
00011|import pandas as pd
00012|from django.conf import settings
00013|from django.core.files.uploadedfile import UploadedFile
00014|
00015|from apps.core.models import DataImportBatch, DataImportError
00016|
00017|
00018|class ImportValidationError(Exception):
00019|    pass
00020|
00021|
00022|def cell_str(value: Any) -> str:
00023|    if value is None or (isinstance(value, float) and pd.isna(value)):
00024|        return ""
00025|    return str(value).strip()
00026|
00027|
00028|def row_to_json(row: pd.Series) -> dict:
00029|    data = {}
00030|    for key, value in row.items():
00031|        if pd.isna(value):
00032|            data[str(key)] = None
00033|        elif hasattr(value, "isoformat"):
00034|            data[str(key)] = value.isoformat()
00035|        else:
00036|            data[str(key)] = str(value)
00037|    return data
00038|
00039|
00040|def read_dataframe(uploaded_file: UploadedFile, sheet_name=0) -> pd.DataFrame:
00041|    name = (uploaded_file.name or "").lower()
00042|    raw = uploaded_file.read()
00043|    uploaded_file.seek(0)
00044|    if not raw:
00045|        raise ImportValidationError("El archivo está vacío.")
00046|    if name.endswith((".xlsx", ".xls")):
00047|        if sheet_name is None:
00048|            xls = pd.ExcelFile(io.BytesIO(raw))
00049|            sheet_name = xls.sheet_names[0]
00050|            for candidate in xls.sheet_names:
00051|                low = candidate.lower()
00052|                if any(k in low for k in ("base", "leasing", "datos", "ticket", "hoja")):
00053|                    sheet_name = candidate
00054|                    break
00055|            df = pd.read_excel(xls, sheet_name=sheet_name)
00056|        else:
00057|            df = pd.read_excel(io.BytesIO(raw), sheet_name=sheet_name)
00058|    elif name.endswith((".csv", ".tsv", ".txt")):
00059|        df = pd.read_csv(io.BytesIO(raw))
00060|    else:
00061|        raise ImportValidationError("Formato no soportado. Use CSV o XLSX.")
00062|    if df.empty:
00063|        raise ImportValidationError("El archivo no contiene filas de datos.")
00064|    return df.dropna(how="all")
00065|
00066|
00067|def save_upload_copy(uploaded_file: UploadedFile) -> tuple[str, str]:
00068|    uploads_root = Path(settings.UPLOADS_ROOT)
00069|    uploads_root.mkdir(parents=True, exist_ok=True)
00070|    raw = uploaded_file.read()
00071|    uploaded_file.seek(0)
00072|    file_hash = hashlib.sha256(raw).hexdigest()
00073|    dest = uploads_root / f"{file_hash[:16]}_{uploaded_file.name}"
00074|    if not dest.exists():
00075|        dest.write_bytes(raw)
00076|    return str(dest.relative_to(settings.BASE_DIR)), file_hash
00077|
00078|
00079|def run_import_batch(
00080|    *,
00081|    user,
00082|    modulo: str,
00083|    tipo_importacion: str,
00084|    uploaded_file: UploadedFile,
00085|    preprocess: Callable[[pd.DataFrame], pd.DataFrame] | None = None,
00086|    row_handler: Callable[..., tuple[bool, bool] | None],
00087|) -> DataImportBatch:
00088|    """
00089|    Ejecuta importación fila a fila.
00090|    row_handler retorna (creado, actualizado) o None si hubo errores en row_errors.
00091|    """
00092|    archivo_ruta, archivo_hash = save_upload_copy(uploaded_file)
00093|    batch = DataImportBatch.objects.create(
00094|        modulo=modulo,
00095|        tipo_importacion=tipo_importacion,
00096|        archivo_nombre=uploaded_file.name,
00097|        archivo_hash=archivo_hash,
00098|        archivo_ruta=archivo_ruta,
00099|        usuario=user,
00100|        estado=DataImportBatch.ESTADO_PROCESANDO,
00101|    )
00102|    creados = 0
00103|    actualizados = 0
00104|    logs: list[str] = []
00105|
00106|    try:
00107|        df = read_dataframe(uploaded_file)
00108|        if preprocess:
00109|            df = preprocess(df)
00110|        batch.filas_leidas = len(df)
00111|
00112|        for idx, row in df.iterrows():
00113|            fila_numero = int(idx) + 2
00114|            row_errors: list[str] = []
00115|            try:
00116|                result = row_handler(row, row_errors, batch)
00117|                if row_errors:
00118|                    batch.filas_error += 1
00119|                    for msg in row_errors:
00120|                        DataImportError.objects.create(
00121|                            batch=batch,
00122|                            fila_numero=fila_numero,
00123|                            mensaje_error=msg,
00124|                            payload_json=row_to_json(row),
00125|                        )
00126|                    logs.append(f"Fila {fila_numero}: {'; '.join(row_errors)}")
00127|                elif result is not None:
00128|                    created, updated = result
00129|                    batch.filas_validas += 1
00130|                    if created:
00131|                        creados += 1
00132|                    if updated:
00133|                        actualizados += 1
00134|                else:
00135|                    batch.filas_error += 1
00136|                    DataImportError.objects.create(
00137|                        batch=batch,
00138|                        fila_numero=fila_numero,
00139|                        mensaje_error="Fila omitida sin detalle.",
00140|                        payload_json=row_to_json(row),
00141|                    )
00142|            except Exception as exc:
00143|                batch.filas_error += 1
00144|                DataImportError.objects.create(
00145|                    batch=batch,
00146|                    fila_numero=fila_numero,
00147|                    mensaje_error=str(exc),
00148|                    payload_json=row_to_json(row),
00149|                )
00150|                logs.append(f"Fila {fila_numero}: {exc}")
00151|
00152|        if batch.filas_error == 0 and batch.filas_validas > 0:
00153|            batch.estado = DataImportBatch.ESTADO_OK
00154|        elif batch.filas_validas > 0:
00155|            batch.estado = DataImportBatch.ESTADO_PARCIAL
00156|        elif batch.filas_leidas == 0:
00157|            batch.estado = DataImportBatch.ESTADO_ERROR
00158|            logs.append("No se encontraron filas para procesar.")
00159|        else:
00160|            batch.estado = DataImportBatch.ESTADO_ERROR
00161|
00162|    except ImportValidationError as exc:
00163|        batch.estado = DataImportBatch.ESTADO_ERROR
00164|        logs.append(str(exc))
00165|    except Exception as exc:
00166|        batch.estado = DataImportBatch.ESTADO_ERROR
00167|        logs.append(f"Error general: {exc}")
00168|
00169|    batch.observaciones = (
00170|        f"Creados: {creados}, Actualizados: {actualizados}. "
00171|        + (" | ".join(logs[:20]) if logs else "")
00172|    )[:8000]
00173|    batch.save()
00174|    return batch

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiVXRpbGlkYWRlcyBjb21wYXJ0aWRhcyBkZSBpbXBvcnRhY2nDs24gQ1NWL1hMU1guIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgppbXBvcnQgaGFzaGxpYgppbXBvcnQgaW8KaW1wb3J0IGpzb24KZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCmZyb20gdHlwaW5nIGltcG9ydCBBbnksIENhbGxhYmxlCgppbXBvcnQgcGFuZGFzIGFzIHBkCmZyb20gZGphbmdvLmNvbmYgaW1wb3J0IHNldHRpbmdzCmZyb20gZGphbmdvLmNvcmUuZmlsZXMudXBsb2FkZWRmaWxlIGltcG9ydCBVcGxvYWRlZEZpbGUKCmZyb20gYXBwcy5jb3JlLm1vZGVscyBpbXBvcnQgRGF0YUltcG9ydEJhdGNoLCBEYXRhSW1wb3J0RXJyb3IKCgpjbGFzcyBJbXBvcnRWYWxpZGF0aW9uRXJyb3IoRXhjZXB0aW9uKToKICAgIHBhc3MKCgpkZWYgY2VsbF9zdHIodmFsdWU6IEFueSkgLT4gc3RyOgogICAgaWYgdmFsdWUgaXMgTm9uZSBvciAoaXNpbnN0YW5jZSh2YWx1ZSwgZmxvYXQpIGFuZCBwZC5pc25hKHZhbHVlKSk6CiAgICAgICAgcmV0dXJuICIiCiAgICByZXR1cm4gc3RyKHZhbHVlKS5zdHJpcCgpCgoKZGVmIHJvd190b19qc29uKHJvdzogcGQuU2VyaWVzKSAtPiBkaWN0OgogICAgZGF0YSA9IHt9CiAgICBmb3Iga2V5LCB2YWx1ZSBpbiByb3cuaXRlbXMoKToKICAgICAgICBpZiBwZC5pc25hKHZhbHVlKToKICAgICAgICAgICAgZGF0YVtzdHIoa2V5KV0gPSBOb25lCiAgICAgICAgZWxpZiBoYXNhdHRyKHZhbHVlLCAiaXNvZm9ybWF0Iik6CiAgICAgICAgICAgIGRhdGFbc3RyKGtleSldID0gdmFsdWUuaXNvZm9ybWF0KCkKICAgICAgICBlbHNlOgogICAgICAgICAgICBkYXRhW3N0cihrZXkpXSA9IHN0cih2YWx1ZSkKICAgIHJldHVybiBkYXRhCgoKZGVmIHJlYWRfZGF0YWZyYW1lKHVwbG9hZGVkX2ZpbGU6IFVwbG9hZGVkRmlsZSwgc2hlZXRfbmFtZT0wKSAtPiBwZC5EYXRhRnJhbWU6CiAgICBuYW1lID0gKHVwbG9hZGVkX2ZpbGUubmFtZSBvciAiIikubG93ZXIoKQogICAgcmF3ID0gdXBsb2FkZWRfZmlsZS5yZWFkKCkKICAgIHVwbG9hZGVkX2ZpbGUuc2VlaygwKQogICAgaWYgbm90IHJhdzoKICAgICAgICByYWlzZSBJbXBvcnRWYWxpZGF0aW9uRXJyb3IoIkVsIGFyY2hpdm8gZXN0w6EgdmFjw61vLiIpCiAgICBpZiBuYW1lLmVuZHN3aXRoKCgiLnhsc3giLCAiLnhscyIpKToKICAgICAgICBpZiBzaGVldF9uYW1lIGlzIE5vbmU6CiAgICAgICAgICAgIHhscyA9IHBkLkV4Y2VsRmlsZShpby5CeXRlc0lPKHJhdykpCiAgICAgICAgICAgIHNoZWV0X25hbWUgPSB4bHMuc2hlZXRfbmFtZXNbMF0KICAgICAgICAgICAgZm9yIGNhbmRpZGF0ZSBpbiB4bHMuc2hlZXRfbmFtZXM6CiAgICAgICAgICAgICAgICBsb3cgPSBjYW5kaWRhdGUubG93ZXIoKQogICAgICAgICAgICAgICAgaWYgYW55KGsgaW4gbG93IGZvciBrIGluICgiYmFzZSIsICJsZWFzaW5nIiwgImRhdG9zIiwgInRpY2tldCIsICJob2phIikpOgogICAgICAgICAgICAgICAgICAgIHNoZWV0X25hbWUgPSBjYW5kaWRhdGUKICAgICAgICAgICAgICAgICAgICBicmVhawogICAgICAgICAgICBkZiA9IHBkLnJlYWRfZXhjZWwoeGxzLCBzaGVldF9uYW1lPXNoZWV0X25hbWUpCiAgICAgICAgZWxzZToKICAgICAgICAgICAgZGYgPSBwZC5yZWFkX2V4Y2VsKGlvLkJ5dGVzSU8ocmF3KSwgc2hlZXRfbmFtZT1zaGVldF9uYW1lKQogICAgZWxpZiBuYW1lLmVuZHN3aXRoKCgiLmNzdiIsICIudHN2IiwgIi50eHQiKSk6CiAgICAgICAgZGYgPSBwZC5yZWFkX2Nzdihpby5CeXRlc0lPKHJhdykpCiAgICBlbHNlOgogICAgICAgIHJhaXNlIEltcG9ydFZhbGlkYXRpb25FcnJvcigiRm9ybWF0byBubyBzb3BvcnRhZG8uIFVzZSBDU1YgbyBYTFNYLiIpCiAgICBpZiBkZi5lbXB0eToKICAgICAgICByYWlzZSBJbXBvcnRWYWxpZGF0aW9uRXJyb3IoIkVsIGFyY2hpdm8gbm8gY29udGllbmUgZmlsYXMgZGUgZGF0b3MuIikKICAgIHJldHVybiBkZi5kcm9wbmEoaG93PSJhbGwiKQoKCmRlZiBzYXZlX3VwbG9hZF9jb3B5KHVwbG9hZGVkX2ZpbGU6IFVwbG9hZGVkRmlsZSkgLT4gdHVwbGVbc3RyLCBzdHJdOgogICAgdXBsb2Fkc19yb290ID0gUGF0aChzZXR0aW5ncy5VUExPQURTX1JPT1QpCiAgICB1cGxvYWRzX3Jvb3QubWtkaXIocGFyZW50cz1UcnVlLCBleGlzdF9vaz1UcnVlKQogICAgcmF3ID0gdXBsb2FkZWRfZmlsZS5yZWFkKCkKICAgIHVwbG9hZGVkX2ZpbGUuc2VlaygwKQogICAgZmlsZV9oYXNoID0gaGFzaGxpYi5zaGEyNTYocmF3KS5oZXhkaWdlc3QoKQogICAgZGVzdCA9IHVwbG9hZHNfcm9vdCAvIGYie2ZpbGVfaGFzaFs6MTZdfV97dXBsb2FkZWRfZmlsZS5uYW1lfSIKICAgIGlmIG5vdCBkZXN0LmV4aXN0cygpOgogICAgICAgIGRlc3Qud3JpdGVfYnl0ZXMocmF3KQogICAgcmV0dXJuIHN0cihkZXN0LnJlbGF0aXZlX3RvKHNldHRpbmdzLkJBU0VfRElSKSksIGZpbGVfaGFzaAoKCmRlZiBydW5faW1wb3J0X2JhdGNoKAogICAgKiwKICAgIHVzZXIsCiAgICBtb2R1bG86IHN0ciwKICAgIHRpcG9faW1wb3J0YWNpb246IHN0ciwKICAgIHVwbG9hZGVkX2ZpbGU6IFVwbG9hZGVkRmlsZSwKICAgIHByZXByb2Nlc3M6IENhbGxhYmxlW1twZC5EYXRhRnJhbWVdLCBwZC5EYXRhRnJhbWVdIHwgTm9uZSA9IE5vbmUsCiAgICByb3dfaGFuZGxlcjogQ2FsbGFibGVbLi4uLCB0dXBsZVtib29sLCBib29sXSB8IE5vbmVdLAopIC0+IERhdGFJbXBvcnRCYXRjaDoKICAgICIiIgogICAgRWplY3V0YSBpbXBvcnRhY2nDs24gZmlsYSBhIGZpbGEuCiAgICByb3dfaGFuZGxlciByZXRvcm5hIChjcmVhZG8sIGFjdHVhbGl6YWRvKSBvIE5vbmUgc2kgaHVibyBlcnJvcmVzIGVuIHJvd19lcnJvcnMuCiAgICAiIiIKICAgIGFyY2hpdm9fcnV0YSwgYXJjaGl2b19oYXNoID0gc2F2ZV91cGxvYWRfY29weSh1cGxvYWRlZF9maWxlKQogICAgYmF0Y2ggPSBEYXRhSW1wb3J0QmF0Y2gub2JqZWN0cy5jcmVhdGUoCiAgICAgICAgbW9kdWxvPW1vZHVsbywKICAgICAgICB0aXBvX2ltcG9ydGFjaW9uPXRpcG9faW1wb3J0YWNpb24sCiAgICAgICAgYXJjaGl2b19ub21icmU9dXBsb2FkZWRfZmlsZS5uYW1lLAogICAgICAgIGFyY2hpdm9faGFzaD1hcmNoaXZvX2hhc2gsCiAgICAgICAgYXJjaGl2b19ydXRhPWFyY2hpdm9fcnV0YSwKICAgICAgICB1c3VhcmlvPXVzZXIsCiAgICAgICAgZXN0YWRvPURhdGFJbXBvcnRCYXRjaC5FU1RBRE9fUFJPQ0VTQU5ETywKICAgICkKICAgIGNyZWFkb3MgPSAwCiAgICBhY3R1YWxpemFkb3MgPSAwCiAgICBsb2dzOiBsaXN0W3N0cl0gPSBbXQoKICAgIHRyeToKICAgICAgICBkZiA9IHJlYWRfZGF0YWZyYW1lKHVwbG9hZGVkX2ZpbGUpCiAgICAgICAgaWYgcHJlcHJvY2VzczoKICAgICAgICAgICAgZGYgPSBwcmVwcm9jZXNzKGRmKQogICAgICAgIGJhdGNoLmZpbGFzX2xlaWRhcyA9IGxlbihkZikKCiAgICAgICAgZm9yIGlkeCwgcm93IGluIGRmLml0ZXJyb3dzKCk6CiAgICAgICAgICAgIGZpbGFfbnVtZXJvID0gaW50KGlkeCkgKyAyCiAgICAgICAgICAgIHJvd19lcnJvcnM6IGxpc3Rbc3RyXSA9IFtdCiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIHJlc3VsdCA9IHJvd19oYW5kbGVyKHJvdywgcm93X2Vycm9ycywgYmF0Y2gpCiAgICAgICAgICAgICAgICBpZiByb3dfZXJyb3JzOgogICAgICAgICAgICAgICAgICAgIGJhdGNoLmZpbGFzX2Vycm9yICs9IDEKICAgICAgICAgICAgICAgICAgICBmb3IgbXNnIGluIHJvd19lcnJvcnM6CiAgICAgICAgICAgICAgICAgICAgICAgIERhdGFJbXBvcnRFcnJvci5vYmplY3RzLmNyZWF0ZSgKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGJhdGNoPWJhdGNoLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgZmlsYV9udW1lcm89ZmlsYV9udW1lcm8sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBtZW5zYWplX2Vycm9yPW1zZywKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHBheWxvYWRfanNvbj1yb3dfdG9fanNvbihyb3cpLAogICAgICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAgICAgbG9ncy5hcHBlbmQoZiJGaWxhIHtmaWxhX251bWVyb306IHsnOyAnLmpvaW4ocm93X2Vycm9ycyl9IikKICAgICAgICAgICAgICAgIGVsaWYgcmVzdWx0IGlzIG5vdCBOb25lOgogICAgICAgICAgICAgICAgICAgIGNyZWF0ZWQsIHVwZGF0ZWQgPSByZXN1bHQKICAgICAgICAgICAgICAgICAgICBiYXRjaC5maWxhc192YWxpZGFzICs9IDEKICAgICAgICAgICAgICAgICAgICBpZiBjcmVhdGVkOgogICAgICAgICAgICAgICAgICAgICAgICBjcmVhZG9zICs9IDEKICAgICAgICAgICAgICAgICAgICBpZiB1cGRhdGVkOgogICAgICAgICAgICAgICAgICAgICAgICBhY3R1YWxpemFkb3MgKz0gMQogICAgICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgICAgICBiYXRjaC5maWxhc19lcnJvciArPSAxCiAgICAgICAgICAgICAgICAgICAgRGF0YUltcG9ydEVycm9yLm9iamVjdHMuY3JlYXRlKAogICAgICAgICAgICAgICAgICAgICAgICBiYXRjaD1iYXRjaCwKICAgICAgICAgICAgICAgICAgICAgICAgZmlsYV9udW1lcm89ZmlsYV9udW1lcm8sCiAgICAgICAgICAgICAgICAgICAgICAgIG1lbnNhamVfZXJyb3I9IkZpbGEgb21pdGlkYSBzaW4gZGV0YWxsZS4iLAogICAgICAgICAgICAgICAgICAgICAgICBwYXlsb2FkX2pzb249cm93X3RvX2pzb24ocm93KSwKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZXhjOgogICAgICAgICAgICAgICAgYmF0Y2guZmlsYXNfZXJyb3IgKz0gMQogICAgICAgICAgICAgICAgRGF0YUltcG9ydEVycm9yLm9iamVjdHMuY3JlYXRlKAogICAgICAgICAgICAgICAgICAgIGJhdGNoPWJhdGNoLAogICAgICAgICAgICAgICAgICAgIGZpbGFfbnVtZXJvPWZpbGFfbnVtZXJvLAogICAgICAgICAgICAgICAgICAgIG1lbnNhamVfZXJyb3I9c3RyKGV4YyksCiAgICAgICAgICAgICAgICAgICAgcGF5bG9hZF9qc29uPXJvd190b19qc29uKHJvdyksCiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBsb2dzLmFwcGVuZChmIkZpbGEge2ZpbGFfbnVtZXJvfToge2V4Y30iKQoKICAgICAgICBpZiBiYXRjaC5maWxhc19lcnJvciA9PSAwIGFuZCBiYXRjaC5maWxhc192YWxpZGFzID4gMDoKICAgICAgICAgICAgYmF0Y2guZXN0YWRvID0gRGF0YUltcG9ydEJhdGNoLkVTVEFET19PSwogICAgICAgIGVsaWYgYmF0Y2guZmlsYXNfdmFsaWRhcyA+IDA6CiAgICAgICAgICAgIGJhdGNoLmVzdGFkbyA9IERhdGFJbXBvcnRCYXRjaC5FU1RBRE9fUEFSQ0lBTAogICAgICAgIGVsaWYgYmF0Y2guZmlsYXNfbGVpZGFzID09IDA6CiAgICAgICAgICAgIGJhdGNoLmVzdGFkbyA9IERhdGFJbXBvcnRCYXRjaC5FU1RBRE9fRVJST1IKICAgICAgICAgICAgbG9ncy5hcHBlbmQoIk5vIHNlIGVuY29udHJhcm9uIGZpbGFzIHBhcmEgcHJvY2VzYXIuIikKICAgICAgICBlbHNlOgogICAgICAgICAgICBiYXRjaC5lc3RhZG8gPSBEYXRhSW1wb3J0QmF0Y2guRVNUQURPX0VSUk9SCgogICAgZXhjZXB0IEltcG9ydFZhbGlkYXRpb25FcnJvciBhcyBleGM6CiAgICAgICAgYmF0Y2guZXN0YWRvID0gRGF0YUltcG9ydEJhdGNoLkVTVEFET19FUlJPUgogICAgICAgIGxvZ3MuYXBwZW5kKHN0cihleGMpKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICAgICAgYmF0Y2guZXN0YWRvID0gRGF0YUltcG9ydEJhdGNoLkVTVEFET19FUlJPUgogICAgICAgIGxvZ3MuYXBwZW5kKGYiRXJyb3IgZ2VuZXJhbDoge2V4Y30iKQoKICAgIGJhdGNoLm9ic2VydmFjaW9uZXMgPSAoCiAgICAgICAgZiJDcmVhZG9zOiB7Y3JlYWRvc30sIEFjdHVhbGl6YWRvczoge2FjdHVhbGl6YWRvc30uICIKICAgICAgICArICgiIHwgIi5qb2luKGxvZ3NbOjIwXSkgaWYgbG9ncyBlbHNlICIiKQogICAgKVs6ODAwMF0KICAgIGJhdGNoLnNhdmUoKQogICAgcmV0dXJuIGJhdGNoCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/imports/columns.py
PATH_JSON="apps/core/imports/columns.py"
FILENAME=columns.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=66
SIZE_BYTES_UTF8=1915
CONTENT_SHA256=37e6ffc632187f1fa4d00aec819f2b751b8a4cd92faf90660239dab1fb563589
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Normalización de columnas y lectura de celdas."""

from __future__ import annotations

import re
import unicodedata
from decimal import Decimal, InvalidOperation

import pandas as pd

from .base import ImportValidationError, cell_str


def _norm_header(name: str) -> str:
    s = unicodedata.normalize("NFKD", str(name))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.strip().lower()
    s = re.sub(r"[^\w]+", "_", s)
    return s.strip("_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [_norm_header(c) for c in out.columns]
    return out


def pick(row: pd.Series, *aliases: str) -> str:
    for alias in aliases:
        key = _norm_header(alias)
        if key in row.index:
            val = cell_str(row.get(key))
            if val:
                return val
    return ""


def pick_decimal(row: pd.Series, *aliases: str, default: str = "0") -> Decimal:
    raw = pick(row, *aliases) or default
    try:
        cleaned = raw.replace(",", "").replace("Q", "").replace("$", "").strip()
        if cleaned in ("", "-", "nan"):
            return Decimal(default)
        return Decimal(cleaned)
    except (InvalidOperation, AttributeError):
        return Decimal(default)


def pick_int(row: pd.Series, *aliases: str, default: int = 0) -> int:
    try:
        return int(pick_decimal(row, *aliases, default=str(default)))
    except (ValueError, TypeError):
        return default


def require_any(df: pd.DataFrame, groups: list[list[str]]) -> None:
    cols = set(df.columns)
    missing_groups = []
    for group in groups:
        keys = {_norm_header(g) for g in group}
        if not keys.intersection(cols):
            missing_groups.append(" o ".join(group))
    if missing_groups:
        raise ImportValidationError(
            "Faltan columnas (al menos una por grupo): " + "; ".join(missing_groups)
        )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Normalización de columnas y lectura de celdas."""
00002|
00003|from __future__ import annotations
00004|
00005|import re
00006|import unicodedata
00007|from decimal import Decimal, InvalidOperation
00008|
00009|import pandas as pd
00010|
00011|from .base import ImportValidationError, cell_str
00012|
00013|
00014|def _norm_header(name: str) -> str:
00015|    s = unicodedata.normalize("NFKD", str(name))
00016|    s = "".join(c for c in s if not unicodedata.combining(c))
00017|    s = s.strip().lower()
00018|    s = re.sub(r"[^\w]+", "_", s)
00019|    return s.strip("_")
00020|
00021|
00022|def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
00023|    out = df.copy()
00024|    out.columns = [_norm_header(c) for c in out.columns]
00025|    return out
00026|
00027|
00028|def pick(row: pd.Series, *aliases: str) -> str:
00029|    for alias in aliases:
00030|        key = _norm_header(alias)
00031|        if key in row.index:
00032|            val = cell_str(row.get(key))
00033|            if val:
00034|                return val
00035|    return ""
00036|
00037|
00038|def pick_decimal(row: pd.Series, *aliases: str, default: str = "0") -> Decimal:
00039|    raw = pick(row, *aliases) or default
00040|    try:
00041|        cleaned = raw.replace(",", "").replace("Q", "").replace("$", "").strip()
00042|        if cleaned in ("", "-", "nan"):
00043|            return Decimal(default)
00044|        return Decimal(cleaned)
00045|    except (InvalidOperation, AttributeError):
00046|        return Decimal(default)
00047|
00048|
00049|def pick_int(row: pd.Series, *aliases: str, default: int = 0) -> int:
00050|    try:
00051|        return int(pick_decimal(row, *aliases, default=str(default)))
00052|    except (ValueError, TypeError):
00053|        return default
00054|
00055|
00056|def require_any(df: pd.DataFrame, groups: list[list[str]]) -> None:
00057|    cols = set(df.columns)
00058|    missing_groups = []
00059|    for group in groups:
00060|        keys = {_norm_header(g) for g in group}
00061|        if not keys.intersection(cols):
00062|            missing_groups.append(" o ".join(group))
00063|    if missing_groups:
00064|        raise ImportValidationError(
00065|            "Faltan columnas (al menos una por grupo): " + "; ".join(missing_groups)
00066|        )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiTm9ybWFsaXphY2nDs24gZGUgY29sdW1uYXMgeSBsZWN0dXJhIGRlIGNlbGRhcy4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmltcG9ydCByZQppbXBvcnQgdW5pY29kZWRhdGEKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsLCBJbnZhbGlkT3BlcmF0aW9uCgppbXBvcnQgcGFuZGFzIGFzIHBkCgpmcm9tIC5iYXNlIGltcG9ydCBJbXBvcnRWYWxpZGF0aW9uRXJyb3IsIGNlbGxfc3RyCgoKZGVmIF9ub3JtX2hlYWRlcihuYW1lOiBzdHIpIC0+IHN0cjoKICAgIHMgPSB1bmljb2RlZGF0YS5ub3JtYWxpemUoIk5GS0QiLCBzdHIobmFtZSkpCiAgICBzID0gIiIuam9pbihjIGZvciBjIGluIHMgaWYgbm90IHVuaWNvZGVkYXRhLmNvbWJpbmluZyhjKSkKICAgIHMgPSBzLnN0cmlwKCkubG93ZXIoKQogICAgcyA9IHJlLnN1YihyIlteXHddKyIsICJfIiwgcykKICAgIHJldHVybiBzLnN0cmlwKCJfIikKCgpkZWYgbm9ybWFsaXplX2NvbHVtbnMoZGY6IHBkLkRhdGFGcmFtZSkgLT4gcGQuRGF0YUZyYW1lOgogICAgb3V0ID0gZGYuY29weSgpCiAgICBvdXQuY29sdW1ucyA9IFtfbm9ybV9oZWFkZXIoYykgZm9yIGMgaW4gb3V0LmNvbHVtbnNdCiAgICByZXR1cm4gb3V0CgoKZGVmIHBpY2socm93OiBwZC5TZXJpZXMsICphbGlhc2VzOiBzdHIpIC0+IHN0cjoKICAgIGZvciBhbGlhcyBpbiBhbGlhc2VzOgogICAgICAgIGtleSA9IF9ub3JtX2hlYWRlcihhbGlhcykKICAgICAgICBpZiBrZXkgaW4gcm93LmluZGV4OgogICAgICAgICAgICB2YWwgPSBjZWxsX3N0cihyb3cuZ2V0KGtleSkpCiAgICAgICAgICAgIGlmIHZhbDoKICAgICAgICAgICAgICAgIHJldHVybiB2YWwKICAgIHJldHVybiAiIgoKCmRlZiBwaWNrX2RlY2ltYWwocm93OiBwZC5TZXJpZXMsICphbGlhc2VzOiBzdHIsIGRlZmF1bHQ6IHN0ciA9ICIwIikgLT4gRGVjaW1hbDoKICAgIHJhdyA9IHBpY2socm93LCAqYWxpYXNlcykgb3IgZGVmYXVsdAogICAgdHJ5OgogICAgICAgIGNsZWFuZWQgPSByYXcucmVwbGFjZSgiLCIsICIiKS5yZXBsYWNlKCJRIiwgIiIpLnJlcGxhY2UoIiQiLCAiIikuc3RyaXAoKQogICAgICAgIGlmIGNsZWFuZWQgaW4gKCIiLCAiLSIsICJuYW4iKToKICAgICAgICAgICAgcmV0dXJuIERlY2ltYWwoZGVmYXVsdCkKICAgICAgICByZXR1cm4gRGVjaW1hbChjbGVhbmVkKQogICAgZXhjZXB0IChJbnZhbGlkT3BlcmF0aW9uLCBBdHRyaWJ1dGVFcnJvcik6CiAgICAgICAgcmV0dXJuIERlY2ltYWwoZGVmYXVsdCkKCgpkZWYgcGlja19pbnQocm93OiBwZC5TZXJpZXMsICphbGlhc2VzOiBzdHIsIGRlZmF1bHQ6IGludCA9IDApIC0+IGludDoKICAgIHRyeToKICAgICAgICByZXR1cm4gaW50KHBpY2tfZGVjaW1hbChyb3csICphbGlhc2VzLCBkZWZhdWx0PXN0cihkZWZhdWx0KSkpCiAgICBleGNlcHQgKFZhbHVlRXJyb3IsIFR5cGVFcnJvcik6CiAgICAgICAgcmV0dXJuIGRlZmF1bHQKCgpkZWYgcmVxdWlyZV9hbnkoZGY6IHBkLkRhdGFGcmFtZSwgZ3JvdXBzOiBsaXN0W2xpc3Rbc3RyXV0pIC0+IE5vbmU6CiAgICBjb2xzID0gc2V0KGRmLmNvbHVtbnMpCiAgICBtaXNzaW5nX2dyb3VwcyA9IFtdCiAgICBmb3IgZ3JvdXAgaW4gZ3JvdXBzOgogICAgICAgIGtleXMgPSB7X25vcm1faGVhZGVyKGcpIGZvciBnIGluIGdyb3VwfQogICAgICAgIGlmIG5vdCBrZXlzLmludGVyc2VjdGlvbihjb2xzKToKICAgICAgICAgICAgbWlzc2luZ19ncm91cHMuYXBwZW5kKCIgbyAiLmpvaW4oZ3JvdXApKQogICAgaWYgbWlzc2luZ19ncm91cHM6CiAgICAgICAgcmFpc2UgSW1wb3J0VmFsaWRhdGlvbkVycm9yKAogICAgICAgICAgICAiRmFsdGFuIGNvbHVtbmFzIChhbCBtZW5vcyB1bmEgcG9yIGdydXBvKTogIiArICI7ICIuam9pbihtaXNzaW5nX2dyb3VwcykKICAgICAgICApCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/imports/entities.py
PATH_JSON="apps/core/imports/entities.py"
FILENAME=entities.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=136
SIZE_BYTES_UTF8=4217
CONTENT_SHA256=61a4609f01e510197c8fd842d5174a0689d5c81b3727896ed8f98f8866076718
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Resolución de entidades y unidades para importadores."""

from __future__ import annotations

import re

import pandas as pd

from apps.core.models import Contacto, Entidad, UnidadNegocio

from .columns import pick


def normalize_nit(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z]", "", value or "").upper()


def normalize_nombre(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def find_entidad(*, nit: str = "", nombre: str = "") -> Entidad | None:
    nit_clean = normalize_nit(nit)
    if nit_clean:
        entidad = Entidad.objects.filter(nit__iexact=nit_clean).first()
        if entidad:
            return entidad
        entidad = Entidad.objects.filter(nit__icontains=nit_clean[:20]).first()
        if entidad:
            return entidad
    nombre_clean = normalize_nombre(nombre)
    if nombre_clean:
        return Entidad.objects.filter(nombre__iexact=nombre_clean).first()
    return None


def upsert_entidad(
    *,
    nit: str = "",
    nombre: str,
    defaults: dict | None = None,
) -> tuple[Entidad, bool, bool]:
    """Retorna (entidad, creado, actualizado)."""
    defaults = defaults or {}
    nombre_clean = normalize_nombre(nombre)
    if not nombre_clean:
        raise ValueError("Nombre de entidad obligatorio.")
    nit_clean = normalize_nit(nit)
    entidad = find_entidad(nit=nit_clean, nombre=nombre_clean)
    field_defaults = {
        "nombre": nombre_clean,
        "activo": True,
        **defaults,
    }
    if nit_clean:
        field_defaults["nit"] = nit_clean
    if entidad:
        changed = False
        for key, value in field_defaults.items():
            if value and getattr(entidad, key) != value:
                setattr(entidad, key, value)
                changed = True
        if changed:
            entidad.save()
        return entidad, False, changed
    entidad = Entidad.objects.create(**field_defaults)
    return entidad, True, False


def resolve_unidad(code_or_name: str) -> UnidadNegocio | None:
    if not code_or_name:
        return None
    raw = code_or_name.strip()
    mapping = {
        "INVESTMENT - WC FACTORING": "FACTORING",
        "INVESTMENT - WC LEASING": "LEASING",
        "FACTORAJE": "FACTORING",
        "LEASING": "LEASING",
        "TI": "TI",
    }
    code = mapping.get(raw.upper(), raw.upper().replace(" ", "_")[:30])
    unidad = UnidadNegocio.objects.filter(codigo__iexact=code).first()
    if unidad:
        return unidad
    return UnidadNegocio.objects.filter(nombre__icontains=raw[:25]).first()


def upsert_contacto_from_row(entidad: Entidad, row: pd.Series) -> tuple[Contacto | None, bool]:
    contacto_nombre = pick(row, "contacto", "contacto_nombre", "nombre_contacto")
    if not contacto_nombre:
        return None, False
    email = pick(row, "email", "correo", "correo_electronico")
    defaults = {
        "nombre": contacto_nombre,
        "email": email,
        "telefono_movil": pick(row, "telefono", "tel", "celular", "telefono_movil"),
        "cargo": pick(row, "cargo", "puesto"),
        "activo": True,
    }
    if email:
        contacto, created = Contacto.objects.update_or_create(
            entidad=entidad,
            email=email,
            defaults=defaults,
        )
        return contacto, created
    contacto, created = Contacto.objects.update_or_create(
        entidad=entidad,
        nombre=contacto_nombre,
        defaults=defaults,
    )
    return contacto, created


def ensure_entidad_from_row(row: pd.Series, errors: list[str]) -> Entidad | None:
    nombre = pick(row, "nombre", "razon_social", "cliente", "nombre_cliente")
    nit = pick(row, "nit", "nit_cliente")
    if not nombre and not nit:
        errors.append("Falta nombre o NIT de entidad.")
        return None
    if not nombre:
        nombre = nit
    try:
        entidad, _, _ = upsert_entidad(
            nit=nit,
            nombre=nombre,
            defaults={
                "telefono": pick(row, "telefono", "tel"),
                "email": pick(row, "email", "correo"),
                "origen": "importacion",
            },
        )
        return entidad
    except ValueError as exc:
        errors.append(str(exc))
        return None

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Resolución de entidades y unidades para importadores."""
00002|
00003|from __future__ import annotations
00004|
00005|import re
00006|
00007|import pandas as pd
00008|
00009|from apps.core.models import Contacto, Entidad, UnidadNegocio
00010|
00011|from .columns import pick
00012|
00013|
00014|def normalize_nit(value: str) -> str:
00015|    return re.sub(r"[^0-9A-Za-z]", "", value or "").upper()
00016|
00017|
00018|def normalize_nombre(value: str) -> str:
00019|    return re.sub(r"\s+", " ", (value or "").strip())
00020|
00021|
00022|def find_entidad(*, nit: str = "", nombre: str = "") -> Entidad | None:
00023|    nit_clean = normalize_nit(nit)
00024|    if nit_clean:
00025|        entidad = Entidad.objects.filter(nit__iexact=nit_clean).first()
00026|        if entidad:
00027|            return entidad
00028|        entidad = Entidad.objects.filter(nit__icontains=nit_clean[:20]).first()
00029|        if entidad:
00030|            return entidad
00031|    nombre_clean = normalize_nombre(nombre)
00032|    if nombre_clean:
00033|        return Entidad.objects.filter(nombre__iexact=nombre_clean).first()
00034|    return None
00035|
00036|
00037|def upsert_entidad(
00038|    *,
00039|    nit: str = "",
00040|    nombre: str,
00041|    defaults: dict | None = None,
00042|) -> tuple[Entidad, bool, bool]:
00043|    """Retorna (entidad, creado, actualizado)."""
00044|    defaults = defaults or {}
00045|    nombre_clean = normalize_nombre(nombre)
00046|    if not nombre_clean:
00047|        raise ValueError("Nombre de entidad obligatorio.")
00048|    nit_clean = normalize_nit(nit)
00049|    entidad = find_entidad(nit=nit_clean, nombre=nombre_clean)
00050|    field_defaults = {
00051|        "nombre": nombre_clean,
00052|        "activo": True,
00053|        **defaults,
00054|    }
00055|    if nit_clean:
00056|        field_defaults["nit"] = nit_clean
00057|    if entidad:
00058|        changed = False
00059|        for key, value in field_defaults.items():
00060|            if value and getattr(entidad, key) != value:
00061|                setattr(entidad, key, value)
00062|                changed = True
00063|        if changed:
00064|            entidad.save()
00065|        return entidad, False, changed
00066|    entidad = Entidad.objects.create(**field_defaults)
00067|    return entidad, True, False
00068|
00069|
00070|def resolve_unidad(code_or_name: str) -> UnidadNegocio | None:
00071|    if not code_or_name:
00072|        return None
00073|    raw = code_or_name.strip()
00074|    mapping = {
00075|        "INVESTMENT - WC FACTORING": "FACTORING",
00076|        "INVESTMENT - WC LEASING": "LEASING",
00077|        "FACTORAJE": "FACTORING",
00078|        "LEASING": "LEASING",
00079|        "TI": "TI",
00080|    }
00081|    code = mapping.get(raw.upper(), raw.upper().replace(" ", "_")[:30])
00082|    unidad = UnidadNegocio.objects.filter(codigo__iexact=code).first()
00083|    if unidad:
00084|        return unidad
00085|    return UnidadNegocio.objects.filter(nombre__icontains=raw[:25]).first()
00086|
00087|
00088|def upsert_contacto_from_row(entidad: Entidad, row: pd.Series) -> tuple[Contacto | None, bool]:
00089|    contacto_nombre = pick(row, "contacto", "contacto_nombre", "nombre_contacto")
00090|    if not contacto_nombre:
00091|        return None, False
00092|    email = pick(row, "email", "correo", "correo_electronico")
00093|    defaults = {
00094|        "nombre": contacto_nombre,
00095|        "email": email,
00096|        "telefono_movil": pick(row, "telefono", "tel", "celular", "telefono_movil"),
00097|        "cargo": pick(row, "cargo", "puesto"),
00098|        "activo": True,
00099|    }
00100|    if email:
00101|        contacto, created = Contacto.objects.update_or_create(
00102|            entidad=entidad,
00103|            email=email,
00104|            defaults=defaults,
00105|        )
00106|        return contacto, created
00107|    contacto, created = Contacto.objects.update_or_create(
00108|        entidad=entidad,
00109|        nombre=contacto_nombre,
00110|        defaults=defaults,
00111|    )
00112|    return contacto, created
00113|
00114|
00115|def ensure_entidad_from_row(row: pd.Series, errors: list[str]) -> Entidad | None:
00116|    nombre = pick(row, "nombre", "razon_social", "cliente", "nombre_cliente")
00117|    nit = pick(row, "nit", "nit_cliente")
00118|    if not nombre and not nit:
00119|        errors.append("Falta nombre o NIT de entidad.")
00120|        return None
00121|    if not nombre:
00122|        nombre = nit
00123|    try:
00124|        entidad, _, _ = upsert_entidad(
00125|            nit=nit,
00126|            nombre=nombre,
00127|            defaults={
00128|                "telefono": pick(row, "telefono", "tel"),
00129|                "email": pick(row, "email", "correo"),
00130|                "origen": "importacion",
00131|            },
00132|        )
00133|        return entidad
00134|    except ValueError as exc:
00135|        errors.append(str(exc))
00136|        return None

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiUmVzb2x1Y2nDs24gZGUgZW50aWRhZGVzIHkgdW5pZGFkZXMgcGFyYSBpbXBvcnRhZG9yZXMuIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgppbXBvcnQgcmUKCmltcG9ydCBwYW5kYXMgYXMgcGQKCmZyb20gYXBwcy5jb3JlLm1vZGVscyBpbXBvcnQgQ29udGFjdG8sIEVudGlkYWQsIFVuaWRhZE5lZ29jaW8KCmZyb20gLmNvbHVtbnMgaW1wb3J0IHBpY2sKCgpkZWYgbm9ybWFsaXplX25pdCh2YWx1ZTogc3RyKSAtPiBzdHI6CiAgICByZXR1cm4gcmUuc3ViKHIiW14wLTlBLVphLXpdIiwgIiIsIHZhbHVlIG9yICIiKS51cHBlcigpCgoKZGVmIG5vcm1hbGl6ZV9ub21icmUodmFsdWU6IHN0cikgLT4gc3RyOgogICAgcmV0dXJuIHJlLnN1YihyIlxzKyIsICIgIiwgKHZhbHVlIG9yICIiKS5zdHJpcCgpKQoKCmRlZiBmaW5kX2VudGlkYWQoKiwgbml0OiBzdHIgPSAiIiwgbm9tYnJlOiBzdHIgPSAiIikgLT4gRW50aWRhZCB8IE5vbmU6CiAgICBuaXRfY2xlYW4gPSBub3JtYWxpemVfbml0KG5pdCkKICAgIGlmIG5pdF9jbGVhbjoKICAgICAgICBlbnRpZGFkID0gRW50aWRhZC5vYmplY3RzLmZpbHRlcihuaXRfX2lleGFjdD1uaXRfY2xlYW4pLmZpcnN0KCkKICAgICAgICBpZiBlbnRpZGFkOgogICAgICAgICAgICByZXR1cm4gZW50aWRhZAogICAgICAgIGVudGlkYWQgPSBFbnRpZGFkLm9iamVjdHMuZmlsdGVyKG5pdF9faWNvbnRhaW5zPW5pdF9jbGVhbls6MjBdKS5maXJzdCgpCiAgICAgICAgaWYgZW50aWRhZDoKICAgICAgICAgICAgcmV0dXJuIGVudGlkYWQKICAgIG5vbWJyZV9jbGVhbiA9IG5vcm1hbGl6ZV9ub21icmUobm9tYnJlKQogICAgaWYgbm9tYnJlX2NsZWFuOgogICAgICAgIHJldHVybiBFbnRpZGFkLm9iamVjdHMuZmlsdGVyKG5vbWJyZV9faWV4YWN0PW5vbWJyZV9jbGVhbikuZmlyc3QoKQogICAgcmV0dXJuIE5vbmUKCgpkZWYgdXBzZXJ0X2VudGlkYWQoCiAgICAqLAogICAgbml0OiBzdHIgPSAiIiwKICAgIG5vbWJyZTogc3RyLAogICAgZGVmYXVsdHM6IGRpY3QgfCBOb25lID0gTm9uZSwKKSAtPiB0dXBsZVtFbnRpZGFkLCBib29sLCBib29sXToKICAgICIiIlJldG9ybmEgKGVudGlkYWQsIGNyZWFkbywgYWN0dWFsaXphZG8pLiIiIgogICAgZGVmYXVsdHMgPSBkZWZhdWx0cyBvciB7fQogICAgbm9tYnJlX2NsZWFuID0gbm9ybWFsaXplX25vbWJyZShub21icmUpCiAgICBpZiBub3Qgbm9tYnJlX2NsZWFuOgogICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIk5vbWJyZSBkZSBlbnRpZGFkIG9ibGlnYXRvcmlvLiIpCiAgICBuaXRfY2xlYW4gPSBub3JtYWxpemVfbml0KG5pdCkKICAgIGVudGlkYWQgPSBmaW5kX2VudGlkYWQobml0PW5pdF9jbGVhbiwgbm9tYnJlPW5vbWJyZV9jbGVhbikKICAgIGZpZWxkX2RlZmF1bHRzID0gewogICAgICAgICJub21icmUiOiBub21icmVfY2xlYW4sCiAgICAgICAgImFjdGl2byI6IFRydWUsCiAgICAgICAgKipkZWZhdWx0cywKICAgIH0KICAgIGlmIG5pdF9jbGVhbjoKICAgICAgICBmaWVsZF9kZWZhdWx0c1sibml0Il0gPSBuaXRfY2xlYW4KICAgIGlmIGVudGlkYWQ6CiAgICAgICAgY2hhbmdlZCA9IEZhbHNlCiAgICAgICAgZm9yIGtleSwgdmFsdWUgaW4gZmllbGRfZGVmYXVsdHMuaXRlbXMoKToKICAgICAgICAgICAgaWYgdmFsdWUgYW5kIGdldGF0dHIoZW50aWRhZCwga2V5KSAhPSB2YWx1ZToKICAgICAgICAgICAgICAgIHNldGF0dHIoZW50aWRhZCwga2V5LCB2YWx1ZSkKICAgICAgICAgICAgICAgIGNoYW5nZWQgPSBUcnVlCiAgICAgICAgaWYgY2hhbmdlZDoKICAgICAgICAgICAgZW50aWRhZC5zYXZlKCkKICAgICAgICByZXR1cm4gZW50aWRhZCwgRmFsc2UsIGNoYW5nZWQKICAgIGVudGlkYWQgPSBFbnRpZGFkLm9iamVjdHMuY3JlYXRlKCoqZmllbGRfZGVmYXVsdHMpCiAgICByZXR1cm4gZW50aWRhZCwgVHJ1ZSwgRmFsc2UKCgpkZWYgcmVzb2x2ZV91bmlkYWQoY29kZV9vcl9uYW1lOiBzdHIpIC0+IFVuaWRhZE5lZ29jaW8gfCBOb25lOgogICAgaWYgbm90IGNvZGVfb3JfbmFtZToKICAgICAgICByZXR1cm4gTm9uZQogICAgcmF3ID0gY29kZV9vcl9uYW1lLnN0cmlwKCkKICAgIG1hcHBpbmcgPSB7CiAgICAgICAgIklOVkVTVE1FTlQgLSBXQyBGQUNUT1JJTkciOiAiRkFDVE9SSU5HIiwKICAgICAgICAiSU5WRVNUTUVOVCAtIFdDIExFQVNJTkciOiAiTEVBU0lORyIsCiAgICAgICAgIkZBQ1RPUkFKRSI6ICJGQUNUT1JJTkciLAogICAgICAgICJMRUFTSU5HIjogIkxFQVNJTkciLAogICAgICAgICJUSSI6ICJUSSIsCiAgICB9CiAgICBjb2RlID0gbWFwcGluZy5nZXQocmF3LnVwcGVyKCksIHJhdy51cHBlcigpLnJlcGxhY2UoIiAiLCAiXyIpWzozMF0pCiAgICB1bmlkYWQgPSBVbmlkYWROZWdvY2lvLm9iamVjdHMuZmlsdGVyKGNvZGlnb19faWV4YWN0PWNvZGUpLmZpcnN0KCkKICAgIGlmIHVuaWRhZDoKICAgICAgICByZXR1cm4gdW5pZGFkCiAgICByZXR1cm4gVW5pZGFkTmVnb2Npby5vYmplY3RzLmZpbHRlcihub21icmVfX2ljb250YWlucz1yYXdbOjI1XSkuZmlyc3QoKQoKCmRlZiB1cHNlcnRfY29udGFjdG9fZnJvbV9yb3coZW50aWRhZDogRW50aWRhZCwgcm93OiBwZC5TZXJpZXMpIC0+IHR1cGxlW0NvbnRhY3RvIHwgTm9uZSwgYm9vbF06CiAgICBjb250YWN0b19ub21icmUgPSBwaWNrKHJvdywgImNvbnRhY3RvIiwgImNvbnRhY3RvX25vbWJyZSIsICJub21icmVfY29udGFjdG8iKQogICAgaWYgbm90IGNvbnRhY3RvX25vbWJyZToKICAgICAgICByZXR1cm4gTm9uZSwgRmFsc2UKICAgIGVtYWlsID0gcGljayhyb3csICJlbWFpbCIsICJjb3JyZW8iLCAiY29ycmVvX2VsZWN0cm9uaWNvIikKICAgIGRlZmF1bHRzID0gewogICAgICAgICJub21icmUiOiBjb250YWN0b19ub21icmUsCiAgICAgICAgImVtYWlsIjogZW1haWwsCiAgICAgICAgInRlbGVmb25vX21vdmlsIjogcGljayhyb3csICJ0ZWxlZm9ubyIsICJ0ZWwiLCAiY2VsdWxhciIsICJ0ZWxlZm9ub19tb3ZpbCIpLAogICAgICAgICJjYXJnbyI6IHBpY2socm93LCAiY2FyZ28iLCAicHVlc3RvIiksCiAgICAgICAgImFjdGl2byI6IFRydWUsCiAgICB9CiAgICBpZiBlbWFpbDoKICAgICAgICBjb250YWN0bywgY3JlYXRlZCA9IENvbnRhY3RvLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgZW50aWRhZD1lbnRpZGFkLAogICAgICAgICAgICBlbWFpbD1lbWFpbCwKICAgICAgICAgICAgZGVmYXVsdHM9ZGVmYXVsdHMsCiAgICAgICAgKQogICAgICAgIHJldHVybiBjb250YWN0bywgY3JlYXRlZAogICAgY29udGFjdG8sIGNyZWF0ZWQgPSBDb250YWN0by5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgZW50aWRhZD1lbnRpZGFkLAogICAgICAgIG5vbWJyZT1jb250YWN0b19ub21icmUsCiAgICAgICAgZGVmYXVsdHM9ZGVmYXVsdHMsCiAgICApCiAgICByZXR1cm4gY29udGFjdG8sIGNyZWF0ZWQKCgpkZWYgZW5zdXJlX2VudGlkYWRfZnJvbV9yb3cocm93OiBwZC5TZXJpZXMsIGVycm9yczogbGlzdFtzdHJdKSAtPiBFbnRpZGFkIHwgTm9uZToKICAgIG5vbWJyZSA9IHBpY2socm93LCAibm9tYnJlIiwgInJhem9uX3NvY2lhbCIsICJjbGllbnRlIiwgIm5vbWJyZV9jbGllbnRlIikKICAgIG5pdCA9IHBpY2socm93LCAibml0IiwgIm5pdF9jbGllbnRlIikKICAgIGlmIG5vdCBub21icmUgYW5kIG5vdCBuaXQ6CiAgICAgICAgZXJyb3JzLmFwcGVuZCgiRmFsdGEgbm9tYnJlIG8gTklUIGRlIGVudGlkYWQuIikKICAgICAgICByZXR1cm4gTm9uZQogICAgaWYgbm90IG5vbWJyZToKICAgICAgICBub21icmUgPSBuaXQKICAgIHRyeToKICAgICAgICBlbnRpZGFkLCBfLCBfID0gdXBzZXJ0X2VudGlkYWQoCiAgICAgICAgICAgIG5pdD1uaXQsCiAgICAgICAgICAgIG5vbWJyZT1ub21icmUsCiAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICJ0ZWxlZm9ubyI6IHBpY2socm93LCAidGVsZWZvbm8iLCAidGVsIiksCiAgICAgICAgICAgICAgICAiZW1haWwiOiBwaWNrKHJvdywgImVtYWlsIiwgImNvcnJlbyIpLAogICAgICAgICAgICAgICAgIm9yaWdlbiI6ICJpbXBvcnRhY2lvbiIsCiAgICAgICAgICAgIH0sCiAgICAgICAgKQogICAgICAgIHJldHVybiBlbnRpZGFkCiAgICBleGNlcHQgVmFsdWVFcnJvciBhcyBleGM6CiAgICAgICAgZXJyb3JzLmFwcGVuZChzdHIoZXhjKSkKICAgICAgICByZXR1cm4gTm9uZQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/management/__init__.py
PATH_JSON="apps/core/management/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/management/commands/__init__.py
PATH_JSON="apps/core/management/commands/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/management/commands/seed_wcg_demo.py
PATH_JSON="apps/core/management/commands/seed_wcg_demo.py"
FILENAME=seed_wcg_demo.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=369
SIZE_BYTES_UTF8=15043
CONTENT_SHA256=dd220508c3f1b117b7f04526b1440be77d3a9e14eb2dc01ad136c4771310ccfb
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""
Carga datos demo coherentes para presentación gerencial de WCG One.

Uso:
    python manage.py seed_wcg_demo
    python manage.py seed_wcg_demo --fresh   # elimina datos marcados origen=demo y re-siembra
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.core.models import (
    Contacto,
    DataImportBatch,
    Entidad,
    Producto,
    RelacionEntidadProducto,
    UnidadNegocio,
)
from apps.crm.models import Interaccion, Tarea
from apps.pgo.models import PgoTicket
from apps.risk.models import EstadoFinanciero, RiskAlerta, RiskOperacion, RiskOperationSnapshot

User = get_user_model()
DEMO_ORIGIN = "demo"


class Command(BaseCommand):
    help = "Sembra datos demo para CRM, Risk y PGO (presentación interna)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Elimina registros con origen=demo antes de sembrar de nuevo.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["fresh"]:
            self._clear_demo()
        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        self.stdout.write("Sembrando datos demo WCG One...")
        unidades = self._seed_unidades()
        productos = self._seed_productos(unidades)
        entidades = self._seed_entidades()
        self._seed_contactos(entidades)
        self._seed_relaciones(entidades, productos, unidades)
        self._seed_crm(entidades, user)
        batches = self._seed_import_batches(user)
        operaciones = self._seed_risk(entidades, productos, unidades, batches.get("risk"))
        self._seed_eeff(entidades, batches.get("risk"))
        self._seed_alertas(entidades, operaciones)
        self._seed_tickets(unidades, user, batches.get("pgo"))
        self.stdout.write(
            self.style.SUCCESS(
                f"Demo OK — entidades: {Entidad.objects.filter(origen=DEMO_ORIGIN).count()}, "
                f"snapshots: {RiskOperationSnapshot.objects.count()}, "
                f"tickets: {PgoTicket.objects.filter(ticket_externo_id__startswith='TI-DEMO').count()}"
            )
        )

    def _clear_demo(self):
        PgoTicket.objects.filter(ticket_externo_id__startswith="TI-DEMO").delete()
        RiskOperationSnapshot.objects.filter(archivo_origen="demo_seed").delete()
        RiskOperacion.objects.filter(
            codigo_operacion__in=["PG01260302", "LG01260115", "FC01260288"]
        ).delete()
        RiskAlerta.objects.filter(origen=DEMO_ORIGIN).delete()
        EstadoFinanciero.objects.filter(observaciones__icontains="demo").delete()
        Interaccion.objects.filter(notas__icontains="demo").delete()
        Tarea.objects.filter(notas__icontains="demo").delete()
        DataImportBatch.objects.filter(archivo_hash__startswith="demo_seed_").delete()
        Entidad.objects.filter(origen=DEMO_ORIGIN).delete()
        self.stdout.write("Datos demo previos eliminados.")

    def _seed_unidades(self):
        data = [
            ("LEASING", "Leasing", 1),
            ("FACTORING", "Factoraje", 2),
            ("TI", "Tecnología", 3),
            ("INSURANCE", "Insurance", 4),
            ("INVESTMENT", "Inversiones", 5),
        ]
        out = {}
        for codigo, nombre, orden in data:
            obj, _ = UnidadNegocio.objects.update_or_create(
                codigo=codigo,
                defaults={"nombre": nombre, "activa": True, "orden": orden},
            )
            out[codigo] = obj
        return out

    def _seed_productos(self, unidades):
        data = [
            ("LEASING", "Leasing operativo", "LEASING"),
            ("FACTORING", "Factoraje comercial", "FACTORING"),
        ]
        out = {}
        for codigo, nombre, un_code in data:
            obj, _ = Producto.objects.update_or_create(
                codigo=codigo,
                defaults={"nombre": nombre, "activo": True},
            )
            out[codigo] = obj
        return out

    def _seed_entidades(self):
        data = [
            ("9852115", "VICENTE SOLER MUNGUÍA", "Guatemala", "medio"),
            ("12345678", "Distribuidora Me Llega, S.A.", "Quetzaltenango", "bajo"),
            ("87654321", "Ingenio Palo Gordo, S.A.", "Escuintla", "alto"),
            ("55667789", "Helvetia Centroamérica", "Ciudad de Guatemala", "bajo"),
            ("99887765", "Corporación Mogori", "Mixco", "medio"),
        ]
        out = {}
        for nit, nombre, ciudad, riesgo in data:
            obj, _ = Entidad.objects.update_or_create(
                nit=nit,
                defaults={
                    "nombre": nombre,
                    "tipo_entidad": Entidad.TIPO_CLIENTE,
                    "ciudad": ciudad,
                    "categoria_riesgo": riesgo,
                    "pais": "Guatemala",
                    "activo": True,
                    "origen": DEMO_ORIGIN,
                    "email": f"contacto@{nit[:6]}.demo.gt",
                    "telefono": "5025550101",
                },
            )
            out[nit] = obj
        return out

    def _seed_contactos(self, entidades):
        samples = [
            ("9852115", "María Soler", "maria.soler@demo.gt", "Gerente General"),
            ("12345678", "Juan Pérez", "jperez@demo.gt", "CFO"),
            ("87654321", "Ana Morales", "ana.morales@demo.gt", "Tesorería"),
            ("55667789", "Carlos Ruiz", "cruiz@demo.gt", "Director Comercial"),
        ]
        for nit, nombre, email, cargo in samples:
            ent = entidades[nit]
            Contacto.objects.update_or_create(
                entidad=ent,
                email=email,
                defaults={
                    "nombre": nombre,
                    "cargo": cargo,
                    "es_contacto_operativo": True,
                    "activo": True,
                },
            )

    def _seed_relaciones(self, entidades, productos, unidades):
        pairs = [
            ("9852115", "LEASING", "LEASING"),
            ("87654321", "LEASING", "LEASING"),
            ("12345678", "FACTORING", "FACTORING"),
        ]
        for nit, prod_code, un_code in pairs:
            RelacionEntidadProducto.objects.update_or_create(
                entidad=entidades[nit],
                producto=productos[prod_code],
                defaults={
                    "unidad_negocio": unidades[un_code],
                    "estado": "activo",
                    "moneda": "GTQ",
                },
            )

    def _seed_crm(self, entidades, user):
        ent = entidades["9852115"]
        Interaccion.objects.update_or_create(
            entidad=ent,
            resumen="Revisión cartera leasing Q2",
            defaults={
                "fecha": date.today() - timedelta(days=5),
                "tipo_interaccion": "reunion",
                "resultado": "Cliente confirma envío de EEFF.",
                "usuario": user,
                "notas": "Registro demo",
            },
        )
        Interaccion.objects.update_or_create(
            entidad=entidades["87654321"],
            resumen="Llamada seguimiento mora",
            defaults={
                "fecha": date.today() - timedelta(days=2),
                "tipo_interaccion": "llamada",
                "resultado": "Compromiso de pago parcial.",
                "seguimiento_requerido": True,
                "usuario": user,
                "notas": "Registro demo",
            },
        )
        Tarea.objects.update_or_create(
            entidad=ent,
            descripcion="Enviar estados financieros actualizados",
            defaults={
                "fecha_limite": date.today() + timedelta(days=7),
                "estado": "pendiente",
                "prioridad": "alta",
                "asignado_a": user,
                "notas": "Tarea demo",
            },
        )
        Tarea.objects.update_or_create(
            entidad=entidades["12345678"],
            descripcion="Agendar visita comercial factoraje",
            defaults={
                "fecha_limite": date.today() + timedelta(days=14),
                "estado": "pendiente",
                "prioridad": "media",
                "notas": "Tarea demo",
            },
        )

    def _seed_import_batches(self, user):
        specs = [
            ("demo_seed_crm", "crm", "entidades_clientes", "demo_crm_entidades.csv", 5),
            ("demo_seed_risk", "risk", "snapshots_leasing", "demo_leasing_mayo.xlsx", 8),
            ("demo_seed_pgo", "pgo", "tickets", "demo_tickets_ti.xlsx", 12),
        ]
        batches = {}
        for hash_key, modulo, tipo, nombre, validas in specs:
            batch, _ = DataImportBatch.objects.update_or_create(
                archivo_hash=hash_key,
                defaults={
                    "modulo": modulo,
                    "tipo_importacion": tipo,
                    "archivo_nombre": nombre,
                    "archivo_ruta": "uploads/demo",
                    "usuario": user,
                    "filas_leidas": validas,
                    "filas_validas": validas,
                    "filas_error": 0,
                    "estado": DataImportBatch.ESTADO_OK,
                    "observaciones": "Lote simulado — seed_wcg_demo",
                },
            )
            batches[modulo] = batch
        return batches

    def _seed_risk(self, entidades, productos, unidades, batch):
        ops_data = [
            ("9852115", "PG01260302", "LEASING", 45, Decimal("125000"), Decimal("42000")),
            ("87654321", "LG01260115", "LEASING", 62, Decimal("890000"), Decimal("120000")),
            ("12345678", "FC01260288", "FACTORING", 0, Decimal("55000"), Decimal("0")),
        ]
        operaciones = {}
        for nit, codigo_op, prod, mora, capital, vencido in ops_data:
            ent = entidades[nit]
            op, _ = RiskOperacion.objects.update_or_create(
                entidad=ent,
                codigo_operacion=codigo_op,
                defaults={
                    "producto": productos[prod],
                    "unidad_negocio": unidades[prod],
                    "moneda": "GTQ",
                    "estado": "vigente",
                    "notas": "Operación demo",
                },
            )
            operaciones[codigo_op] = op
            for offset, mora_i, vencido_i in [(60, max(mora - 15, 0), max(vencido - 5000, 0)), (30, mora, vencido)]:
                snap_date = date(2026, 5, 31) - timedelta(days=offset)
                RiskOperationSnapshot.objects.update_or_create(
                    operacion=op,
                    fecha_snapshot=snap_date,
                    defaults={
                        "entidad": ent,
                        "estado_operacion": "vigente",
                        "producto_nombre_raw": prod.title(),
                        "capital_balance": capital,
                        "past_due_balance": vencido_i,
                        "due_days": mora_i,
                        "monthly_rent": Decimal("8500"),
                        "archivo_origen": "demo_seed",
                        "import_batch": batch,
                    },
                )
        return operaciones

    def _seed_eeff(self, entidades, batch):
        cuts = [
            ("9852115", date(2025, 12, 31), Decimal("2500000"), Decimal("180000")),
            ("87654321", date(2025, 12, 31), Decimal("8900000"), Decimal("420000")),
        ]
        for nit, corte, ventas, utilidad in cuts:
            EstadoFinanciero.objects.update_or_create(
                entidad=entidades[nit],
                fecha_corte=corte,
                defaults={
                    "ventas": ventas,
                    "utilidad_neta": utilidad,
                    "patrimonio": ventas * Decimal("0.35"),
                    "ebitda": utilidad * Decimal("1.2"),
                    "observaciones": "EEFF demo",
                    "import_batch": batch,
                },
            )

    def _seed_alertas(self, entidades, operaciones):
        op = operaciones.get("LG01260115")
        if not op:
            return
        RiskAlerta.objects.update_or_create(
            entidad=entidades["87654321"],
            operacion=op,
            tipo_alerta="mora",
            defaults={
                "fecha_alerta": date.today(),
                "severidad": "alta",
                "mensaje": "Días de atraso superiores a 60 — seguimiento cobranza.",
                "activa": True,
                "origen": DEMO_ORIGIN,
            },
        )

    def _seed_tickets(self, unidades, user, batch):
        now = timezone.now()
        samples = [
            ("TI-DEMO-001", "VPN no conecta", "cerrado", "alta", 18, True),
            ("TI-DEMO-002", "Nuevo usuario CRM", "cerrado", "media", 36, True),
            ("TI-DEMO-003", "Impresora piso 3", "en_proceso", "baja", None, False),
            ("TI-DEMO-004", "Error reporte PGO", "abierto", "alta", None, False),
            ("TI-DEMO-005", "Correo bloqueado", "cerrado", "media", 40, True),
            ("TI-DEMO-006", "Acceso Balón de Riesgo", "cerrado", "media", 12, True),
            ("TI-DEMO-007", "Lentitud de red", "en_proceso", "alta", None, False),
            ("TI-DEMO-008", "Backup fallido", "abierto", "alta", None, False),
        ]
        for i, (tid, titulo, estado, prioridad, horas, sla_ok) in enumerate(samples):
            apertura = now - timedelta(days=20 - i)
            cierre = apertura + timedelta(hours=horas) if horas else None
            if estado == "cerrado" and not cierre:
                cierre = apertura + timedelta(hours=24)
            duracion = Decimal(str(horas)) if horas else None
            PgoTicket.objects.update_or_create(
                ticket_externo_id=tid,
                defaults={
                    "titulo": titulo,
                    "estado_raw": estado.upper(),
                    "estado_normalizado": estado,
                    "prioridad": prioridad,
                    "departamento": "Tecnología",
                    "sistema": "Helpdesk WCG",
                    "usuario_solicita": "Usuario demo",
                    "correo_solicita": "usuario@wcg.demo.gt",
                    "fecha_apertura": apertura,
                    "fecha_cierre": cierre,
                    "fecha_registro": apertura,
                    "anio_mes": apertura.strftime("%Y-%m"),
                    "duracion_horas": duracion,
                    "sla_horas": Decimal("48"),
                    "sla_cumplido": sla_ok,
                    "unidad_negocio": unidades["TI"],
                    "responsable": user,
                    "import_batch": batch,
                    "solucion": "Resuelto en demo" if estado == "cerrado" else "",
                },
            )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Carga datos demo coherentes para presentación gerencial de WCG One.
00003|
00004|Uso:
00005|    python manage.py seed_wcg_demo
00006|    python manage.py seed_wcg_demo --fresh   # elimina datos marcados origen=demo y re-siembra
00007|"""
00008|
00009|from __future__ import annotations
00010|
00011|from datetime import date, timedelta
00012|from decimal import Decimal
00013|
00014|from django.contrib.auth import get_user_model
00015|from django.core.management.base import BaseCommand
00016|from django.db import transaction
00017|from django.utils import timezone
00018|
00019|from apps.core.models import (
00020|    Contacto,
00021|    DataImportBatch,
00022|    Entidad,
00023|    Producto,
00024|    RelacionEntidadProducto,
00025|    UnidadNegocio,
00026|)
00027|from apps.crm.models import Interaccion, Tarea
00028|from apps.pgo.models import PgoTicket
00029|from apps.risk.models import EstadoFinanciero, RiskAlerta, RiskOperacion, RiskOperationSnapshot
00030|
00031|User = get_user_model()
00032|DEMO_ORIGIN = "demo"
00033|
00034|
00035|class Command(BaseCommand):
00036|    help = "Sembra datos demo para CRM, Risk y PGO (presentación interna)"
00037|
00038|    def add_arguments(self, parser):
00039|        parser.add_argument(
00040|            "--fresh",
00041|            action="store_true",
00042|            help="Elimina registros con origen=demo antes de sembrar de nuevo.",
00043|        )
00044|
00045|    @transaction.atomic
00046|    def handle(self, *args, **options):
00047|        if options["fresh"]:
00048|            self._clear_demo()
00049|        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
00050|        self.stdout.write("Sembrando datos demo WCG One...")
00051|        unidades = self._seed_unidades()
00052|        productos = self._seed_productos(unidades)
00053|        entidades = self._seed_entidades()
00054|        self._seed_contactos(entidades)
00055|        self._seed_relaciones(entidades, productos, unidades)
00056|        self._seed_crm(entidades, user)
00057|        batches = self._seed_import_batches(user)
00058|        operaciones = self._seed_risk(entidades, productos, unidades, batches.get("risk"))
00059|        self._seed_eeff(entidades, batches.get("risk"))
00060|        self._seed_alertas(entidades, operaciones)
00061|        self._seed_tickets(unidades, user, batches.get("pgo"))
00062|        self.stdout.write(
00063|            self.style.SUCCESS(
00064|                f"Demo OK — entidades: {Entidad.objects.filter(origen=DEMO_ORIGIN).count()}, "
00065|                f"snapshots: {RiskOperationSnapshot.objects.count()}, "
00066|                f"tickets: {PgoTicket.objects.filter(ticket_externo_id__startswith='TI-DEMO').count()}"
00067|            )
00068|        )
00069|
00070|    def _clear_demo(self):
00071|        PgoTicket.objects.filter(ticket_externo_id__startswith="TI-DEMO").delete()
00072|        RiskOperationSnapshot.objects.filter(archivo_origen="demo_seed").delete()
00073|        RiskOperacion.objects.filter(
00074|            codigo_operacion__in=["PG01260302", "LG01260115", "FC01260288"]
00075|        ).delete()
00076|        RiskAlerta.objects.filter(origen=DEMO_ORIGIN).delete()
00077|        EstadoFinanciero.objects.filter(observaciones__icontains="demo").delete()
00078|        Interaccion.objects.filter(notas__icontains="demo").delete()
00079|        Tarea.objects.filter(notas__icontains="demo").delete()
00080|        DataImportBatch.objects.filter(archivo_hash__startswith="demo_seed_").delete()
00081|        Entidad.objects.filter(origen=DEMO_ORIGIN).delete()
00082|        self.stdout.write("Datos demo previos eliminados.")
00083|
00084|    def _seed_unidades(self):
00085|        data = [
00086|            ("LEASING", "Leasing", 1),
00087|            ("FACTORING", "Factoraje", 2),
00088|            ("TI", "Tecnología", 3),
00089|            ("INSURANCE", "Insurance", 4),
00090|            ("INVESTMENT", "Inversiones", 5),
00091|        ]
00092|        out = {}
00093|        for codigo, nombre, orden in data:
00094|            obj, _ = UnidadNegocio.objects.update_or_create(
00095|                codigo=codigo,
00096|                defaults={"nombre": nombre, "activa": True, "orden": orden},
00097|            )
00098|            out[codigo] = obj
00099|        return out
00100|
00101|    def _seed_productos(self, unidades):
00102|        data = [
00103|            ("LEASING", "Leasing operativo", "LEASING"),
00104|            ("FACTORING", "Factoraje comercial", "FACTORING"),
00105|        ]
00106|        out = {}
00107|        for codigo, nombre, un_code in data:
00108|            obj, _ = Producto.objects.update_or_create(
00109|                codigo=codigo,
00110|                defaults={"nombre": nombre, "activo": True},
00111|            )
00112|            out[codigo] = obj
00113|        return out
00114|
00115|    def _seed_entidades(self):
00116|        data = [
00117|            ("9852115", "VICENTE SOLER MUNGUÍA", "Guatemala", "medio"),
00118|            ("12345678", "Distribuidora Me Llega, S.A.", "Quetzaltenango", "bajo"),
00119|            ("87654321", "Ingenio Palo Gordo, S.A.", "Escuintla", "alto"),
00120|            ("55667789", "Helvetia Centroamérica", "Ciudad de Guatemala", "bajo"),
00121|            ("99887765", "Corporación Mogori", "Mixco", "medio"),
00122|        ]
00123|        out = {}
00124|        for nit, nombre, ciudad, riesgo in data:
00125|            obj, _ = Entidad.objects.update_or_create(
00126|                nit=nit,
00127|                defaults={
00128|                    "nombre": nombre,
00129|                    "tipo_entidad": Entidad.TIPO_CLIENTE,
00130|                    "ciudad": ciudad,
00131|                    "categoria_riesgo": riesgo,
00132|                    "pais": "Guatemala",
00133|                    "activo": True,
00134|                    "origen": DEMO_ORIGIN,
00135|                    "email": f"contacto@{nit[:6]}.demo.gt",
00136|                    "telefono": "5025550101",
00137|                },
00138|            )
00139|            out[nit] = obj
00140|        return out
00141|
00142|    def _seed_contactos(self, entidades):
00143|        samples = [
00144|            ("9852115", "María Soler", "maria.soler@demo.gt", "Gerente General"),
00145|            ("12345678", "Juan Pérez", "jperez@demo.gt", "CFO"),
00146|            ("87654321", "Ana Morales", "ana.morales@demo.gt", "Tesorería"),
00147|            ("55667789", "Carlos Ruiz", "cruiz@demo.gt", "Director Comercial"),
00148|        ]
00149|        for nit, nombre, email, cargo in samples:
00150|            ent = entidades[nit]
00151|            Contacto.objects.update_or_create(
00152|                entidad=ent,
00153|                email=email,
00154|                defaults={
00155|                    "nombre": nombre,
00156|                    "cargo": cargo,
00157|                    "es_contacto_operativo": True,
00158|                    "activo": True,
00159|                },
00160|            )
00161|
00162|    def _seed_relaciones(self, entidades, productos, unidades):
00163|        pairs = [
00164|            ("9852115", "LEASING", "LEASING"),
00165|            ("87654321", "LEASING", "LEASING"),
00166|            ("12345678", "FACTORING", "FACTORING"),
00167|        ]
00168|        for nit, prod_code, un_code in pairs:
00169|            RelacionEntidadProducto.objects.update_or_create(
00170|                entidad=entidades[nit],
00171|                producto=productos[prod_code],
00172|                defaults={
00173|                    "unidad_negocio": unidades[un_code],
00174|                    "estado": "activo",
00175|                    "moneda": "GTQ",
00176|                },
00177|            )
00178|
00179|    def _seed_crm(self, entidades, user):
00180|        ent = entidades["9852115"]
00181|        Interaccion.objects.update_or_create(
00182|            entidad=ent,
00183|            resumen="Revisión cartera leasing Q2",
00184|            defaults={
00185|                "fecha": date.today() - timedelta(days=5),
00186|                "tipo_interaccion": "reunion",
00187|                "resultado": "Cliente confirma envío de EEFF.",
00188|                "usuario": user,
00189|                "notas": "Registro demo",
00190|            },
00191|        )
00192|        Interaccion.objects.update_or_create(
00193|            entidad=entidades["87654321"],
00194|            resumen="Llamada seguimiento mora",
00195|            defaults={
00196|                "fecha": date.today() - timedelta(days=2),
00197|                "tipo_interaccion": "llamada",
00198|                "resultado": "Compromiso de pago parcial.",
00199|                "seguimiento_requerido": True,
00200|                "usuario": user,
00201|                "notas": "Registro demo",
00202|            },
00203|        )
00204|        Tarea.objects.update_or_create(
00205|            entidad=ent,
00206|            descripcion="Enviar estados financieros actualizados",
00207|            defaults={
00208|                "fecha_limite": date.today() + timedelta(days=7),
00209|                "estado": "pendiente",
00210|                "prioridad": "alta",
00211|                "asignado_a": user,
00212|                "notas": "Tarea demo",
00213|            },
00214|        )
00215|        Tarea.objects.update_or_create(
00216|            entidad=entidades["12345678"],
00217|            descripcion="Agendar visita comercial factoraje",
00218|            defaults={
00219|                "fecha_limite": date.today() + timedelta(days=14),
00220|                "estado": "pendiente",
00221|                "prioridad": "media",
00222|                "notas": "Tarea demo",
00223|            },
00224|        )
00225|
00226|    def _seed_import_batches(self, user):
00227|        specs = [
00228|            ("demo_seed_crm", "crm", "entidades_clientes", "demo_crm_entidades.csv", 5),
00229|            ("demo_seed_risk", "risk", "snapshots_leasing", "demo_leasing_mayo.xlsx", 8),
00230|            ("demo_seed_pgo", "pgo", "tickets", "demo_tickets_ti.xlsx", 12),
00231|        ]
00232|        batches = {}
00233|        for hash_key, modulo, tipo, nombre, validas in specs:
00234|            batch, _ = DataImportBatch.objects.update_or_create(
00235|                archivo_hash=hash_key,
00236|                defaults={
00237|                    "modulo": modulo,
00238|                    "tipo_importacion": tipo,
00239|                    "archivo_nombre": nombre,
00240|                    "archivo_ruta": "uploads/demo",
00241|                    "usuario": user,
00242|                    "filas_leidas": validas,
00243|                    "filas_validas": validas,
00244|                    "filas_error": 0,
00245|                    "estado": DataImportBatch.ESTADO_OK,
00246|                    "observaciones": "Lote simulado — seed_wcg_demo",
00247|                },
00248|            )
00249|            batches[modulo] = batch
00250|        return batches
00251|
00252|    def _seed_risk(self, entidades, productos, unidades, batch):
00253|        ops_data = [
00254|            ("9852115", "PG01260302", "LEASING", 45, Decimal("125000"), Decimal("42000")),
00255|            ("87654321", "LG01260115", "LEASING", 62, Decimal("890000"), Decimal("120000")),
00256|            ("12345678", "FC01260288", "FACTORING", 0, Decimal("55000"), Decimal("0")),
00257|        ]
00258|        operaciones = {}
00259|        for nit, codigo_op, prod, mora, capital, vencido in ops_data:
00260|            ent = entidades[nit]
00261|            op, _ = RiskOperacion.objects.update_or_create(
00262|                entidad=ent,
00263|                codigo_operacion=codigo_op,
00264|                defaults={
00265|                    "producto": productos[prod],
00266|                    "unidad_negocio": unidades[prod],
00267|                    "moneda": "GTQ",
00268|                    "estado": "vigente",
00269|                    "notas": "Operación demo",
00270|                },
00271|            )
00272|            operaciones[codigo_op] = op
00273|            for offset, mora_i, vencido_i in [(60, max(mora - 15, 0), max(vencido - 5000, 0)), (30, mora, vencido)]:
00274|                snap_date = date(2026, 5, 31) - timedelta(days=offset)
00275|                RiskOperationSnapshot.objects.update_or_create(
00276|                    operacion=op,
00277|                    fecha_snapshot=snap_date,
00278|                    defaults={
00279|                        "entidad": ent,
00280|                        "estado_operacion": "vigente",
00281|                        "producto_nombre_raw": prod.title(),
00282|                        "capital_balance": capital,
00283|                        "past_due_balance": vencido_i,
00284|                        "due_days": mora_i,
00285|                        "monthly_rent": Decimal("8500"),
00286|                        "archivo_origen": "demo_seed",
00287|                        "import_batch": batch,
00288|                    },
00289|                )
00290|        return operaciones
00291|
00292|    def _seed_eeff(self, entidades, batch):
00293|        cuts = [
00294|            ("9852115", date(2025, 12, 31), Decimal("2500000"), Decimal("180000")),
00295|            ("87654321", date(2025, 12, 31), Decimal("8900000"), Decimal("420000")),
00296|        ]
00297|        for nit, corte, ventas, utilidad in cuts:
00298|            EstadoFinanciero.objects.update_or_create(
00299|                entidad=entidades[nit],
00300|                fecha_corte=corte,
00301|                defaults={
00302|                    "ventas": ventas,
00303|                    "utilidad_neta": utilidad,
00304|                    "patrimonio": ventas * Decimal("0.35"),
00305|                    "ebitda": utilidad * Decimal("1.2"),
00306|                    "observaciones": "EEFF demo",
00307|                    "import_batch": batch,
00308|                },
00309|            )
00310|
00311|    def _seed_alertas(self, entidades, operaciones):
00312|        op = operaciones.get("LG01260115")
00313|        if not op:
00314|            return
00315|        RiskAlerta.objects.update_or_create(
00316|            entidad=entidades["87654321"],
00317|            operacion=op,
00318|            tipo_alerta="mora",
00319|            defaults={
00320|                "fecha_alerta": date.today(),
00321|                "severidad": "alta",
00322|                "mensaje": "Días de atraso superiores a 60 — seguimiento cobranza.",
00323|                "activa": True,
00324|                "origen": DEMO_ORIGIN,
00325|            },
00326|        )
00327|
00328|    def _seed_tickets(self, unidades, user, batch):
00329|        now = timezone.now()
00330|        samples = [
00331|            ("TI-DEMO-001", "VPN no conecta", "cerrado", "alta", 18, True),
00332|            ("TI-DEMO-002", "Nuevo usuario CRM", "cerrado", "media", 36, True),
00333|            ("TI-DEMO-003", "Impresora piso 3", "en_proceso", "baja", None, False),
00334|            ("TI-DEMO-004", "Error reporte PGO", "abierto", "alta", None, False),
00335|            ("TI-DEMO-005", "Correo bloqueado", "cerrado", "media", 40, True),
00336|            ("TI-DEMO-006", "Acceso Balón de Riesgo", "cerrado", "media", 12, True),
00337|            ("TI-DEMO-007", "Lentitud de red", "en_proceso", "alta", None, False),
00338|            ("TI-DEMO-008", "Backup fallido", "abierto", "alta", None, False),
00339|        ]
00340|        for i, (tid, titulo, estado, prioridad, horas, sla_ok) in enumerate(samples):
00341|            apertura = now - timedelta(days=20 - i)
00342|            cierre = apertura + timedelta(hours=horas) if horas else None
00343|            if estado == "cerrado" and not cierre:
00344|                cierre = apertura + timedelta(hours=24)
00345|            duracion = Decimal(str(horas)) if horas else None
00346|            PgoTicket.objects.update_or_create(
00347|                ticket_externo_id=tid,
00348|                defaults={
00349|                    "titulo": titulo,
00350|                    "estado_raw": estado.upper(),
00351|                    "estado_normalizado": estado,
00352|                    "prioridad": prioridad,
00353|                    "departamento": "Tecnología",
00354|                    "sistema": "Helpdesk WCG",
00355|                    "usuario_solicita": "Usuario demo",
00356|                    "correo_solicita": "usuario@wcg.demo.gt",
00357|                    "fecha_apertura": apertura,
00358|                    "fecha_cierre": cierre,
00359|                    "fecha_registro": apertura,
00360|                    "anio_mes": apertura.strftime("%Y-%m"),
00361|                    "duracion_horas": duracion,
00362|                    "sla_horas": Decimal("48"),
00363|                    "sla_cumplido": sla_ok,
00364|                    "unidad_negocio": unidades["TI"],
00365|                    "responsable": user,
00366|                    "import_batch": batch,
00367|                    "solucion": "Resuelto en demo" if estado == "cerrado" else "",
00368|                },
00369|            )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCkNhcmdhIGRhdG9zIGRlbW8gY29oZXJlbnRlcyBwYXJhIHByZXNlbnRhY2nDs24gZ2VyZW5jaWFsIGRlIFdDRyBPbmUuCgpVc286CiAgICBweXRob24gbWFuYWdlLnB5IHNlZWRfd2NnX2RlbW8KICAgIHB5dGhvbiBtYW5hZ2UucHkgc2VlZF93Y2dfZGVtbyAtLWZyZXNoICAgIyBlbGltaW5hIGRhdG9zIG1hcmNhZG9zIG9yaWdlbj1kZW1vIHkgcmUtc2llbWJyYQoiIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gZGF0ZXRpbWUgaW1wb3J0IGRhdGUsIHRpbWVkZWx0YQpmcm9tIGRlY2ltYWwgaW1wb3J0IERlY2ltYWwKCmZyb20gZGphbmdvLmNvbnRyaWIuYXV0aCBpbXBvcnQgZ2V0X3VzZXJfbW9kZWwKZnJvbSBkamFuZ28uY29yZS5tYW5hZ2VtZW50LmJhc2UgaW1wb3J0IEJhc2VDb21tYW5kCmZyb20gZGphbmdvLmRiIGltcG9ydCB0cmFuc2FjdGlvbgpmcm9tIGRqYW5nby51dGlscyBpbXBvcnQgdGltZXpvbmUKCmZyb20gYXBwcy5jb3JlLm1vZGVscyBpbXBvcnQgKAogICAgQ29udGFjdG8sCiAgICBEYXRhSW1wb3J0QmF0Y2gsCiAgICBFbnRpZGFkLAogICAgUHJvZHVjdG8sCiAgICBSZWxhY2lvbkVudGlkYWRQcm9kdWN0bywKICAgIFVuaWRhZE5lZ29jaW8sCikKZnJvbSBhcHBzLmNybS5tb2RlbHMgaW1wb3J0IEludGVyYWNjaW9uLCBUYXJlYQpmcm9tIGFwcHMucGdvLm1vZGVscyBpbXBvcnQgUGdvVGlja2V0CmZyb20gYXBwcy5yaXNrLm1vZGVscyBpbXBvcnQgRXN0YWRvRmluYW5jaWVybywgUmlza0FsZXJ0YSwgUmlza09wZXJhY2lvbiwgUmlza09wZXJhdGlvblNuYXBzaG90CgpVc2VyID0gZ2V0X3VzZXJfbW9kZWwoKQpERU1PX09SSUdJTiA9ICJkZW1vIgoKCmNsYXNzIENvbW1hbmQoQmFzZUNvbW1hbmQpOgogICAgaGVscCA9ICJTZW1icmEgZGF0b3MgZGVtbyBwYXJhIENSTSwgUmlzayB5IFBHTyAocHJlc2VudGFjacOzbiBpbnRlcm5hKSIKCiAgICBkZWYgYWRkX2FyZ3VtZW50cyhzZWxmLCBwYXJzZXIpOgogICAgICAgIHBhcnNlci5hZGRfYXJndW1lbnQoCiAgICAgICAgICAgICItLWZyZXNoIiwKICAgICAgICAgICAgYWN0aW9uPSJzdG9yZV90cnVlIiwKICAgICAgICAgICAgaGVscD0iRWxpbWluYSByZWdpc3Ryb3MgY29uIG9yaWdlbj1kZW1vIGFudGVzIGRlIHNlbWJyYXIgZGUgbnVldm8uIiwKICAgICAgICApCgogICAgQHRyYW5zYWN0aW9uLmF0b21pYwogICAgZGVmIGhhbmRsZShzZWxmLCAqYXJncywgKipvcHRpb25zKToKICAgICAgICBpZiBvcHRpb25zWyJmcmVzaCJdOgogICAgICAgICAgICBzZWxmLl9jbGVhcl9kZW1vKCkKICAgICAgICB1c2VyID0gVXNlci5vYmplY3RzLmZpbHRlcihpc19zdXBlcnVzZXI9VHJ1ZSkuZmlyc3QoKSBvciBVc2VyLm9iamVjdHMuZmlyc3QoKQogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKCJTZW1icmFuZG8gZGF0b3MgZGVtbyBXQ0cgT25lLi4uIikKICAgICAgICB1bmlkYWRlcyA9IHNlbGYuX3NlZWRfdW5pZGFkZXMoKQogICAgICAgIHByb2R1Y3RvcyA9IHNlbGYuX3NlZWRfcHJvZHVjdG9zKHVuaWRhZGVzKQogICAgICAgIGVudGlkYWRlcyA9IHNlbGYuX3NlZWRfZW50aWRhZGVzKCkKICAgICAgICBzZWxmLl9zZWVkX2NvbnRhY3RvcyhlbnRpZGFkZXMpCiAgICAgICAgc2VsZi5fc2VlZF9yZWxhY2lvbmVzKGVudGlkYWRlcywgcHJvZHVjdG9zLCB1bmlkYWRlcykKICAgICAgICBzZWxmLl9zZWVkX2NybShlbnRpZGFkZXMsIHVzZXIpCiAgICAgICAgYmF0Y2hlcyA9IHNlbGYuX3NlZWRfaW1wb3J0X2JhdGNoZXModXNlcikKICAgICAgICBvcGVyYWNpb25lcyA9IHNlbGYuX3NlZWRfcmlzayhlbnRpZGFkZXMsIHByb2R1Y3RvcywgdW5pZGFkZXMsIGJhdGNoZXMuZ2V0KCJyaXNrIikpCiAgICAgICAgc2VsZi5fc2VlZF9lZWZmKGVudGlkYWRlcywgYmF0Y2hlcy5nZXQoInJpc2siKSkKICAgICAgICBzZWxmLl9zZWVkX2FsZXJ0YXMoZW50aWRhZGVzLCBvcGVyYWNpb25lcykKICAgICAgICBzZWxmLl9zZWVkX3RpY2tldHModW5pZGFkZXMsIHVzZXIsIGJhdGNoZXMuZ2V0KCJwZ28iKSkKICAgICAgICBzZWxmLnN0ZG91dC53cml0ZSgKICAgICAgICAgICAgc2VsZi5zdHlsZS5TVUNDRVNTKAogICAgICAgICAgICAgICAgZiJEZW1vIE9LIOKAlCBlbnRpZGFkZXM6IHtFbnRpZGFkLm9iamVjdHMuZmlsdGVyKG9yaWdlbj1ERU1PX09SSUdJTikuY291bnQoKX0sICIKICAgICAgICAgICAgICAgIGYic25hcHNob3RzOiB7Umlza09wZXJhdGlvblNuYXBzaG90Lm9iamVjdHMuY291bnQoKX0sICIKICAgICAgICAgICAgICAgIGYidGlja2V0czoge1Bnb1RpY2tldC5vYmplY3RzLmZpbHRlcih0aWNrZXRfZXh0ZXJub19pZF9fc3RhcnRzd2l0aD0nVEktREVNTycpLmNvdW50KCl9IgogICAgICAgICAgICApCiAgICAgICAgKQoKICAgIGRlZiBfY2xlYXJfZGVtbyhzZWxmKToKICAgICAgICBQZ29UaWNrZXQub2JqZWN0cy5maWx0ZXIodGlja2V0X2V4dGVybm9faWRfX3N0YXJ0c3dpdGg9IlRJLURFTU8iKS5kZWxldGUoKQogICAgICAgIFJpc2tPcGVyYXRpb25TbmFwc2hvdC5vYmplY3RzLmZpbHRlcihhcmNoaXZvX29yaWdlbj0iZGVtb19zZWVkIikuZGVsZXRlKCkKICAgICAgICBSaXNrT3BlcmFjaW9uLm9iamVjdHMuZmlsdGVyKAogICAgICAgICAgICBjb2RpZ29fb3BlcmFjaW9uX19pbj1bIlBHMDEyNjAzMDIiLCAiTEcwMTI2MDExNSIsICJGQzAxMjYwMjg4Il0KICAgICAgICApLmRlbGV0ZSgpCiAgICAgICAgUmlza0FsZXJ0YS5vYmplY3RzLmZpbHRlcihvcmlnZW49REVNT19PUklHSU4pLmRlbGV0ZSgpCiAgICAgICAgRXN0YWRvRmluYW5jaWVyby5vYmplY3RzLmZpbHRlcihvYnNlcnZhY2lvbmVzX19pY29udGFpbnM9ImRlbW8iKS5kZWxldGUoKQogICAgICAgIEludGVyYWNjaW9uLm9iamVjdHMuZmlsdGVyKG5vdGFzX19pY29udGFpbnM9ImRlbW8iKS5kZWxldGUoKQogICAgICAgIFRhcmVhLm9iamVjdHMuZmlsdGVyKG5vdGFzX19pY29udGFpbnM9ImRlbW8iKS5kZWxldGUoKQogICAgICAgIERhdGFJbXBvcnRCYXRjaC5vYmplY3RzLmZpbHRlcihhcmNoaXZvX2hhc2hfX3N0YXJ0c3dpdGg9ImRlbW9fc2VlZF8iKS5kZWxldGUoKQogICAgICAgIEVudGlkYWQub2JqZWN0cy5maWx0ZXIob3JpZ2VuPURFTU9fT1JJR0lOKS5kZWxldGUoKQogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKCJEYXRvcyBkZW1vIHByZXZpb3MgZWxpbWluYWRvcy4iKQoKICAgIGRlZiBfc2VlZF91bmlkYWRlcyhzZWxmKToKICAgICAgICBkYXRhID0gWwogICAgICAgICAgICAoIkxFQVNJTkciLCAiTGVhc2luZyIsIDEpLAogICAgICAgICAgICAoIkZBQ1RPUklORyIsICJGYWN0b3JhamUiLCAyKSwKICAgICAgICAgICAgKCJUSSIsICJUZWNub2xvZ8OtYSIsIDMpLAogICAgICAgICAgICAoIklOU1VSQU5DRSIsICJJbnN1cmFuY2UiLCA0KSwKICAgICAgICAgICAgKCJJTlZFU1RNRU5UIiwgIkludmVyc2lvbmVzIiwgNSksCiAgICAgICAgXQogICAgICAgIG91dCA9IHt9CiAgICAgICAgZm9yIGNvZGlnbywgbm9tYnJlLCBvcmRlbiBpbiBkYXRhOgogICAgICAgICAgICBvYmosIF8gPSBVbmlkYWROZWdvY2lvLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgIGNvZGlnbz1jb2RpZ28sCiAgICAgICAgICAgICAgICBkZWZhdWx0cz17Im5vbWJyZSI6IG5vbWJyZSwgImFjdGl2YSI6IFRydWUsICJvcmRlbiI6IG9yZGVufSwKICAgICAgICAgICAgKQogICAgICAgICAgICBvdXRbY29kaWdvXSA9IG9iagogICAgICAgIHJldHVybiBvdXQKCiAgICBkZWYgX3NlZWRfcHJvZHVjdG9zKHNlbGYsIHVuaWRhZGVzKToKICAgICAgICBkYXRhID0gWwogICAgICAgICAgICAoIkxFQVNJTkciLCAiTGVhc2luZyBvcGVyYXRpdm8iLCAiTEVBU0lORyIpLAogICAgICAgICAgICAoIkZBQ1RPUklORyIsICJGYWN0b3JhamUgY29tZXJjaWFsIiwgIkZBQ1RPUklORyIpLAogICAgICAgIF0KICAgICAgICBvdXQgPSB7fQogICAgICAgIGZvciBjb2RpZ28sIG5vbWJyZSwgdW5fY29kZSBpbiBkYXRhOgogICAgICAgICAgICBvYmosIF8gPSBQcm9kdWN0by5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBjb2RpZ289Y29kaWdvLAogICAgICAgICAgICAgICAgZGVmYXVsdHM9eyJub21icmUiOiBub21icmUsICJhY3Rpdm8iOiBUcnVlfSwKICAgICAgICAgICAgKQogICAgICAgICAgICBvdXRbY29kaWdvXSA9IG9iagogICAgICAgIHJldHVybiBvdXQKCiAgICBkZWYgX3NlZWRfZW50aWRhZGVzKHNlbGYpOgogICAgICAgIGRhdGEgPSBbCiAgICAgICAgICAgICgiOTg1MjExNSIsICJWSUNFTlRFIFNPTEVSIE1VTkdVw41BIiwgIkd1YXRlbWFsYSIsICJtZWRpbyIpLAogICAgICAgICAgICAoIjEyMzQ1Njc4IiwgIkRpc3RyaWJ1aWRvcmEgTWUgTGxlZ2EsIFMuQS4iLCAiUXVldHphbHRlbmFuZ28iLCAiYmFqbyIpLAogICAgICAgICAgICAoIjg3NjU0MzIxIiwgIkluZ2VuaW8gUGFsbyBHb3JkbywgUy5BLiIsICJFc2N1aW50bGEiLCAiYWx0byIpLAogICAgICAgICAgICAoIjU1NjY3Nzg5IiwgIkhlbHZldGlhIENlbnRyb2Ftw6lyaWNhIiwgIkNpdWRhZCBkZSBHdWF0ZW1hbGEiLCAiYmFqbyIpLAogICAgICAgICAgICAoIjk5ODg3NzY1IiwgIkNvcnBvcmFjacOzbiBNb2dvcmkiLCAiTWl4Y28iLCAibWVkaW8iKSwKICAgICAgICBdCiAgICAgICAgb3V0ID0ge30KICAgICAgICBmb3Igbml0LCBub21icmUsIGNpdWRhZCwgcmllc2dvIGluIGRhdGE6CiAgICAgICAgICAgIG9iaiwgXyA9IEVudGlkYWQub2JqZWN0cy51cGRhdGVfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgbml0PW5pdCwKICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICAgICAibm9tYnJlIjogbm9tYnJlLAogICAgICAgICAgICAgICAgICAgICJ0aXBvX2VudGlkYWQiOiBFbnRpZGFkLlRJUE9fQ0xJRU5URSwKICAgICAgICAgICAgICAgICAgICAiY2l1ZGFkIjogY2l1ZGFkLAogICAgICAgICAgICAgICAgICAgICJjYXRlZ29yaWFfcmllc2dvIjogcmllc2dvLAogICAgICAgICAgICAgICAgICAgICJwYWlzIjogIkd1YXRlbWFsYSIsCiAgICAgICAgICAgICAgICAgICAgImFjdGl2byI6IFRydWUsCiAgICAgICAgICAgICAgICAgICAgIm9yaWdlbiI6IERFTU9fT1JJR0lOLAogICAgICAgICAgICAgICAgICAgICJlbWFpbCI6IGYiY29udGFjdG9Ae25pdFs6Nl19LmRlbW8uZ3QiLAogICAgICAgICAgICAgICAgICAgICJ0ZWxlZm9ubyI6ICI1MDI1NTUwMTAxIiwKICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICkKICAgICAgICAgICAgb3V0W25pdF0gPSBvYmoKICAgICAgICByZXR1cm4gb3V0CgogICAgZGVmIF9zZWVkX2NvbnRhY3RvcyhzZWxmLCBlbnRpZGFkZXMpOgogICAgICAgIHNhbXBsZXMgPSBbCiAgICAgICAgICAgICgiOTg1MjExNSIsICJNYXLDrWEgU29sZXIiLCAibWFyaWEuc29sZXJAZGVtby5ndCIsICJHZXJlbnRlIEdlbmVyYWwiKSwKICAgICAgICAgICAgKCIxMjM0NTY3OCIsICJKdWFuIFDDqXJleiIsICJqcGVyZXpAZGVtby5ndCIsICJDRk8iKSwKICAgICAgICAgICAgKCI4NzY1NDMyMSIsICJBbmEgTW9yYWxlcyIsICJhbmEubW9yYWxlc0BkZW1vLmd0IiwgIlRlc29yZXLDrWEiKSwKICAgICAgICAgICAgKCI1NTY2Nzc4OSIsICJDYXJsb3MgUnVpeiIsICJjcnVpekBkZW1vLmd0IiwgIkRpcmVjdG9yIENvbWVyY2lhbCIpLAogICAgICAgIF0KICAgICAgICBmb3Igbml0LCBub21icmUsIGVtYWlsLCBjYXJnbyBpbiBzYW1wbGVzOgogICAgICAgICAgICBlbnQgPSBlbnRpZGFkZXNbbml0XQogICAgICAgICAgICBDb250YWN0by5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBlbnRpZGFkPWVudCwKICAgICAgICAgICAgICAgIGVtYWlsPWVtYWlsLAogICAgICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgICAgICJub21icmUiOiBub21icmUsCiAgICAgICAgICAgICAgICAgICAgImNhcmdvIjogY2FyZ28sCiAgICAgICAgICAgICAgICAgICAgImVzX2NvbnRhY3RvX29wZXJhdGl2byI6IFRydWUsCiAgICAgICAgICAgICAgICAgICAgImFjdGl2byI6IFRydWUsCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICApCgogICAgZGVmIF9zZWVkX3JlbGFjaW9uZXMoc2VsZiwgZW50aWRhZGVzLCBwcm9kdWN0b3MsIHVuaWRhZGVzKToKICAgICAgICBwYWlycyA9IFsKICAgICAgICAgICAgKCI5ODUyMTE1IiwgIkxFQVNJTkciLCAiTEVBU0lORyIpLAogICAgICAgICAgICAoIjg3NjU0MzIxIiwgIkxFQVNJTkciLCAiTEVBU0lORyIpLAogICAgICAgICAgICAoIjEyMzQ1Njc4IiwgIkZBQ1RPUklORyIsICJGQUNUT1JJTkciKSwKICAgICAgICBdCiAgICAgICAgZm9yIG5pdCwgcHJvZF9jb2RlLCB1bl9jb2RlIGluIHBhaXJzOgogICAgICAgICAgICBSZWxhY2lvbkVudGlkYWRQcm9kdWN0by5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBlbnRpZGFkPWVudGlkYWRlc1tuaXRdLAogICAgICAgICAgICAgICAgcHJvZHVjdG89cHJvZHVjdG9zW3Byb2RfY29kZV0sCiAgICAgICAgICAgICAgICBkZWZhdWx0cz17CiAgICAgICAgICAgICAgICAgICAgInVuaWRhZF9uZWdvY2lvIjogdW5pZGFkZXNbdW5fY29kZV0sCiAgICAgICAgICAgICAgICAgICAgImVzdGFkbyI6ICJhY3Rpdm8iLAogICAgICAgICAgICAgICAgICAgICJtb25lZGEiOiAiR1RRIiwKICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICkKCiAgICBkZWYgX3NlZWRfY3JtKHNlbGYsIGVudGlkYWRlcywgdXNlcik6CiAgICAgICAgZW50ID0gZW50aWRhZGVzWyI5ODUyMTE1Il0KICAgICAgICBJbnRlcmFjY2lvbi5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgIGVudGlkYWQ9ZW50LAogICAgICAgICAgICByZXN1bWVuPSJSZXZpc2nDs24gY2FydGVyYSBsZWFzaW5nIFEyIiwKICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgImZlY2hhIjogZGF0ZS50b2RheSgpIC0gdGltZWRlbHRhKGRheXM9NSksCiAgICAgICAgICAgICAgICAidGlwb19pbnRlcmFjY2lvbiI6ICJyZXVuaW9uIiwKICAgICAgICAgICAgICAgICJyZXN1bHRhZG8iOiAiQ2xpZW50ZSBjb25maXJtYSBlbnbDrW8gZGUgRUVGRi4iLAogICAgICAgICAgICAgICAgInVzdWFyaW8iOiB1c2VyLAogICAgICAgICAgICAgICAgIm5vdGFzIjogIlJlZ2lzdHJvIGRlbW8iLAogICAgICAgICAgICB9LAogICAgICAgICkKICAgICAgICBJbnRlcmFjY2lvbi5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgIGVudGlkYWQ9ZW50aWRhZGVzWyI4NzY1NDMyMSJdLAogICAgICAgICAgICByZXN1bWVuPSJMbGFtYWRhIHNlZ3VpbWllbnRvIG1vcmEiLAogICAgICAgICAgICBkZWZhdWx0cz17CiAgICAgICAgICAgICAgICAiZmVjaGEiOiBkYXRlLnRvZGF5KCkgLSB0aW1lZGVsdGEoZGF5cz0yKSwKICAgICAgICAgICAgICAgICJ0aXBvX2ludGVyYWNjaW9uIjogImxsYW1hZGEiLAogICAgICAgICAgICAgICAgInJlc3VsdGFkbyI6ICJDb21wcm9taXNvIGRlIHBhZ28gcGFyY2lhbC4iLAogICAgICAgICAgICAgICAgInNlZ3VpbWllbnRvX3JlcXVlcmlkbyI6IFRydWUsCiAgICAgICAgICAgICAgICAidXN1YXJpbyI6IHVzZXIsCiAgICAgICAgICAgICAgICAibm90YXMiOiAiUmVnaXN0cm8gZGVtbyIsCiAgICAgICAgICAgIH0sCiAgICAgICAgKQogICAgICAgIFRhcmVhLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgZW50aWRhZD1lbnQsCiAgICAgICAgICAgIGRlc2NyaXBjaW9uPSJFbnZpYXIgZXN0YWRvcyBmaW5hbmNpZXJvcyBhY3R1YWxpemFkb3MiLAogICAgICAgICAgICBkZWZhdWx0cz17CiAgICAgICAgICAgICAgICAiZmVjaGFfbGltaXRlIjogZGF0ZS50b2RheSgpICsgdGltZWRlbHRhKGRheXM9NyksCiAgICAgICAgICAgICAgICAiZXN0YWRvIjogInBlbmRpZW50ZSIsCiAgICAgICAgICAgICAgICAicHJpb3JpZGFkIjogImFsdGEiLAogICAgICAgICAgICAgICAgImFzaWduYWRvX2EiOiB1c2VyLAogICAgICAgICAgICAgICAgIm5vdGFzIjogIlRhcmVhIGRlbW8iLAogICAgICAgICAgICB9LAogICAgICAgICkKICAgICAgICBUYXJlYS5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgIGVudGlkYWQ9ZW50aWRhZGVzWyIxMjM0NTY3OCJdLAogICAgICAgICAgICBkZXNjcmlwY2lvbj0iQWdlbmRhciB2aXNpdGEgY29tZXJjaWFsIGZhY3RvcmFqZSIsCiAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICJmZWNoYV9saW1pdGUiOiBkYXRlLnRvZGF5KCkgKyB0aW1lZGVsdGEoZGF5cz0xNCksCiAgICAgICAgICAgICAgICAiZXN0YWRvIjogInBlbmRpZW50ZSIsCiAgICAgICAgICAgICAgICAicHJpb3JpZGFkIjogIm1lZGlhIiwKICAgICAgICAgICAgICAgICJub3RhcyI6ICJUYXJlYSBkZW1vIiwKICAgICAgICAgICAgfSwKICAgICAgICApCgogICAgZGVmIF9zZWVkX2ltcG9ydF9iYXRjaGVzKHNlbGYsIHVzZXIpOgogICAgICAgIHNwZWNzID0gWwogICAgICAgICAgICAoImRlbW9fc2VlZF9jcm0iLCAiY3JtIiwgImVudGlkYWRlc19jbGllbnRlcyIsICJkZW1vX2NybV9lbnRpZGFkZXMuY3N2IiwgNSksCiAgICAgICAgICAgICgiZGVtb19zZWVkX3Jpc2siLCAicmlzayIsICJzbmFwc2hvdHNfbGVhc2luZyIsICJkZW1vX2xlYXNpbmdfbWF5by54bHN4IiwgOCksCiAgICAgICAgICAgICgiZGVtb19zZWVkX3BnbyIsICJwZ28iLCAidGlja2V0cyIsICJkZW1vX3RpY2tldHNfdGkueGxzeCIsIDEyKSwKICAgICAgICBdCiAgICAgICAgYmF0Y2hlcyA9IHt9CiAgICAgICAgZm9yIGhhc2hfa2V5LCBtb2R1bG8sIHRpcG8sIG5vbWJyZSwgdmFsaWRhcyBpbiBzcGVjczoKICAgICAgICAgICAgYmF0Y2gsIF8gPSBEYXRhSW1wb3J0QmF0Y2gub2JqZWN0cy51cGRhdGVfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgYXJjaGl2b19oYXNoPWhhc2hfa2V5LAogICAgICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgICAgICJtb2R1bG8iOiBtb2R1bG8sCiAgICAgICAgICAgICAgICAgICAgInRpcG9faW1wb3J0YWNpb24iOiB0aXBvLAogICAgICAgICAgICAgICAgICAgICJhcmNoaXZvX25vbWJyZSI6IG5vbWJyZSwKICAgICAgICAgICAgICAgICAgICAiYXJjaGl2b19ydXRhIjogInVwbG9hZHMvZGVtbyIsCiAgICAgICAgICAgICAgICAgICAgInVzdWFyaW8iOiB1c2VyLAogICAgICAgICAgICAgICAgICAgICJmaWxhc19sZWlkYXMiOiB2YWxpZGFzLAogICAgICAgICAgICAgICAgICAgICJmaWxhc192YWxpZGFzIjogdmFsaWRhcywKICAgICAgICAgICAgICAgICAgICAiZmlsYXNfZXJyb3IiOiAwLAogICAgICAgICAgICAgICAgICAgICJlc3RhZG8iOiBEYXRhSW1wb3J0QmF0Y2guRVNUQURPX09LLAogICAgICAgICAgICAgICAgICAgICJvYnNlcnZhY2lvbmVzIjogIkxvdGUgc2ltdWxhZG8g4oCUIHNlZWRfd2NnX2RlbW8iLAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgKQogICAgICAgICAgICBiYXRjaGVzW21vZHVsb10gPSBiYXRjaAogICAgICAgIHJldHVybiBiYXRjaGVzCgogICAgZGVmIF9zZWVkX3Jpc2soc2VsZiwgZW50aWRhZGVzLCBwcm9kdWN0b3MsIHVuaWRhZGVzLCBiYXRjaCk6CiAgICAgICAgb3BzX2RhdGEgPSBbCiAgICAgICAgICAgICgiOTg1MjExNSIsICJQRzAxMjYwMzAyIiwgIkxFQVNJTkciLCA0NSwgRGVjaW1hbCgiMTI1MDAwIiksIERlY2ltYWwoIjQyMDAwIikpLAogICAgICAgICAgICAoIjg3NjU0MzIxIiwgIkxHMDEyNjAxMTUiLCAiTEVBU0lORyIsIDYyLCBEZWNpbWFsKCI4OTAwMDAiKSwgRGVjaW1hbCgiMTIwMDAwIikpLAogICAgICAgICAgICAoIjEyMzQ1Njc4IiwgIkZDMDEyNjAyODgiLCAiRkFDVE9SSU5HIiwgMCwgRGVjaW1hbCgiNTUwMDAiKSwgRGVjaW1hbCgiMCIpKSwKICAgICAgICBdCiAgICAgICAgb3BlcmFjaW9uZXMgPSB7fQogICAgICAgIGZvciBuaXQsIGNvZGlnb19vcCwgcHJvZCwgbW9yYSwgY2FwaXRhbCwgdmVuY2lkbyBpbiBvcHNfZGF0YToKICAgICAgICAgICAgZW50ID0gZW50aWRhZGVzW25pdF0KICAgICAgICAgICAgb3AsIF8gPSBSaXNrT3BlcmFjaW9uLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgIGVudGlkYWQ9ZW50LAogICAgICAgICAgICAgICAgY29kaWdvX29wZXJhY2lvbj1jb2RpZ29fb3AsCiAgICAgICAgICAgICAgICBkZWZhdWx0cz17CiAgICAgICAgICAgICAgICAgICAgInByb2R1Y3RvIjogcHJvZHVjdG9zW3Byb2RdLAogICAgICAgICAgICAgICAgICAgICJ1bmlkYWRfbmVnb2NpbyI6IHVuaWRhZGVzW3Byb2RdLAogICAgICAgICAgICAgICAgICAgICJtb25lZGEiOiAiR1RRIiwKICAgICAgICAgICAgICAgICAgICAiZXN0YWRvIjogInZpZ2VudGUiLAogICAgICAgICAgICAgICAgICAgICJub3RhcyI6ICJPcGVyYWNpw7NuIGRlbW8iLAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgKQogICAgICAgICAgICBvcGVyYWNpb25lc1tjb2RpZ29fb3BdID0gb3AKICAgICAgICAgICAgZm9yIG9mZnNldCwgbW9yYV9pLCB2ZW5jaWRvX2kgaW4gWyg2MCwgbWF4KG1vcmEgLSAxNSwgMCksIG1heCh2ZW5jaWRvIC0gNTAwMCwgMCkpLCAoMzAsIG1vcmEsIHZlbmNpZG8pXToKICAgICAgICAgICAgICAgIHNuYXBfZGF0ZSA9IGRhdGUoMjAyNiwgNSwgMzEpIC0gdGltZWRlbHRhKGRheXM9b2Zmc2V0KQogICAgICAgICAgICAgICAgUmlza09wZXJhdGlvblNuYXBzaG90Lm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgICAgICBvcGVyYWNpb249b3AsCiAgICAgICAgICAgICAgICAgICAgZmVjaGFfc25hcHNob3Q9c25hcF9kYXRlLAogICAgICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICAgICAgICAgImVudGlkYWQiOiBlbnQsCiAgICAgICAgICAgICAgICAgICAgICAgICJlc3RhZG9fb3BlcmFjaW9uIjogInZpZ2VudGUiLAogICAgICAgICAgICAgICAgICAgICAgICAicHJvZHVjdG9fbm9tYnJlX3JhdyI6IHByb2QudGl0bGUoKSwKICAgICAgICAgICAgICAgICAgICAgICAgImNhcGl0YWxfYmFsYW5jZSI6IGNhcGl0YWwsCiAgICAgICAgICAgICAgICAgICAgICAgICJwYXN0X2R1ZV9iYWxhbmNlIjogdmVuY2lkb19pLAogICAgICAgICAgICAgICAgICAgICAgICAiZHVlX2RheXMiOiBtb3JhX2ksCiAgICAgICAgICAgICAgICAgICAgICAgICJtb250aGx5X3JlbnQiOiBEZWNpbWFsKCI4NTAwIiksCiAgICAgICAgICAgICAgICAgICAgICAgICJhcmNoaXZvX29yaWdlbiI6ICJkZW1vX3NlZWQiLAogICAgICAgICAgICAgICAgICAgICAgICAiaW1wb3J0X2JhdGNoIjogYmF0Y2gsCiAgICAgICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICkKICAgICAgICByZXR1cm4gb3BlcmFjaW9uZXMKCiAgICBkZWYgX3NlZWRfZWVmZihzZWxmLCBlbnRpZGFkZXMsIGJhdGNoKToKICAgICAgICBjdXRzID0gWwogICAgICAgICAgICAoIjk4NTIxMTUiLCBkYXRlKDIwMjUsIDEyLCAzMSksIERlY2ltYWwoIjI1MDAwMDAiKSwgRGVjaW1hbCgiMTgwMDAwIikpLAogICAgICAgICAgICAoIjg3NjU0MzIxIiwgZGF0ZSgyMDI1LCAxMiwgMzEpLCBEZWNpbWFsKCI4OTAwMDAwIiksIERlY2ltYWwoIjQyMDAwMCIpKSwKICAgICAgICBdCiAgICAgICAgZm9yIG5pdCwgY29ydGUsIHZlbnRhcywgdXRpbGlkYWQgaW4gY3V0czoKICAgICAgICAgICAgRXN0YWRvRmluYW5jaWVyby5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBlbnRpZGFkPWVudGlkYWRlc1tuaXRdLAogICAgICAgICAgICAgICAgZmVjaGFfY29ydGU9Y29ydGUsCiAgICAgICAgICAgICAgICBkZWZhdWx0cz17CiAgICAgICAgICAgICAgICAgICAgInZlbnRhcyI6IHZlbnRhcywKICAgICAgICAgICAgICAgICAgICAidXRpbGlkYWRfbmV0YSI6IHV0aWxpZGFkLAogICAgICAgICAgICAgICAgICAgICJwYXRyaW1vbmlvIjogdmVudGFzICogRGVjaW1hbCgiMC4zNSIpLAogICAgICAgICAgICAgICAgICAgICJlYml0ZGEiOiB1dGlsaWRhZCAqIERlY2ltYWwoIjEuMiIpLAogICAgICAgICAgICAgICAgICAgICJvYnNlcnZhY2lvbmVzIjogIkVFRkYgZGVtbyIsCiAgICAgICAgICAgICAgICAgICAgImltcG9ydF9iYXRjaCI6IGJhdGNoLAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgKQoKICAgIGRlZiBfc2VlZF9hbGVydGFzKHNlbGYsIGVudGlkYWRlcywgb3BlcmFjaW9uZXMpOgogICAgICAgIG9wID0gb3BlcmFjaW9uZXMuZ2V0KCJMRzAxMjYwMTE1IikKICAgICAgICBpZiBub3Qgb3A6CiAgICAgICAgICAgIHJldHVybgogICAgICAgIFJpc2tBbGVydGEub2JqZWN0cy51cGRhdGVfb3JfY3JlYXRlKAogICAgICAgICAgICBlbnRpZGFkPWVudGlkYWRlc1siODc2NTQzMjEiXSwKICAgICAgICAgICAgb3BlcmFjaW9uPW9wLAogICAgICAgICAgICB0aXBvX2FsZXJ0YT0ibW9yYSIsCiAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICJmZWNoYV9hbGVydGEiOiBkYXRlLnRvZGF5KCksCiAgICAgICAgICAgICAgICAic2V2ZXJpZGFkIjogImFsdGEiLAogICAgICAgICAgICAgICAgIm1lbnNhamUiOiAiRMOtYXMgZGUgYXRyYXNvIHN1cGVyaW9yZXMgYSA2MCDigJQgc2VndWltaWVudG8gY29icmFuemEuIiwKICAgICAgICAgICAgICAgICJhY3RpdmEiOiBUcnVlLAogICAgICAgICAgICAgICAgIm9yaWdlbiI6IERFTU9fT1JJR0lOLAogICAgICAgICAgICB9LAogICAgICAgICkKCiAgICBkZWYgX3NlZWRfdGlja2V0cyhzZWxmLCB1bmlkYWRlcywgdXNlciwgYmF0Y2gpOgogICAgICAgIG5vdyA9IHRpbWV6b25lLm5vdygpCiAgICAgICAgc2FtcGxlcyA9IFsKICAgICAgICAgICAgKCJUSS1ERU1PLTAwMSIsICJWUE4gbm8gY29uZWN0YSIsICJjZXJyYWRvIiwgImFsdGEiLCAxOCwgVHJ1ZSksCiAgICAgICAgICAgICgiVEktREVNTy0wMDIiLCAiTnVldm8gdXN1YXJpbyBDUk0iLCAiY2VycmFkbyIsICJtZWRpYSIsIDM2LCBUcnVlKSwKICAgICAgICAgICAgKCJUSS1ERU1PLTAwMyIsICJJbXByZXNvcmEgcGlzbyAzIiwgImVuX3Byb2Nlc28iLCAiYmFqYSIsIE5vbmUsIEZhbHNlKSwKICAgICAgICAgICAgKCJUSS1ERU1PLTAwNCIsICJFcnJvciByZXBvcnRlIFBHTyIsICJhYmllcnRvIiwgImFsdGEiLCBOb25lLCBGYWxzZSksCiAgICAgICAgICAgICgiVEktREVNTy0wMDUiLCAiQ29ycmVvIGJsb3F1ZWFkbyIsICJjZXJyYWRvIiwgIm1lZGlhIiwgNDAsIFRydWUpLAogICAgICAgICAgICAoIlRJLURFTU8tMDA2IiwgIkFjY2VzbyBCYWzDs24gZGUgUmllc2dvIiwgImNlcnJhZG8iLCAibWVkaWEiLCAxMiwgVHJ1ZSksCiAgICAgICAgICAgICgiVEktREVNTy0wMDciLCAiTGVudGl0dWQgZGUgcmVkIiwgImVuX3Byb2Nlc28iLCAiYWx0YSIsIE5vbmUsIEZhbHNlKSwKICAgICAgICAgICAgKCJUSS1ERU1PLTAwOCIsICJCYWNrdXAgZmFsbGlkbyIsICJhYmllcnRvIiwgImFsdGEiLCBOb25lLCBGYWxzZSksCiAgICAgICAgXQogICAgICAgIGZvciBpLCAodGlkLCB0aXR1bG8sIGVzdGFkbywgcHJpb3JpZGFkLCBob3Jhcywgc2xhX29rKSBpbiBlbnVtZXJhdGUoc2FtcGxlcyk6CiAgICAgICAgICAgIGFwZXJ0dXJhID0gbm93IC0gdGltZWRlbHRhKGRheXM9MjAgLSBpKQogICAgICAgICAgICBjaWVycmUgPSBhcGVydHVyYSArIHRpbWVkZWx0YShob3Vycz1ob3JhcykgaWYgaG9yYXMgZWxzZSBOb25lCiAgICAgICAgICAgIGlmIGVzdGFkbyA9PSAiY2VycmFkbyIgYW5kIG5vdCBjaWVycmU6CiAgICAgICAgICAgICAgICBjaWVycmUgPSBhcGVydHVyYSArIHRpbWVkZWx0YShob3Vycz0yNCkKICAgICAgICAgICAgZHVyYWNpb24gPSBEZWNpbWFsKHN0cihob3JhcykpIGlmIGhvcmFzIGVsc2UgTm9uZQogICAgICAgICAgICBQZ29UaWNrZXQub2JqZWN0cy51cGRhdGVfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgdGlja2V0X2V4dGVybm9faWQ9dGlkLAogICAgICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgICAgICJ0aXR1bG8iOiB0aXR1bG8sCiAgICAgICAgICAgICAgICAgICAgImVzdGFkb19yYXciOiBlc3RhZG8udXBwZXIoKSwKICAgICAgICAgICAgICAgICAgICAiZXN0YWRvX25vcm1hbGl6YWRvIjogZXN0YWRvLAogICAgICAgICAgICAgICAgICAgICJwcmlvcmlkYWQiOiBwcmlvcmlkYWQsCiAgICAgICAgICAgICAgICAgICAgImRlcGFydGFtZW50byI6ICJUZWNub2xvZ8OtYSIsCiAgICAgICAgICAgICAgICAgICAgInNpc3RlbWEiOiAiSGVscGRlc2sgV0NHIiwKICAgICAgICAgICAgICAgICAgICAidXN1YXJpb19zb2xpY2l0YSI6ICJVc3VhcmlvIGRlbW8iLAogICAgICAgICAgICAgICAgICAgICJjb3JyZW9fc29saWNpdGEiOiAidXN1YXJpb0B3Y2cuZGVtby5ndCIsCiAgICAgICAgICAgICAgICAgICAgImZlY2hhX2FwZXJ0dXJhIjogYXBlcnR1cmEsCiAgICAgICAgICAgICAgICAgICAgImZlY2hhX2NpZXJyZSI6IGNpZXJyZSwKICAgICAgICAgICAgICAgICAgICAiZmVjaGFfcmVnaXN0cm8iOiBhcGVydHVyYSwKICAgICAgICAgICAgICAgICAgICAiYW5pb19tZXMiOiBhcGVydHVyYS5zdHJmdGltZSgiJVktJW0iKSwKICAgICAgICAgICAgICAgICAgICAiZHVyYWNpb25faG9yYXMiOiBkdXJhY2lvbiwKICAgICAgICAgICAgICAgICAgICAic2xhX2hvcmFzIjogRGVjaW1hbCgiNDgiKSwKICAgICAgICAgICAgICAgICAgICAic2xhX2N1bXBsaWRvIjogc2xhX29rLAogICAgICAgICAgICAgICAgICAgICJ1bmlkYWRfbmVnb2NpbyI6IHVuaWRhZGVzWyJUSSJdLAogICAgICAgICAgICAgICAgICAgICJyZXNwb25zYWJsZSI6IHVzZXIsCiAgICAgICAgICAgICAgICAgICAgImltcG9ydF9iYXRjaCI6IGJhdGNoLAogICAgICAgICAgICAgICAgICAgICJzb2x1Y2lvbiI6ICJSZXN1ZWx0byBlbiBkZW1vIiBpZiBlc3RhZG8gPT0gImNlcnJhZG8iIGVsc2UgIiIsCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICApCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/models/__init__.py
PATH_JSON="apps/core/models/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=19
SIZE_BYTES_UTF8=376
CONTENT_SHA256=60ea85b53f8cfa2743c86f8e32bd957275f009544546a8ab3b0c07de10efadde
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from .imports import DataDictionaryField, DataImportBatch, DataImportError
from .masters import (
    Contacto,
    Entidad,
    Producto,
    RelacionEntidadProducto,
    UnidadNegocio,
)

__all__ = [
    "UnidadNegocio",
    "Entidad",
    "Contacto",
    "Producto",
    "RelacionEntidadProducto",
    "DataDictionaryField",
    "DataImportBatch",
    "DataImportError",
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from .imports import DataDictionaryField, DataImportBatch, DataImportError
00002|from .masters import (
00003|    Contacto,
00004|    Entidad,
00005|    Producto,
00006|    RelacionEntidadProducto,
00007|    UnidadNegocio,
00008|)
00009|
00010|__all__ = [
00011|    "UnidadNegocio",
00012|    "Entidad",
00013|    "Contacto",
00014|    "Producto",
00015|    "RelacionEntidadProducto",
00016|    "DataDictionaryField",
00017|    "DataImportBatch",
00018|    "DataImportError",
00019|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSAuaW1wb3J0cyBpbXBvcnQgRGF0YURpY3Rpb25hcnlGaWVsZCwgRGF0YUltcG9ydEJhdGNoLCBEYXRhSW1wb3J0RXJyb3IKZnJvbSAubWFzdGVycyBpbXBvcnQgKAogICAgQ29udGFjdG8sCiAgICBFbnRpZGFkLAogICAgUHJvZHVjdG8sCiAgICBSZWxhY2lvbkVudGlkYWRQcm9kdWN0bywKICAgIFVuaWRhZE5lZ29jaW8sCikKCl9fYWxsX18gPSBbCiAgICAiVW5pZGFkTmVnb2NpbyIsCiAgICAiRW50aWRhZCIsCiAgICAiQ29udGFjdG8iLAogICAgIlByb2R1Y3RvIiwKICAgICJSZWxhY2lvbkVudGlkYWRQcm9kdWN0byIsCiAgICAiRGF0YURpY3Rpb25hcnlGaWVsZCIsCiAgICAiRGF0YUltcG9ydEJhdGNoIiwKICAgICJEYXRhSW1wb3J0RXJyb3IiLApdCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/models/imports.py
PATH_JSON="apps/core/models/imports.py"
FILENAME=imports.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=95
SIZE_BYTES_UTF8=3443
CONTENT_SHA256=400baebe4e0a414f90aad9ca96e6559b400902dac47673d1c3aa3b7eb702ee07
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Diccionario de datos y trazabilidad de importaciones."""

from django.conf import settings
from django.db import models


class DataDictionaryField(models.Model):
    modulo = models.CharField(max_length=50, db_index=True)
    nombre_logico = models.CharField(max_length=150)
    tabla_fisica = models.CharField(max_length=100)
    campo_fisico = models.CharField(max_length=100)
    tipo_dato = models.CharField(max_length=50, blank=True)
    definicion = models.TextField(blank=True)
    fuente = models.CharField(max_length=255, blank=True)
    periodicidad = models.CharField(max_length=50, blank=True)
    orden = models.PositiveIntegerField(default=0)
    notas = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["modulo", "orden", "tabla_fisica", "campo_fisico"]
        verbose_name = "Campo de diccionario de datos"
        verbose_name_plural = "Diccionario de datos"
        constraints = [
            models.UniqueConstraint(
                fields=["tabla_fisica", "campo_fisico"],
                name="uniq_data_dictionary_tabla_campo",
            ),
        ]

    def __str__(self):
        return f"{self.tabla_fisica}.{self.campo_fisico}"


class DataImportBatch(models.Model):
    ESTADO_PENDIENTE = "pendiente"
    ESTADO_PROCESANDO = "procesando"
    ESTADO_OK = "ok"
    ESTADO_PARCIAL = "parcial"
    ESTADO_ERROR = "error"
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, "Pendiente"),
        (ESTADO_PROCESANDO, "Procesando"),
        (ESTADO_OK, "OK"),
        (ESTADO_PARCIAL, "Parcial"),
        (ESTADO_ERROR, "Error"),
    ]

    modulo = models.CharField(max_length=50, db_index=True)
    tipo_importacion = models.CharField(max_length=100)
    archivo_nombre = models.CharField(max_length=255)
    archivo_hash = models.CharField(max_length=128, blank=True)
    archivo_ruta = models.CharField(max_length=500, blank=True)
    fecha_carga = models.DateTimeField(auto_now_add=True, db_index=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_import_batches",
    )
    filas_leidas = models.PositiveIntegerField(default=0)
    filas_validas = models.PositiveIntegerField(default=0)
    filas_error = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha_carga"]
        verbose_name = "Lote de importación"
        verbose_name_plural = "Lotes de importación"

    def __str__(self):
        return f"{self.modulo}/{self.tipo_importacion} — {self.archivo_nombre}"


class DataImportError(models.Model):
    batch = models.ForeignKey(
        DataImportBatch,
        on_delete=models.CASCADE,
        related_name="errores",
    )
    fila_numero = models.PositiveIntegerField()
    campo = models.CharField(max_length=100, blank=True)
    valor_original = models.TextField(blank=True)
    mensaje_error = models.TextField()
    payload_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["batch", "fila_numero"]
        verbose_name = "Error de importación"
        verbose_name_plural = "Errores de importación"

    def __str__(self):
        return f"Lote {self.batch_id} fila {self.fila_numero}"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Diccionario de datos y trazabilidad de importaciones."""
00002|
00003|from django.conf import settings
00004|from django.db import models
00005|
00006|
00007|class DataDictionaryField(models.Model):
00008|    modulo = models.CharField(max_length=50, db_index=True)
00009|    nombre_logico = models.CharField(max_length=150)
00010|    tabla_fisica = models.CharField(max_length=100)
00011|    campo_fisico = models.CharField(max_length=100)
00012|    tipo_dato = models.CharField(max_length=50, blank=True)
00013|    definicion = models.TextField(blank=True)
00014|    fuente = models.CharField(max_length=255, blank=True)
00015|    periodicidad = models.CharField(max_length=50, blank=True)
00016|    orden = models.PositiveIntegerField(default=0)
00017|    notas = models.TextField(blank=True)
00018|    activo = models.BooleanField(default=True)
00019|
00020|    class Meta:
00021|        ordering = ["modulo", "orden", "tabla_fisica", "campo_fisico"]
00022|        verbose_name = "Campo de diccionario de datos"
00023|        verbose_name_plural = "Diccionario de datos"
00024|        constraints = [
00025|            models.UniqueConstraint(
00026|                fields=["tabla_fisica", "campo_fisico"],
00027|                name="uniq_data_dictionary_tabla_campo",
00028|            ),
00029|        ]
00030|
00031|    def __str__(self):
00032|        return f"{self.tabla_fisica}.{self.campo_fisico}"
00033|
00034|
00035|class DataImportBatch(models.Model):
00036|    ESTADO_PENDIENTE = "pendiente"
00037|    ESTADO_PROCESANDO = "procesando"
00038|    ESTADO_OK = "ok"
00039|    ESTADO_PARCIAL = "parcial"
00040|    ESTADO_ERROR = "error"
00041|    ESTADO_CHOICES = [
00042|        (ESTADO_PENDIENTE, "Pendiente"),
00043|        (ESTADO_PROCESANDO, "Procesando"),
00044|        (ESTADO_OK, "OK"),
00045|        (ESTADO_PARCIAL, "Parcial"),
00046|        (ESTADO_ERROR, "Error"),
00047|    ]
00048|
00049|    modulo = models.CharField(max_length=50, db_index=True)
00050|    tipo_importacion = models.CharField(max_length=100)
00051|    archivo_nombre = models.CharField(max_length=255)
00052|    archivo_hash = models.CharField(max_length=128, blank=True)
00053|    archivo_ruta = models.CharField(max_length=500, blank=True)
00054|    fecha_carga = models.DateTimeField(auto_now_add=True, db_index=True)
00055|    usuario = models.ForeignKey(
00056|        settings.AUTH_USER_MODEL,
00057|        on_delete=models.SET_NULL,
00058|        null=True,
00059|        blank=True,
00060|        related_name="wcgone_import_batches",
00061|    )
00062|    filas_leidas = models.PositiveIntegerField(default=0)
00063|    filas_validas = models.PositiveIntegerField(default=0)
00064|    filas_error = models.PositiveIntegerField(default=0)
00065|    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)
00066|    observaciones = models.TextField(blank=True)
00067|
00068|    class Meta:
00069|        ordering = ["-fecha_carga"]
00070|        verbose_name = "Lote de importación"
00071|        verbose_name_plural = "Lotes de importación"
00072|
00073|    def __str__(self):
00074|        return f"{self.modulo}/{self.tipo_importacion} — {self.archivo_nombre}"
00075|
00076|
00077|class DataImportError(models.Model):
00078|    batch = models.ForeignKey(
00079|        DataImportBatch,
00080|        on_delete=models.CASCADE,
00081|        related_name="errores",
00082|    )
00083|    fila_numero = models.PositiveIntegerField()
00084|    campo = models.CharField(max_length=100, blank=True)
00085|    valor_original = models.TextField(blank=True)
00086|    mensaje_error = models.TextField()
00087|    payload_json = models.JSONField(default=dict, blank=True)
00088|
00089|    class Meta:
00090|        ordering = ["batch", "fila_numero"]
00091|        verbose_name = "Error de importación"
00092|        verbose_name_plural = "Errores de importación"
00093|
00094|    def __str__(self):
00095|        return f"Lote {self.batch_id} fila {self.fila_numero}"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiRGljY2lvbmFyaW8gZGUgZGF0b3MgeSB0cmF6YWJpbGlkYWQgZGUgaW1wb3J0YWNpb25lcy4iIiIKCmZyb20gZGphbmdvLmNvbmYgaW1wb3J0IHNldHRpbmdzCmZyb20gZGphbmdvLmRiIGltcG9ydCBtb2RlbHMKCgpjbGFzcyBEYXRhRGljdGlvbmFyeUZpZWxkKG1vZGVscy5Nb2RlbCk6CiAgICBtb2R1bG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9NTAsIGRiX2luZGV4PVRydWUpCiAgICBub21icmVfbG9naWNvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTE1MCkKICAgIHRhYmxhX2Zpc2ljYSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMDApCiAgICBjYW1wb19maXNpY28gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAwKQogICAgdGlwb19kYXRvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTUwLCBibGFuaz1UcnVlKQogICAgZGVmaW5pY2lvbiA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKICAgIGZ1ZW50ZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUsIGJsYW5rPVRydWUpCiAgICBwZXJpb2RpY2lkYWQgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9NTAsIGJsYW5rPVRydWUpCiAgICBvcmRlbiA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZChkZWZhdWx0PTApCiAgICBub3RhcyA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKICAgIGFjdGl2byA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbIm1vZHVsbyIsICJvcmRlbiIsICJ0YWJsYV9maXNpY2EiLCAiY2FtcG9fZmlzaWNvIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiQ2FtcG8gZGUgZGljY2lvbmFyaW8gZGUgZGF0b3MiCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJEaWNjaW9uYXJpbyBkZSBkYXRvcyIKICAgICAgICBjb25zdHJhaW50cyA9IFsKICAgICAgICAgICAgbW9kZWxzLlVuaXF1ZUNvbnN0cmFpbnQoCiAgICAgICAgICAgICAgICBmaWVsZHM9WyJ0YWJsYV9maXNpY2EiLCAiY2FtcG9fZmlzaWNvIl0sCiAgICAgICAgICAgICAgICBuYW1lPSJ1bmlxX2RhdGFfZGljdGlvbmFyeV90YWJsYV9jYW1wbyIsCiAgICAgICAgICAgICksCiAgICAgICAgXQoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLnRhYmxhX2Zpc2ljYX0ue3NlbGYuY2FtcG9fZmlzaWNvfSIKCgpjbGFzcyBEYXRhSW1wb3J0QmF0Y2gobW9kZWxzLk1vZGVsKToKICAgIEVTVEFET19QRU5ESUVOVEUgPSAicGVuZGllbnRlIgogICAgRVNUQURPX1BST0NFU0FORE8gPSAicHJvY2VzYW5kbyIKICAgIEVTVEFET19PSyA9ICJvayIKICAgIEVTVEFET19QQVJDSUFMID0gInBhcmNpYWwiCiAgICBFU1RBRE9fRVJST1IgPSAiZXJyb3IiCiAgICBFU1RBRE9fQ0hPSUNFUyA9IFsKICAgICAgICAoRVNUQURPX1BFTkRJRU5URSwgIlBlbmRpZW50ZSIpLAogICAgICAgIChFU1RBRE9fUFJPQ0VTQU5ETywgIlByb2Nlc2FuZG8iKSwKICAgICAgICAoRVNUQURPX09LLCAiT0siKSwKICAgICAgICAoRVNUQURPX1BBUkNJQUwsICJQYXJjaWFsIiksCiAgICAgICAgKEVTVEFET19FUlJPUiwgIkVycm9yIiksCiAgICBdCgogICAgbW9kdWxvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTUwLCBkYl9pbmRleD1UcnVlKQogICAgdGlwb19pbXBvcnRhY2lvbiA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMDApCiAgICBhcmNoaXZvX25vbWJyZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUpCiAgICBhcmNoaXZvX2hhc2ggPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTI4LCBibGFuaz1UcnVlKQogICAgYXJjaGl2b19ydXRhID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTUwMCwgYmxhbms9VHJ1ZSkKICAgIGZlY2hhX2NhcmdhID0gbW9kZWxzLkRhdGVUaW1lRmllbGQoYXV0b19ub3dfYWRkPVRydWUsIGRiX2luZGV4PVRydWUpCiAgICB1c3VhcmlvID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgc2V0dGluZ3MuQVVUSF9VU0VSX01PREVMLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJ3Y2dvbmVfaW1wb3J0X2JhdGNoZXMiLAogICAgKQogICAgZmlsYXNfbGVpZGFzID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKGRlZmF1bHQ9MCkKICAgIGZpbGFzX3ZhbGlkYXMgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoZGVmYXVsdD0wKQogICAgZmlsYXNfZXJyb3IgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoZGVmYXVsdD0wKQogICAgZXN0YWRvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTIwLCBjaG9pY2VzPUVTVEFET19DSE9JQ0VTLCBkZWZhdWx0PUVTVEFET19QRU5ESUVOVEUpCiAgICBvYnNlcnZhY2lvbmVzID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbIi1mZWNoYV9jYXJnYSJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIkxvdGUgZGUgaW1wb3J0YWNpw7NuIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiTG90ZXMgZGUgaW1wb3J0YWNpw7NuIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLm1vZHVsb30ve3NlbGYudGlwb19pbXBvcnRhY2lvbn0g4oCUIHtzZWxmLmFyY2hpdm9fbm9tYnJlfSIKCgpjbGFzcyBEYXRhSW1wb3J0RXJyb3IobW9kZWxzLk1vZGVsKToKICAgIGJhdGNoID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgRGF0YUltcG9ydEJhdGNoLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwKICAgICAgICByZWxhdGVkX25hbWU9ImVycm9yZXMiLAogICAgKQogICAgZmlsYV9udW1lcm8gPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQogICAgY2FtcG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAwLCBibGFuaz1UcnVlKQogICAgdmFsb3Jfb3JpZ2luYWwgPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCiAgICBtZW5zYWplX2Vycm9yID0gbW9kZWxzLlRleHRGaWVsZCgpCiAgICBwYXlsb2FkX2pzb24gPSBtb2RlbHMuSlNPTkZpZWxkKGRlZmF1bHQ9ZGljdCwgYmxhbms9VHJ1ZSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWyJiYXRjaCIsICJmaWxhX251bWVybyJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIkVycm9yIGRlIGltcG9ydGFjacOzbiIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIkVycm9yZXMgZGUgaW1wb3J0YWNpw7NuIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIkxvdGUge3NlbGYuYmF0Y2hfaWR9IGZpbGEge3NlbGYuZmlsYV9udW1lcm99Igo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/models/masters.py
PATH_JSON="apps/core/models/masters.py"
FILENAME=masters.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=144
SIZE_BYTES_UTF8=5393
CONTENT_SHA256=510f2a7c8bea322ce4761987db780242d6773b85d585147cb23389afb8585594
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Maestros compartidos: entidades, contactos, productos y unidades."""

from django.db import models


class UnidadNegocio(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Unidad de negocio"
        verbose_name_plural = "Unidades de negocio"

    def __str__(self):
        return self.nombre


class Entidad(models.Model):
    TIPO_CLIENTE = "cliente"
    TIPO_INVERSIONISTA = "inversionista"
    TIPO_AMBOS = "ambos"
    TIPO_PROVEEDOR = "proveedor"
    TIPO_OTRO = "otro"
    TIPO_CHOICES = [
        (TIPO_CLIENTE, "Cliente"),
        (TIPO_INVERSIONISTA, "Inversionista"),
        (TIPO_AMBOS, "Ambos"),
        (TIPO_PROVEEDOR, "Proveedor"),
        (TIPO_OTRO, "Otro"),
    ]

    tipo_entidad = models.CharField(max_length=30, choices=TIPO_CHOICES, default=TIPO_CLIENTE)
    es_persona = models.BooleanField(default=False)
    nombre = models.CharField(max_length=255, db_index=True)
    nombre_comercial = models.CharField(max_length=255, blank=True)
    nit = models.CharField(max_length=50, blank=True, db_index=True)
    pais = models.CharField(max_length=100, blank=True)
    departamento = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    direccion_fiscal = models.TextField(blank=True)
    direccion_operativa = models.TextField(blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    sector_economico = models.CharField(max_length=150, blank=True)
    codigo_sector = models.CharField(max_length=50, blank=True)
    activo = models.BooleanField(default=True)
    categoria_riesgo = models.CharField(max_length=50, blank=True)
    origen = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Entidad"
        verbose_name_plural = "Entidades"
        indexes = [
            models.Index(fields=["activo", "tipo_entidad"]),
        ]

    def __str__(self):
        return self.nombre


class Contacto(models.Model):
    entidad = models.ForeignKey(
        Entidad,
        on_delete=models.CASCADE,
        related_name="contactos",
    )
    nombre = models.CharField(max_length=255)
    cargo = models.CharField(max_length=150, blank=True)
    area = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True, db_index=True)
    telefono_movil = models.CharField(max_length=50, blank=True)
    telefono_oficina = models.CharField(max_length=50, blank=True)
    extension = models.CharField(max_length=20, blank=True)
    es_decisor_credito = models.BooleanField(default=False)
    es_contacto_cobranza = models.BooleanField(default=False)
    es_contacto_operativo = models.BooleanField(default=False)
    nivel_influencia = models.CharField(max_length=50, blank=True)
    nivel_apertura = models.CharField(max_length=50, blank=True)
    notas = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["entidad__nombre", "nombre"]
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        indexes = [
            models.Index(fields=["entidad", "activo"]),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.entidad})"


class Producto(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    tipo_producto = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre


class RelacionEntidadProducto(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="relaciones_producto")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="relaciones_entidad")
    unidad_negocio = models.ForeignKey(
        UnidadNegocio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relaciones_entidad_producto",
    )
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    monto_aprobado = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    moneda = models.CharField(max_length=10, blank=True)
    codigo_operacion_externo = models.CharField(max_length=100, blank=True, db_index=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["entidad__nombre", "producto__nombre"]
        verbose_name = "Relación entidad-producto"
        verbose_name_plural = "Relaciones entidad-producto"
        indexes = [
            models.Index(fields=["entidad", "producto"]),
        ]

    def __str__(self):
        return f"{self.entidad} / {self.producto}"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Maestros compartidos: entidades, contactos, productos y unidades."""
00002|
00003|from django.db import models
00004|
00005|
00006|class UnidadNegocio(models.Model):
00007|    codigo = models.CharField(max_length=30, unique=True)
00008|    nombre = models.CharField(max_length=100)
00009|    activa = models.BooleanField(default=True)
00010|    orden = models.PositiveIntegerField(default=0)
00011|
00012|    class Meta:
00013|        ordering = ["orden", "nombre"]
00014|        verbose_name = "Unidad de negocio"
00015|        verbose_name_plural = "Unidades de negocio"
00016|
00017|    def __str__(self):
00018|        return self.nombre
00019|
00020|
00021|class Entidad(models.Model):
00022|    TIPO_CLIENTE = "cliente"
00023|    TIPO_INVERSIONISTA = "inversionista"
00024|    TIPO_AMBOS = "ambos"
00025|    TIPO_PROVEEDOR = "proveedor"
00026|    TIPO_OTRO = "otro"
00027|    TIPO_CHOICES = [
00028|        (TIPO_CLIENTE, "Cliente"),
00029|        (TIPO_INVERSIONISTA, "Inversionista"),
00030|        (TIPO_AMBOS, "Ambos"),
00031|        (TIPO_PROVEEDOR, "Proveedor"),
00032|        (TIPO_OTRO, "Otro"),
00033|    ]
00034|
00035|    tipo_entidad = models.CharField(max_length=30, choices=TIPO_CHOICES, default=TIPO_CLIENTE)
00036|    es_persona = models.BooleanField(default=False)
00037|    nombre = models.CharField(max_length=255, db_index=True)
00038|    nombre_comercial = models.CharField(max_length=255, blank=True)
00039|    nit = models.CharField(max_length=50, blank=True, db_index=True)
00040|    pais = models.CharField(max_length=100, blank=True)
00041|    departamento = models.CharField(max_length=100, blank=True)
00042|    ciudad = models.CharField(max_length=100, blank=True)
00043|    direccion_fiscal = models.TextField(blank=True)
00044|    direccion_operativa = models.TextField(blank=True)
00045|    telefono = models.CharField(max_length=50, blank=True)
00046|    email = models.EmailField(blank=True)
00047|    sector_economico = models.CharField(max_length=150, blank=True)
00048|    codigo_sector = models.CharField(max_length=50, blank=True)
00049|    activo = models.BooleanField(default=True)
00050|    categoria_riesgo = models.CharField(max_length=50, blank=True)
00051|    origen = models.CharField(max_length=100, blank=True)
00052|    notas = models.TextField(blank=True)
00053|    fecha_creacion = models.DateTimeField(auto_now_add=True)
00054|    fecha_modificacion = models.DateTimeField(auto_now=True)
00055|
00056|    class Meta:
00057|        ordering = ["nombre"]
00058|        verbose_name = "Entidad"
00059|        verbose_name_plural = "Entidades"
00060|        indexes = [
00061|            models.Index(fields=["activo", "tipo_entidad"]),
00062|        ]
00063|
00064|    def __str__(self):
00065|        return self.nombre
00066|
00067|
00068|class Contacto(models.Model):
00069|    entidad = models.ForeignKey(
00070|        Entidad,
00071|        on_delete=models.CASCADE,
00072|        related_name="contactos",
00073|    )
00074|    nombre = models.CharField(max_length=255)
00075|    cargo = models.CharField(max_length=150, blank=True)
00076|    area = models.CharField(max_length=150, blank=True)
00077|    email = models.EmailField(blank=True, db_index=True)
00078|    telefono_movil = models.CharField(max_length=50, blank=True)
00079|    telefono_oficina = models.CharField(max_length=50, blank=True)
00080|    extension = models.CharField(max_length=20, blank=True)
00081|    es_decisor_credito = models.BooleanField(default=False)
00082|    es_contacto_cobranza = models.BooleanField(default=False)
00083|    es_contacto_operativo = models.BooleanField(default=False)
00084|    nivel_influencia = models.CharField(max_length=50, blank=True)
00085|    nivel_apertura = models.CharField(max_length=50, blank=True)
00086|    notas = models.TextField(blank=True)
00087|    activo = models.BooleanField(default=True)
00088|
00089|    class Meta:
00090|        ordering = ["entidad__nombre", "nombre"]
00091|        verbose_name = "Contacto"
00092|        verbose_name_plural = "Contactos"
00093|        indexes = [
00094|            models.Index(fields=["entidad", "activo"]),
00095|        ]
00096|
00097|    def __str__(self):
00098|        return f"{self.nombre} ({self.entidad})"
00099|
00100|
00101|class Producto(models.Model):
00102|    codigo = models.CharField(max_length=30, unique=True)
00103|    nombre = models.CharField(max_length=100)
00104|    tipo_producto = models.CharField(max_length=100, blank=True)
00105|    descripcion = models.TextField(blank=True)
00106|    activo = models.BooleanField(default=True)
00107|
00108|    class Meta:
00109|        ordering = ["nombre"]
00110|        verbose_name = "Producto"
00111|        verbose_name_plural = "Productos"
00112|
00113|    def __str__(self):
00114|        return self.nombre
00115|
00116|
00117|class RelacionEntidadProducto(models.Model):
00118|    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="relaciones_producto")
00119|    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="relaciones_entidad")
00120|    unidad_negocio = models.ForeignKey(
00121|        UnidadNegocio,
00122|        on_delete=models.SET_NULL,
00123|        null=True,
00124|        blank=True,
00125|        related_name="relaciones_entidad_producto",
00126|    )
00127|    fecha_inicio = models.DateField(null=True, blank=True)
00128|    fecha_fin = models.DateField(null=True, blank=True)
00129|    estado = models.CharField(max_length=50, blank=True)
00130|    monto_aprobado = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00131|    moneda = models.CharField(max_length=10, blank=True)
00132|    codigo_operacion_externo = models.CharField(max_length=100, blank=True, db_index=True)
00133|    notas = models.TextField(blank=True)
00134|
00135|    class Meta:
00136|        ordering = ["entidad__nombre", "producto__nombre"]
00137|        verbose_name = "Relación entidad-producto"
00138|        verbose_name_plural = "Relaciones entidad-producto"
00139|        indexes = [
00140|            models.Index(fields=["entidad", "producto"]),
00141|        ]
00142|
00143|    def __str__(self):
00144|        return f"{self.entidad} / {self.producto}"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiTWFlc3Ryb3MgY29tcGFydGlkb3M6IGVudGlkYWRlcywgY29udGFjdG9zLCBwcm9kdWN0b3MgeSB1bmlkYWRlcy4iIiIKCmZyb20gZGphbmdvLmRiIGltcG9ydCBtb2RlbHMKCgpjbGFzcyBVbmlkYWROZWdvY2lvKG1vZGVscy5Nb2RlbCk6CiAgICBjb2RpZ28gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MzAsIHVuaXF1ZT1UcnVlKQogICAgbm9tYnJlID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwMCkKICAgIGFjdGl2YSA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1UcnVlKQogICAgb3JkZW4gPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoZGVmYXVsdD0wKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbIm9yZGVuIiwgIm5vbWJyZSJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIlVuaWRhZCBkZSBuZWdvY2lvIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiVW5pZGFkZXMgZGUgbmVnb2NpbyIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gc2VsZi5ub21icmUKCgpjbGFzcyBFbnRpZGFkKG1vZGVscy5Nb2RlbCk6CiAgICBUSVBPX0NMSUVOVEUgPSAiY2xpZW50ZSIKICAgIFRJUE9fSU5WRVJTSU9OSVNUQSA9ICJpbnZlcnNpb25pc3RhIgogICAgVElQT19BTUJPUyA9ICJhbWJvcyIKICAgIFRJUE9fUFJPVkVFRE9SID0gInByb3ZlZWRvciIKICAgIFRJUE9fT1RSTyA9ICJvdHJvIgogICAgVElQT19DSE9JQ0VTID0gWwogICAgICAgIChUSVBPX0NMSUVOVEUsICJDbGllbnRlIiksCiAgICAgICAgKFRJUE9fSU5WRVJTSU9OSVNUQSwgIkludmVyc2lvbmlzdGEiKSwKICAgICAgICAoVElQT19BTUJPUywgIkFtYm9zIiksCiAgICAgICAgKFRJUE9fUFJPVkVFRE9SLCAiUHJvdmVlZG9yIiksCiAgICAgICAgKFRJUE9fT1RSTywgIk90cm8iKSwKICAgIF0KCiAgICB0aXBvX2VudGlkYWQgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MzAsIGNob2ljZXM9VElQT19DSE9JQ0VTLCBkZWZhdWx0PVRJUE9fQ0xJRU5URSkKICAgIGVzX3BlcnNvbmEgPSBtb2RlbHMuQm9vbGVhbkZpZWxkKGRlZmF1bHQ9RmFsc2UpCiAgICBub21icmUgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjU1LCBkYl9pbmRleD1UcnVlKQogICAgbm9tYnJlX2NvbWVyY2lhbCA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUsIGJsYW5rPVRydWUpCiAgICBuaXQgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9NTAsIGJsYW5rPVRydWUsIGRiX2luZGV4PVRydWUpCiAgICBwYWlzID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwMCwgYmxhbms9VHJ1ZSkKICAgIGRlcGFydGFtZW50byA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMDAsIGJsYW5rPVRydWUpCiAgICBjaXVkYWQgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAwLCBibGFuaz1UcnVlKQogICAgZGlyZWNjaW9uX2Zpc2NhbCA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKICAgIGRpcmVjY2lvbl9vcGVyYXRpdmEgPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCiAgICB0ZWxlZm9ubyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD01MCwgYmxhbms9VHJ1ZSkKICAgIGVtYWlsID0gbW9kZWxzLkVtYWlsRmllbGQoYmxhbms9VHJ1ZSkKICAgIHNlY3Rvcl9lY29ub21pY28gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTUwLCBibGFuaz1UcnVlKQogICAgY29kaWdvX3NlY3RvciA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD01MCwgYmxhbms9VHJ1ZSkKICAgIGFjdGl2byA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1UcnVlKQogICAgY2F0ZWdvcmlhX3JpZXNnbyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD01MCwgYmxhbms9VHJ1ZSkKICAgIG9yaWdlbiA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMDAsIGJsYW5rPVRydWUpCiAgICBub3RhcyA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKICAgIGZlY2hhX2NyZWFjaW9uID0gbW9kZWxzLkRhdGVUaW1lRmllbGQoYXV0b19ub3dfYWRkPVRydWUpCiAgICBmZWNoYV9tb2RpZmljYWNpb24gPSBtb2RlbHMuRGF0ZVRpbWVGaWVsZChhdXRvX25vdz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbIm5vbWJyZSJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIkVudGlkYWQiCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJFbnRpZGFkZXMiCiAgICAgICAgaW5kZXhlcyA9IFsKICAgICAgICAgICAgbW9kZWxzLkluZGV4KGZpZWxkcz1bImFjdGl2byIsICJ0aXBvX2VudGlkYWQiXSksCiAgICAgICAgXQoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBzZWxmLm5vbWJyZQoKCmNsYXNzIENvbnRhY3RvKG1vZGVscy5Nb2RlbCk6CiAgICBlbnRpZGFkID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgRW50aWRhZCwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJjb250YWN0b3MiLAogICAgKQogICAgbm9tYnJlID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTI1NSkKICAgIGNhcmdvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTE1MCwgYmxhbms9VHJ1ZSkKICAgIGFyZWEgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTUwLCBibGFuaz1UcnVlKQogICAgZW1haWwgPSBtb2RlbHMuRW1haWxGaWVsZChibGFuaz1UcnVlLCBkYl9pbmRleD1UcnVlKQogICAgdGVsZWZvbm9fbW92aWwgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9NTAsIGJsYW5rPVRydWUpCiAgICB0ZWxlZm9ub19vZmljaW5hID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTUwLCBibGFuaz1UcnVlKQogICAgZXh0ZW5zaW9uID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTIwLCBibGFuaz1UcnVlKQogICAgZXNfZGVjaXNvcl9jcmVkaXRvID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PUZhbHNlKQogICAgZXNfY29udGFjdG9fY29icmFuemEgPSBtb2RlbHMuQm9vbGVhbkZpZWxkKGRlZmF1bHQ9RmFsc2UpCiAgICBlc19jb250YWN0b19vcGVyYXRpdm8gPSBtb2RlbHMuQm9vbGVhbkZpZWxkKGRlZmF1bHQ9RmFsc2UpCiAgICBuaXZlbF9pbmZsdWVuY2lhID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTUwLCBibGFuaz1UcnVlKQogICAgbml2ZWxfYXBlcnR1cmEgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9NTAsIGJsYW5rPVRydWUpCiAgICBub3RhcyA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKICAgIGFjdGl2byA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbImVudGlkYWRfX25vbWJyZSIsICJub21icmUiXQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICJDb250YWN0byIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIkNvbnRhY3RvcyIKICAgICAgICBpbmRleGVzID0gWwogICAgICAgICAgICBtb2RlbHMuSW5kZXgoZmllbGRzPVsiZW50aWRhZCIsICJhY3Rpdm8iXSksCiAgICAgICAgXQoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLm5vbWJyZX0gKHtzZWxmLmVudGlkYWR9KSIKCgpjbGFzcyBQcm9kdWN0byhtb2RlbHMuTW9kZWwpOgogICAgY29kaWdvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTMwLCB1bmlxdWU9VHJ1ZSkKICAgIG5vbWJyZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMDApCiAgICB0aXBvX3Byb2R1Y3RvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwMCwgYmxhbms9VHJ1ZSkKICAgIGRlc2NyaXBjaW9uID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQogICAgYWN0aXZvID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsibm9tYnJlIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiUHJvZHVjdG8iCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJQcm9kdWN0b3MiCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIHNlbGYubm9tYnJlCgoKY2xhc3MgUmVsYWNpb25FbnRpZGFkUHJvZHVjdG8obW9kZWxzLk1vZGVsKToKICAgIGVudGlkYWQgPSBtb2RlbHMuRm9yZWlnbktleShFbnRpZGFkLCBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsIHJlbGF0ZWRfbmFtZT0icmVsYWNpb25lc19wcm9kdWN0byIpCiAgICBwcm9kdWN0byA9IG1vZGVscy5Gb3JlaWduS2V5KFByb2R1Y3RvLCBvbl9kZWxldGU9bW9kZWxzLlBST1RFQ1QsIHJlbGF0ZWRfbmFtZT0icmVsYWNpb25lc19lbnRpZGFkIikKICAgIHVuaWRhZF9uZWdvY2lvID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgVW5pZGFkTmVnb2NpbywKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0icmVsYWNpb25lc19lbnRpZGFkX3Byb2R1Y3RvIiwKICAgICkKICAgIGZlY2hhX2luaWNpbyA9IG1vZGVscy5EYXRlRmllbGQobnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgZmVjaGFfZmluID0gbW9kZWxzLkRhdGVGaWVsZChudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBlc3RhZG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9NTAsIGJsYW5rPVRydWUpCiAgICBtb250b19hcHJvYmFkbyA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9MiwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgbW9uZWRhID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwLCBibGFuaz1UcnVlKQogICAgY29kaWdvX29wZXJhY2lvbl9leHRlcm5vID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwMCwgYmxhbms9VHJ1ZSwgZGJfaW5kZXg9VHJ1ZSkKICAgIG5vdGFzID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbImVudGlkYWRfX25vbWJyZSIsICJwcm9kdWN0b19fbm9tYnJlIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiUmVsYWNpw7NuIGVudGlkYWQtcHJvZHVjdG8iCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJSZWxhY2lvbmVzIGVudGlkYWQtcHJvZHVjdG8iCiAgICAgICAgaW5kZXhlcyA9IFsKICAgICAgICAgICAgbW9kZWxzLkluZGV4KGZpZWxkcz1bImVudGlkYWQiLCAicHJvZHVjdG8iXSksCiAgICAgICAgXQoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLmVudGlkYWR9IC8ge3NlbGYucHJvZHVjdG99Igo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/urls.py
PATH_JSON="apps/core/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=9
SIZE_BYTES_UTF8=187
CONTENT_SHA256=348eab3b0fbc616ed9cab6da5dfe9c542b35e4e53a95fa3a050b39212278ced5
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.urls import path

from . import views

app_name = "wcgone_core"

urlpatterns = [
    path("importaciones/<int:pk>/", views.import_batch_detail, name="import_batch_detail"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|
00003|from . import views
00004|
00005|app_name = "wcgone_core"
00006|
00007|urlpatterns = [
00008|    path("importaciones/<int:pk>/", views.import_batch_detail, name="import_batch_detail"),
00009|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aAoKZnJvbSAuIGltcG9ydCB2aWV3cwoKYXBwX25hbWUgPSAid2Nnb25lX2NvcmUiCgp1cmxwYXR0ZXJucyA9IFsKICAgIHBhdGgoImltcG9ydGFjaW9uZXMvPGludDpwaz4vIiwgdmlld3MuaW1wb3J0X2JhdGNoX2RldGFpbCwgbmFtZT0iaW1wb3J0X2JhdGNoX2RldGFpbCIpLApdCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/core/views.py
PATH_JSON="apps/core/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=23
SIZE_BYTES_UTF8=709
CONTENT_SHA256=121e81929828842839b76d0598bd0266a6f6f2b17d9db158b3a7012729cc954c
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from apps.core.models import DataImportBatch, DataImportError


@login_required
def import_batch_detail(request, pk):
    batch = get_object_or_404(
        DataImportBatch.objects.select_related("usuario"),
        pk=pk,
    )
    errores = batch.errores.all()[:200]
    context = {
        "batch": batch,
        "errores": errores,
        "breadcrumbs": [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Importaciones"},
            {"label": f"Lote #{batch.pk}"},
        ],
    }
    return render(request, "wcgone/imports/batch_result.html", context)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib.auth.decorators import login_required
00002|from django.shortcuts import get_object_or_404, render
00003|
00004|from apps.core.models import DataImportBatch, DataImportError
00005|
00006|
00007|@login_required
00008|def import_batch_detail(request, pk):
00009|    batch = get_object_or_404(
00010|        DataImportBatch.objects.select_related("usuario"),
00011|        pk=pk,
00012|    )
00013|    errores = batch.errores.all()[:200]
00014|    context = {
00015|        "batch": batch,
00016|        "errores": errores,
00017|        "breadcrumbs": [
00018|            {"label": "Panel principal", "url": "/panel/"},
00019|            {"label": "Importaciones"},
00020|            {"label": f"Lote #{batch.pk}"},
00021|        ],
00022|    }
00023|    return render(request, "wcgone/imports/batch_result.html", context)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYi5hdXRoLmRlY29yYXRvcnMgaW1wb3J0IGxvZ2luX3JlcXVpcmVkCmZyb20gZGphbmdvLnNob3J0Y3V0cyBpbXBvcnQgZ2V0X29iamVjdF9vcl80MDQsIHJlbmRlcgoKZnJvbSBhcHBzLmNvcmUubW9kZWxzIGltcG9ydCBEYXRhSW1wb3J0QmF0Y2gsIERhdGFJbXBvcnRFcnJvcgoKCkBsb2dpbl9yZXF1aXJlZApkZWYgaW1wb3J0X2JhdGNoX2RldGFpbChyZXF1ZXN0LCBwayk6CiAgICBiYXRjaCA9IGdldF9vYmplY3Rfb3JfNDA0KAogICAgICAgIERhdGFJbXBvcnRCYXRjaC5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJ1c3VhcmlvIiksCiAgICAgICAgcGs9cGssCiAgICApCiAgICBlcnJvcmVzID0gYmF0Y2guZXJyb3Jlcy5hbGwoKVs6MjAwXQogICAgY29udGV4dCA9IHsKICAgICAgICAiYmF0Y2giOiBiYXRjaCwKICAgICAgICAiZXJyb3JlcyI6IGVycm9yZXMsCiAgICAgICAgImJyZWFkY3J1bWJzIjogWwogICAgICAgICAgICB7ImxhYmVsIjogIlBhbmVsIHByaW5jaXBhbCIsICJ1cmwiOiAiL3BhbmVsLyJ9LAogICAgICAgICAgICB7ImxhYmVsIjogIkltcG9ydGFjaW9uZXMifSwKICAgICAgICAgICAgeyJsYWJlbCI6IGYiTG90ZSAje2JhdGNoLnBrfSJ9LAogICAgICAgIF0sCiAgICB9CiAgICByZXR1cm4gcmVuZGVyKHJlcXVlc3QsICJ3Y2dvbmUvaW1wb3J0cy9iYXRjaF9yZXN1bHQuaHRtbCIsIGNvbnRleHQpCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/crm/__init__.py
PATH_JSON="apps/crm/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/crm/admin.py
PATH_JSON="apps/crm/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=46
SIZE_BYTES_UTF8=1379
CONTENT_SHA256=fdb0a94b892776d3984b8e2f918509d679e90a2a110edc13f016c5a708f1c711
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.contrib import admin

from .models import Interaccion, NotaEntidad, Tarea


@admin.register(Interaccion)
class InteraccionAdmin(admin.ModelAdmin):
    list_display = (
        "fecha",
        "entidad",
        "tipo_interaccion",
        "resumen",
        "usuario",
        "seguimiento_requerido",
    )
    list_filter = ("tipo_interaccion", "fecha", "seguimiento_requerido")
    search_fields = ("resumen", "resultado", "entidad__nombre", "entidad__nit")
    date_hierarchy = "fecha"
    autocomplete_fields = ("entidad", "producto", "usuario")
    ordering = ("-fecha",)


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = (
        "descripcion",
        "entidad",
        "estado",
        "prioridad",
        "fecha_limite",
        "completada",
        "asignado_a",
    )
    list_filter = ("estado", "completada", "prioridad", "fecha_limite")
    search_fields = ("descripcion", "entidad__nombre", "entidad__nit")
    autocomplete_fields = ("entidad", "contacto", "asignado_a")
    ordering = ("completada", "fecha_limite")


@admin.register(NotaEntidad)
class NotaEntidadAdmin(admin.ModelAdmin):
    list_display = ("fecha", "entidad", "titulo", "autor")
    list_filter = ("fecha",)
    search_fields = ("titulo", "contenido", "entidad__nombre")
    autocomplete_fields = ("entidad", "autor")
    ordering = ("-fecha",)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import admin
00002|
00003|from .models import Interaccion, NotaEntidad, Tarea
00004|
00005|
00006|@admin.register(Interaccion)
00007|class InteraccionAdmin(admin.ModelAdmin):
00008|    list_display = (
00009|        "fecha",
00010|        "entidad",
00011|        "tipo_interaccion",
00012|        "resumen",
00013|        "usuario",
00014|        "seguimiento_requerido",
00015|    )
00016|    list_filter = ("tipo_interaccion", "fecha", "seguimiento_requerido")
00017|    search_fields = ("resumen", "resultado", "entidad__nombre", "entidad__nit")
00018|    date_hierarchy = "fecha"
00019|    autocomplete_fields = ("entidad", "producto", "usuario")
00020|    ordering = ("-fecha",)
00021|
00022|
00023|@admin.register(Tarea)
00024|class TareaAdmin(admin.ModelAdmin):
00025|    list_display = (
00026|        "descripcion",
00027|        "entidad",
00028|        "estado",
00029|        "prioridad",
00030|        "fecha_limite",
00031|        "completada",
00032|        "asignado_a",
00033|    )
00034|    list_filter = ("estado", "completada", "prioridad", "fecha_limite")
00035|    search_fields = ("descripcion", "entidad__nombre", "entidad__nit")
00036|    autocomplete_fields = ("entidad", "contacto", "asignado_a")
00037|    ordering = ("completada", "fecha_limite")
00038|
00039|
00040|@admin.register(NotaEntidad)
00041|class NotaEntidadAdmin(admin.ModelAdmin):
00042|    list_display = ("fecha", "entidad", "titulo", "autor")
00043|    list_filter = ("fecha",)
00044|    search_fields = ("titulo", "contenido", "entidad__nombre")
00045|    autocomplete_fields = ("entidad", "autor")
00046|    ordering = ("-fecha",)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgYWRtaW4KCmZyb20gLm1vZGVscyBpbXBvcnQgSW50ZXJhY2Npb24sIE5vdGFFbnRpZGFkLCBUYXJlYQoKCkBhZG1pbi5yZWdpc3RlcihJbnRlcmFjY2lvbikKY2xhc3MgSW50ZXJhY2Npb25BZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAiZmVjaGEiLAogICAgICAgICJlbnRpZGFkIiwKICAgICAgICAidGlwb19pbnRlcmFjY2lvbiIsCiAgICAgICAgInJlc3VtZW4iLAogICAgICAgICJ1c3VhcmlvIiwKICAgICAgICAic2VndWltaWVudG9fcmVxdWVyaWRvIiwKICAgICkKICAgIGxpc3RfZmlsdGVyID0gKCJ0aXBvX2ludGVyYWNjaW9uIiwgImZlY2hhIiwgInNlZ3VpbWllbnRvX3JlcXVlcmlkbyIpCiAgICBzZWFyY2hfZmllbGRzID0gKCJyZXN1bWVuIiwgInJlc3VsdGFkbyIsICJlbnRpZGFkX19ub21icmUiLCAiZW50aWRhZF9fbml0IikKICAgIGRhdGVfaGllcmFyY2h5ID0gImZlY2hhIgogICAgYXV0b2NvbXBsZXRlX2ZpZWxkcyA9ICgiZW50aWRhZCIsICJwcm9kdWN0byIsICJ1c3VhcmlvIikKICAgIG9yZGVyaW5nID0gKCItZmVjaGEiLCkKCgpAYWRtaW4ucmVnaXN0ZXIoVGFyZWEpCmNsYXNzIFRhcmVhQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoCiAgICAgICAgImRlc2NyaXBjaW9uIiwKICAgICAgICAiZW50aWRhZCIsCiAgICAgICAgImVzdGFkbyIsCiAgICAgICAgInByaW9yaWRhZCIsCiAgICAgICAgImZlY2hhX2xpbWl0ZSIsCiAgICAgICAgImNvbXBsZXRhZGEiLAogICAgICAgICJhc2lnbmFkb19hIiwKICAgICkKICAgIGxpc3RfZmlsdGVyID0gKCJlc3RhZG8iLCAiY29tcGxldGFkYSIsICJwcmlvcmlkYWQiLCAiZmVjaGFfbGltaXRlIikKICAgIHNlYXJjaF9maWVsZHMgPSAoImRlc2NyaXBjaW9uIiwgImVudGlkYWRfX25vbWJyZSIsICJlbnRpZGFkX19uaXQiKQogICAgYXV0b2NvbXBsZXRlX2ZpZWxkcyA9ICgiZW50aWRhZCIsICJjb250YWN0byIsICJhc2lnbmFkb19hIikKICAgIG9yZGVyaW5nID0gKCJjb21wbGV0YWRhIiwgImZlY2hhX2xpbWl0ZSIpCgoKQGFkbWluLnJlZ2lzdGVyKE5vdGFFbnRpZGFkKQpjbGFzcyBOb3RhRW50aWRhZEFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKCJmZWNoYSIsICJlbnRpZGFkIiwgInRpdHVsbyIsICJhdXRvciIpCiAgICBsaXN0X2ZpbHRlciA9ICgiZmVjaGEiLCkKICAgIHNlYXJjaF9maWVsZHMgPSAoInRpdHVsbyIsICJjb250ZW5pZG8iLCAiZW50aWRhZF9fbm9tYnJlIikKICAgIGF1dG9jb21wbGV0ZV9maWVsZHMgPSAoImVudGlkYWQiLCAiYXV0b3IiKQogICAgb3JkZXJpbmcgPSAoIi1mZWNoYSIsKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/crm/apps.py
PATH_JSON="apps/crm/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=8
SIZE_BYTES_UTF8=193
CONTENT_SHA256=14d0834230ed4e43dde77491304010efa63aa2bd22bd95ba3bdfc7e0a8d9b4f1
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.apps import AppConfig


class CrmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.crm"
    label = "wcgone_crm"
    verbose_name = "CRM"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class CrmConfig(AppConfig):
00005|    default_auto_field = "django.db.models.BigAutoField"
00006|    name = "apps.crm"
00007|    label = "wcgone_crm"
00008|    verbose_name = "CRM"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgQ3JtQ29uZmlnKEFwcENvbmZpZyk6CiAgICBkZWZhdWx0X2F1dG9fZmllbGQgPSAiZGphbmdvLmRiLm1vZGVscy5CaWdBdXRvRmllbGQiCiAgICBuYW1lID0gImFwcHMuY3JtIgogICAgbGFiZWwgPSAid2Nnb25lX2NybSIKICAgIHZlcmJvc2VfbmFtZSA9ICJDUk0iCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/crm/imports/__init__.py
PATH_JSON="apps/crm/imports/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=106
CONTENT_SHA256=a376fa7ca77d732379ed5c6c435e5d3066d685a3750f23a5f0f97d0dd0967286
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from apps.crm.imports.entidades import import_entidades_clientes

__all__ = ["import_entidades_clientes"]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from apps.crm.imports.entidades import import_entidades_clientes
00002|
00003|__all__ = ["import_entidades_clientes"]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBhcHBzLmNybS5pbXBvcnRzLmVudGlkYWRlcyBpbXBvcnQgaW1wb3J0X2VudGlkYWRlc19jbGllbnRlcwoKX19hbGxfXyA9IFsiaW1wb3J0X2VudGlkYWRlc19jbGllbnRlcyJdCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/crm/imports/entidades.py
PATH_JSON="apps/crm/imports/entidades.py"
FILENAME=entidades.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=76
SIZE_BYTES_UTF8=2449
CONTENT_SHA256=2ff809bbf801b9aa1a2290c7e345c0bf147ea3abe078c22e86b258e31d084d7c
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Importador CRM: entidades y contactos desde CSV/XLSX."""

from __future__ import annotations

import pandas as pd

from apps.core.imports.base import run_import_batch
from apps.core.imports.columns import normalize_columns, pick, require_any
from apps.core.imports.entities import upsert_contacto_from_row, upsert_entidad
from apps.core.models import Entidad


MODULO = "crm"
TIPO = "entidades_clientes"


def _preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    require_any(
        df,
        [
            ["nit", "nit_cliente", "codigo", "codigo_cliente"],
            ["nombre", "razon_social", "cliente", "nombre_cliente"],
        ],
    )
    return df


def import_entidades_clientes(user, uploaded_file):
    uploaded_file.seek(0)

    def handler(row: pd.Series, errors: list[str], batch=None):
        nombre = pick(row, "nombre", "razon_social", "cliente", "nombre_cliente")
        nit = pick(row, "nit", "nit_cliente", "codigo", "codigo_cliente")
        if not nombre and not nit:
            errors.append("Falta nombre o NIT.")
            return None
        if not nombre:
            nombre = nit
        tipo_raw = pick(row, "tipo", "tipo_entidad", "tipo_cliente").lower()
        tipo = Entidad.TIPO_CLIENTE
        if "prospect" in tipo_raw:
            tipo = Entidad.TIPO_PROSPECTO
        elif "proveedor" in tipo_raw:
            tipo = Entidad.TIPO_PROVEEDOR
        try:
            entidad, created_e, updated_e = upsert_entidad(
                nit=nit,
                nombre=nombre,
                defaults={
                    "tipo_entidad": tipo,
                    "telefono": pick(row, "telefono", "tel"),
                    "email": pick(row, "email", "correo"),
                    "ciudad": pick(row, "ciudad"),
                    "notas": pick(row, "notas", "observaciones"),
                    "origen": "importacion_crm",
                },
            )
        except ValueError as exc:
            errors.append(str(exc))
            return None
        _, created_c = upsert_contacto_from_row(entidad, row)
        if created_e or created_c:
            return True, False
        if updated_e:
            return False, True
        return False, False

    return run_import_batch(
        user=user,
        modulo=MODULO,
        tipo_importacion=TIPO,
        uploaded_file=uploaded_file,
        preprocess=_preprocess,
        row_handler=handler,
    )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Importador CRM: entidades y contactos desde CSV/XLSX."""
00002|
00003|from __future__ import annotations
00004|
00005|import pandas as pd
00006|
00007|from apps.core.imports.base import run_import_batch
00008|from apps.core.imports.columns import normalize_columns, pick, require_any
00009|from apps.core.imports.entities import upsert_contacto_from_row, upsert_entidad
00010|from apps.core.models import Entidad
00011|
00012|
00013|MODULO = "crm"
00014|TIPO = "entidades_clientes"
00015|
00016|
00017|def _preprocess(df: pd.DataFrame) -> pd.DataFrame:
00018|    df = normalize_columns(df)
00019|    require_any(
00020|        df,
00021|        [
00022|            ["nit", "nit_cliente", "codigo", "codigo_cliente"],
00023|            ["nombre", "razon_social", "cliente", "nombre_cliente"],
00024|        ],
00025|    )
00026|    return df
00027|
00028|
00029|def import_entidades_clientes(user, uploaded_file):
00030|    uploaded_file.seek(0)
00031|
00032|    def handler(row: pd.Series, errors: list[str], batch=None):
00033|        nombre = pick(row, "nombre", "razon_social", "cliente", "nombre_cliente")
00034|        nit = pick(row, "nit", "nit_cliente", "codigo", "codigo_cliente")
00035|        if not nombre and not nit:
00036|            errors.append("Falta nombre o NIT.")
00037|            return None
00038|        if not nombre:
00039|            nombre = nit
00040|        tipo_raw = pick(row, "tipo", "tipo_entidad", "tipo_cliente").lower()
00041|        tipo = Entidad.TIPO_CLIENTE
00042|        if "prospect" in tipo_raw:
00043|            tipo = Entidad.TIPO_PROSPECTO
00044|        elif "proveedor" in tipo_raw:
00045|            tipo = Entidad.TIPO_PROVEEDOR
00046|        try:
00047|            entidad, created_e, updated_e = upsert_entidad(
00048|                nit=nit,
00049|                nombre=nombre,
00050|                defaults={
00051|                    "tipo_entidad": tipo,
00052|                    "telefono": pick(row, "telefono", "tel"),
00053|                    "email": pick(row, "email", "correo"),
00054|                    "ciudad": pick(row, "ciudad"),
00055|                    "notas": pick(row, "notas", "observaciones"),
00056|                    "origen": "importacion_crm",
00057|                },
00058|            )
00059|        except ValueError as exc:
00060|            errors.append(str(exc))
00061|            return None
00062|        _, created_c = upsert_contacto_from_row(entidad, row)
00063|        if created_e or created_c:
00064|            return True, False
00065|        if updated_e:
00066|            return False, True
00067|        return False, False
00068|
00069|    return run_import_batch(
00070|        user=user,
00071|        modulo=MODULO,
00072|        tipo_importacion=TIPO,
00073|        uploaded_file=uploaded_file,
00074|        preprocess=_preprocess,
00075|        row_handler=handler,
00076|    )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiSW1wb3J0YWRvciBDUk06IGVudGlkYWRlcyB5IGNvbnRhY3RvcyBkZXNkZSBDU1YvWExTWC4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmltcG9ydCBwYW5kYXMgYXMgcGQKCmZyb20gYXBwcy5jb3JlLmltcG9ydHMuYmFzZSBpbXBvcnQgcnVuX2ltcG9ydF9iYXRjaApmcm9tIGFwcHMuY29yZS5pbXBvcnRzLmNvbHVtbnMgaW1wb3J0IG5vcm1hbGl6ZV9jb2x1bW5zLCBwaWNrLCByZXF1aXJlX2FueQpmcm9tIGFwcHMuY29yZS5pbXBvcnRzLmVudGl0aWVzIGltcG9ydCB1cHNlcnRfY29udGFjdG9fZnJvbV9yb3csIHVwc2VydF9lbnRpZGFkCmZyb20gYXBwcy5jb3JlLm1vZGVscyBpbXBvcnQgRW50aWRhZAoKCk1PRFVMTyA9ICJjcm0iClRJUE8gPSAiZW50aWRhZGVzX2NsaWVudGVzIgoKCmRlZiBfcHJlcHJvY2VzcyhkZjogcGQuRGF0YUZyYW1lKSAtPiBwZC5EYXRhRnJhbWU6CiAgICBkZiA9IG5vcm1hbGl6ZV9jb2x1bW5zKGRmKQogICAgcmVxdWlyZV9hbnkoCiAgICAgICAgZGYsCiAgICAgICAgWwogICAgICAgICAgICBbIm5pdCIsICJuaXRfY2xpZW50ZSIsICJjb2RpZ28iLCAiY29kaWdvX2NsaWVudGUiXSwKICAgICAgICAgICAgWyJub21icmUiLCAicmF6b25fc29jaWFsIiwgImNsaWVudGUiLCAibm9tYnJlX2NsaWVudGUiXSwKICAgICAgICBdLAogICAgKQogICAgcmV0dXJuIGRmCgoKZGVmIGltcG9ydF9lbnRpZGFkZXNfY2xpZW50ZXModXNlciwgdXBsb2FkZWRfZmlsZSk6CiAgICB1cGxvYWRlZF9maWxlLnNlZWsoMCkKCiAgICBkZWYgaGFuZGxlcihyb3c6IHBkLlNlcmllcywgZXJyb3JzOiBsaXN0W3N0cl0sIGJhdGNoPU5vbmUpOgogICAgICAgIG5vbWJyZSA9IHBpY2socm93LCAibm9tYnJlIiwgInJhem9uX3NvY2lhbCIsICJjbGllbnRlIiwgIm5vbWJyZV9jbGllbnRlIikKICAgICAgICBuaXQgPSBwaWNrKHJvdywgIm5pdCIsICJuaXRfY2xpZW50ZSIsICJjb2RpZ28iLCAiY29kaWdvX2NsaWVudGUiKQogICAgICAgIGlmIG5vdCBub21icmUgYW5kIG5vdCBuaXQ6CiAgICAgICAgICAgIGVycm9ycy5hcHBlbmQoIkZhbHRhIG5vbWJyZSBvIE5JVC4iKQogICAgICAgICAgICByZXR1cm4gTm9uZQogICAgICAgIGlmIG5vdCBub21icmU6CiAgICAgICAgICAgIG5vbWJyZSA9IG5pdAogICAgICAgIHRpcG9fcmF3ID0gcGljayhyb3csICJ0aXBvIiwgInRpcG9fZW50aWRhZCIsICJ0aXBvX2NsaWVudGUiKS5sb3dlcigpCiAgICAgICAgdGlwbyA9IEVudGlkYWQuVElQT19DTElFTlRFCiAgICAgICAgaWYgInByb3NwZWN0IiBpbiB0aXBvX3JhdzoKICAgICAgICAgICAgdGlwbyA9IEVudGlkYWQuVElQT19QUk9TUEVDVE8KICAgICAgICBlbGlmICJwcm92ZWVkb3IiIGluIHRpcG9fcmF3OgogICAgICAgICAgICB0aXBvID0gRW50aWRhZC5USVBPX1BST1ZFRURPUgogICAgICAgIHRyeToKICAgICAgICAgICAgZW50aWRhZCwgY3JlYXRlZF9lLCB1cGRhdGVkX2UgPSB1cHNlcnRfZW50aWRhZCgKICAgICAgICAgICAgICAgIG5pdD1uaXQsCiAgICAgICAgICAgICAgICBub21icmU9bm9tYnJlLAogICAgICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgICAgICJ0aXBvX2VudGlkYWQiOiB0aXBvLAogICAgICAgICAgICAgICAgICAgICJ0ZWxlZm9ubyI6IHBpY2socm93LCAidGVsZWZvbm8iLCAidGVsIiksCiAgICAgICAgICAgICAgICAgICAgImVtYWlsIjogcGljayhyb3csICJlbWFpbCIsICJjb3JyZW8iKSwKICAgICAgICAgICAgICAgICAgICAiY2l1ZGFkIjogcGljayhyb3csICJjaXVkYWQiKSwKICAgICAgICAgICAgICAgICAgICAibm90YXMiOiBwaWNrKHJvdywgIm5vdGFzIiwgIm9ic2VydmFjaW9uZXMiKSwKICAgICAgICAgICAgICAgICAgICAib3JpZ2VuIjogImltcG9ydGFjaW9uX2NybSIsCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICApCiAgICAgICAgZXhjZXB0IFZhbHVlRXJyb3IgYXMgZXhjOgogICAgICAgICAgICBlcnJvcnMuYXBwZW5kKHN0cihleGMpKQogICAgICAgICAgICByZXR1cm4gTm9uZQogICAgICAgIF8sIGNyZWF0ZWRfYyA9IHVwc2VydF9jb250YWN0b19mcm9tX3JvdyhlbnRpZGFkLCByb3cpCiAgICAgICAgaWYgY3JlYXRlZF9lIG9yIGNyZWF0ZWRfYzoKICAgICAgICAgICAgcmV0dXJuIFRydWUsIEZhbHNlCiAgICAgICAgaWYgdXBkYXRlZF9lOgogICAgICAgICAgICByZXR1cm4gRmFsc2UsIFRydWUKICAgICAgICByZXR1cm4gRmFsc2UsIEZhbHNlCgogICAgcmV0dXJuIHJ1bl9pbXBvcnRfYmF0Y2goCiAgICAgICAgdXNlcj11c2VyLAogICAgICAgIG1vZHVsbz1NT0RVTE8sCiAgICAgICAgdGlwb19pbXBvcnRhY2lvbj1USVBPLAogICAgICAgIHVwbG9hZGVkX2ZpbGU9dXBsb2FkZWRfZmlsZSwKICAgICAgICBwcmVwcm9jZXNzPV9wcmVwcm9jZXNzLAogICAgICAgIHJvd19oYW5kbGVyPWhhbmRsZXIsCiAgICApCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/crm/models.py
PATH_JSON="apps/crm/models.py"
FILENAME=models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=116
SIZE_BYTES_UTF8=3485
CONTENT_SHA256=38f200cc5f21135f1a885ca9b2e32a4a79880a8877854b1ce1267d2ff0633a6a
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.conf import settings
from django.db import models


class Interaccion(models.Model):
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="interacciones",
    )
    producto = models.ForeignKey(
        "wcgone_core.Producto",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interacciones",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_crm_interacciones",
    )
    fecha = models.DateField(db_index=True)
    hora = models.TimeField(null=True, blank=True)
    tipo_interaccion = models.CharField(max_length=50, db_index=True)
    resumen = models.CharField(max_length=255)
    resultado = models.TextField(blank=True)
    seguimiento_requerido = models.BooleanField(default=False)
    notas = models.TextField(blank=True)
    import_batch = models.ForeignKey(
        "wcgone_core.DataImportBatch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_crm_interacciones",
    )

    class Meta:
        ordering = ["-fecha", "-id"]
        verbose_name = "Interacción"
        verbose_name_plural = "Interacciones"
        indexes = [
            models.Index(fields=["entidad", "fecha"]),
        ]

    def __str__(self):
        return f"{self.entidad} — {self.resumen}"


class Tarea(models.Model):
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="tareas",
    )
    contacto = models.ForeignKey(
        "wcgone_core.Contacto",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tareas",
    )
    asignado_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_crm_tareas",
    )
    fecha_limite = models.DateField(null=True, blank=True)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=30, default="pendiente")
    completada = models.BooleanField(default=False)
    fecha_completada = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["completada", "fecha_limite", "-id"]
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        indexes = [
            models.Index(fields=["completada", "fecha_limite"]),
            models.Index(fields=["entidad", "estado"]),
        ]

    def __str__(self):
        return f"{self.entidad} — {self.descripcion[:50]}"


class NotaEntidad(models.Model):
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="notas_entidad",
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_notas_entidad",
    )
    fecha = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Nota de entidad"
        verbose_name_plural = "Notas de entidad"

    def __str__(self):
        return f"{self.entidad} — {self.titulo}"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.conf import settings
00002|from django.db import models
00003|
00004|
00005|class Interaccion(models.Model):
00006|    entidad = models.ForeignKey(
00007|        "wcgone_core.Entidad",
00008|        on_delete=models.CASCADE,
00009|        related_name="interacciones",
00010|    )
00011|    producto = models.ForeignKey(
00012|        "wcgone_core.Producto",
00013|        on_delete=models.SET_NULL,
00014|        null=True,
00015|        blank=True,
00016|        related_name="interacciones",
00017|    )
00018|    usuario = models.ForeignKey(
00019|        settings.AUTH_USER_MODEL,
00020|        on_delete=models.SET_NULL,
00021|        null=True,
00022|        blank=True,
00023|        related_name="wcgone_crm_interacciones",
00024|    )
00025|    fecha = models.DateField(db_index=True)
00026|    hora = models.TimeField(null=True, blank=True)
00027|    tipo_interaccion = models.CharField(max_length=50, db_index=True)
00028|    resumen = models.CharField(max_length=255)
00029|    resultado = models.TextField(blank=True)
00030|    seguimiento_requerido = models.BooleanField(default=False)
00031|    notas = models.TextField(blank=True)
00032|    import_batch = models.ForeignKey(
00033|        "wcgone_core.DataImportBatch",
00034|        on_delete=models.SET_NULL,
00035|        null=True,
00036|        blank=True,
00037|        related_name="wcgone_crm_interacciones",
00038|    )
00039|
00040|    class Meta:
00041|        ordering = ["-fecha", "-id"]
00042|        verbose_name = "Interacción"
00043|        verbose_name_plural = "Interacciones"
00044|        indexes = [
00045|            models.Index(fields=["entidad", "fecha"]),
00046|        ]
00047|
00048|    def __str__(self):
00049|        return f"{self.entidad} — {self.resumen}"
00050|
00051|
00052|class Tarea(models.Model):
00053|    entidad = models.ForeignKey(
00054|        "wcgone_core.Entidad",
00055|        on_delete=models.CASCADE,
00056|        related_name="tareas",
00057|    )
00058|    contacto = models.ForeignKey(
00059|        "wcgone_core.Contacto",
00060|        on_delete=models.SET_NULL,
00061|        null=True,
00062|        blank=True,
00063|        related_name="tareas",
00064|    )
00065|    asignado_a = models.ForeignKey(
00066|        settings.AUTH_USER_MODEL,
00067|        on_delete=models.SET_NULL,
00068|        null=True,
00069|        blank=True,
00070|        related_name="wcgone_crm_tareas",
00071|    )
00072|    fecha_limite = models.DateField(null=True, blank=True)
00073|    descripcion = models.TextField()
00074|    prioridad = models.CharField(max_length=20, blank=True)
00075|    estado = models.CharField(max_length=30, default="pendiente")
00076|    completada = models.BooleanField(default=False)
00077|    fecha_completada = models.DateField(null=True, blank=True)
00078|    notas = models.TextField(blank=True)
00079|
00080|    class Meta:
00081|        ordering = ["completada", "fecha_limite", "-id"]
00082|        verbose_name = "Tarea"
00083|        verbose_name_plural = "Tareas"
00084|        indexes = [
00085|            models.Index(fields=["completada", "fecha_limite"]),
00086|            models.Index(fields=["entidad", "estado"]),
00087|        ]
00088|
00089|    def __str__(self):
00090|        return f"{self.entidad} — {self.descripcion[:50]}"
00091|
00092|
00093|class NotaEntidad(models.Model):
00094|    entidad = models.ForeignKey(
00095|        "wcgone_core.Entidad",
00096|        on_delete=models.CASCADE,
00097|        related_name="notas_entidad",
00098|    )
00099|    autor = models.ForeignKey(
00100|        settings.AUTH_USER_MODEL,
00101|        on_delete=models.SET_NULL,
00102|        null=True,
00103|        blank=True,
00104|        related_name="crm_notas_entidad",
00105|    )
00106|    fecha = models.DateTimeField(auto_now_add=True)
00107|    titulo = models.CharField(max_length=200)
00108|    contenido = models.TextField()
00109|
00110|    class Meta:
00111|        ordering = ["-fecha"]
00112|        verbose_name = "Nota de entidad"
00113|        verbose_name_plural = "Notas de entidad"
00114|
00115|    def __str__(self):
00116|        return f"{self.entidad} — {self.titulo}"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29uZiBpbXBvcnQgc2V0dGluZ3MKZnJvbSBkamFuZ28uZGIgaW1wb3J0IG1vZGVscwoKCmNsYXNzIEludGVyYWNjaW9uKG1vZGVscy5Nb2RlbCk6CiAgICBlbnRpZGFkID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgIndjZ29uZV9jb3JlLkVudGlkYWQiLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwKICAgICAgICByZWxhdGVkX25hbWU9ImludGVyYWNjaW9uZXMiLAogICAgKQogICAgcHJvZHVjdG8gPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICAid2Nnb25lX2NvcmUuUHJvZHVjdG8iLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJpbnRlcmFjY2lvbmVzIiwKICAgICkKICAgIHVzdWFyaW8gPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICBzZXR0aW5ncy5BVVRIX1VTRVJfTU9ERUwsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5TRVRfTlVMTCwKICAgICAgICBudWxsPVRydWUsCiAgICAgICAgYmxhbms9VHJ1ZSwKICAgICAgICByZWxhdGVkX25hbWU9IndjZ29uZV9jcm1faW50ZXJhY2Npb25lcyIsCiAgICApCiAgICBmZWNoYSA9IG1vZGVscy5EYXRlRmllbGQoZGJfaW5kZXg9VHJ1ZSkKICAgIGhvcmEgPSBtb2RlbHMuVGltZUZpZWxkKG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIHRpcG9faW50ZXJhY2Npb24gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9NTAsIGRiX2luZGV4PVRydWUpCiAgICByZXN1bWVuID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTI1NSkKICAgIHJlc3VsdGFkbyA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKICAgIHNlZ3VpbWllbnRvX3JlcXVlcmlkbyA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1GYWxzZSkKICAgIG5vdGFzID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQogICAgaW1wb3J0X2JhdGNoID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgIndjZ29uZV9jb3JlLkRhdGFJbXBvcnRCYXRjaCIsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5TRVRfTlVMTCwKICAgICAgICBudWxsPVRydWUsCiAgICAgICAgYmxhbms9VHJ1ZSwKICAgICAgICByZWxhdGVkX25hbWU9IndjZ29uZV9jcm1faW50ZXJhY2Npb25lcyIsCiAgICApCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsiLWZlY2hhIiwgIi1pZCJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIkludGVyYWNjacOzbiIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIkludGVyYWNjaW9uZXMiCiAgICAgICAgaW5kZXhlcyA9IFsKICAgICAgICAgICAgbW9kZWxzLkluZGV4KGZpZWxkcz1bImVudGlkYWQiLCAiZmVjaGEiXSksCiAgICAgICAgXQoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLmVudGlkYWR9IOKAlCB7c2VsZi5yZXN1bWVufSIKCgpjbGFzcyBUYXJlYShtb2RlbHMuTW9kZWwpOgogICAgZW50aWRhZCA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgICJ3Y2dvbmVfY29yZS5FbnRpZGFkIiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJ0YXJlYXMiLAogICAgKQogICAgY29udGFjdG8gPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICAid2Nnb25lX2NvcmUuQ29udGFjdG8iLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJ0YXJlYXMiLAogICAgKQogICAgYXNpZ25hZG9fYSA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIHNldHRpbmdzLkFVVEhfVVNFUl9NT0RFTCwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0id2Nnb25lX2NybV90YXJlYXMiLAogICAgKQogICAgZmVjaGFfbGltaXRlID0gbW9kZWxzLkRhdGVGaWVsZChudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBkZXNjcmlwY2lvbiA9IG1vZGVscy5UZXh0RmllbGQoKQogICAgcHJpb3JpZGFkID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTIwLCBibGFuaz1UcnVlKQogICAgZXN0YWRvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTMwLCBkZWZhdWx0PSJwZW5kaWVudGUiKQogICAgY29tcGxldGFkYSA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1GYWxzZSkKICAgIGZlY2hhX2NvbXBsZXRhZGEgPSBtb2RlbHMuRGF0ZUZpZWxkKG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIG5vdGFzID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbImNvbXBsZXRhZGEiLCAiZmVjaGFfbGltaXRlIiwgIi1pZCJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIlRhcmVhIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiVGFyZWFzIgogICAgICAgIGluZGV4ZXMgPSBbCiAgICAgICAgICAgIG1vZGVscy5JbmRleChmaWVsZHM9WyJjb21wbGV0YWRhIiwgImZlY2hhX2xpbWl0ZSJdKSwKICAgICAgICAgICAgbW9kZWxzLkluZGV4KGZpZWxkcz1bImVudGlkYWQiLCAiZXN0YWRvIl0pLAogICAgICAgIF0KCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5lbnRpZGFkfSDigJQge3NlbGYuZGVzY3JpcGNpb25bOjUwXX0iCgoKY2xhc3MgTm90YUVudGlkYWQobW9kZWxzLk1vZGVsKToKICAgIGVudGlkYWQgPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICAid2Nnb25lX2NvcmUuRW50aWRhZCIsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0ibm90YXNfZW50aWRhZCIsCiAgICApCiAgICBhdXRvciA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIHNldHRpbmdzLkFVVEhfVVNFUl9NT0RFTCwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0iY3JtX25vdGFzX2VudGlkYWQiLAogICAgKQogICAgZmVjaGEgPSBtb2RlbHMuRGF0ZVRpbWVGaWVsZChhdXRvX25vd19hZGQ9VHJ1ZSkKICAgIHRpdHVsbyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yMDApCiAgICBjb250ZW5pZG8gPSBtb2RlbHMuVGV4dEZpZWxkKCkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWyItZmVjaGEiXQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICJOb3RhIGRlIGVudGlkYWQiCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJOb3RhcyBkZSBlbnRpZGFkIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLmVudGlkYWR9IOKAlCB7c2VsZi50aXR1bG99Igo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/crm/selectors.py
PATH_JSON="apps/crm/selectors.py"
FILENAME=selectors.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=49
SIZE_BYTES_UTF8=1495
CONTENT_SHA256=c15404e6173b701d0f7d26cbf23013f8f6f6d6a71fef46aaeb641d1befbc9359
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Consultas reutilizables para listados CRM y KPIs."""

from __future__ import annotations

from django.db.models import Count, Q

from apps.core.models import Entidad


def entidad_list_queryset(request):
    qs = Entidad.objects.annotate(
        num_contactos=Count("contactos", distinct=True),
        num_productos=Count("relaciones_producto", distinct=True),
    ).order_by("nombre")
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(nombre__icontains=q) | Q(nit__icontains=q))
    tipo = request.GET.get("tipo", "").strip()
    if tipo:
        qs = qs.filter(tipo_entidad=tipo)
    activo = request.GET.get("activo", "").strip()
    if activo == "1":
        qs = qs.filter(activo=True)
    elif activo == "0":
        qs = qs.filter(activo=False)
    return qs


def entidad_summary(queryset=None):
    base = queryset if queryset is not None else Entidad.objects.all()
    por_ciudad = list(
        base.exclude(ciudad="")
        .values("ciudad")
        .annotate(total=Count("id"))
        .order_by("-total", "ciudad")[:5]
    )
    por_riesgo = list(
        base.exclude(categoria_riesgo="")
        .values("categoria_riesgo")
        .annotate(total=Count("id"))
        .order_by("-total", "categoria_riesgo")[:5]
    )
    return {
        "total": base.count(),
        "activas": base.filter(activo=True).count(),
        "inactivas": base.filter(activo=False).count(),
        "por_ciudad": por_ciudad,
        "por_riesgo": por_riesgo,
    }

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Consultas reutilizables para listados CRM y KPIs."""
00002|
00003|from __future__ import annotations
00004|
00005|from django.db.models import Count, Q
00006|
00007|from apps.core.models import Entidad
00008|
00009|
00010|def entidad_list_queryset(request):
00011|    qs = Entidad.objects.annotate(
00012|        num_contactos=Count("contactos", distinct=True),
00013|        num_productos=Count("relaciones_producto", distinct=True),
00014|    ).order_by("nombre")
00015|    q = request.GET.get("q", "").strip()
00016|    if q:
00017|        qs = qs.filter(Q(nombre__icontains=q) | Q(nit__icontains=q))
00018|    tipo = request.GET.get("tipo", "").strip()
00019|    if tipo:
00020|        qs = qs.filter(tipo_entidad=tipo)
00021|    activo = request.GET.get("activo", "").strip()
00022|    if activo == "1":
00023|        qs = qs.filter(activo=True)
00024|    elif activo == "0":
00025|        qs = qs.filter(activo=False)
00026|    return qs
00027|
00028|
00029|def entidad_summary(queryset=None):
00030|    base = queryset if queryset is not None else Entidad.objects.all()
00031|    por_ciudad = list(
00032|        base.exclude(ciudad="")
00033|        .values("ciudad")
00034|        .annotate(total=Count("id"))
00035|        .order_by("-total", "ciudad")[:5]
00036|    )
00037|    por_riesgo = list(
00038|        base.exclude(categoria_riesgo="")
00039|        .values("categoria_riesgo")
00040|        .annotate(total=Count("id"))
00041|        .order_by("-total", "categoria_riesgo")[:5]
00042|    )
00043|    return {
00044|        "total": base.count(),
00045|        "activas": base.filter(activo=True).count(),
00046|        "inactivas": base.filter(activo=False).count(),
00047|        "por_ciudad": por_ciudad,
00048|        "por_riesgo": por_riesgo,
00049|    }

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiQ29uc3VsdGFzIHJldXRpbGl6YWJsZXMgcGFyYSBsaXN0YWRvcyBDUk0geSBLUElzLiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBkamFuZ28uZGIubW9kZWxzIGltcG9ydCBDb3VudCwgUQoKZnJvbSBhcHBzLmNvcmUubW9kZWxzIGltcG9ydCBFbnRpZGFkCgoKZGVmIGVudGlkYWRfbGlzdF9xdWVyeXNldChyZXF1ZXN0KToKICAgIHFzID0gRW50aWRhZC5vYmplY3RzLmFubm90YXRlKAogICAgICAgIG51bV9jb250YWN0b3M9Q291bnQoImNvbnRhY3RvcyIsIGRpc3RpbmN0PVRydWUpLAogICAgICAgIG51bV9wcm9kdWN0b3M9Q291bnQoInJlbGFjaW9uZXNfcHJvZHVjdG8iLCBkaXN0aW5jdD1UcnVlKSwKICAgICkub3JkZXJfYnkoIm5vbWJyZSIpCiAgICBxID0gcmVxdWVzdC5HRVQuZ2V0KCJxIiwgIiIpLnN0cmlwKCkKICAgIGlmIHE6CiAgICAgICAgcXMgPSBxcy5maWx0ZXIoUShub21icmVfX2ljb250YWlucz1xKSB8IFEobml0X19pY29udGFpbnM9cSkpCiAgICB0aXBvID0gcmVxdWVzdC5HRVQuZ2V0KCJ0aXBvIiwgIiIpLnN0cmlwKCkKICAgIGlmIHRpcG86CiAgICAgICAgcXMgPSBxcy5maWx0ZXIodGlwb19lbnRpZGFkPXRpcG8pCiAgICBhY3Rpdm8gPSByZXF1ZXN0LkdFVC5nZXQoImFjdGl2byIsICIiKS5zdHJpcCgpCiAgICBpZiBhY3Rpdm8gPT0gIjEiOgogICAgICAgIHFzID0gcXMuZmlsdGVyKGFjdGl2bz1UcnVlKQogICAgZWxpZiBhY3Rpdm8gPT0gIjAiOgogICAgICAgIHFzID0gcXMuZmlsdGVyKGFjdGl2bz1GYWxzZSkKICAgIHJldHVybiBxcwoKCmRlZiBlbnRpZGFkX3N1bW1hcnkocXVlcnlzZXQ9Tm9uZSk6CiAgICBiYXNlID0gcXVlcnlzZXQgaWYgcXVlcnlzZXQgaXMgbm90IE5vbmUgZWxzZSBFbnRpZGFkLm9iamVjdHMuYWxsKCkKICAgIHBvcl9jaXVkYWQgPSBsaXN0KAogICAgICAgIGJhc2UuZXhjbHVkZShjaXVkYWQ9IiIpCiAgICAgICAgLnZhbHVlcygiY2l1ZGFkIikKICAgICAgICAuYW5ub3RhdGUodG90YWw9Q291bnQoImlkIikpCiAgICAgICAgLm9yZGVyX2J5KCItdG90YWwiLCAiY2l1ZGFkIilbOjVdCiAgICApCiAgICBwb3Jfcmllc2dvID0gbGlzdCgKICAgICAgICBiYXNlLmV4Y2x1ZGUoY2F0ZWdvcmlhX3JpZXNnbz0iIikKICAgICAgICAudmFsdWVzKCJjYXRlZ29yaWFfcmllc2dvIikKICAgICAgICAuYW5ub3RhdGUodG90YWw9Q291bnQoImlkIikpCiAgICAgICAgLm9yZGVyX2J5KCItdG90YWwiLCAiY2F0ZWdvcmlhX3JpZXNnbyIpWzo1XQogICAgKQogICAgcmV0dXJuIHsKICAgICAgICAidG90YWwiOiBiYXNlLmNvdW50KCksCiAgICAgICAgImFjdGl2YXMiOiBiYXNlLmZpbHRlcihhY3Rpdm89VHJ1ZSkuY291bnQoKSwKICAgICAgICAiaW5hY3RpdmFzIjogYmFzZS5maWx0ZXIoYWN0aXZvPUZhbHNlKS5jb3VudCgpLAogICAgICAgICJwb3JfY2l1ZGFkIjogcG9yX2NpdWRhZCwKICAgICAgICAicG9yX3JpZXNnbyI6IHBvcl9yaWVzZ28sCiAgICB9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/crm/urls.py
PATH_JSON="apps/crm/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=14
SIZE_BYTES_UTF8=566
CONTENT_SHA256=1e4f8661fac8a9202c53d6d19b6e5723683b398496a2d111d645baed50c24461
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.urls import path

from . import views

app_name = "wcgone_crm"

urlpatterns = [
    path("entidades/", views.EntidadListView.as_view(), name="entidad_list"),
    path("entidades/exportar/", views.export_entidades_csv, name="export_entidades"),
    path("entidades/<int:pk>/", views.EntidadDetailView.as_view(), name="entidad_detail"),
    path("contactos/", views.ContactoListView.as_view(), name="contacto_list"),
    path("tareas/", views.TareaListView.as_view(), name="tarea_list"),
    path("importar/", views.importar_entidades, name="importar"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|
00003|from . import views
00004|
00005|app_name = "wcgone_crm"
00006|
00007|urlpatterns = [
00008|    path("entidades/", views.EntidadListView.as_view(), name="entidad_list"),
00009|    path("entidades/exportar/", views.export_entidades_csv, name="export_entidades"),
00010|    path("entidades/<int:pk>/", views.EntidadDetailView.as_view(), name="entidad_detail"),
00011|    path("contactos/", views.ContactoListView.as_view(), name="contacto_list"),
00012|    path("tareas/", views.TareaListView.as_view(), name="tarea_list"),
00013|    path("importar/", views.importar_entidades, name="importar"),
00014|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aAoKZnJvbSAuIGltcG9ydCB2aWV3cwoKYXBwX25hbWUgPSAid2Nnb25lX2NybSIKCnVybHBhdHRlcm5zID0gWwogICAgcGF0aCgiZW50aWRhZGVzLyIsIHZpZXdzLkVudGlkYWRMaXN0Vmlldy5hc192aWV3KCksIG5hbWU9ImVudGlkYWRfbGlzdCIpLAogICAgcGF0aCgiZW50aWRhZGVzL2V4cG9ydGFyLyIsIHZpZXdzLmV4cG9ydF9lbnRpZGFkZXNfY3N2LCBuYW1lPSJleHBvcnRfZW50aWRhZGVzIiksCiAgICBwYXRoKCJlbnRpZGFkZXMvPGludDpwaz4vIiwgdmlld3MuRW50aWRhZERldGFpbFZpZXcuYXNfdmlldygpLCBuYW1lPSJlbnRpZGFkX2RldGFpbCIpLAogICAgcGF0aCgiY29udGFjdG9zLyIsIHZpZXdzLkNvbnRhY3RvTGlzdFZpZXcuYXNfdmlldygpLCBuYW1lPSJjb250YWN0b19saXN0IiksCiAgICBwYXRoKCJ0YXJlYXMvIiwgdmlld3MuVGFyZWFMaXN0Vmlldy5hc192aWV3KCksIG5hbWU9InRhcmVhX2xpc3QiKSwKICAgIHBhdGgoImltcG9ydGFyLyIsIHZpZXdzLmltcG9ydGFyX2VudGlkYWRlcywgbmFtZT0iaW1wb3J0YXIiKSwKXQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/crm/views.py
PATH_JSON="apps/crm/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=157
SIZE_BYTES_UTF8=5161
CONTENT_SHA256=d7ed8b0f6a87ad7baa5fbaacef5e17f3940ba2f13fec95a5a323ae1690eb8e4a
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import DetailView, ListView

from apps.core.models import Contacto, Entidad

from .models import Tarea
from .selectors import entidad_list_queryset, entidad_summary


class EntidadListView(LoginRequiredMixin, ListView):
    model = Entidad
    template_name = "wcgone/crm/entidad_list.html"
    context_object_name = "entidades"
    paginate_by = 25

    def get_queryset(self):
        return entidad_list_queryset(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = entidad_list_queryset(self.request)
        context["summary"] = entidad_summary(qs)
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "CRM — Clientes"},
        ]
        context["tipo_choices"] = Entidad.TIPO_CHOICES
        context["export_query"] = self.request.GET.urlencode()
        return context


class EntidadDetailView(LoginRequiredMixin, DetailView):
    model = Entidad
    template_name = "wcgone/crm/entidad_detail.html"
    context_object_name = "entidad"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entidad = self.object
        context["contactos"] = entidad.contactos.filter(activo=True).order_by("nombre")
        context["relaciones_producto"] = entidad.relaciones_producto.select_related(
            "producto", "unidad_negocio"
        )
        context["interacciones"] = entidad.interacciones.select_related("usuario").order_by(
            "-fecha"
        )[:10]
        context["tareas"] = entidad.tareas.filter(completada=False).order_by("fecha_limite")[:10]
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "CRM — Clientes", "url": "/wcgone/crm/entidades/"},
            {"label": entidad.nombre},
        ]
        return context


class ContactoListView(LoginRequiredMixin, ListView):
    model = Contacto
    template_name = "wcgone/crm/contacto_list.html"
    context_object_name = "contactos"
    paginate_by = 25

    def get_queryset(self):
        qs = Contacto.objects.select_related("entidad").order_by("entidad__nombre", "nombre")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "CRM — Clientes", "url": "/wcgone/crm/entidades/"},
            {"label": "Contactos"},
        ]
        return context


class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = "wcgone/crm/tarea_list.html"
    context_object_name = "tareas"
    paginate_by = 25

    def get_queryset(self):
        qs = Tarea.objects.select_related("entidad", "asignado_a").order_by(
            "completada", "fecha_limite"
        )
        estado = self.request.GET.get("estado", "").strip()
        if estado:
            qs = qs.filter(estado=estado)
        if self.request.GET.get("pendientes") == "1":
            qs = qs.filter(completada=False)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "CRM — Clientes", "url": "/wcgone/crm/entidades/"},
            {"label": "Tareas"},
        ]
        return context


from django.contrib import messages  # noqa: E402
from django.contrib.auth.decorators import login_required  # noqa: E402
from django.shortcuts import redirect, render  # noqa: E402
from django.utils import timezone  # noqa: E402

from apps.core.exports import csv_response  # noqa: E402
from apps.core.forms import ImportFileForm  # noqa: E402

from .imports.entidades import import_entidades_clientes  # noqa: E402
from .selectors import entidad_list_queryset  # noqa: E402


@login_required
def export_entidades_csv(request):
    qs = entidad_list_queryset(request)
    rows = []
    for e in qs:
        rows.append([
            e.nombre,
            e.nit or "",
            e.get_tipo_entidad_display(),
            e.ciudad or "",
            e.categoria_riesgo or "",
            "Activo" if e.activo else "Inactivo",
            e.num_contactos,
            e.num_productos,
            e.email or "",
            e.telefono or "",
        ])
    filename = f"crm_entidades_{timezone.localdate().isoformat()}.csv"
    return csv_response(
        filename,
        [
            "Nombre",
            "NIT",
            "Tipo",
            "Ciudad",
            "Categoría riesgo",
            "Estado",
            "Contactos",
            "Productos",
            "Email",
            "Teléfono",
        ],
        rows,
    )


@login_required
def importar_entidades(request):
    return redirect("imports:import_hub")

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib.auth.mixins import LoginRequiredMixin
00002|from django.db.models import Q
00003|from django.views.generic import DetailView, ListView
00004|
00005|from apps.core.models import Contacto, Entidad
00006|
00007|from .models import Tarea
00008|from .selectors import entidad_list_queryset, entidad_summary
00009|
00010|
00011|class EntidadListView(LoginRequiredMixin, ListView):
00012|    model = Entidad
00013|    template_name = "wcgone/crm/entidad_list.html"
00014|    context_object_name = "entidades"
00015|    paginate_by = 25
00016|
00017|    def get_queryset(self):
00018|        return entidad_list_queryset(self.request)
00019|
00020|    def get_context_data(self, **kwargs):
00021|        context = super().get_context_data(**kwargs)
00022|        qs = entidad_list_queryset(self.request)
00023|        context["summary"] = entidad_summary(qs)
00024|        context["breadcrumbs"] = [
00025|            {"label": "Panel principal", "url": "/panel/"},
00026|            {"label": "CRM — Clientes"},
00027|        ]
00028|        context["tipo_choices"] = Entidad.TIPO_CHOICES
00029|        context["export_query"] = self.request.GET.urlencode()
00030|        return context
00031|
00032|
00033|class EntidadDetailView(LoginRequiredMixin, DetailView):
00034|    model = Entidad
00035|    template_name = "wcgone/crm/entidad_detail.html"
00036|    context_object_name = "entidad"
00037|
00038|    def get_context_data(self, **kwargs):
00039|        context = super().get_context_data(**kwargs)
00040|        entidad = self.object
00041|        context["contactos"] = entidad.contactos.filter(activo=True).order_by("nombre")
00042|        context["relaciones_producto"] = entidad.relaciones_producto.select_related(
00043|            "producto", "unidad_negocio"
00044|        )
00045|        context["interacciones"] = entidad.interacciones.select_related("usuario").order_by(
00046|            "-fecha"
00047|        )[:10]
00048|        context["tareas"] = entidad.tareas.filter(completada=False).order_by("fecha_limite")[:10]
00049|        context["breadcrumbs"] = [
00050|            {"label": "Panel principal", "url": "/panel/"},
00051|            {"label": "CRM — Clientes", "url": "/wcgone/crm/entidades/"},
00052|            {"label": entidad.nombre},
00053|        ]
00054|        return context
00055|
00056|
00057|class ContactoListView(LoginRequiredMixin, ListView):
00058|    model = Contacto
00059|    template_name = "wcgone/crm/contacto_list.html"
00060|    context_object_name = "contactos"
00061|    paginate_by = 25
00062|
00063|    def get_queryset(self):
00064|        qs = Contacto.objects.select_related("entidad").order_by("entidad__nombre", "nombre")
00065|        q = self.request.GET.get("q", "").strip()
00066|        if q:
00067|            qs = qs.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
00068|        return qs
00069|
00070|    def get_context_data(self, **kwargs):
00071|        context = super().get_context_data(**kwargs)
00072|        context["breadcrumbs"] = [
00073|            {"label": "Panel principal", "url": "/panel/"},
00074|            {"label": "CRM — Clientes", "url": "/wcgone/crm/entidades/"},
00075|            {"label": "Contactos"},
00076|        ]
00077|        return context
00078|
00079|
00080|class TareaListView(LoginRequiredMixin, ListView):
00081|    model = Tarea
00082|    template_name = "wcgone/crm/tarea_list.html"
00083|    context_object_name = "tareas"
00084|    paginate_by = 25
00085|
00086|    def get_queryset(self):
00087|        qs = Tarea.objects.select_related("entidad", "asignado_a").order_by(
00088|            "completada", "fecha_limite"
00089|        )
00090|        estado = self.request.GET.get("estado", "").strip()
00091|        if estado:
00092|            qs = qs.filter(estado=estado)
00093|        if self.request.GET.get("pendientes") == "1":
00094|            qs = qs.filter(completada=False)
00095|        return qs
00096|
00097|    def get_context_data(self, **kwargs):
00098|        context = super().get_context_data(**kwargs)
00099|        context["breadcrumbs"] = [
00100|            {"label": "Panel principal", "url": "/panel/"},
00101|            {"label": "CRM — Clientes", "url": "/wcgone/crm/entidades/"},
00102|            {"label": "Tareas"},
00103|        ]
00104|        return context
00105|
00106|
00107|from django.contrib import messages  # noqa: E402
00108|from django.contrib.auth.decorators import login_required  # noqa: E402
00109|from django.shortcuts import redirect, render  # noqa: E402
00110|from django.utils import timezone  # noqa: E402
00111|
00112|from apps.core.exports import csv_response  # noqa: E402
00113|from apps.core.forms import ImportFileForm  # noqa: E402
00114|
00115|from .imports.entidades import import_entidades_clientes  # noqa: E402
00116|from .selectors import entidad_list_queryset  # noqa: E402
00117|
00118|
00119|@login_required
00120|def export_entidades_csv(request):
00121|    qs = entidad_list_queryset(request)
00122|    rows = []
00123|    for e in qs:
00124|        rows.append([
00125|            e.nombre,
00126|            e.nit or "",
00127|            e.get_tipo_entidad_display(),
00128|            e.ciudad or "",
00129|            e.categoria_riesgo or "",
00130|            "Activo" if e.activo else "Inactivo",
00131|            e.num_contactos,
00132|            e.num_productos,
00133|            e.email or "",
00134|            e.telefono or "",
00135|        ])
00136|    filename = f"crm_entidades_{timezone.localdate().isoformat()}.csv"
00137|    return csv_response(
00138|        filename,
00139|        [
00140|            "Nombre",
00141|            "NIT",
00142|            "Tipo",
00143|            "Ciudad",
00144|            "Categoría riesgo",
00145|            "Estado",
00146|            "Contactos",
00147|            "Productos",
00148|            "Email",
00149|            "Teléfono",
00150|        ],
00151|        rows,
00152|    )
00153|
00154|
00155|@login_required
00156|def importar_entidades(request):
00157|    return redirect("imports:import_hub")

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYi5hdXRoLm1peGlucyBpbXBvcnQgTG9naW5SZXF1aXJlZE1peGluCmZyb20gZGphbmdvLmRiLm1vZGVscyBpbXBvcnQgUQpmcm9tIGRqYW5nby52aWV3cy5nZW5lcmljIGltcG9ydCBEZXRhaWxWaWV3LCBMaXN0VmlldwoKZnJvbSBhcHBzLmNvcmUubW9kZWxzIGltcG9ydCBDb250YWN0bywgRW50aWRhZAoKZnJvbSAubW9kZWxzIGltcG9ydCBUYXJlYQpmcm9tIC5zZWxlY3RvcnMgaW1wb3J0IGVudGlkYWRfbGlzdF9xdWVyeXNldCwgZW50aWRhZF9zdW1tYXJ5CgoKY2xhc3MgRW50aWRhZExpc3RWaWV3KExvZ2luUmVxdWlyZWRNaXhpbiwgTGlzdFZpZXcpOgogICAgbW9kZWwgPSBFbnRpZGFkCiAgICB0ZW1wbGF0ZV9uYW1lID0gIndjZ29uZS9jcm0vZW50aWRhZF9saXN0Lmh0bWwiCiAgICBjb250ZXh0X29iamVjdF9uYW1lID0gImVudGlkYWRlcyIKICAgIHBhZ2luYXRlX2J5ID0gMjUKCiAgICBkZWYgZ2V0X3F1ZXJ5c2V0KHNlbGYpOgogICAgICAgIHJldHVybiBlbnRpZGFkX2xpc3RfcXVlcnlzZXQoc2VsZi5yZXF1ZXN0KQoKICAgIGRlZiBnZXRfY29udGV4dF9kYXRhKHNlbGYsICoqa3dhcmdzKToKICAgICAgICBjb250ZXh0ID0gc3VwZXIoKS5nZXRfY29udGV4dF9kYXRhKCoqa3dhcmdzKQogICAgICAgIHFzID0gZW50aWRhZF9saXN0X3F1ZXJ5c2V0KHNlbGYucmVxdWVzdCkKICAgICAgICBjb250ZXh0WyJzdW1tYXJ5Il0gPSBlbnRpZGFkX3N1bW1hcnkocXMpCiAgICAgICAgY29udGV4dFsiYnJlYWRjcnVtYnMiXSA9IFsKICAgICAgICAgICAgeyJsYWJlbCI6ICJQYW5lbCBwcmluY2lwYWwiLCAidXJsIjogIi9wYW5lbC8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJDUk0g4oCUIENsaWVudGVzIn0sCiAgICAgICAgXQogICAgICAgIGNvbnRleHRbInRpcG9fY2hvaWNlcyJdID0gRW50aWRhZC5USVBPX0NIT0lDRVMKICAgICAgICBjb250ZXh0WyJleHBvcnRfcXVlcnkiXSA9IHNlbGYucmVxdWVzdC5HRVQudXJsZW5jb2RlKCkKICAgICAgICByZXR1cm4gY29udGV4dAoKCmNsYXNzIEVudGlkYWREZXRhaWxWaWV3KExvZ2luUmVxdWlyZWRNaXhpbiwgRGV0YWlsVmlldyk6CiAgICBtb2RlbCA9IEVudGlkYWQKICAgIHRlbXBsYXRlX25hbWUgPSAid2Nnb25lL2NybS9lbnRpZGFkX2RldGFpbC5odG1sIgogICAgY29udGV4dF9vYmplY3RfbmFtZSA9ICJlbnRpZGFkIgoKICAgIGRlZiBnZXRfY29udGV4dF9kYXRhKHNlbGYsICoqa3dhcmdzKToKICAgICAgICBjb250ZXh0ID0gc3VwZXIoKS5nZXRfY29udGV4dF9kYXRhKCoqa3dhcmdzKQogICAgICAgIGVudGlkYWQgPSBzZWxmLm9iamVjdAogICAgICAgIGNvbnRleHRbImNvbnRhY3RvcyJdID0gZW50aWRhZC5jb250YWN0b3MuZmlsdGVyKGFjdGl2bz1UcnVlKS5vcmRlcl9ieSgibm9tYnJlIikKICAgICAgICBjb250ZXh0WyJyZWxhY2lvbmVzX3Byb2R1Y3RvIl0gPSBlbnRpZGFkLnJlbGFjaW9uZXNfcHJvZHVjdG8uc2VsZWN0X3JlbGF0ZWQoCiAgICAgICAgICAgICJwcm9kdWN0byIsICJ1bmlkYWRfbmVnb2NpbyIKICAgICAgICApCiAgICAgICAgY29udGV4dFsiaW50ZXJhY2Npb25lcyJdID0gZW50aWRhZC5pbnRlcmFjY2lvbmVzLnNlbGVjdF9yZWxhdGVkKCJ1c3VhcmlvIikub3JkZXJfYnkoCiAgICAgICAgICAgICItZmVjaGEiCiAgICAgICAgKVs6MTBdCiAgICAgICAgY29udGV4dFsidGFyZWFzIl0gPSBlbnRpZGFkLnRhcmVhcy5maWx0ZXIoY29tcGxldGFkYT1GYWxzZSkub3JkZXJfYnkoImZlY2hhX2xpbWl0ZSIpWzoxMF0KICAgICAgICBjb250ZXh0WyJicmVhZGNydW1icyJdID0gWwogICAgICAgICAgICB7ImxhYmVsIjogIlBhbmVsIHByaW5jaXBhbCIsICJ1cmwiOiAiL3BhbmVsLyJ9LAogICAgICAgICAgICB7ImxhYmVsIjogIkNSTSDigJQgQ2xpZW50ZXMiLCAidXJsIjogIi93Y2dvbmUvY3JtL2VudGlkYWRlcy8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6IGVudGlkYWQubm9tYnJlfSwKICAgICAgICBdCiAgICAgICAgcmV0dXJuIGNvbnRleHQKCgpjbGFzcyBDb250YWN0b0xpc3RWaWV3KExvZ2luUmVxdWlyZWRNaXhpbiwgTGlzdFZpZXcpOgogICAgbW9kZWwgPSBDb250YWN0bwogICAgdGVtcGxhdGVfbmFtZSA9ICJ3Y2dvbmUvY3JtL2NvbnRhY3RvX2xpc3QuaHRtbCIKICAgIGNvbnRleHRfb2JqZWN0X25hbWUgPSAiY29udGFjdG9zIgogICAgcGFnaW5hdGVfYnkgPSAyNQoKICAgIGRlZiBnZXRfcXVlcnlzZXQoc2VsZik6CiAgICAgICAgcXMgPSBDb250YWN0by5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJlbnRpZGFkIikub3JkZXJfYnkoImVudGlkYWRfX25vbWJyZSIsICJub21icmUiKQogICAgICAgIHEgPSBzZWxmLnJlcXVlc3QuR0VULmdldCgicSIsICIiKS5zdHJpcCgpCiAgICAgICAgaWYgcToKICAgICAgICAgICAgcXMgPSBxcy5maWx0ZXIoUShub21icmVfX2ljb250YWlucz1xKSB8IFEoZW1haWxfX2ljb250YWlucz1xKSkKICAgICAgICByZXR1cm4gcXMKCiAgICBkZWYgZ2V0X2NvbnRleHRfZGF0YShzZWxmLCAqKmt3YXJncyk6CiAgICAgICAgY29udGV4dCA9IHN1cGVyKCkuZ2V0X2NvbnRleHRfZGF0YSgqKmt3YXJncykKICAgICAgICBjb250ZXh0WyJicmVhZGNydW1icyJdID0gWwogICAgICAgICAgICB7ImxhYmVsIjogIlBhbmVsIHByaW5jaXBhbCIsICJ1cmwiOiAiL3BhbmVsLyJ9LAogICAgICAgICAgICB7ImxhYmVsIjogIkNSTSDigJQgQ2xpZW50ZXMiLCAidXJsIjogIi93Y2dvbmUvY3JtL2VudGlkYWRlcy8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJDb250YWN0b3MifSwKICAgICAgICBdCiAgICAgICAgcmV0dXJuIGNvbnRleHQKCgpjbGFzcyBUYXJlYUxpc3RWaWV3KExvZ2luUmVxdWlyZWRNaXhpbiwgTGlzdFZpZXcpOgogICAgbW9kZWwgPSBUYXJlYQogICAgdGVtcGxhdGVfbmFtZSA9ICJ3Y2dvbmUvY3JtL3RhcmVhX2xpc3QuaHRtbCIKICAgIGNvbnRleHRfb2JqZWN0X25hbWUgPSAidGFyZWFzIgogICAgcGFnaW5hdGVfYnkgPSAyNQoKICAgIGRlZiBnZXRfcXVlcnlzZXQoc2VsZik6CiAgICAgICAgcXMgPSBUYXJlYS5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJlbnRpZGFkIiwgImFzaWduYWRvX2EiKS5vcmRlcl9ieSgKICAgICAgICAgICAgImNvbXBsZXRhZGEiLCAiZmVjaGFfbGltaXRlIgogICAgICAgICkKICAgICAgICBlc3RhZG8gPSBzZWxmLnJlcXVlc3QuR0VULmdldCgiZXN0YWRvIiwgIiIpLnN0cmlwKCkKICAgICAgICBpZiBlc3RhZG86CiAgICAgICAgICAgIHFzID0gcXMuZmlsdGVyKGVzdGFkbz1lc3RhZG8pCiAgICAgICAgaWYgc2VsZi5yZXF1ZXN0LkdFVC5nZXQoInBlbmRpZW50ZXMiKSA9PSAiMSI6CiAgICAgICAgICAgIHFzID0gcXMuZmlsdGVyKGNvbXBsZXRhZGE9RmFsc2UpCiAgICAgICAgcmV0dXJuIHFzCgogICAgZGVmIGdldF9jb250ZXh0X2RhdGEoc2VsZiwgKiprd2FyZ3MpOgogICAgICAgIGNvbnRleHQgPSBzdXBlcigpLmdldF9jb250ZXh0X2RhdGEoKiprd2FyZ3MpCiAgICAgICAgY29udGV4dFsiYnJlYWRjcnVtYnMiXSA9IFsKICAgICAgICAgICAgeyJsYWJlbCI6ICJQYW5lbCBwcmluY2lwYWwiLCAidXJsIjogIi9wYW5lbC8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJDUk0g4oCUIENsaWVudGVzIiwgInVybCI6ICIvd2Nnb25lL2NybS9lbnRpZGFkZXMvIn0sCiAgICAgICAgICAgIHsibGFiZWwiOiAiVGFyZWFzIn0sCiAgICAgICAgXQogICAgICAgIHJldHVybiBjb250ZXh0CgoKZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgbWVzc2FnZXMgICMgbm9xYTogRTQwMgpmcm9tIGRqYW5nby5jb250cmliLmF1dGguZGVjb3JhdG9ycyBpbXBvcnQgbG9naW5fcmVxdWlyZWQgICMgbm9xYTogRTQwMgpmcm9tIGRqYW5nby5zaG9ydGN1dHMgaW1wb3J0IHJlZGlyZWN0LCByZW5kZXIgICMgbm9xYTogRTQwMgpmcm9tIGRqYW5nby51dGlscyBpbXBvcnQgdGltZXpvbmUgICMgbm9xYTogRTQwMgoKZnJvbSBhcHBzLmNvcmUuZXhwb3J0cyBpbXBvcnQgY3N2X3Jlc3BvbnNlICAjIG5vcWE6IEU0MDIKZnJvbSBhcHBzLmNvcmUuZm9ybXMgaW1wb3J0IEltcG9ydEZpbGVGb3JtICAjIG5vcWE6IEU0MDIKCmZyb20gLmltcG9ydHMuZW50aWRhZGVzIGltcG9ydCBpbXBvcnRfZW50aWRhZGVzX2NsaWVudGVzICAjIG5vcWE6IEU0MDIKZnJvbSAuc2VsZWN0b3JzIGltcG9ydCBlbnRpZGFkX2xpc3RfcXVlcnlzZXQgICMgbm9xYTogRTQwMgoKCkBsb2dpbl9yZXF1aXJlZApkZWYgZXhwb3J0X2VudGlkYWRlc19jc3YocmVxdWVzdCk6CiAgICBxcyA9IGVudGlkYWRfbGlzdF9xdWVyeXNldChyZXF1ZXN0KQogICAgcm93cyA9IFtdCiAgICBmb3IgZSBpbiBxczoKICAgICAgICByb3dzLmFwcGVuZChbCiAgICAgICAgICAgIGUubm9tYnJlLAogICAgICAgICAgICBlLm5pdCBvciAiIiwKICAgICAgICAgICAgZS5nZXRfdGlwb19lbnRpZGFkX2Rpc3BsYXkoKSwKICAgICAgICAgICAgZS5jaXVkYWQgb3IgIiIsCiAgICAgICAgICAgIGUuY2F0ZWdvcmlhX3JpZXNnbyBvciAiIiwKICAgICAgICAgICAgIkFjdGl2byIgaWYgZS5hY3Rpdm8gZWxzZSAiSW5hY3Rpdm8iLAogICAgICAgICAgICBlLm51bV9jb250YWN0b3MsCiAgICAgICAgICAgIGUubnVtX3Byb2R1Y3RvcywKICAgICAgICAgICAgZS5lbWFpbCBvciAiIiwKICAgICAgICAgICAgZS50ZWxlZm9ubyBvciAiIiwKICAgICAgICBdKQogICAgZmlsZW5hbWUgPSBmImNybV9lbnRpZGFkZXNfe3RpbWV6b25lLmxvY2FsZGF0ZSgpLmlzb2Zvcm1hdCgpfS5jc3YiCiAgICByZXR1cm4gY3N2X3Jlc3BvbnNlKAogICAgICAgIGZpbGVuYW1lLAogICAgICAgIFsKICAgICAgICAgICAgIk5vbWJyZSIsCiAgICAgICAgICAgICJOSVQiLAogICAgICAgICAgICAiVGlwbyIsCiAgICAgICAgICAgICJDaXVkYWQiLAogICAgICAgICAgICAiQ2F0ZWdvcsOtYSByaWVzZ28iLAogICAgICAgICAgICAiRXN0YWRvIiwKICAgICAgICAgICAgIkNvbnRhY3RvcyIsCiAgICAgICAgICAgICJQcm9kdWN0b3MiLAogICAgICAgICAgICAiRW1haWwiLAogICAgICAgICAgICAiVGVsw6lmb25vIiwKICAgICAgICBdLAogICAgICAgIHJvd3MsCiAgICApCgoKQGxvZ2luX3JlcXVpcmVkCmRlZiBpbXBvcnRhcl9lbnRpZGFkZXMocmVxdWVzdCk6CiAgICByZXR1cm4gcmVkaXJlY3QoImltcG9ydHM6aW1wb3J0X2h1YiIpCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/legacy_pgc1/__init__.py
PATH_JSON="apps/legacy_pgc1/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/legacy_pgc1/apps.py
PATH_JSON="apps/legacy_pgc1/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=8
SIZE_BYTES_UTF8=223
CONTENT_SHA256=26c5635eab211db408dbeb25f566310848fbb53f9a52e098d361c4ce85ad2583
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.apps import AppConfig


class LegacyPgc1Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.legacy_pgc1"
    label = "wcgone_legacy_pgc1"
    verbose_name = "PGC Legado"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class LegacyPgc1Config(AppConfig):
00005|    default_auto_field = "django.db.models.BigAutoField"
00006|    name = "apps.legacy_pgc1"
00007|    label = "wcgone_legacy_pgc1"
00008|    verbose_name = "PGC Legado"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgTGVnYWN5UGdjMUNvbmZpZyhBcHBDb25maWcpOgogICAgZGVmYXVsdF9hdXRvX2ZpZWxkID0gImRqYW5nby5kYi5tb2RlbHMuQmlnQXV0b0ZpZWxkIgogICAgbmFtZSA9ICJhcHBzLmxlZ2FjeV9wZ2MxIgogICAgbGFiZWwgPSAid2Nnb25lX2xlZ2FjeV9wZ2MxIgogICAgdmVyYm9zZV9uYW1lID0gIlBHQyBMZWdhZG8iCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/legacy_pgc1/urls.py
PATH_JSON="apps/legacy_pgc1/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=9
SIZE_BYTES_UTF8=136
CONTENT_SHA256=78c6571e2fe5087b33a4c09eb2048cab20b8d52bdd315bc05098b2e5836fdc0a
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.urls import path

from . import views

app_name = "wcgone_legacy"

urlpatterns = [
    path("", views.home, name="home"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|
00003|from . import views
00004|
00005|app_name = "wcgone_legacy"
00006|
00007|urlpatterns = [
00008|    path("", views.home, name="home"),
00009|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aAoKZnJvbSAuIGltcG9ydCB2aWV3cwoKYXBwX25hbWUgPSAid2Nnb25lX2xlZ2FjeSIKCnVybHBhdHRlcm5zID0gWwogICAgcGF0aCgiIiwgdmlld3MuaG9tZSwgbmFtZT0iaG9tZSIpLApdCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/legacy_pgc1/views.py
PATH_JSON="apps/legacy_pgc1/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=6
SIZE_BYTES_UTF8=175
CONTENT_SHA256=131518991a7383c0ba1c7a1b116eae040d5c9ffa4264b1b580d872e0e2e03f90
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.shortcuts import redirect


def home(request):
    """Sustituye el placeholder: apunta al PGC real del árbol unificado."""
    return redirect("pgc:module_home")

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.shortcuts import redirect
00002|
00003|
00004|def home(request):
00005|    """Sustituye el placeholder: apunta al PGC real del árbol unificado."""
00006|    return redirect("pgc:module_home")

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uc2hvcnRjdXRzIGltcG9ydCByZWRpcmVjdAoKCmRlZiBob21lKHJlcXVlc3QpOgogICAgIiIiU3VzdGl0dXllIGVsIHBsYWNlaG9sZGVyOiBhcHVudGEgYWwgUEdDIHJlYWwgZGVsIMOhcmJvbCB1bmlmaWNhZG8uIiIiCiAgICByZXR1cm4gcmVkaXJlY3QoInBnYzptb2R1bGVfaG9tZSIpCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/pgc/__init__.py
PATH_JSON="apps/pgc/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/pgc/apps.py
PATH_JSON="apps/pgc/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=8
SIZE_BYTES_UTF8=193
CONTENT_SHA256=2e8347172a3ad9b37d396bc0a74545a21c16f7499adf18da18deace4174cb8b4
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.apps import AppConfig


class PgcConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.pgc"
    label = "wcgone_pgc"
    verbose_name = "PGC"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class PgcConfig(AppConfig):
00005|    default_auto_field = "django.db.models.BigAutoField"
00006|    name = "apps.pgc"
00007|    label = "wcgone_pgc"
00008|    verbose_name = "PGC"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgUGdjQ29uZmlnKEFwcENvbmZpZyk6CiAgICBkZWZhdWx0X2F1dG9fZmllbGQgPSAiZGphbmdvLmRiLm1vZGVscy5CaWdBdXRvRmllbGQiCiAgICBuYW1lID0gImFwcHMucGdjIgogICAgbGFiZWwgPSAid2Nnb25lX3BnYyIKICAgIHZlcmJvc2VfbmFtZSA9ICJQR0MiCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/pgc/urls.py
PATH_JSON="apps/pgc/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=9
SIZE_BYTES_UTF8=133
CONTENT_SHA256=9752d9444412712f3bb3a91b3a4a4b9dea192958dab9a6cd6aab4ff90d615ed0
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.urls import path

from . import views

app_name = "wcgone_pgc"

urlpatterns = [
    path("", views.home, name="home"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|
00003|from . import views
00004|
00005|app_name = "wcgone_pgc"
00006|
00007|urlpatterns = [
00008|    path("", views.home, name="home"),
00009|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aAoKZnJvbSAuIGltcG9ydCB2aWV3cwoKYXBwX25hbWUgPSAid2Nnb25lX3BnYyIKCnVybHBhdHRlcm5zID0gWwogICAgcGF0aCgiIiwgdmlld3MuaG9tZSwgbmFtZT0iaG9tZSIpLApdCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/pgc/views.py
PATH_JSON="apps/pgc/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=6
SIZE_BYTES_UTF8=164
CONTENT_SHA256=ecfd8fd9dee519ae9160468f74f7658f0a8b06941d31f4e6cf286ec65bf237a8
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.shortcuts import redirect


def home(request):
    """Sustituye el stub PGC de wcg_one por el PGC productivo."""
    return redirect("pgc:module_home")

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.shortcuts import redirect
00002|
00003|
00004|def home(request):
00005|    """Sustituye el stub PGC de wcg_one por el PGC productivo."""
00006|    return redirect("pgc:module_home")

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uc2hvcnRjdXRzIGltcG9ydCByZWRpcmVjdAoKCmRlZiBob21lKHJlcXVlc3QpOgogICAgIiIiU3VzdGl0dXllIGVsIHN0dWIgUEdDIGRlIHdjZ19vbmUgcG9yIGVsIFBHQyBwcm9kdWN0aXZvLiIiIgogICAgcmV0dXJuIHJlZGlyZWN0KCJwZ2M6bW9kdWxlX2hvbWUiKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/pgo/__init__.py
PATH_JSON="apps/pgo/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/pgo/admin.py
PATH_JSON="apps/pgo/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=88
SIZE_BYTES_UTF8=2273
CONTENT_SHA256=f076c7ad53671e5f9b14dd2347ba8aa2294b64dbf1d1b08a86ab18ca32889324
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.contrib import admin

from .models import PgoMetricRule, PgoMonthlyAgg, PgoPeriodScore, PgoTicket


@admin.register(PgoTicket)
class PgoTicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_externo_id",
        "titulo",
        "estado_normalizado",
        "prioridad",
        "departamento",
        "sistema",
        "anio_mes",
        "sla_cumplido",
        "fecha_apertura",
    )
    list_filter = (
        "estado_normalizado",
        "prioridad",
        "departamento",
        "sistema",
        "anio_mes",
        "sla_cumplido",
    )
    search_fields = (
        "ticket_externo_id",
        "titulo",
        "usuario_solicita",
        "correo_solicita",
        "departamento",
    )
    autocomplete_fields = ("unidad_negocio", "responsable", "import_batch")
    ordering = ("-fecha_apertura",)


@admin.register(PgoMetricRule)
class PgoMetricRuleAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "area",
        "variable",
        "puntos",
        "peso",
        "tipo_regla",
        "activo",
    )
    list_filter = ("area", "tipo_regla", "activo", "unidad_negocio")
    search_fields = ("codigo", "variable", "criterio")
    autocomplete_fields = ("unidad_negocio",)
    ordering = ("area", "codigo")


@admin.register(PgoPeriodScore)
class PgoPeriodScoreAdmin(admin.ModelAdmin):
    list_display = (
        "periodo",
        "area",
        "unidad_negocio",
        "usuario",
        "puntaje_total",
        "clasifica",
        "fecha_calculo",
    )
    list_filter = ("periodo", "clasifica", "area", "unidad_negocio")
    search_fields = ("periodo", "area")
    date_hierarchy = "fecha_calculo"
    autocomplete_fields = ("unidad_negocio", "usuario")
    ordering = ("-periodo",)


@admin.register(PgoMonthlyAgg)
class PgoMonthlyAggAdmin(admin.ModelAdmin):
    list_display = (
        "periodo",
        "unidad_negocio",
        "departamento",
        "tickets_recibidos",
        "tickets_cerrados",
        "tiempo_promedio_horas",
        "sla_cumplidos",
        "sla_incumplidos",
    )
    list_filter = ("periodo", "unidad_negocio", "departamento")
    search_fields = ("periodo", "departamento")
    autocomplete_fields = ("unidad_negocio",)
    ordering = ("-periodo",)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import admin
00002|
00003|from .models import PgoMetricRule, PgoMonthlyAgg, PgoPeriodScore, PgoTicket
00004|
00005|
00006|@admin.register(PgoTicket)
00007|class PgoTicketAdmin(admin.ModelAdmin):
00008|    list_display = (
00009|        "ticket_externo_id",
00010|        "titulo",
00011|        "estado_normalizado",
00012|        "prioridad",
00013|        "departamento",
00014|        "sistema",
00015|        "anio_mes",
00016|        "sla_cumplido",
00017|        "fecha_apertura",
00018|    )
00019|    list_filter = (
00020|        "estado_normalizado",
00021|        "prioridad",
00022|        "departamento",
00023|        "sistema",
00024|        "anio_mes",
00025|        "sla_cumplido",
00026|    )
00027|    search_fields = (
00028|        "ticket_externo_id",
00029|        "titulo",
00030|        "usuario_solicita",
00031|        "correo_solicita",
00032|        "departamento",
00033|    )
00034|    autocomplete_fields = ("unidad_negocio", "responsable", "import_batch")
00035|    ordering = ("-fecha_apertura",)
00036|
00037|
00038|@admin.register(PgoMetricRule)
00039|class PgoMetricRuleAdmin(admin.ModelAdmin):
00040|    list_display = (
00041|        "codigo",
00042|        "area",
00043|        "variable",
00044|        "puntos",
00045|        "peso",
00046|        "tipo_regla",
00047|        "activo",
00048|    )
00049|    list_filter = ("area", "tipo_regla", "activo", "unidad_negocio")
00050|    search_fields = ("codigo", "variable", "criterio")
00051|    autocomplete_fields = ("unidad_negocio",)
00052|    ordering = ("area", "codigo")
00053|
00054|
00055|@admin.register(PgoPeriodScore)
00056|class PgoPeriodScoreAdmin(admin.ModelAdmin):
00057|    list_display = (
00058|        "periodo",
00059|        "area",
00060|        "unidad_negocio",
00061|        "usuario",
00062|        "puntaje_total",
00063|        "clasifica",
00064|        "fecha_calculo",
00065|    )
00066|    list_filter = ("periodo", "clasifica", "area", "unidad_negocio")
00067|    search_fields = ("periodo", "area")
00068|    date_hierarchy = "fecha_calculo"
00069|    autocomplete_fields = ("unidad_negocio", "usuario")
00070|    ordering = ("-periodo",)
00071|
00072|
00073|@admin.register(PgoMonthlyAgg)
00074|class PgoMonthlyAggAdmin(admin.ModelAdmin):
00075|    list_display = (
00076|        "periodo",
00077|        "unidad_negocio",
00078|        "departamento",
00079|        "tickets_recibidos",
00080|        "tickets_cerrados",
00081|        "tiempo_promedio_horas",
00082|        "sla_cumplidos",
00083|        "sla_incumplidos",
00084|    )
00085|    list_filter = ("periodo", "unidad_negocio", "departamento")
00086|    search_fields = ("periodo", "departamento")
00087|    autocomplete_fields = ("unidad_negocio",)
00088|    ordering = ("-periodo",)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgYWRtaW4KCmZyb20gLm1vZGVscyBpbXBvcnQgUGdvTWV0cmljUnVsZSwgUGdvTW9udGhseUFnZywgUGdvUGVyaW9kU2NvcmUsIFBnb1RpY2tldAoKCkBhZG1pbi5yZWdpc3RlcihQZ29UaWNrZXQpCmNsYXNzIFBnb1RpY2tldEFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKAogICAgICAgICJ0aWNrZXRfZXh0ZXJub19pZCIsCiAgICAgICAgInRpdHVsbyIsCiAgICAgICAgImVzdGFkb19ub3JtYWxpemFkbyIsCiAgICAgICAgInByaW9yaWRhZCIsCiAgICAgICAgImRlcGFydGFtZW50byIsCiAgICAgICAgInNpc3RlbWEiLAogICAgICAgICJhbmlvX21lcyIsCiAgICAgICAgInNsYV9jdW1wbGlkbyIsCiAgICAgICAgImZlY2hhX2FwZXJ0dXJhIiwKICAgICkKICAgIGxpc3RfZmlsdGVyID0gKAogICAgICAgICJlc3RhZG9fbm9ybWFsaXphZG8iLAogICAgICAgICJwcmlvcmlkYWQiLAogICAgICAgICJkZXBhcnRhbWVudG8iLAogICAgICAgICJzaXN0ZW1hIiwKICAgICAgICAiYW5pb19tZXMiLAogICAgICAgICJzbGFfY3VtcGxpZG8iLAogICAgKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgKICAgICAgICAidGlja2V0X2V4dGVybm9faWQiLAogICAgICAgICJ0aXR1bG8iLAogICAgICAgICJ1c3VhcmlvX3NvbGljaXRhIiwKICAgICAgICAiY29ycmVvX3NvbGljaXRhIiwKICAgICAgICAiZGVwYXJ0YW1lbnRvIiwKICAgICkKICAgIGF1dG9jb21wbGV0ZV9maWVsZHMgPSAoInVuaWRhZF9uZWdvY2lvIiwgInJlc3BvbnNhYmxlIiwgImltcG9ydF9iYXRjaCIpCiAgICBvcmRlcmluZyA9ICgiLWZlY2hhX2FwZXJ0dXJhIiwpCgoKQGFkbWluLnJlZ2lzdGVyKFBnb01ldHJpY1J1bGUpCmNsYXNzIFBnb01ldHJpY1J1bGVBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAiY29kaWdvIiwKICAgICAgICAiYXJlYSIsCiAgICAgICAgInZhcmlhYmxlIiwKICAgICAgICAicHVudG9zIiwKICAgICAgICAicGVzbyIsCiAgICAgICAgInRpcG9fcmVnbGEiLAogICAgICAgICJhY3Rpdm8iLAogICAgKQogICAgbGlzdF9maWx0ZXIgPSAoImFyZWEiLCAidGlwb19yZWdsYSIsICJhY3Rpdm8iLCAidW5pZGFkX25lZ29jaW8iKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiY29kaWdvIiwgInZhcmlhYmxlIiwgImNyaXRlcmlvIikKICAgIGF1dG9jb21wbGV0ZV9maWVsZHMgPSAoInVuaWRhZF9uZWdvY2lvIiwpCiAgICBvcmRlcmluZyA9ICgiYXJlYSIsICJjb2RpZ28iKQoKCkBhZG1pbi5yZWdpc3RlcihQZ29QZXJpb2RTY29yZSkKY2xhc3MgUGdvUGVyaW9kU2NvcmVBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAicGVyaW9kbyIsCiAgICAgICAgImFyZWEiLAogICAgICAgICJ1bmlkYWRfbmVnb2NpbyIsCiAgICAgICAgInVzdWFyaW8iLAogICAgICAgICJwdW50YWplX3RvdGFsIiwKICAgICAgICAiY2xhc2lmaWNhIiwKICAgICAgICAiZmVjaGFfY2FsY3VsbyIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgicGVyaW9kbyIsICJjbGFzaWZpY2EiLCAiYXJlYSIsICJ1bmlkYWRfbmVnb2NpbyIpCiAgICBzZWFyY2hfZmllbGRzID0gKCJwZXJpb2RvIiwgImFyZWEiKQogICAgZGF0ZV9oaWVyYXJjaHkgPSAiZmVjaGFfY2FsY3VsbyIKICAgIGF1dG9jb21wbGV0ZV9maWVsZHMgPSAoInVuaWRhZF9uZWdvY2lvIiwgInVzdWFyaW8iKQogICAgb3JkZXJpbmcgPSAoIi1wZXJpb2RvIiwpCgoKQGFkbWluLnJlZ2lzdGVyKFBnb01vbnRobHlBZ2cpCmNsYXNzIFBnb01vbnRobHlBZ2dBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAicGVyaW9kbyIsCiAgICAgICAgInVuaWRhZF9uZWdvY2lvIiwKICAgICAgICAiZGVwYXJ0YW1lbnRvIiwKICAgICAgICAidGlja2V0c19yZWNpYmlkb3MiLAogICAgICAgICJ0aWNrZXRzX2NlcnJhZG9zIiwKICAgICAgICAidGllbXBvX3Byb21lZGlvX2hvcmFzIiwKICAgICAgICAic2xhX2N1bXBsaWRvcyIsCiAgICAgICAgInNsYV9pbmN1bXBsaWRvcyIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgicGVyaW9kbyIsICJ1bmlkYWRfbmVnb2NpbyIsICJkZXBhcnRhbWVudG8iKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgicGVyaW9kbyIsICJkZXBhcnRhbWVudG8iKQogICAgYXV0b2NvbXBsZXRlX2ZpZWxkcyA9ICgidW5pZGFkX25lZ29jaW8iLCkKICAgIG9yZGVyaW5nID0gKCItcGVyaW9kbyIsKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/pgo/apps.py
PATH_JSON="apps/pgo/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=8
SIZE_BYTES_UTF8=193
CONTENT_SHA256=a56dd45d935d750c487d560676e4691153fee5d4a7a2c3318221a56ebce0135e
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.apps import AppConfig


class PgoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.pgo"
    label = "wcgone_pgo"
    verbose_name = "PGO"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class PgoConfig(AppConfig):
00005|    default_auto_field = "django.db.models.BigAutoField"
00006|    name = "apps.pgo"
00007|    label = "wcgone_pgo"
00008|    verbose_name = "PGO"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgUGdvQ29uZmlnKEFwcENvbmZpZyk6CiAgICBkZWZhdWx0X2F1dG9fZmllbGQgPSAiZGphbmdvLmRiLm1vZGVscy5CaWdBdXRvRmllbGQiCiAgICBuYW1lID0gImFwcHMucGdvIgogICAgbGFiZWwgPSAid2Nnb25lX3BnbyIKICAgIHZlcmJvc2VfbmFtZSA9ICJQR08iCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/pgo/imports/__init__.py
PATH_JSON="apps/pgo/imports/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=82
CONTENT_SHA256=de0786c1197b475c20de846217a3aaf3e20dd61ace6ee8eeea92ab1c664d1324
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from apps.pgo.imports.tickets import import_tickets

__all__ = ["import_tickets"]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from apps.pgo.imports.tickets import import_tickets
00002|
00003|__all__ = ["import_tickets"]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBhcHBzLnBnby5pbXBvcnRzLnRpY2tldHMgaW1wb3J0IGltcG9ydF90aWNrZXRzCgpfX2FsbF9fID0gWyJpbXBvcnRfdGlja2V0cyJdCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
