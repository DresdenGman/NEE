# 图像生成提示词 (Image Generation Prompts)

本文档包含三张关键科研图表的详细提示词，用于 AI 图像生成工具（如 DALL-E, Midjourney, Stable Diffusion）生成高质量的科研可视化图像。

---

## 1. 意大利面图 (Spaghetti Plot) - `fig_spaghetti.png`

### 提示词 (Prompt):

```
A scientific line graph visualization showing multiple overlapping stochastic trajectories, 
depicting cognitive state evolution over time. The image shows:

- **Background**: Clean white background with subtle grid lines
- **Main Content**: 30-50 semi-transparent blue lines (alpha=0.25) representing individual 
  stochastic differential equation (SDE) paths, all starting from B=1.0 at t=0
- **Trajectory Behavior**: 
  * Most paths show gradual decline with random fluctuations
  * Some paths drop sharply toward zero (representing cognitive collapse)
  * Paths exhibit natural variation and stochastic noise
- **Key Elements**:
  * Horizontal dashed gray line at y=0.1 labeled "崩溃阈值" (collapse threshold)
  * X-axis: "Time" (0 to 100)
  * Y-axis: "B (认知状态)" (0 to 1.2)
  * Title: "SDE Paths (showing N paths)"
- **Style**: 
  * Publication-quality scientific plot
  * Minimalist design with clear axis labels
  * Professional color scheme (steel blue for paths, gray for threshold)
  * High resolution (300 DPI)
  * Clean typography, sans-serif font
```

### 中文提示词 (Chinese Prompt):

```
科学线图可视化，展示多条重叠的随机轨迹，描述认知状态随时间演化。

- **背景**：干净的白色背景，带细微网格线
- **主要内容**：30-50 条半透明蓝色线条（透明度 0.25），代表单个随机微分方程路径，均从 t=0 时的 B=1.0 开始
- **轨迹行为**：
  * 大多数路径显示逐渐下降并带有随机波动
  * 部分路径急剧下降至零（代表认知崩溃）
  * 路径呈现自然变化和随机噪声
- **关键元素**：
  * 在 y=0.1 处的水平灰色虚线，标注"崩溃阈值"
  * X 轴："Time"（0 到 100）
  * Y 轴："B (认知状态)"（0 到 1.2）
  * 标题："SDE Paths (showing N paths)"
- **风格**：
  * 发表级科学图表
  * 极简设计，清晰的坐标轴标签
  * 专业配色（钢蓝色路径，灰色阈值线）
  * 高分辨率（300 DPI）
  * 清晰的字体，无衬线字体
```

---

## 2. 势能景观图 (Potential Landscape) - `fig_potential.png`

### 提示词 (Prompt):

```
A scientific line graph showing potential energy landscape curves for a cognitive system 
under different algorithmic attack intensities. The image displays:

- **Background**: White background with subtle grid
- **Main Content**: Four distinct smooth curves representing potential energy V(B) vs. 
  cognitive state B, each labeled with different alpha values (α=0.1, 0.5, 1.0, 2.0)
- **Curve Characteristics**:
  * α=0.1: Deep potential well (stable state) at moderate B values
  * α=0.5: Shallower well, showing reduced stability
  * α=1.0: Very shallow or flat well, near critical transition
  * α=2.0: Inverted or nearly flat curve, representing system collapse
- **Visual Progression**: The curves show a clear transition from deep wells (bistability) 
  to flat landscapes (monostability/collapse) as alpha increases
- **Key Elements**:
  * X-axis: "B" (0.0 to 1.2)
  * Y-axis: "Potential V(B)" (negative values at bottom, positive at top, or vice versa)
  * Title: "Potential Landscape under Different α"
  * Legend showing four alpha values with distinct colors
- **Style**:
  * Clean scientific visualization
  * Smooth, continuous curves
  * Color-coded legend (e.g., blue, green, orange, red for increasing alpha)
  * Professional typography
  * Grid lines for reference
  * High resolution (300 DPI)
```

### 中文提示词 (Chinese Prompt):

