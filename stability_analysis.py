import numpy as np
import matplotlib.pyplot as plt


def drift_function(B, alpha, r=0.5, theta=0.2):
    return r * B * (1.0 - B) * (B - theta) - alpha * B


def potential_energy(B_vals, alpha, r=0.5, theta=0.2):
    # Numerically integrates drift function to compute potential landscape
    f_vals = drift_function(B_vals, alpha, r=r, theta=theta)
    dB = B_vals[1] - B_vals[0]
    V = -np.cumsum(f_vals) * dB
    return V


def plot_potential_landscape(save_path="fig_potential.png"):
    B_vals = np.linspace(0.0, 1.2, 400)
    alphas = [0.1, 0.5, 1.0, 2.0]

    plt.figure(figsize=(8, 6))
    for alpha in alphas:
        V = potential_energy(B_vals, alpha)
        plt.plot(B_vals, V, label=f"alpha={alpha}")

    plt.xlabel("B")
    plt.ylabel("Potential V(B)")
    plt.title("Potential Landscape under Different α")
    plt.legend()
    plt.grid(True, linestyle=":")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Image saved: {save_path}")
    plt.show()


def estimate_lyapunov(
    alpha,
    sigma=0.05,
    T=50.0,
    dt=0.01,
    r=0.5,
    theta=0.2,
    attack_coeff=1.0,
    delta0=1e-5,
    crash_floor=1e-12,
    seed=None,
):
    # Estimates Lyapunov exponent using two-trajectory perturbation method
    rng = np.random.default_rng(seed)
    steps = int(T / dt)

    B1 = 1.0
    B2 = 1.0 + delta0

    for _ in range(steps):
        dW = rng.normal(0.0, np.sqrt(dt))
        drift1 = drift_function(B1, alpha, r=r, theta=theta) - attack_coeff * (alpha - 1.0) * 0.0
        drift2 = drift_function(B2, alpha, r=r, theta=theta) - attack_coeff * (alpha - 1.0) * 0.0
        diff1 = sigma * B1
        diff2 = sigma * B2
        B1 = max(0.0, B1 + drift1 * dt + diff1 * dW)
        B2 = max(0.0, B2 + drift2 * dt + diff2 * dW)

    delta_T = abs(B2 - B1)
    delta_T = max(delta_T, crash_floor)
    lam = (1.0 / T) * np.log(delta_T / delta0)
    return lam


def scan_lyapunov(
    alpha_grid,
    sigma=0.05,
    T=50.0,
    dt=0.01,
    r=0.5,
    theta=0.2,
    delta0=1e-5,
    seed=123,
):
    lambdas = []
    for alpha in alpha_grid:
        lam = estimate_lyapunov(
            alpha=alpha,
            sigma=sigma,
            T=T,
            dt=dt,
            r=r,
            theta=theta,
            delta0=delta0,
            seed=seed + int(alpha * 1000),
        )
        lambdas.append(lam)
    return np.array(lambdas)


def plot_lyapunov_curve(save_path="fig_lyapunov.png"):
    alpha_grid = np.linspace(0.05, 3.0, 40)
    lambdas = scan_lyapunov(alpha_grid, sigma=0.05, T=60.0, dt=0.01, r=0.5, theta=0.2)

    plt.figure(figsize=(8, 5))
    plt.plot(alpha_grid, lambdas, color="#8e44ad", linewidth=2.2, label="Lyapunov λ")
    plt.axhline(y=0.0, color="gray", linestyle="--", label="λ = 0")

    idx = int(np.argmin(np.abs(lambdas)))
    alpha_star = alpha_grid[idx]
    lambda_star = lambdas[idx]
    plt.scatter([alpha_star], [lambda_star], color="red", s=70, zorder=5, label=f"cross ~ {alpha_star:.2f}")

    plt.xlabel("α (Algorithm Intensity)")
    plt.ylabel("λ (Lyapunov)")
    plt.title("Lyapunov Exponent vs. α")
    plt.legend()
    plt.grid(True, linestyle=":")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Image saved: {save_path}")
    plt.show()

    print(f"λ≈0 crossing point: alpha≈{alpha_star:.3f}, λ≈{lambda_star:.3e}")


def main():
    plot_potential_landscape()
    plot_lyapunov_curve()


if __name__ == "__main__":
    main()
