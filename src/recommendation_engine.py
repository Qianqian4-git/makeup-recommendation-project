import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到 sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 仅保留 TARGET_ATTRS（用于测试，实际函数未直接使用，但保留无妨）
from src.config import TARGET_ATTRS

load_dotenv()

# ==================== 特征描述词库 ====================
FEATURE_DESC = {
    'Oval_Face': '标准的鹅蛋脸',
    'Chubby': '饱满的圆脸',
    'High_Cheekbones': '立体的高颧骨',
    'Double_Chin': '圆润的下巴',
    'Narrow_Eyes': '细长的丹凤眼',
    'Arched_Eyebrows': '柔和的弯眉',
    'Bushy_Eyebrows': '英气的浓眉',
    'Big_Nose': '挺阔的鼻梁',
    'Pointy_Nose': '精致的尖鼻',
    'Big_Lips': '饱满的唇形',
    'Mouth_Slightly_Open': '微启的唇部',
    'Pale_Skin': '白皙的肤色',
    'Young': '年轻有活力的状态'
}

# ==================== 妆容印象词库 ====================
IMPRESSION = {
    '韩系水光妆': '清透温柔',
    '日系元气妆': '甜美可爱',
    '亚裔混血妆': '立体高级',
    '职场通勤妆': '干练专业',
    '千金妆': '贵气优雅',
    '新中式妆': '古典韵味',
    '轻泰妆': '明艳大气',
    '美式慵懒雀斑妆': '随性高级',
    '韩系欧巴妆': '清爽干净',
    '硬朗轮廓妆': '硬朗有型',
    '自然净澈妆': '自然清爽',
    '日系盐系妆': '清冷少年'
}

