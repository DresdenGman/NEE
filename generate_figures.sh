#!/bin/bash
# 生成三张关键科研图片的脚本

echo "正在生成科研图片..."
echo ""

# 设置 matplotlib 后端为非交互式（避免显示窗口）
export MPLBACKEND=Agg

# 1. 生成意大利面图
echo "1/3 生成意大利面图 (fig_spaghetti.png)..."
cd /Users/a24300/Documents/NEE
./.venv/bin/python -c "
from stochastic_simulation import *
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt

time, B_paths, collapsed_count, collapse_time = run_sde_simulation(
    alpha=1.5, sigma=0.08, T=50, dt=0.02, simulations=500,
    r=0.8, theta=0.3, attack_coeff=0.5, crash_threshold=0.1, seed=123
)
plot_spaghetti(time, B_paths, crash_threshold=0.1, max_paths=60, save_path='fig_spaghetti.png')
print('✓ fig_spaghetti.png 已生成')
"

# 2. 生成势能图和 Lyapunov 图
echo "2/3 生成势能景观图 (fig_potential.png)..."
./.venv/bin/python -c "
from stability_analysis import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plot_potential_landscape(save_path='fig_potential.png')
print('✓ fig_potential.png 已生成')
"

echo "3/3 生成 Lyapunov 指数图 (fig_lyapunov.png)..."
./.venv/bin/python -c "
from stability_analysis import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plot_lyapunov_curve(save_path='fig_lyapunov.png')
print('✓ fig_lyapunov.png 已生成')
"

echo ""
echo "所有图片已生成完成！"
echo "文件位置："
echo "  - fig_spaghetti.png"
echo "  - fig_potential.png"
echo "  - fig_lyapunov.png"

