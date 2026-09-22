"""读取并检查共享的领域资料。"""

import json
from pathlib import Path

def load_domain(path: Path) -> dict:
    """返回字段完整且带版本的业务资料。"""
    value = json.loads(path.read_text(encoding="utf-8"))
    required = {"domain", "version", "sample_id", "actors", "facts", "constraints"}
    if not required.issubset(value):
        raise ValueError("共享资料缺少必要字段")
    if value["version"] < 1 or len(value["actors"]) < 2 or len(value["facts"]) < 2 or len(value["constraints"]) < 2:
        raise ValueError("共享资料内容不完整")
    if value["version"] >= 2:
        _check_settlement(value)
    return value

def _check_settlement(value: dict) -> None:
    """检查得率结算的数量链、控制点与角色视图。"""
    needed = {"quantity_chain", "conservation", "controls", "views"}
    if not needed.issubset(value):
        raise ValueError("结算资料缺少数量链、守恒规则、控制点或角色视图")
    if len(value["quantity_chain"]) < 2:
        raise ValueError("数量链环节不完整")
    for control in value["controls"]:
        if not control.get("dual_confirmation") or not control.get("versioned"):
            raise ValueError("控制点必须双人确认并保留版本记录")
