from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils import timezone

from pgo.capturas_services import is_out_of_period, latest_version, validate_operation_id
from pgo.models import PgoManualCaptureVersion

User = get_user_model()


class PgoManualCaptureVersionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="capturador", password="x")

    def test_append_only_versions(self):
        v1 = PgoManualCaptureVersion.objects.create(
            capture_type="ti_backup_nas",
            period_year=2026,
            period_month=3,
            user=self.user,
            payload={"quarter": "1"},
        )
        v2 = PgoManualCaptureVersion.objects.create(
            capture_type="ti_backup_nas",
            period_year=2026,
            period_month=3,
            user=self.user,
            payload={"quarter": "1", "backup_nas_done": "yes"},
            change_note="Corrección",
        )
        self.assertEqual(PgoManualCaptureVersion.objects.filter(capture_type="ti_backup_nas").count(), 2)
        latest = latest_version("ti_backup_nas", 2026, 3)
        self.assertEqual(latest.pk, v2.pk)
        self.assertNotEqual(latest.pk, v1.pk)

    def test_is_out_of_period_flag(self):
        now = timezone.now()
        self.assertFalse(is_out_of_period(now.year, now.month))
        self.assertTrue(is_out_of_period(2020, 1))

    def test_operation_id_validation(self):
        self.assertIsNone(validate_operation_id("AB12_3"))
        self.assertIsNotNone(validate_operation_id("AB"))
