import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 50)
print("Generating scientific figures...")
print("=" * 50)

print("\n[1/6] Generating spaghetti plot (fig_spaghetti.png)...")
from stochastic_simulation import run_sde_simulation, plot_spaghetti
import numpy as np

time, B_paths, collapsed_count, collapse_time = run_sde_simulation(
    alpha=1.5, sigma=0.08, T=50, dt=0.02, simulations=500,
    r=0.8, theta=0.3, attack_coeff=0.5, crash_threshold=0.1, seed=123
)
plot_spaghetti(time, B_paths, crash_threshold=0.1, max_paths=60, save_path='fig_spaghetti.png')
print("✓ fig_spaghetti.png generated")

print("\n[2/6] Generating potential landscape (fig_potential.png)...")
from stability_analysis import plot_potential_landscape

plot_potential_landscape(save_path='fig_potential.png')
print("✓ fig_potential.png generated")

print("\n[3/6] Generating Lyapunov exponent plot (fig_lyapunov.png)...")
from stability_analysis import plot_lyapunov_curve

plot_lyapunov_curve(save_path='fig_lyapunov.png')
print("✓ fig_lyapunov.png generated")

print("\n[4/6] Generating entropy distribution (fig_entropy.png)...")
exec(open('data_calibration_v3.py').read())
print("✓ fig_entropy.png generated")

print("\n[5/6] Generating Zipf's law plot (fig_zipf.png)...")
exec(open('structural_analysis.py').read())
print("✓ fig_zipf.png generated")

print("\n[6/6] Generating intervention simulation (fig_intervention.png)...")
exec(open('intervention_simulation.py').read())
print("✓ fig_intervention.png generated")

print("\n" + "=" * 50)
print("All figures generated successfully!")
print("=" * 50)
print("\nFile locations:")
print("  - fig_spaghetti.png")
print("  - fig_potential.png")
print("  - fig_lyapunov.png")
print("  - fig_entropy.png")
print("  - fig_zipf.png")
print("  - fig_intervention.png")
print("\nPrompt file: image_prompts.md")
