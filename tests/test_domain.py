import unittest
from pathlib import Path
from src.domain import load_domain

class DomainTest(unittest.TestCase):
    def test_fixture_matches_domain(self):
        value = load_domain(Path("fixtures/domain.json"))
        self.assertEqual(value["domain"], "seafood-yield-settlement")
        self.assertGreaterEqual(len(value["constraints"]), 2)

    def test_quantity_chain_covers_settlement_flow(self):
        value = load_domain(Path("fixtures/domain.json"))
        stages = [item["stage"] for item in value["quantity_chain"]]
        for expected in ["采购合同", "到货称重", "抽样品质", "加工工单", "分级产物", "副产物", "合理损耗", "成品交付"]:
            self.assertIn(expected, stages)
        self.assertIn("=", value["conservation"])

    def test_controls_require_dual_confirmation_and_versioning(self):
        value = load_domain(Path("fixtures/domain.json"))
        operations = {item["operation"] for item in value["controls"]}
        for expected in ["跨班次投料", "混批", "复称更正", "部分拒收", "委外加工", "币种换算"]:
            self.assertIn(expected, operations)
        for item in value["controls"]:
            self.assertTrue(item["dual_confirmation"])
            self.assertTrue(item["versioned"])

    def test_views_cover_all_parties(self):
        value = load_domain(Path("fixtures/domain.json"))
        for role in ["东盟水产供应商", "车间质量人员", "采购财务人员", "管理层"]:
            self.assertIn(role, value["views"])

if __name__ == "__main__":
    unittest.main()
