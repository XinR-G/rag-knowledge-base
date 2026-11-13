# Day 15 PDF 解析质量记录

- 工具：Unstructured 0.27.37，`partition_pdf`
- 日期：2026-11-13

## 文件 1：attention_is_all_you_need.pdf

- 页数：15
- 解析耗时：6.74 秒
- 元素总数：393
- 元素类型：Title 156、NarrativeText 144、UncategorizedText 67、Footer 15、ListItem 11

### 正文完整性
正文段落基本完整，Abstract、Introduction、Model Architecture 等大段文字可读。

### 公式处理
**失败**。`Attention(Q,K,V) = softmax(QK^T/√d_k)V` 被拆成多行碎片：
- `Attention(Q,K,V ) = softmax(` 单独一行
- `QKT √ dk` 单独一行
- `√` 单独一行

公式结构丢失，无法直接还原成 LaTeX 或可读形式。

### 表格保留情况
**部分失败**。Table 1 的表头（Layer Type、Self-Attention、Recurrent 等）和数值被保留，但变成线性列表，行列对应关系丢失。Table 2 同理，BLEU 分数和模型名混在一起，无法直接判断哪个分数属于哪个模型。

### 页眉/水印
**失败**。arXiv 左侧竖排水印被解析成乱码，例如 `3 2 0 2`、`g u A 2`、`] L C . s c [`。

### 主要失效模式
1. 公式被打碎成多行，数学结构丢失。
2. 表格退化为线性文本，行列关系丢失。
3. 页眉水印变成乱码，污染正文。
4. Title 数量偏高（156），作者名、邮箱、页码、短行被误判为标题。

## 文件 2：bert_paper.pdf

- 页数：16
- 解析耗时：2.16 秒
- 元素总数：654
- 元素类型：Title 271、NarrativeText 197、UncategorizedText 153、ListItem 33

### 正文完整性
正文段落基本完整，Abstract、Introduction、Model 等大段文字可读。

### 公式处理
未逐条核对，初步观察与 attention 论文类似，公式有碎片化风险。

### 表格保留情况
未逐条核对，初步观察与 attention 论文类似，表格结构有退化风险。

### 主要失效模式
1. Title 数量明显偏高（271），大量短行被误判为标题。
2. UncategorizedText 偏多（153），说明部分内容无法归类，可能是公式、表格碎片或页眉页脚。
3. 与 attention 论文类似，表格和公式结构有退化风险。

## 初步结论

- 两份论文的**纯正文段落解析基本可用**，适合直接进入切分和检索。
- **公式和表格是明确短板**：公式被打碎、表格行列关系丢失，这两类内容进入 RAG 后会导致检索不准或回答错误。
- **页眉水印和 Title 误判**会产生噪声 chunk，需要在切分或清洗阶段过滤。
- 对后续 RAG 的影响：如果评测集里包含公式或表格类问题，纯 Unstructured 解析的基线会明显偏低；这也为项目二“用 VLM 解析表格/公式”提供了动机。