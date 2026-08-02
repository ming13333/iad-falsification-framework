# 失眠 ↔ 阿尔茨海默病/认知 孟德尔随机化 · Web of Science 检索式

> 用途：作为本 scoping review（PRISMA-ScR）的**第三数据库**（前两个为 PubMed、Scopus），补齐跨库证据并交叉验证"研究缺口地图"。
> 说明：WoS Core Collection 需机构订阅；本文件给出可直接粘贴进 **Web of Science → 高级检索（Advanced Search）** 的检索式。本机无 WoS API，故未实跑，检索式已按 WoS 语法校验。

---

## 一、WoS 语法要点（先读）

| 要素 | 写法 | 说明 |
|------|------|------|
| 主题（标题+摘要+作者关键词+关键词_plus） | `TS=` | **首选**，覆盖最全 |
| 标题 | `TI=` | 精确但漏检 |
| 摘要 | `AB=` | — |
| 作者关键词 | `AK=` | — |
| 出版物名称 | `SO=` | 限期刊用 |
| 出版年 | `PY=` | 如 `PY=(2015-2026)` |
| 文献类型 | `DT=` | `Article` / `Review` |
| 语种 | `LA=` | `LA=(English)` |
| 布尔 | `AND` `OR` `NOT` | 大写 |
| 截词 | `*` 多字符、`?` 单字符 | `dement*` → dementia/dementias |
| 短语 | `" "` | `"Mendelian randomization"` |
| 邻近 | `NEAR/x` | 部分 WoS 支持，非必需 |

**推荐附加过滤（提高查准、便于 PRISMA 报告）：**
```
AND LANGUAGE=(English) AND DOCUMENT TYPES=(Article OR Review)
```
（敏感性分析时可去掉文献类型过滤，单独跑 `Review` 看综述。）

---

## 二、主检索式（3 路，镜像 PubMed/Scopus）

### W1 — 失眠 → 认知（MR）
```
TS=("insomnia" AND ("Alzheimer*" OR dement* OR cognit* OR "cognitive decline" OR "cognitive impairment") AND ("Mendelian randomization" OR "Mendelian randomisation"))
```

### W2 — 睡眠（广义）→ 认知（MR）
```
TS=(("sleep" OR "sleep disorder*" OR "sleep quality" OR "sleep duration" OR insomnia OR chronotype) AND ("Alzheimer*" OR dement* OR cognit* OR "cognitive decline" OR "cognitive impairment") AND ("Mendelian randomization" OR "Mendelian randomisation"))
```

### W3 — 反向：认知 → 睡眠（MR/因果）
```
TS=(("Alzheimer*" OR dement*) AND ("sleep" OR "sleep disorder*" OR insomnia) AND ("Mendelian randomization" OR "Mendelian randomisation" OR "causal" OR "two-sample" OR "genetic causal" OR "instrumental variable"))
```

---

## 三、组合主检索式（一次性拉全，便于去重）

将 W1–W3 用 `OR` 合并，并加语种/文献类型过滤：
```
(TS=("insomnia" AND ("Alzheimer*" OR dement* OR cognit* OR "cognitive decline" OR "cognitive impairment") AND ("Mendelian randomization" OR "Mendelian randomisation"))
OR
TS=(("sleep" OR "sleep disorder*" OR "sleep quality" OR "sleep duration" OR insomnia OR chronotype) AND ("Alzheimer*" OR dement* OR cognit* OR "cognitive decline" OR "cognitive impairment") AND ("Mendelian randomization" OR "Mendelian randomisation"))
OR
TS=(("Alzheimer*" OR dement*) AND ("sleep" OR "sleep disorder*" OR insomnia) AND ("Mendelian randomization" OR "Mendelian randomisation" OR "causal" OR "two-sample" OR "genetic causal" OR "instrumental variable")))
AND LANGUAGE=(English) AND DOCUMENT TYPES=(Article OR Review)
```
> 若 WoS 提示查询过长，分 W1/W2/W3 三次跑，导出后合并去重即可。