```
科学线图，展示不同算法攻击强度下认知系统的势能景观曲线。

- **背景**：白色背景，带细微网格
- **主要内容**：四条不同的平滑曲线，表示势能 V(B) 随认知状态 B 的变化，每条曲线标注不同的 alpha 值（α=0.1, 0.5, 1.0, 2.0）
- **曲线特征**：
  * α=0.1：在中等 B 值处有深势阱（稳定态）
  * α=0.5：较浅的势阱，稳定性降低
  * α=1.0：非常浅或平坦的势阱，接近临界转变
  * α=2.0：倒置或几乎平坦的曲线，代表系统崩溃
- **视觉进展**：曲线清晰显示从深阱（双稳态）到平坦景观（单稳态/崩溃）的转变，随 alpha 增加
- **关键元素**：
  * X 轴："B"（0.0 到 1.2）
  * Y 轴："Potential V(B)"（底部为负值，顶部为正值，或相反）
  * 标题："Potential Landscape under Different α"
  * 图例显示四个 alpha 值，使用不同颜色
- **风格**：
  * 干净的科学可视化
  * 平滑、连续的曲线
  * 颜色编码图例（例如，蓝色、绿色、橙色、红色对应递增的 alpha）
  * 专业字体
  * 参考网格线
  * 高分辨率（300 DPI）
```

---

## 3. Lyapunov 指数图 (Lyapunov Exponent Plot) - `fig_lyapunov.png`

### 提示词 (Prompt):

```
A scientific line graph showing Lyapunov exponent (λ) as a function of algorithmic 
attack intensity (α), with a critical transition point marked. The image contains:

- **Background**: White background with subtle grid
- **Main Content**: 
  * A smooth purple/violet curve showing λ(α) relationship
  * The curve starts negative (stable region) and crosses zero at a critical point
  * After crossing zero, the curve becomes positive (unstable/chaotic region)
- **Key Elements**:
  * Horizontal dashed gray line at λ=0 (stability threshold)
  * Red scatter point marking the critical transition (where λ≈0)
  * X-axis: "α (算法强度)" (0.05 to 3.0)
  * Y-axis: "λ (Lyapunov)" (negative values at bottom, positive at top)
  * Title: "Lyapunov Exponent vs. α"
  * Legend showing "Lyapunov λ", "λ = 0", and "cross ~ α*" (critical point)
- **Visual Characteristics**:
  * Smooth, continuous curve with slight curvature
  * Clear transition from negative to positive values
  * Critical point prominently marked with red dot
  * Professional color scheme (purple/violet for main curve, gray for threshold, red for critical point)
- **Style**:
  * Publication-quality scientific plot
  * Clean, minimalist design
  * Clear axis labels and legend
  * Grid lines for reference
  * High resolution (300 DPI)
  * Professional typography
```

### 中文提示词 (Chinese Prompt):

```
科学线图，展示 Lyapunov 指数（λ）随算法攻击强度（α）的变化，并标记临界转变点。

- **背景**：白色背景，带细微网格
- **主要内容**：
  * 一条平滑的紫色/紫罗兰色曲线，显示 λ(α) 关系
  * 曲线从负值开始（稳定区域），在临界点处穿过零
  * 穿过零后，曲线变为正值（不稳定/混沌区域）
- **关键元素**：
  * 在 λ=0 处的水平灰色虚线（稳定性阈值）
  * 红色散点标记临界转变点（λ≈0 处）
  * X 轴："α (算法强度)"（0.05 到 3.0）
  * Y 轴："λ (Lyapunov)"（底部为负值，顶部为正值）
  * 标题："Lyapunov Exponent vs. α"
  * 图例显示 "Lyapunov λ"、"λ = 0" 和 "cross ~ α*"（临界点）
- **视觉特征**：
  * 平滑、连续的曲线，带有轻微弯曲
  * 从负值到正值的清晰转变
  * 临界点用红点突出标记
  * 专业配色（紫色/紫罗兰色主曲线，灰色阈值线，红色临界点）
- **风格**：
  * 发表级科学图表
  * 干净、极简设计
  * 清晰的坐标轴标签和图例
  * 参考网格线
  * 高分辨率（300 DPI）
  * 专业字体
```

---

## 4. 熵分布对比图 (Entropy Distribution Comparison) - `fig_entropy.png`

### 提示词 (Prompt):

