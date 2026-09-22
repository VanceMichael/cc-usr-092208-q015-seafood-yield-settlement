import json
import tempfile
import unittest
from pathlib import Path
from src.domain import load_domain

FIXTURE = Path("fixtures/domain.json")


class DomainTest(unittest.TestCase):
    def test_fixture_matches_domain(self):
        value = load_domain(FIXTURE)
        self.assertEqual(value["domain"], "seafood-yield-settlement")
        self.assertGreaterEqual(value["version"], 2)

    def test_quantity_chain_runs_contract_to_delivery(self):
        value = load_domain(FIXTURE)
        chain = value["quantity_chain"]
        self.assertEqual(chain[0], "采购合同")
        self.assertEqual(chain[-1], "成品交付")
        for stage in ("到货称重", "抽样品质", "加工工单", "分级产物", "副产物", "合理损耗"):
            self.assertIn(stage, chain)

    def test_controlled_events_cover_special_operations(self):
        value = load_domain(FIXTURE)
        for event in ("跨班次投料", "混批", "复称更正", "部分拒收", "委外加工", "币种换算"):
            self.assertIn(event, value["controlled_events"])

    def test_actor_needs_cover_four_views(self):
        value = load_domain(FIXTURE)
        needs = {actor["role"]: actor["need"] for actor in value["actors"]}
        self.assertIn("扣价依据", needs["东盟水产供应商"])
        self.assertIn("可执行配料", needs["车间"])
        self.assertIn("来源", needs["财务"])
        self.assertIn("真实得率", needs["管理层"])

    def test_material_without_controlled_events_rejected(self):
        value = load_domain(FIXTURE)
        broken = {key: item for key, item in value.items() if key != "controlled_events"}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.json"
            path.write_text(json.dumps(broken, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_domain(path)

    def test_actor_without_need_rejected(self):
        value = load_domain(FIXTURE)
        broken = dict(value, actors=[{"role": "车间"} for _ in value["actors"]])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.json"
            path.write_text(json.dumps(broken, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_domain(path)


if __name__ == "__main__":
    unittest.main()
