"""Render public, editable SVG infographics for the technology portfolio."""
from __future__ import annotations

from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "assets" / "visuals"
W, H = 1600, 900

BG = "#101820"
PANEL = "#182630"
PANEL_2 = "#203541"
TEXT = "#F4F7F5"
MUTED = "#B5C7C8"
GREEN = "#9AD8B7"
YELLOW = "#F2C879"
BLUE = "#8DC7E8"
CORAL = "#F29D83"
LINE = "#49636A"


def esc(value: str) -> str:
    return escape(value, quote=True)


def text(x: int, y: int, value: str, size: int = 24, color: str = TEXT, weight: int = 400) -> str:
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, Microsoft YaHei, sans-serif" font-size="{size}px" font-weight="{weight}">{esc(value)}</text>'


def rect(x: int, y: int, w: int, h: int, fill: str = PANEL, stroke: str = "none", radius: int = 18) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def line(x1: int, y1: int, x2: int, y2: int, color: str = LINE, width: int = 3, dash: str = "") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{dash_attr}/>'


def pill(x: int, y: int, label: str, color: str) -> str:
    width = max(120, 22 * len(label) + 38)
    return rect(x, y, width, 42, color, "none", 21) + text(x + 20, y + 28, label, 18, BG, 700)


def panel(x: int, y: int, w: int, h: int, title_: str, body: list[str], accent: str, stage: str | None = None) -> str:
    out = [rect(x, y, w, h, PANEL, LINE, 18), rect(x, y, 8, h, accent, "none", 4), text(x + 30, y + 44, title_, 28, TEXT, 700)]
    cy = y + 84
    for item in body:
        out.append(text(x + 30, cy, item, 20, MUTED, 400))
        cy += 36
    if stage:
        out.append(pill(x + 28, y + h - 62, stage, accent))
    return "".join(out)


def arrow(x1: int, y1: int, x2: int, y2: int, color: str = GREEN) -> str:
    return line(x1, y1, x2, y2, color, 4) + f'<path d="M {x2-16} {y2-10} L {x2} {y2} L {x2-16} {y2+10}" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'


def frame(title_: str, subtitle: str) -> list[str]:
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', rect(0, 0, W, H, BG, "none", 0), text(72, 78, title_, 42, TEXT, 700), text(74, 120, subtitle, 21, MUTED, 400), line(72, 150, 1528, 150, LINE, 2)]


def finish(parts: list[str], name: str) -> None:
    parts.append(text(74, 850, "公开技术资产回顾 · 当前阶段与下一步验收", 17, MUTED, 400))
    parts.append("</svg>")
    (OUT / name).write_text("".join(parts) + "\n", encoding="utf-8")


def render_platform() -> None:
    p = frame("农业模型技术全景", "从空间观测、视觉识别到评价、处方和现场回执")
    boxes = [
        (90, 250, "数据与观测", ["Sentinel-2 · 无人机 · 手机", "报告 · 传感 · 地块主数据"], BLUE, "工程基础"),
        (430, 250, "模型与识别", ["NDVI 分区 · 地块分割", "出苗率 · 杂草 · 病虫害", "生育期 · 农资 · 测土"], GREEN, "能力资产"),
        (770, 250, "决策与产品", ["地块评价 · 风险评分", "变量播种/施肥/点喷处方", "智能体与知识服务"], YELLOW, "受控试点"),
        (1110, 250, "现场与反馈", ["审核 · 任务 · 设备回执", "人工修订 · 质量监控", "专利/版本/证据台账"], CORAL, "未来重点"),
    ]
    for x, y, t, b, c, s in boxes:
        p.append(panel(x, y, 300, 310, t, b, c, s))
    for x in [390, 730, 1070]:
        p.append(arrow(x, 405, x + 40, 405))
    p.append(text(100, 680, "当前最接近产品价值", 24, GREEN, 700))
    p.append(text(100, 720, "Sentinel-2 分区处方 · 农资/测土识别 · 地块评估", 22, TEXT, 400))
    p.append(text(830, 680, "优先补证据", 24, CORAL, 700))
    p.append(text(830, 720, "无人机出苗率 · 杂草点喷 · 病斑严重度 · 设备回执", 22, TEXT, 400))
    finish(p, "01-platform-landscape.svg")


def render_remote() -> None:
    p = frame("遥感质量与地块洞察", "把观测、恢复、分区和处方分成可追溯的阶段")
    steps = [
        (90, "观测", ["Sentinel-2", "RGB / NDVI"], BLUE),
        (390, "质量", ["云影识别", "清晰 / 恢复 / 拒绝"], CORAL),
        (690, "空间", ["地块分割", "五级 NDVI 分区"], GREEN),
        (990, "处方", ["Shapefile", "ISOXML / 施肥档位"], YELLOW),
    ]
    for x, t, b, c in steps:
        p.append(panel(x, 250, 250, 270, t, b, c, "当前链路"))
    for x in [340, 640, 940]:
        p.append(arrow(x, 380, x + 48, 380))
    p.append(panel(90, 610, 650, 150, "当前阶段", ["已有产品链路；云影与 NDVI 修复有专利/申请依据", "跨区域清晰锚点和业务效果仍待验证"], GREEN, "工程到试点"))
    p.append(panel(780, 610, 650, 150, "未来动作", ["日期留出、空间稳定、面积/剂量守恒", "接收真实地块回执，再写成现场验收"], YELLOW, "下一步"))
    finish(p, "02-remote-sensing.svg")