```
A scientific density plot (KDE) showing the comparison of Shannon entropy distributions 
between two text corpora. The image displays:

- **Background**: Clean white background with subtle grid
- **Main Content**: Two overlapping density curves (KDE plots) with filled areas:
  * Green curve (left side, higher peak): "Literature (High B)" - representing high cognitive 
    bandwidth text samples
  * Red curve (right side, slightly shifted): "Social Media (Low B)" - representing low 
    cognitive bandwidth text samples
- **Key Elements**:
  * Two vertical dashed lines marking the mean entropy for each group:
    - Green dashed line: Mean of Literature distribution
    - Red dashed line: Mean of Twitter/Social Media distribution
  * X-axis: "Shannon Entropy (Bits)" (typically range 3.5 to 6.0)
  * Y-axis: "Density" (normalized probability density)
  * Title: "Neuro-Entropic Evidence: Text Entropy at Fixed Length (N=40)"
  * Legend showing both distributions with distinct colors
- **Visual Characteristics**:
  * Smooth, bell-shaped density curves
  * Green distribution slightly left-shifted (lower mean entropy)
  * Red distribution slightly right-shifted (higher mean entropy)
  * Overlapping region in the middle showing common entropy values
  * Professional color scheme: green (#2ecc71) and red (#e74c3c)
- **Style**:
  * Publication-quality scientific visualization
  * Clean, minimalist design
  * Clear axis labels and legend
  * Grid lines for reference
  * High resolution (300 DPI)
  * Professional typography
```

### 中文提示词 (Chinese Prompt):

```
科学密度图（KDE），展示两个文本语料库的香农熵分布对比。

- **背景**：干净的白色背景，带细微网格
- **主要内容**：两条重叠的密度曲线（KDE 图），带填充区域：
  * 绿色曲线（左侧，峰值较高）："Literature (High B)" - 代表高认知带宽文本样本
  * 红色曲线（右侧，略微偏移）："Social Media (Low B)" - 代表低认知带宽文本样本
- **关键元素**：
  * 两条垂直虚线标记每组平均熵：
    - 绿色虚线：文学分布的平均值
    - 红色虚线：Twitter/社交媒体分布的平均值
  * X 轴："Shannon Entropy (Bits)"（通常范围 3.5 到 6.0）
  * Y 轴："Density"（归一化概率密度）
  * 标题："Neuro-Entropic Evidence: Text Entropy at Fixed Length (N=40)"
  * 图例显示两种分布，使用不同颜色
- **视觉特征**：
  * 平滑、钟形密度曲线
  * 绿色分布略微左移（较低平均熵）
  * 红色分布略微右移（较高平均熵）
  * 中间重叠区域显示共同熵值
  * 专业配色：绿色（#2ecc71）和红色（#e74c3c）
- **风格**：
  * 发表级科学可视化
  * 干净、极简设计
  * 清晰的坐标轴标签和图例
  * 参考网格线
  * 高分辨率（300 DPI）
  * 专业字体
```

---

## 5. Zipf 定律分析图 (Zipf's Law Analysis) - `fig_zipf.png`

### 提示词 (Prompt):

```
A scientific two-panel figure showing Zipf's law analysis for two text corpora. The image contains:

**Panel 1 (Top): Log-Log Zipf Distribution**
- **Background**: White with subtle grid
- **Main Content**: Two smooth curves on a double logarithmic (log-log) scale:
  * Green curve: "Literature" - showing word frequency vs. rank for literary texts
  * Red curve: "Twitter" - showing word frequency vs. rank for social media texts
- **Key Elements**:
  * X-axis: "Word Rank (log scale)" (typically 1 to 10,000+)
  * Y-axis: "Frequency (log scale)" (typically 1 to 100,000+)
  * Both axes use logarithmic scale (powers of 10)
  * Title: "The Signature of Cognitive Structure: Zipf's Law Analysis"
  * Legend showing both curves with slope values (e.g., Slope=-1.00, R²=0.996)
  * Both curves should appear as nearly straight lines (characteristic of Zipf's law)
- **Visual Characteristics**:
  * Green and red lines with moderate transparency (alpha=0.8)
  * Lines should be smooth and continuous
  * Both curves follow a power-law distribution (straight line on log-log plot)
  * Slight differences in slope or curvature may be visible

**Panel 2 (Bottom): Top 10 High-Frequency Words Bar Chart**
- **Background**: White with subtle grid
- **Main Content**: Side-by-side bar chart comparing top 10 words:
  * Green bars: Literature word frequencies
  * Red bars: Twitter word frequencies
  * Words on X-axis (e.g., "the", "of", "and", "in", "to", etc.)
- **Key Elements**:
  * X-axis: "Top 10 Words" (word labels, rotated 45 degrees)
  * Y-axis: "Frequency" (linear scale)
  * Title: "Top 10 High-Frequency Words Comparison"
  * Legend distinguishing Literature vs. Twitter
- **Style**:
  * Publication-quality scientific visualization
  * Clean, professional design
  * Consistent color scheme (green for Literature, red for Twitter)
  * High resolution (300 DPI)
  * Clear typography and labels
```

