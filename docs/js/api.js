// Claude API 客户端 — 纯前端调用

const CLAUDE_API = "https://api.anthropic.com/v1/messages";
const MODEL = "claude-sonnet-4-20250514";

/**
 * 调用 Claude API
 * @param {string} systemPrompt
 * @param {string} userMessage
 * @param {string} apiKey
 * @param {string} [proxyUrl] - CORS 代理地址
 * @param {number} [maxTokens=8192]
 * @returns {Promise<string>}
 */
async function callClaude(systemPrompt, userMessage, apiKey, proxyUrl, maxTokens = 8192) {
    const url = proxyUrl ? proxyUrl.replace(/\/$/, "") + "/v1/messages" : CLAUDE_API;

    const headers = {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
    };

    const body = JSON.stringify({
        model: MODEL,
        max_tokens: maxTokens,
        system: systemPrompt,
        messages: [{ role: "user", content: userMessage }],
    });

    const resp = await fetch(url, { method: "POST", headers, body });

    if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        const msg = err?.error?.message || `API 请求失败 (${resp.status})`;
        throw new Error(msg);
    }

    const data = await resp.json();
    return data.content[0].text;
}

// Agent prompts（精简版，完整版在 agents/ 目录）
const PROMPTS = {
    analyze: (discipline) => `你是论文分析专家，负责对论文做全面扫描和风险评估。

学科类别：${discipline}

你的职责：
1. AI风险扫描 — 识别具有AI写作特征的段落
2. 查重风险扫描 — 识别可能触发查重系统的段落
3. 格式问题扫描 — 识别格式不规范之处

约束：
- 你只做分析，绝不修改论文任何内容
- 所有发现必须标注具体位置
- 风险等级必须给出依据

输出格式：
# 论文分析报告

## 风险概览
| 维度 | 高风险 | 中风险 | 低风险 |
|------|--------|--------|--------|
| AI检测 | N | N | N |
| 查重 | N | N | N |
| 格式 | N | N | N |

## 章节详情
（逐章分析）

## 优化建议
（按优先级排序）`,

    reduce_ai: () => `你是降AI检测专家，专门消除文本中的AI写作痕迹。

约束：
- 修改范围严格限制在单句内
- 绝不大段推翻重写
- 保留原始书写逻辑与思维跳跃
- 研究贡献、实验数据、公式、图表、引用文献、专业术语绝不修改

执行机制：
1. 句内重组 — 改变主谓宾顺序，保持语义不变
2. 同义微调 — 替换非核心词汇，保留专业术语
3. 语气调整 — 从客观陈述转向适度主观
4. 打破规整化 — 替换"首先其次最后"，插入长短句变化

输出要求：
- 输出修改后的完整论文文本
- 在末尾附上修订日志（表格形式：序号 | 原文 | 修改后 | 修改理由）`,

    plagiarism: (discipline, citation) => `你是学术降重专家，专门降低论文查重率。

学科：${discipline}，引用格式：${citation}

约束：
- 保持学术严谨性
- 不改变原文核心论点和数据
- 保留所有引用标注
- 仅改写高相似度段落

执行策略：
1. 同义替换 — 替换非专业词汇
2. 句式转换 — 主被动互换、长短句调整
3. 语序重组 — 调整句子成分顺序
4. 补充原创表述 — 增加个人分析和评论

输出要求：
- 输出修改后的完整论文文本
- 在末尾附上修订日志`,

    polish: (discipline) => `你是学术润色专家，专门提升论文的学术表达质量。

学科：${discipline}

润色方向：
1. 学术用词规范化
2. 句式多样化
3. 逻辑衔接自然化
4. 段落结构优化

约束：
- 不改变原文含义
- 不增删研究内容
- 保持作者的写作风格
- 仅优化表达方式

输出要求：
- 输出润色后的完整论文文本
- 在末尾附上修订日志`,

    format: (discipline) => `你是论文格式检查专家。

学科：${discipline}

检查项目：
1. 标题层级是否规范
2. 段落格式是否统一
3. 引用格式是否正确
4. 图表编号是否连续
5. 公式编号是否规范
6. 参考文献格式是否符合标准

输出格式：
# 格式检查报告

## 检查结果
| 检查项 | 状态 | 问题描述 |
|--------|------|----------|
（逐项列出）

## 修改建议
（按章节列出具体修改建议）`,

    evaluate: () => `你是论文评估专家，对优化后的论文进行综合评估。

评估维度：
1. AI检测率（0-100，越低越好）
2. 查重率预估（0-100，越低越好）
3. 学术表达（1-10分）
4. 格式规范（1-10分）
5. 内容完整性（1-10分）

输出格式：
# 评估报告

## 综合评分
| 维度 | 得分/预估 | 说明 |
|------|-----------|------|
| AI检测率 | XX% | ... |
| 查重率 | XX% | ... |
| 学术表达 | X/10 | ... |
| 格式规范 | X/10 | ... |
| 内容完整性 | X/10 | ... |
| **综合** | **XX/100** | ... |

## 优势
（列出优化后的改进点）

## 仍存在的问题
（列出需要进一步修改的地方）

## 改进建议
（给出具体建议）`,
};

