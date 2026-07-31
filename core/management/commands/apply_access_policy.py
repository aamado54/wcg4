"""Aplica política de acceso: allowlist Balón/Gerencia + ops sin superuser."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import UserProfile


class Command(BaseCommand):
    help = (
        "Solo 'caa' queda como superusuario; todos los usuarios activos son staff "
        "con acceso total PGC (default_all_une_access). "
        "Balón/Gerencia se controla por WCG_RISK_GERENCIA_USERNAMES."
    )

    def handle(self, *args, **options):
        User = get_user_model()
        keep_super = {
            str(u).strip().lower()
            for u in getattr(settings, "WCG_SUPERUSER_USERNAMES", ("caa",))
            if str(u).strip()
        }
        if not keep_super:
            keep_super = {"caa"}

        updated_super = demoted = staffed = profiles = 0
        for user in User.objects.all():
            uname = user.username.lower()
            changed = False

            if uname in keep_super:
                if not user.is_superuser or not user.is_staff:
                    user.is_superuser = True
                    user.is_staff = True
                    changed = True
                    updated_super += 1
            else:
                if user.is_superuser:
                    user.is_superuser = False
                    changed = True
                    demoted += 1
                if not user.is_staff:
                    user.is_staff = True
                    changed = True
                    staffed += 1

            if changed:
                user.save(update_fields=["is_superuser", "is_staff"])

            profile, _ = UserProfile.objects.get_or_create(user=user)
            pref_changed = False
            if not profile.default_all_une_access:
                profile.default_all_une_access = True
                pref_changed = True
            if uname in keep_super and profile.role_label != UserProfile.ROLE_ADMIN:
                profile.role_label = UserProfile.ROLE_ADMIN
                pref_changed = True
            elif (
                uname not in keep_super
                and profile.role_label == UserProfile.ROLE_ADMIN
            ):
                profile.role_label = UserProfile.ROLE_USUARIO
                pref_changed = True
            if pref_changed:
                profile.save()
                profiles += 1

        allow = sorted(
            {
                str(u).strip().lower()
                for u in getattr(
                    settings, "WCG_RISK_GERENCIA_USERNAMES", ("caa", "gsoler")
                )
                if str(u).strip()
            }
        )
        missing = [u for u in allow if not User.objects.filter(username__iexact=u).exists()]

        self.stdout.write(
            self.style.SUCCESS(
                f"OK super keep={sorted(keep_super)} updated_super={updated_super} "
                f"demoted={demoted} staffed={staffed} profiles={profiles}"
            )
        )
        self.stdout.write(f"Allowlist Balón/Gerencia: {allow}")
        if missing:
            self.stdout.write(
                self.style.WARNING(
                    f"Usuarios de la allowlist aún no existen en DB: {missing}"
                )
            )
