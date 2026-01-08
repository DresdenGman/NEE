import numpy as np
import matplotlib.pyplot as plt


def hysteresis_drift(B, r=0.8, theta=0.3, alpha=1.0, attack_coeff=0.5):
    # bistable recovery term with Allee threshold
    recovery = r * B * (1.0 - B) * (B - theta)
    extraction = alpha * attack_coeff * B
    return recovery - extraction


def run_sde_simulation(
    alpha,
    sigma,
    T=100.0,
    dt=0.01,
    simulations=500,
    r=0.8,
    theta=0.3,
    attack_coeff=0.5,
    crash_threshold=0.1,
    seed=None,
):
    # Solves the SDE using Euler-Maruyama method with Monte Carlo paths
    rng = np.random.default_rng(seed)
    num_steps = int(T / dt)
    time = np.linspace(0.0, T, num_steps)

    B_paths = np.zeros((simulations, num_steps))
    B_paths[:, 0] = 1.0
    collapsed_count = np.zeros(num_steps)
    collapse_time = np.full(simulations, fill_value=T)

    for t_idx in range(1, num_steps):
        B_prev = B_paths[:, t_idx - 1]
        drift = hysteresis_drift(B_prev, r=r, theta=theta, alpha=alpha, attack_coeff=attack_coeff)
        diffusion = sigma * B_prev
        dW = rng.normal(0.0, np.sqrt(dt), simulations)
        B_new = B_prev + drift * dt + diffusion * dW
        B_new = np.maximum(B_new, 0.0)
        just_collapsed = (B_new < crash_threshold) & (collapse_time == T)
        collapse_time[just_collapsed] = time[t_idx]
        B_paths[:, t_idx] = B_new
        collapsed_count[t_idx] = np.sum(B_new < crash_threshold)

    return time, B_paths, collapsed_count, collapse_time


def plot_spaghetti(time, B_paths, crash_threshold=0.1, max_paths=50, save_path="fig_spaghetti.png"):
    n_paths = min(max_paths, B_paths.shape[0])
    plt.figure(figsize=(10, 6))
    plt.plot(time, B_paths[:n_paths, :].T, color="steelblue", alpha=0.25)
    plt.axhline(y=crash_threshold, color="gray", linestyle="--", label="Collapse Threshold")
    plt.ylim(0, 1.2 * np.max(B_paths))
    plt.xlabel("Time")
    plt.ylabel("B (Cognitive State)")
    plt.title(f"SDE Paths (showing {n_paths}/{B_paths.shape[0]} paths)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Image saved: {save_path}")
    plt.show()


def plot_survival(time, collapsed_count, simulations):
    survival = 1.0 - collapsed_count / simulations
    plt.figure(figsize=(7, 4))
    plt.plot(time, survival, color="#e74c3c", linewidth=2.0)
    plt.ylim(0, 1.05)
    plt.xlabel("Time")
    plt.ylabel("Survival Probability")
    plt.title("Survival Curve (B >= threshold)")
    plt.grid(True, linestyle=":")
    plt.tight_layout()
    plt.show()


def collapse_heatmap(
    alpha_grid,
    sigma_grid,
    T=100.0,
    dt=0.01,
    simulations=200,
    r=0.8,
    theta=0.3,
    attack_coeff=0.5,
    crash_threshold=0.1,
    seed=42,
):
    rng = np.random.default_rng(seed)
    heat = np.zeros((len(sigma_grid), len(alpha_grid)))

    for i, sigma in enumerate(sigma_grid):
        for j, alpha in enumerate(alpha_grid):
            sub_seed = rng.integers(0, 1_000_000_000)
            _, _, _, collapse_time = run_sde_simulation(
                alpha=alpha,
                sigma=sigma,
                T=T,
                dt=dt,
                simulations=simulations,
                r=r,
                theta=theta,
                attack_coeff=attack_coeff,
                crash_threshold=crash_threshold,
                seed=sub_seed,
            )
            heat[i, j] = np.mean(collapse_time)

    plt.figure(figsize=(10, 6))
    im = plt.imshow(
        heat,
        origin="lower",
        aspect="auto",
        extent=[alpha_grid[0], alpha_grid[-1], sigma_grid[0], sigma_grid[-1]],
        cmap="inferno",
    )
    plt.colorbar(im, label="Mean Collapse Time T_crash")
    plt.xlabel("α (Algorithm Intensity)")
    plt.ylabel("σ (Noise/Volatility)")
    plt.title("Cognitive Collapse Heatmap")
    plt.tight_layout()
    plt.show()

    return heat


def main():
    alpha = 1.5
    sigma = 0.08
    time, B_paths, collapsed_count, _ = run_sde_simulation(
        alpha=alpha,
        sigma=sigma,
        T=80.0,
        dt=0.02,
        simulations=400,
        r=0.8,
        theta=0.3,
        attack_coeff=0.5,
        crash_threshold=0.1,
        seed=123,
    )
    plot_spaghetti(time, B_paths, crash_threshold=0.1, max_paths=60)
    plot_survival(time, collapsed_count, simulations=B_paths.shape[0])

    alpha_grid = np.linspace(0.2, 3.5, 24)
    sigma_grid = np.linspace(0.0, 0.4, 20)
    collapse_heatmap(
        alpha_grid=alpha_grid,
        sigma_grid=sigma_grid,
        T=60.0,
        dt=0.02,
        simulations=150,
        r=0.8,
        theta=0.3,
        attack_coeff=0.5,
        crash_threshold=0.1,
        seed=99,
    )


if __name__ == "__main__":
    main()
