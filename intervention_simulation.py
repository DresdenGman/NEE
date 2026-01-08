import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'font.size': 12,
    'axes.linewidth': 1.5,
    'axes.titlesize': 14,
    'axes.labelsize': 13,
    'xtick.major.width': 1.5,
    'ytick.major.width': 1.5,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'legend.frameon': False,
    'lines.linewidth': 2.0,
    'figure.dpi': 300
})


def run_simulation():
    # Simulates cognitive collapse and recovery through intervention
    T = 100
    dt = 0.01
    steps = int(T / dt)
    time = np.linspace(0, T, steps)
    
    B = np.zeros(steps)
    B[0] = 1.0
    
    intervention_t = 40
    
    alpha_crisis = 0.8
    sigma_crisis = 0.45
    
    sigma_fixed = 0.15
    music_amp = 0.08
    music_freq = 0.5
    
    np.random.seed(42)
    
    control_signal = np.zeros(steps)

    for i in range(1, steps):
        if time[i] < intervention_t:
            curr_alpha = alpha_crisis
            curr_sigma = sigma_crisis
            u_t = 0
        else:
            curr_alpha = alpha_crisis
            curr_sigma = sigma_fixed
            u_t = music_amp * (np.sin(music_freq * time[i]) + 1) / 2
            
        control_signal[i] = u_t
        
        r = 0.5
        drift = r * B[i-1] * (1 - B[i-1]) - curr_alpha * B[i-1] + u_t
        diffusion = curr_sigma * B[i-1] * np.random.normal(0, np.sqrt(dt))
        
        B[i] = B[i-1] + drift * dt + diffusion
        
        if B[i] < 0.01: 
            B[i] = 0.01 

    return time, B, intervention_t, control_signal


def run_control_simulation():
    T = 100
    dt = 0.01
    steps = int(T / dt)
    time = np.linspace(0, T, steps)
    
    B = np.zeros(steps)
    B[0] = 1.0
    
    alpha_crisis = 0.8
    sigma_crisis = 0.45
    
    np.random.seed(42)
    
    for i in range(1, steps):
        r = 0.5
        drift = r * B[i-1] * (1 - B[i-1]) - alpha_crisis * B[i-1]
        diffusion = sigma_crisis * B[i-1] * np.random.normal(0, np.sqrt(dt))
        
        B[i] = B[i-1] + drift * dt + diffusion
        
        if B[i] < 0.01: 
            B[i] = 0.01 
    
    return time, B


def main():
    print("Running Intervention Simulation...")
    print("=" * 50)
    
    t, B_intervention, t_int, signal = run_simulation()
    t_control, B_control = run_control_simulation()
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.axvspan(0, t_int, color='#e74c3c', alpha=0.08, label='Algorithmic Overload')
    ax.axvspan(t_int, 100, color='#2ecc71', alpha=0.08, label='Negentropic Intervention')
    
    ax.plot(t_control, B_control, color='#95a5a6', linestyle='--', 
            linewidth=2, alpha=0.7, label='No Intervention (Control)')
    
    ax.plot(t, B_intervention, color='#2c3e50', alpha=0.9, 
            linewidth=2.5, label='Cognitive State $B(t)$ (With Intervention)')
    
    intervention_mask = t >= t_int
    ax.plot(t[intervention_mask], signal[intervention_mask] * 2, 
            color='#e67e22', linestyle=':', alpha=0.6, 
            linewidth=1.5, label='Structured Resonance $u(t)$')
    
    ax.axvline(x=t_int, color='#7f8c8d', linestyle='--', linewidth=1.5)
    ax.text(t_int + 2, 0.95, 'Technology + Art\nActivated', 
            fontsize=11, fontweight='bold', color='#27ae60',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
    
    pre_intervention_mask = t < t_int
    if np.any(pre_intervention_mask):
        min_idx_pre = np.argmin(B_intervention[pre_intervention_mask])
        min_t_pre = t[pre_intervention_mask][min_idx_pre]
        min_val_pre = B_intervention[pre_intervention_mask][min_idx_pre]
        
        ax.annotate('Cognitive Collapse\n(Risk Zone)', 
                   xy=(min_t_pre, min_val_pre), 
                   xytext=(min_t_pre - 15, min_val_pre + 0.3),
                   arrowprops=dict(facecolor='black', shrink=0.05, 
                                 width=1.5, headwidth=8),
                   fontsize=10, color='#c0392b',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
    
    post_intervention_mask = t >= t_int
    if np.any(post_intervention_mask):
        avg_post = np.mean(B_intervention[post_intervention_mask])
        ax.axhline(y=avg_post, color='#27ae60', linestyle=':', 
                  alpha=0.5, linewidth=1)
        ax.text(85, avg_post + 0.05, f'Recovery Level\n≈{avg_post:.2f}', 
               fontsize=10, color='#27ae60',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
    
    ax.set_xlabel('Time (normalized)', fontweight='bold')
    ax.set_ylabel('Cognitive Bandwidth / Order', fontweight='bold')
    ax.set_title('The Resurrection Effect: Engineering & Artistic Intervention', 
                fontsize=16, pad=20, fontweight='bold')
    ax.set_ylim(0, 1.2)
    ax.set_xlim(0, 100)
    
    ax.legend(loc='upper right', frameon=True, fancybox=True, 
             framealpha=0.9, fontsize=10)
    
    ax.grid(True, which='major', linestyle='--', alpha=0.4)
    
    print("\nSimulation Statistics:")
    print("-" * 50)
    print(f"Intervention Time: t = {t_int}")
    
    pre_mask = t < t_int
    post_mask = t >= t_int
    
    if np.any(pre_mask):
        min_pre = np.min(B_intervention[pre_mask])
        print(f"Minimum B (Pre-Intervention): {min_pre:.4f}")
    
    if np.any(post_mask):
        avg_post = np.mean(B_intervention[post_mask])
        max_post = np.max(B_intervention[post_mask])
        print(f"Average B (Post-Intervention): {avg_post:.4f}")
        print(f"Maximum B (Post-Intervention): {max_post:.4f}")
        print(f"Recovery Ratio: {(avg_post / B_intervention[0]):.2%}")
    
    final_control = B_control[-1]
    final_intervention = B_intervention[-1]
    print(f"\nFinal State Comparison:")
    print(f"  Control (No Intervention):     {final_control:.4f}")
    print(f"  With Intervention:            {final_intervention:.4f}")
    print(f"  Improvement:                   {final_intervention - final_control:.4f}")
    print(f"  Relative Improvement:         {((final_intervention - final_control) / final_control * 100):.1f}%")
    print("=" * 50)
    
    plt.tight_layout()
    plt.savefig("fig_intervention.png", dpi=300, bbox_inches='tight')
    print("\nImage saved: fig_intervention.png")
    plt.show()


if __name__ == "__main__":
    main()