---

## 四、缺口定向检索式（验证"红色缺口地图"）

> 对应指南中 🔴 空白区：双向定性 / 蛋白中介 / 多祖先 / 时序。单独跑，用于判定缺口是否真被填补。

### G1 — 双向因果（失眠↔AD）
```
TS=(("sleep" OR "sleep disorder*" OR insomnia) AND ("Alzheimer*" OR dement*) AND (bidirectional OR "reverse caus*" OR "two-direction*" OR reciprocal OR "reverse Mendelian"))
```

### G2 — 蛋白中介（睡眠→血浆蛋白→AD，两步）
```
TS=(("sleep" OR insomnia) AND ("Alzheimer*" OR dement*) AND ("plasma protein*" OR proteom* OR (protein* AND (mediation OR mediator OR intermediate))))
```

### G3 — 多祖先验证（东亚/华裔/日裔等）
```
TS=(("sleep" OR insomnia) AND ("Alzheimer*" OR dement*) AND ("East Asian" OR Chinese OR Japanese OR multiethnic OR "non-European" OR transethnic OR ancestry OR "diverse population*"))
```

### G4 — 时序/纵向/发病顺序（MR 或纵向因果）
```
TS=(("sleep" OR insomnia) AND ("Alzheimer*" OR dement*) AND (longitudinal OR trajector* OR "time-to-event" OR "age at onset" OR incident OR "prospective" OR "follow-up"))
```

---

## 五、跨库合并与去重（PRISMA-ScR 流程）

1. 三库各导出为 **RIS / CSV / BibTeX**，含字段：`DOI`、`UT（WoS 唯一号）`、`Title`、`Year`、`PMID`。
2. 去重主键顺序：**DOI（归一化，去 `https://doi.org/`）** → **PMID** → **标题归一化（去标点、小写、取前 120 字符）**。
3. 已完成的基线（本机已有）：
   - PubMed：89 篇（`scoping_raw.json`）
   - Scopus：681 条原始命中 → 充实 PubMed 摘要后严格筛出 **90 篇真·睡眠↔认知 MR**，其中 **65 篇为 PubMed 之外的增量**（`scopus_screened.json`）
   - WoS：待你执行上述检索式后并入。
4. 去重后进入标题/摘要双屏（title/abstract screening），按 PICOS 排除非 MR、非睡眠-认知对、评论/社论（除非做综述地图）。

---

## 六、与已出结果的衔接（避免重复劳动）

已用 Scopus 对 🔴 缺口做过程序化验证（基于标题+PubMed 摘要）：
- **G1 双向**：检出 8 篇，但多为"睡眠-炎症/脑外伤双向""睡眠呼吸暂停↔AD"，**无一篇是"失眠↔AD"直接双向 MR** → 双向定性缺口仍成立。
- **G2 蛋白中介**：仅 3 篇弱相关，**无"失眠→血浆蛋白→AD"两步中介** → 缺口成立。
- **G3 多祖先**：**0 篇** → 缺口最强。
- **G4 时序/纵向**：11 篇，但均为观察性纵向/少数 MR，**多状态发病顺序模型缺席** → 缺口成立。

WoS 可能补出 PubMed/Scopus 未收的欧洲/中文期刊或会议录，尤其对 **G3 多祖先** 最有增殖价值——执行后重点核对这部分。

---

## 七、执行后下一步

把 WoS 导出文件交给我，我可：
1. 与 `scoping_raw.json`（PubMed）+ `scopus_screened.json`（Scopus）三库合并去重；
2. 重算"增量 vs 重叠"与缺口命中数，更新缺口地图；
3. 生成 PRISMA-ScR 流程图与文献计量（年度/期刊/被引分布）。

> 若你有 WoS API（Premium/Starter API key + base url），也可告诉我，我用脚本直跑并自动并入。