### 中文提示词 (Chinese Prompt):

```
科学双面板图，展示两个文本语料库的 Zipf 定律分析。

**面板 1（顶部）：双对数 Zipf 分布**
- **背景**：白色，带细微网格
- **主要内容**：双对数（log-log）坐标上的两条平滑曲线：
  * 绿色曲线："Literature" - 显示文学文本的词频 vs. 排名
  * 红色曲线："Twitter" - 显示社交媒体文本的词频 vs. 排名
- **关键元素**：
  * X 轴："Word Rank (log scale)"（通常 1 到 10,000+）
  * Y 轴："Frequency (log scale)"（通常 1 到 100,000+）
  * 两个坐标轴都使用对数刻度（10 的幂次）
  * 标题："The Signature of Cognitive Structure: Zipf's Law Analysis"
  * 图例显示两条曲线及其斜率值（例如，Slope=-1.00, R²=0.996）
  * 两条曲线应呈现为近似直线（Zipf 定律的特征）
- **视觉特征**：
  * 绿色和红色线条，中等透明度（alpha=0.8）
  * 线条应平滑连续
  * 两条曲线都遵循幂律分布（在 log-log 图上为直线）
  * 斜率或曲率的细微差异可能可见

**面板 2（底部）：Top 10 高频词条形图**
- **背景**：白色，带细微网格
- **主要内容**：并排条形图对比前 10 个词：
  * 绿色条形：文学词频
  * 红色条形：Twitter 词频
  * X 轴上的词（例如，"the", "of", "and", "in", "to" 等）
- **关键元素**：
  * X 轴："Top 10 Words"（词标签，旋转 45 度）
  * Y 轴："Frequency"（线性刻度）
  * 标题："Top 10 High-Frequency Words Comparison"
  * 图例区分 Literature 和 Twitter
- **风格**：
  * 发表级科学可视化
  * 干净、专业设计
  * 一致的配色方案（绿色代表 Literature，红色代表 Twitter）
  * 高分辨率（300 DPI）
  * 清晰的字体和标签
```

---

## 使用说明 (Usage Instructions)

1. **运行脚本生成原始图片**：
   ```bash
   # 生成所有图片（推荐）
   python generate_all_figures.py
   
   # 或单独生成
   python stochastic_simulation.py      # 意大利面图
   python stability_analysis.py         # 势能图和 Lyapunov 图
   python data_calibration_v3.py        # 熵分布图
   python structural_analysis.py        # Zipf 图
   ```

2. **图片将自动保存为**：
   - `fig_spaghetti.png`
   - `fig_potential.png`
   - `fig_lyapunov.png`
   - `fig_entropy.png`
   - `fig_zipf.png`

3. **使用 AI 生成工具**：
   - 将上述提示词复制到 DALL-E、Midjourney 或 Stable Diffusion
   - 调整参数以获得最佳效果
   - 对比 AI 生成版本与 Python 生成版本，选择更优者

4. **优化建议**：
   - 如果 AI 生成的图片风格不符合科研论文要求，可以添加 "scientific publication style" 或 "Nature/Science journal style"
   - 对于更精确的数值标注，可以在提示词中明确指定坐标轴范围和数值

---

## 技术规格 (Technical Specifications)

- **分辨率**: 300 DPI（适合打印和发表）
- **格式**: PNG（支持透明背景，如需要）
- **尺寸**: 
  - 意大利面图: 10×6 英寸
  - 势能图: 8×6 英寸
  - Lyapunov 图: 8×5 英寸
  - 熵分布图: 10×6 英寸
  - Zipf 图: 12×8 英寸（双面板）
- **字体**: Sans-serif（Arial 或 DejaVu Sans）
- **配色**: 专业科研配色方案（避免过于鲜艳的颜色）

