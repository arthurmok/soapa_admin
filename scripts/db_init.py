# --*-- coding: utf-8 --*--
from asset import db
from asset.models.assets import AssetAgentType, AssetType
from insp.models.inspect_model import InspectAssessType, InspectObject, InspectInjureLevel, InspectObjectLevelRela


def _init_asset_type():
    defaults = (
        ("个人终端",""),
        ("服务器", ""),
        ("网络设备", ""),
        ("周边设备", ""),
        ("应用系统", "")
    )
    for name, desc in defaults:
        asset_type = AssetType(name, desc)
        db.session.add(asset_type)
        db.session.commit()


def _init_asset_agent_type():
    defaults = (
        ("Agent", ""),
        ("SYSlog", ""),
        ("无", ""),

    )
    for name, desc in defaults:
        agent_type = AssetAgentType(name, desc)
        db.session.add(agent_type)
        db.session.commit()


def _init_inspect_assess_type():
    defaults = (
        ("业务信息安全保护等级自评", ""),
        ("系统服务安全保护等级自评", "")
    )
    for name, desc in defaults:
        assess_type = InspectAssessType(name, desc)
        db.session.add(assess_type)
        db.session.commit()


def _init_inspect_object():
    defaults = (
        ("公民、法人和其他组织的合法权益", ""),
        ("社会秩序、公共利益", ""),
        ("国家安全", ""),
    )
    for name, desc in defaults:
        inspect_object = InspectObject(name, desc)
        db.session.add(inspect_object)
        db.session.commit()


def _init_inspect_injure_level():
    defaults = (
        ("一般损害", ""),
        ("严重损害", ""),
        ("特别严重损害", ""),
    )
    for name, desc in defaults:
        injure_level = InspectInjureLevel(name, desc)
        db.session.add(injure_level)
        db.session.commit()


def _init_object_level_rela():
    defaults = (
        (1, 1, "第一级", 1, ""),
        (1, 2, "第二级", 2, ""),
        (1, 3, "第二级", 2, ""),
        (2, 1, "第二级", 2, ""),
        (2, 2, "第三级", 3, ""),
        (2, 3, "第四级", 4, ""),
        (3, 1, "第三级", 3, ""),
        (3, 2, "第四级", 4, ""),
        (3, 3, "第五级", 5, "")
    )
    for object_id, injure_level_id, name, level, describe in defaults:
        object_level_rela = InspectObjectLevelRela(object_id, injure_level_id, name, level, describe)
        db.session.add(object_level_rela)
        db.session.commit()


def main():
    # _init_asset_type()
    # _init_asset_agent_type()
    # _init_inspect_assess_type()
    # _init_inspect_object()
    # _init_inspect_injure_level()
    _init_object_level_rela()


if __name__ == '__main__':
    main()