# ==================== 核心推荐函数 ====================
def recommend_makeup(attributes):
    """
    输入: 14个属性的预测值 (0或1的列表，顺序与 config.TARGET_ATTRS 一致)
    输出: 推荐妆容名称 + 推荐理由（含特征描述）
    """
    # 解包属性
    (male, oval_face, chubby, high_cheekbones, double_chin,
     narrow_eyes, arched_eyebrows, bushy_eyebrows,
     big_nose, pointy_nose, big_lips, mouth_open,
     pale_skin, young) = attributes

    # 1. 构建用户面部特征描述
    detected_features = []
    if oval_face: detected_features.append(FEATURE_DESC['Oval_Face'])
    if chubby: detected_features.append(FEATURE_DESC['Chubby'])
    if high_cheekbones: detected_features.append(FEATURE_DESC['High_Cheekbones'])
    if double_chin: detected_features.append(FEATURE_DESC['Double_Chin'])
    if narrow_eyes: detected_features.append(FEATURE_DESC['Narrow_Eyes'])
    if arched_eyebrows: detected_features.append(FEATURE_DESC['Arched_Eyebrows'])
    if bushy_eyebrows: detected_features.append(FEATURE_DESC['Bushy_Eyebrows'])
    if big_nose: detected_features.append(FEATURE_DESC['Big_Nose'])
    if pointy_nose: detected_features.append(FEATURE_DESC['Pointy_Nose'])
    if big_lips: detected_features.append(FEATURE_DESC['Big_Lips'])
    if mouth_open: detected_features.append(FEATURE_DESC['Mouth_Slightly_Open'])
    if pale_skin: detected_features.append(FEATURE_DESC['Pale_Skin'])
    if young: detected_features.append(FEATURE_DESC['Young'])

    if not detected_features:
        detected_features = ["匀称的五官"]
    desc_str = "、".join(detected_features)

    # 2. 根据属性组合选择妆容
    if male == 1:  # 男性
        if narrow_eyes == 1 or bushy_eyebrows == 1:
            makeup = "韩系欧巴妆"
            core = "清透底妆和干净的眉形"
            effect = "突出清爽的少年感"
        elif high_cheekbones == 1 and oval_face == 0:
            makeup = "硬朗轮廓妆"
            core = "立体修容和利落线条"
            effect = "强化骨相的硬朗特质"
        elif chubby == 1:
            makeup = "自然净澈妆"
            core = "轻遮瑕和自然肤色"
            effect = "减少油腻感，提升清爽度"
        elif young == 1:
            makeup = "日系盐系妆"
            core = "轻薄底妆和清透质感"
            effect = "打造清冷少年的氛围感"
        elif pale_skin == 1:
            makeup = "韩系欧巴妆"
            core = "水光感和干净眉形"
            effect = "突出白皙皮肤的清透优势"
        else:
            makeup = "职场干练妆"
            core = "哑光底妆和利落眉形"
            effect = "塑造干练专业的形象"
    else:  # 女性
        if pale_skin == 1 and (oval_face == 1 or arched_eyebrows == 1):
            makeup = "韩系水光妆"
            core = "水光肌底妆和渐变咬唇"
            effect = "放大清透温柔的气质"
        elif chubby == 1 or (high_cheekbones == 1 and young == 1):
            makeup = "日系元气妆"
            core = "大面积腮红和明亮色彩"
            effect = "提升面部的饱满度和元气感"
        elif high_cheekbones == 1 and (big_lips == 1 or pointy_nose == 1):
            makeup = "亚裔混血妆"
            core = "立体修容和高光提亮"
            effect = "强化骨相的立体优势"
        elif bushy_eyebrows == 1 and big_lips == 1:
            makeup = "千金妆"
            core = "精致的眉眼和饱满唇色"
            effect = "凸显贵气与优雅"
        elif high_cheekbones == 1 and pointy_nose == 1:
            makeup = "轻泰妆"
            core = "浓颜系眉眼和高光"
            effect = "打造明艳大气的混血感"
        elif arched_eyebrows == 1 and (oval_face == 1 or narrow_eyes == 1):
            makeup = "新中式妆"
            core = "古典眉形和朱唇"
            effect = "营造东方古典韵味"
        elif pale_skin == 1 and big_lips == 1:
            makeup = "美式慵懒雀斑妆"
            core = "质感底妆和自然雀斑"
            effect = "营造随性高级的氛围"
        elif oval_face == 1 or narrow_eyes == 1:
            makeup = "职场通勤妆"
            core = "哑光底妆和大地色眼影"
            effect = "突出干练专业的气质"
        else:
            makeup = "自然裸妆"
            core = "轻薄底妆和自然色彩"
            effect = "放大天生好皮肤的优势"

    impression = IMPRESSION.get(makeup, "独特")
    reason = (
        f"根据您的面部特征分析：您拥有{desc_str}。"
        f"整体给人一种{impression}的感觉。"
        f"因此，我为您推荐【{makeup}】。"
        f"这个妆容的核心是{core}，能够很好地{effect}，"
        f"打造出{impression}的效果。"
    )
    return makeup, reason

# ==================== 测试入口 ====================
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("💄 妆容推荐引擎测试")
    print("=" * 60)

    # 测试用例：男性，单眼皮，浓眉
    test_attrs_1 = [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
    name, reason = recommend_makeup(test_attrs_1)
    print(f"\n👤 男性, 单眼皮, 浓眉")
    print(f"💄 推荐妆容: {name}")
    print(f"📝 推荐理由: {reason}")

    # 测试用例：女性，白皮，鹅蛋脸，弯眉，年轻
    test_attrs_2 = [-1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1]
    name, reason = recommend_makeup(test_attrs_2)
    print(f"\n👤 女性, 白皮, 鹅蛋脸, 弯眉, 年轻")
    print(f"💄 推荐妆容: {name}")
    print(f"📝 推荐理由: {reason}")

    # 测试用例：女性，高颧骨，厚唇，尖鼻
    test_attrs_3 = [-1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
    name, reason = recommend_makeup(test_attrs_3)
    print(f"\n👤 女性, 高颧骨, 厚唇, 尖鼻")
    print(f"💄 推荐妆容: {name}")
    print(f"📝 推荐理由: {reason}")