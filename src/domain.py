"""读取并检查共享的领域资料。"""

import json
from pathlib import Path

REQUIRED_FIELDS = {
    "domain",
    "version",
    "sample_id",
    "actors",
    "quantity_chain",
    "controlled_events",
    "facts",
    "constraints",
}


def load_domain(path: Path) -> dict:
    """返回字段完整且带版本的业务资料。"""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not REQUIRED_FIELDS.issubset(value):
        raise ValueError("共享资料缺少必要字段")
    if value["version"] < 1:
        raise ValueError("共享资料版本无效")
    _check_actors(value["actors"])
    _check_stages(value["quantity_chain"], "数量链")
    _check_stages(value["controlled_events"], "受控事件")
    if len(value["facts"]) < 2 or len(value["constraints"]) < 2:
        raise ValueError("共享资料内容不完整")
    return value


def _check_actors(actors: list) -> None:
    if len(actors) < 2:
        raise ValueError("共享资料内容不完整")
    for actor in actors:
        if not isinstance(actor, dict):
            raise ValueError("参与方必须写明角色与核对诉求")
        role, need = actor.get("role"), actor.get("need")
        if not isinstance(role, str) or not role or not isinstance(need, str) or not need:
            raise ValueError("参与方必须写明角色与核对诉求")


def _check_stages(stages: list, label: str) -> None:
    if not all(isinstance(stage, str) and stage for stage in stages):
        raise ValueError(f"{label}环节必须是非空文字")
    if len(stages) < 2 or len(set(stages)) != len(stages):
        raise ValueError(f"{label}必须包含两个以上不重复的环节")
