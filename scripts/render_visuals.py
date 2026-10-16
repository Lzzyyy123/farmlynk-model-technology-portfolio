"""Render public-facing raster infographics for the portfolio.

The visuals intentionally communicate scope, maturity and next steps without
exposing repository names, local paths, branches or implementation locations.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "assets" / "visuals"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1600, 900
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
BG = "#101C26"
PAPER = "#F7F8F4"
INK = "#13232E"
MUTED = "#A8B5B5"
TEAL = "#46C2B3"
CORAL = "#FF8A73"
GOLD = "#F0C36A"
BLUE = "#65A9E6"
LIME = "#B8D878"
PANEL = "#1B2C37"
PANEL2 = "#243A46"


def font(size: int, bold: bool = False):
    try:
        return ImageFont.truetype(FONT, size, index=0)
    except OSError:
        return ImageFont.load_default()


def canvas(title: str, subtitle: str, number: str):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((72, 48), number, fill=TEAL, font=font(22, True))
    d.text((72, 88), title, fill=PAPER, font=font(48, True))
    d.text((74, 154), subtitle, fill=MUTED, font=font(22))
    d.line((72, 202, 1528, 202), fill="#314652", width=2)
    d.text((72, 850), "FarmLynk · 模型技术资产与研发路线 · 公开整理版 V2.0", fill="#71858A", font=font(16))
    return im, d


def rounded(d, xy, fill, outline=None, radius=18, width=2):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def text_center(d, box, title, detail, color=INK, accent=TEAL):
    x1, y1, x2, y2 = box
    d.text(((x1 + x2) / 2, y1 + 20), title, anchor="ma", fill=accent, font=font(24, True))
    d.multiline_text(((x1 + x2) / 2, y1 + 69), detail, anchor="ma", align="center", fill=color, font=font(19), spacing=8)


def arrow(d, start, end, fill=TEAL, width=5):
    d.line((*start, *end), fill=fill, width=width)
    x1, y1 = start; x2, y2 = end
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 16
    p1 = (x2 - size * math.cos(angle - 0.45), y2 - size * math.sin(angle - 0.45))
    p2 = (x2 - size * math.cos(angle + 0.45), y2 - size * math.sin(angle + 0.45))
    d.polygon([(x2, y2), p1, p2], fill=fill)


def badge(d, x, y, label, color):
    rounded(d, (x, y, x + 172, y + 42), color, radius=21, width=0)
    d.text((x + 86, y + 21), label, anchor="mm", fill=BG, font=font(17, True))


def save(im, name):
    im.save(OUT / name, format="PNG", optimize=True)


def platform():
    im, d = canvas("农业智能技术全景", "一张图看懂：数据从哪里来，能力做什么，产品如何承接，下一步补什么证据。", "01 / PORTFOLIO")
    cols = [(70, 260, 430, 735), (510, 260, 890, 735), (970, 260, 1530, 735)]
    for box in cols: rounded(d, box, PANEL, outline="#38505A", radius=24, width=2)
    d.text((105, 292), "事实与观测", fill=GOLD, font=font(27, True)); d.text((545, 292), "模型与认知", fill=TEAL, font=font(27, True)); d.text((1005, 292), "业务与现场", fill=CORAL, font=font(27, True))
    inputs=[("空间数据", "地块 · 土壤 · 地形"), ("环境数据", "天气 · NDVI · 传感"), ("业务数据", "农事 · 试验 · 主数据"), ("视觉证据", "卫星 · 无人机 · 包装")]
    for i,(a,b) in enumerate(inputs):
        y=360+i*82; rounded(d,(104,y,396,y+58),PANEL2,outline="#4C6670",radius=14); d.text((125,y+12),a,fill=PAPER,font=font(21,True)); d.text((250,y+15),b,fill=MUTED,font=font(16))
    models=[("遥感质量", "去云 · 时序 · 分区"), ("多模态识别", "农资 · 报告 · 病虫草"), ("智能体", "知识 · 工具 · 证据"), ("评估与处方", "风险 · 地块 · 作业")]
    for i,(a,b) in enumerate(models):
        y=360+i*82; rounded(d,(544,y,856,y+58),"#214A4D",outline=TEAL,radius=14); d.text((565,y+12),a,fill=TEAL,font=font(21,True)); d.text((700,y+15),b,fill=PAPER,font=font(16))
    products=[("产品服务", "生产管理 · 评估 · 识别"), ("农事协同", "任务 · 处方 · 回执"), ("研究转化", "候选成果 · 试点"), ("效果闭环", "人工复核 · 现场真值")]
    for i,(a,b) in enumerate(products):
        y=360+i*82; rounded(d,(1004,y,1496,y+58),"#49343A",outline=CORAL,radius=14); d.text((1025,y+12),a,fill=CORAL,font=font(21,True)); d.text((1150,y+15),b,fill=PAPER,font=font(16))
    for y in [388,470,552,634]: arrow(d,(430,y),(505,y),GOLD); arrow(d,(890,y),(965,y),CORAL)
    badge(d, 70, 770, "当前：工程能力成型", TEAL); badge(d, 520, 770, "缺口：真值与验收", GOLD); badge(d, 970, 770, "未来：规模化闭环", CORAL)
    save(im,"01-platform-landscape.png")


def remote():
    im, d = canvas("遥感质量与地块洞察", "把“看见”与“估算”分开：先判断可信度，再决定是否进入统计、评估和处方。", "02 / REMOTE SENSING")
    # Satellite and field scene
    d.ellipse((82, 300, 290, 510), fill="#304954", outline=BLUE, width=4); d.ellipse((132,350,240,458), fill="#102A35", outline=TEAL, width=3)
    d.line((185, 510, 420, 650), fill=BLUE, width=4); d.line((230, 500, 500, 650), fill=BLUE, width=4)
    d.text((106, 555), "卫星观测", fill=PAPER, font=font(25, True)); d.text((98, 594), "日期 · 覆盖 · 云影", fill=MUTED, font=font(18))
    # flow cards
    cards=[("质量分层", "clear / partial / reject", GOLD), ("时序恢复", "候选来源 + 不确定性", TEAL), ("空间洞察", "NDVI · 分区 · 边界", BLUE), ("业务消费", "地图 / 评估 / 处方", CORAL)]
    for i,(title,detail,c) in enumerate(cards):
        x=400+i*275; rounded(d,(x,330,x+220,540),PANEL,outline=c,radius=24); d.ellipse((x+78,360,x+142,424),fill=c); d.text((x+110,392),str(i+1),anchor="mm",fill=BG,font=font(25,True)); d.text((x+110,455),title,anchor="ma",fill=c,font=font(23,True)); d.multiline_text((x+110,492),detail,anchor="ma",align="center",fill=PAPER,font=font(16),spacing=4)
        if i<3: arrow(d,(x+225,435),(x+265,435),c)
    # mini NDVI chart
    d.line((445,690,1330,690),fill="#4A6872",width=2); d.line((445,590,445,690),fill="#4A6872",width=2)
    pts=[(470,660),(550,642),(635,620),(720,635),(805,610),(890,600),(975,575),(1060,590),(1145,545),(1230,560),(1310,525)]
    d.line(pts,fill=TEAL,width=5); d.text((448,708),"时间",fill=MUTED,font=font(16)); d.text((350,570),"NDVI",fill=MUTED,font=font(16)); d.text((450,735),"当前：质量门禁与候选恢复",fill=TEAL,font=font(19,True)); d.text((1030,735),"下一步：真实锚点与跨区验证",fill=GOLD,font=font(19,True))
    save(im,"02-remote-sensing.png")


def agent():
    im, d = canvas("农业智能体与知识服务", "智能体的核心不是“会聊天”，而是能调用正确工具、引用证据、在失败后恢复并留下可审计结果。", "03 / AGENT")
    # center core
    rounded(d,(630,300,970,610),"#214A4D",outline=TEAL,radius=40,width=4); d.ellipse((720,365,880,525),fill=TEAL); d.ellipse((755,400,790,435),fill=BG); d.ellipse((810,400,845,435),fill=BG); d.arc((755,420,845,500),0,180,fill=BG,width=7); d.text((800,555),"统一运行时",anchor="ma",fill=PAPER,font=font(23,True))
    left=[("知识", "农业资料 · 规则 · 历史"), ("上下文", "组织 · 地块 · 会话"), ("策略", "模型 · 成本 · 证据")]
    for i,(a,b) in enumerate(left):
        y=292+i*118; rounded(d,(90,y,485,y+82),PANEL,outline=BLUE,radius=18); d.text((120,y+18),a,fill=BLUE,font=font(23,True)); d.text((120,y+52),b,fill=PAPER,font=font(17)); arrow(d,(485,y+40),(615,y+40),BLUE)
    right=[("查询工具", "天气 · 土壤 · 遥感"), ("识别工具", "图像 · 包装 · 报告"), ("业务动作", "任务 · 报告 · 人工确认")]
    for i,(a,b) in enumerate(right):
        y=292+i*118; rounded(d,(1115,y,1510,y+82),PANEL,outline=CORAL,radius=18); d.text((1145,y+18),a,fill=CORAL,font=font(23,True)); d.text((1145,y+52),b,fill=PAPER,font=font(17)); arrow(d,(985,y+40),(1100,y+40),CORAL)
    rounded(d,(360,700,1240,770),"#243A46",outline=GOLD,radius=22); d.text((800,735),"证据门禁 → 结果解释 → 人工确认 → 状态回写 → 可复盘",anchor="mm",fill=GOLD,font=font(22,True))
    badge(d, 90, 790, "当前：工程骨架", TEAL); badge(d, 575, 790, "补齐：评测与成本", GOLD); badge(d, 1110, 790, "未来：可靠执行", CORAL)
    save(im,"03-agent.png")


def recognition():
    im, d = canvas("农资与测土报告识别", "四类输入共享同一原则：字段有来源、缺失要留空、低置信度进入人工复核。", "04 / RECOGNITION")
    inputs=[("农药", "二维码 / 登记信息", CORAL), ("肥料", "包装字段 / 规格", GOLD), ("助剂", "名称 / 用量 / 价格", TEAL), ("测土报告", "14项指标 / 单位", BLUE)]
    for i,(a,b,c) in enumerate(inputs):
        x=90+i*370; rounded(d,(x,300,x+300,470),PANEL,outline=c,radius=25); d.rounded_rectangle((x+95,330,x+205,420),radius=14,fill=c); d.rectangle((x+122,353,x+178,397),fill=BG); d.text((x+150,443),a,anchor="ma",fill=c,font=font(25,True)); d.text((x+150,486),b,anchor="ma",fill=PAPER,font=font(16))
        arrow(d,(x+305,385),(x+350,385),c)
    stages=[("图像质量", "可读 / 拒识"), ("VLM + OCR", "抽取 / 原文"), ("规则校验", "单位 / 范围"), ("人工复核", "确认 / 纠错")]
    for i,(a,b) in enumerate(stages):
        x=140+i*360; rounded(d,(x,575,x+285,705),"#243A46",outline=TEAL if i<3 else CORAL,radius=20); d.text((x+142,610),a,anchor="ma",fill=TEAL if i<3 else CORAL,font=font(22,True)); d.text((x+142,655),b,anchor="ma",fill=PAPER,font=font(18));
        if i<3: arrow(d,(x+290,640),(x+345,640),TEAL)
    d.text((90,770),"当前：服务化候选",fill=TEAL,font=font(20,True)); d.text((620,770),"下一步：字段级真值 + 正确留空 + 批测成本",fill=GOLD,font=font(20,True));
    save(im,"04-recognition.png")


def assessment():
    im, d = canvas("地块评估与风险解释", "将空间、环境和经营证据组织成可解释报告；分数必须能回到输入快照、规则版本和人工复核。", "05 / ASSESSMENT")
    # map
    rounded(d,(80,280,780,730),"#183943",outline=TEAL,radius=28); d.text((120,315),"地块证据",fill=TEAL,font=font(28,True))
    polys=[[(150,420),(350,360),(470,445),(390,580),(190,560)],[(480,410),(680,380),(710,540),(530,620),(440,510)]]
    for poly,c in zip(polys,[GOLD,CORAL]): d.polygon(poly,fill="#2B4D52",outline=c,width=5)
    d.line((150,420,350,360,470,445,390,580,190,560,150,420),fill=GOLD,width=2); d.text((182,505),"土壤",fill=PAPER,font=font(18)); d.text((560,480),"经营",fill=PAPER,font=font(18)); d.text((400,655),"地形 · 气候 · 植被",anchor="ma",fill=MUTED,font=font(18))
    arrow(d,(820,500),(950,500),CORAL)
    rounded(d,(980,285,1510,730),PANEL,outline=CORAL,radius=28); d.text((1030,325),"解释式报告",fill=CORAL,font=font(28,True));
    rows=[("输入快照", "区域 / 时间 / 数据质量"), ("评价维度", "土壤 · 气候 · 地形 · 经营"), ("风险结论", "等级 + 证据 + 不确定性"), ("人工审核", "同意 / 修订 / 退回")]
    for i,(a,b) in enumerate(rows):
        y=395+i*72; d.text((1030,y),a,fill=GOLD if i==2 else TEAL,font=font(20,True)); d.text((1225,y),b,fill=PAPER,font=font(18)); d.line((1030,y+38,1450,y+38),fill="#3D5861",width=2)
    badge(d, 1000, 655, "当前：原型联调", TEAL); badge(d, 1250, 655, "未来：专家一致性", GOLD)
    save(im,"05-land-assessment.png")


def research():
    im, d = canvas("研究成果如何进入产品", "两项外部研究成果先经过许可、数据、复现实验和区域验证，再决定是否进入业务试点。", "06 / RESEARCH")
    # lanes
    items=[("FieldBCQ", "地块边界实例分割\n测试集 2,000 图 / 21,190 实例\nMask mAP50-95：0.420±0.004", CORAL), ("Wheat-KGCA", "知识约束生育期视觉识别\n八类阶段框架\n最终成绩与完整数据待核验", BLUE)]
    for i,(title,detail,c) in enumerate(items):
        x=90+i*430; rounded(d,(x,310,x+360,560),PANEL,outline=c,radius=28); d.text((x+180,350),title,anchor="ma",fill=c,font=font(29,True)); d.multiline_text((x+180,415),detail,anchor="ma",align="center",fill=PAPER,font=font(18),spacing=12)
    arrow(d,(800,435),(980,435),GOLD,width=7)
    rounded(d,(1010,290,1510,575),"#4A3B2A",outline=GOLD,radius=28); d.text((1260,335),"验证闸门",anchor="ma",fill=GOLD,font=font(28,True)); d.multiline_text((1260,410),"许可核验\n数据与权重\n独立复现\n区域盲测",anchor="ma",align="center",fill=PAPER,font=font(21),spacing=13)
    d.line((160,675,1440,675),fill="#526B72",width=5); phases=[("研究",160,CORAL), ("复现",470,GOLD), ("试点",800,TEAL), ("产品",1190,BLUE)]
    for label,x,c in phases: d.ellipse((x,650,x+48,698),fill=c); d.text((x+24,735),label,anchor="ma",fill=c,font=font(20,True))
    d.text((90,790),"当前：研究成果",fill=CORAL,font=font(20,True)); d.text((560,790),"下一步：可复现、可许可、可验收",fill=GOLD,font=font(20,True)); d.text((1200,790),"目标：候选服务",fill=TEAL,font=font(20,True))
    save(im,"06-research-to-product.png")


def ip_roadmap():
    im, d = canvas("知识产权与研发路线", "把专利、软著、研究结果和产品证据放在同一条转化链上，状态清楚、责任清楚、缺口清楚。", "07 / GOVERNANCE")
    stages=[("形成", "问题 / 方案 / 研究记录", BLUE), ("申请", "专利 / 软著 / 联合权属", CORAL), ("验证", "数据 / 指标 / 权利要求对应", GOLD), ("转化", "试点 / 验收 / 许可", TEAL)]
    for i,(a,b,c) in enumerate(stages):
        x=100+i*370; rounded(d,(x,320,x+285,520),PANEL,outline=c,radius=25); d.ellipse((x+102,350,x+183,431),fill=c); d.text((x+142,390),str(i+1),anchor="mm",fill=BG,font=font(30,True)); d.text((x+142,465),a,anchor="ma",fill=c,font=font(25,True)); d.multiline_text((x+142,555),b,anchor="ma",align="center",fill=PAPER,font=font(17),spacing=8)
        if i<3: arrow(d,(x+290,420),(x+350,420),c,width=5)
    rounded(d,(170,700,1430,780),"#243A46",outline=GOLD,radius=20); d.text((800,740),"本版台账：7 项专利事项 + 4 项软著 · 重点补齐权属、许可、权利要求映射和产品验收",anchor="mm",fill=GOLD,font=font(21,True))
    save(im,"07-ip-and-roadmap.png")


def main():
    for fn in (platform, remote, agent, recognition, assessment, research, ip_roadmap):
        fn()
    print({"visuals": len(list(OUT.glob("*.png"))), "directory": str(OUT)})


if __name__ == "__main__":
    main()