/**
 * 拆分正文和修订日志
 */
function splitTextAndLog(result) {
    const markers = ["## 修订日志", "### 修订日志", "修订日志：", "---\n## 修订"];
    for (const marker of markers) {
        const idx = result.indexOf(marker);
        if (idx !== -1) {
            return [result.slice(0, idx).trim(), result.slice(idx).trim()];
        }
    }
    return [result.trim(), ""];
}

/**
 * 完整优化流水线
 */
async function runPipeline(thesisText, apiKey, proxyUrl, discipline, citation, onProgress) {
    const results = {};
    const logs = [];
    let currentText = thesisText;

    const progress = async (stage, pct, msg) => {
        if (onProgress) onProgress(stage, pct, msg);
    };

    // Stage 1: 分析
    await progress("analyze", 5, "正在分析论文...");
    results.analysis = await callClaude(PROMPTS.analyze(discipline),
        `请分析以下论文，学科类别：${discipline}，引用格式：${citation}\n\n---\n\n${currentText}`, apiKey, proxyUrl);
    await progress("analyze", 15, "分析完成");

    // Stage 2: 降AI
    await progress("reduce_ai", 20, "正在降低AI检测率...");
    const aiResult = await callClaude(PROMPTS.reduce_ai(),
        `请对以下论文执行降AI优化。学科：${discipline}\n\n分析报告：\n${results.analysis}\n\n---\n\n论文原文：\n${currentText}\n\n请输出修改后的完整论文文本，并在末尾附上修订日志。`, apiKey, proxyUrl, 16384);
    const [aiText, aiLog] = splitTextAndLog(aiResult);
    currentText = aiText;
    results.ai_reduction = currentText;
    if (aiLog) logs.push(["降AI", aiLog]);
    await progress("reduce_ai", 40, "降AI完成");

    // Stage 3: 降重
    await progress("reduce_plagiarism", 45, "正在降低查重率...");
    const plagResult = await callClaude(PROMPTS.plagiarism(discipline, citation),
        `请对以下论文执行降重优化。学科：${discipline}，引用格式：${citation}\n\n分析报告：\n${results.analysis}\n\n---\n\n论文文本：\n${currentText}\n\n请输出修改后的完整论文文本，并在末尾附上修订日志。`, apiKey, proxyUrl, 16384);
    const [plagText, plagLog] = splitTextAndLog(plagResult);
    currentText = plagText;
    results.plagiarism = currentText;
    if (plagLog) logs.push(["降重", plagLog]);
    await progress("reduce_plagiarism", 60, "降重完成");

    // Stage 4: 润色
    await progress("polish", 65, "正在润色...");
    const polishResult = await callClaude(PROMPTS.polish(discipline),
        `请对以下论文执行学术润色。学科：${discipline}\n\n---\n\n${currentText}\n\n请输出润色后的完整论文文本，并在末尾附上修订日志。`, apiKey, proxyUrl, 16384);
    const [polishText, polishLog] = splitTextAndLog(polishResult);
    currentText = polishText;
    results.polished = currentText;
    if (polishLog) logs.push(["润色", polishLog]);
    await progress("polish", 80, "润色完成");

    // Stage 5: 格式检查
    await progress("check_format", 82, "正在检查格式...");
    results.format_report = await callClaude(PROMPTS.format(discipline),
        `请检查以下论文的格式规范。学科：${discipline}，引用格式：${citation}\n\n---\n\n${currentText}\n\n请生成格式检查报告。`, apiKey, proxyUrl);
    await progress("check_format", 88, "格式检查完成");

    // Stage 6: 评估
    await progress("evaluate", 90, "正在生成评估报告...");
    results.evaluation = await callClaude(PROMPTS.evaluate(),
        `请对以下优化后的论文进行综合评估。学科：${discipline}\n\n优化前分析报告：\n${results.analysis}\n\n---\n\n优化后论文：\n${currentText}`, apiKey, proxyUrl);
    await progress("evaluate", 100, "全部完成");

    results.revision_logs = logs;
    return results;
}
