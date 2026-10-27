from django.test import TestCase

from pgo.models import PgoScorecardCell, PgoScorecardCacheMeta
from pgo.scorecard_cache import (
    META_PK,
    compute_data_fingerprint,
    load_scorecard,
    rebuild_scorecard_cache,
)


class ScorecardCacheTests(TestCase):
    def test_rebuild_persists_cells_and_meta(self):
        meta = rebuild_scorecard_cache(years=[2026])
        self.assertEqual(meta.pk, META_PK)
        self.assertTrue(PgoScorecardCell.objects.filter(year=2026).exists())
        self.assertEqual(meta.fingerprint, compute_data_fingerprint())

    def test_load_uses_cache_when_fingerprint_matches(self):
        rebuild_scorecard_cache(years=[2026])
        loaded = load_scorecard(years=[2026])
        self.assertTrue(loaded.from_cache)
        self.assertIsNotNone(loaded.meta.computed_at)

    def test_load_rebuilds_when_meta_missing(self):
        PgoScorecardCacheMeta.objects.all().delete()
        PgoScorecardCell.objects.all().delete()
        loaded = load_scorecard(years=[2026])
        self.assertFalse(loaded.from_cache)
        self.assertTrue(PgoScorecardCell.objects.exists())