def render_agent() -> None:
    p = frame("农业智能体与知识服务", "让回答、工具调用和业务报告都能回到证据")
    p.append(panel(90, 250, 300, 280, "用户问题", ["地块 / 作物 / 农资", "图片 / 报告 / 任务"], BLUE, "输入"))
    p.append(panel(470, 250, 300, 280, "知识与工具", ["检索证据", "识别模型", "处方和评估工具"], GREEN, "工程骨架"))
    p.append(panel(850, 250, 300, 280, "结果编排", ["诊断候选", "推荐和风险", "报告与待办"], YELLOW, "候选能力"))
    p.append(panel(1230, 250, 280, 280, "证据门禁", ["引用", "置信度", "人工确认"], CORAL, "未来重点"))
    for x in [390, 770, 1150]:
        p.append(arrow(x, 390, x + 52, 390))
    p.append(text(120, 650, "下一步评测", 24, GREEN, 700))
    p.append(text(120, 695, "固定问集 · 工具成功率 · 证据召回 · 事实错误 · P95 · 成本 · 失败恢复", 21, TEXT, 400))
    finish(p, "03-agent.svg")


def render_recognition() -> None:
    p = frame("无人机与多模态识别", "出苗率、杂草点喷、病虫害、病斑和农资识别的真实阶段")
    items = [
        (90, "无人机出苗率", ["多光谱", "出苗密度/率", "PAT-03 已授权"], GREEN, "专利授权"),
        (430, "杂草点喷", ["检测/覆盖/阶段", "地理矢量化", "自动执行待证"], YELLOW, "方案链路"),
        (770, "病虫害/病斑", ["候选识别", "掩膜/严重度", "真值待补"], CORAL, "能力资产"),
        (1110, "农资/测土", ["二维码/包装", "14 项土壤指标", "字段校验"], BLUE, "服务候选"),
    ]
    for x, t, b, c, s in items:
        p.append(panel(x, 240, 300, 310, t, b, c, s))
    p.append(text(120, 650, "共同下一步", 24, GREEN, 700))
    p.append(text(120, 695, "固定测试集 → 字段/像素指标 → 正确留空 → 人工复核 → 地块/任务层验收", 22, TEXT, 400))
    finish(p, "04-recognition.svg")


def render_land() -> None:
    p = frame("地块评估与风险解释", "把多源事实组织成可复核的分数、证据和报告")
    p.append(panel(90, 250, 300, 290, "地块快照", ["位置 / 边界", "遥感 / 土壤 / 气象", "经营与历史信息"], BLUE, "输入"))
    p.append(panel(470, 250, 300, 290, "评价计算", ["指标规则", "风险评分", "缺失与冲突检查"], GREEN, "原型联调"))
    p.append(panel(850, 250, 300, 290, "解释结果", ["风险项", "证据链", "报告与人工复核"], YELLOW, "可审核"))
    p.append(panel(1230, 250, 280, 290, "反馈", ["专家一致性", "真实回执", "版本更新"], CORAL, "未来重点"))
    for x in [390, 770, 1150]:
        p.append(arrow(x, 395, x + 52, 395))
    p.append(text(120, 660, "关键门槛", 24, CORAL, 700))
    p.append(text(120, 705, "同一输入快照 + 评分版本 + 人工确认状态，才能复核一次评价为什么产生", 22, TEXT, 400))
    finish(p, "05-land-assessment.svg")


def render_research() -> None:
    p = frame("研究成果如何进入产品", "先验证权利和结果，再进入受控试点")
    stages = [
        (90, "研究材料", ["FieldBCQ", "Wheat-KGCA"], BLUE, "研究结果"),
        (390, "权利核验", ["数据/权重许可", "合作与权属"], CORAL, "必须通过"),
        (690, "独立复现", ["固定输入", "区域/设备留出"], GREEN, "证据补齐"),
        (990, "受控试点", ["人工复核", "失败边界", "版本回滚"], YELLOW, "可试点"),
    ]
    for x, t, b, c, s in stages:
        p.append(panel(x, 250, 250, 300, t, b, c, s))
    for x in [340, 640, 940]:
        p.append(arrow(x, 395, x + 48, 395))
    p.append(panel(1290, 250, 220, 300, "产品化", ["现场验收", "监控", "漂移"], GREEN, "目标"))
    p.append(arrow(1240, 395, 1290, 395))
    p.append(text(120, 660, "当前结论", 24, GREEN, 700))
    p.append(text(120, 705, "两项研究成果具备转化价值，但尚未替代当前产品的现场验收证据", 22, TEXT, 400))
    finish(p, "06-research-to-product.svg")


def render_ip() -> None:
    p = frame("知识产权与研发路线", "专利状态、模型映射和下一步核验放在一张图里")
    p.append(panel(90, 240, 300, 330, "已授权", ["PAT-01 云影", "PAT-03 出苗率", "PAT-04 地块分割", "PAT-02 时序储备"], GREEN, "4 项"))
    p.append(panel(470, 240, 300, 330, "授权通知", ["PAT-05 样方矢量化", "登记公告与证书", "定位误差待验"], YELLOW, "1 项"))
    p.append(panel(850, 240, 300, 330, "申请阶段", ["PAT-06 生育期", "PAT-07 NDVI 修复", "公布/实审状态待核"], BLUE, "2 项"))
    p.append(panel(1230, 240, 280, 330, "产品映射", ["模型清单", "产品版本", "现场验收", "权属/许可"], CORAL, "持续核验"))
    for x in [390, 770, 1150]:
        p.append(arrow(x, 405, x + 52, 405))
    p.append(text(120, 670, "台账动作", 24, GREEN, 700))
    p.append(text(120, 715, "申请号/公布号 → 当前法律状态 → 覆盖模型 → 产品证据 → 权属与许可", 22, TEXT, 400))
    finish(p, "07-ip-and-roadmap.svg")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    render_platform()
    render_remote()
    render_agent()
    render_recognition()
    render_land()
    render_research()
    render_ip()


if __name__ == "__main__":
    main()
