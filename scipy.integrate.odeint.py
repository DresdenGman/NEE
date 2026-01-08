import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_context("talk")
sns.set_style("whitegrid")


class NeuroEntropicModel:
    def __init__(self, params):
        self.r = params.get('r', 0.5)
        self.K_cap = params.get('K_cap', 1.0)
        self.epsilon = params.get('epsilon', 0.8)
        self.delta = params.get('delta', 0.1)
        self.alpha = params.get('alpha', 1.2)
        self.beta = params.get('beta', 0.05)
        self.strategy = params.get('strategy', 'adaptive')

    def algorithm_policy(self, B, K, t):
        # adaptive noise injection based on cognitive state
        base_noise = 0.2

        if self.strategy == 'constant':
            return base_noise

        if self.strategy == 'periodic':
            return base_noise + 0.3 * np.sin(t) ** 2

        if self.strategy == 'adaptive':
            compute_power = self.beta * K
            predatory_intent = 1.0 if B > 0.3 else 0.2
            return base_noise + compute_power * predatory_intent

        return base_noise

    def derivatives(self, y, t):
        B, K = y
        I = self.algorithm_policy(B, K, t)
        B = max(0.0, B)
        K = max(0.0, K)
        dBdt = self.r * B * (1 - B / self.K_cap) - self.alpha * I * B
        dKdt = self.epsilon * (self.alpha * I * B) - self.delta * K
        return [dBdt, dKdt]

    def run_simulation(self, initial_state, time_span, num_points=1000):
        # Solves the ODE system using scipy's odeint
        t = np.linspace(0, time_span, num_points)
        solution = odeint(self.derivatives, initial_state, t)
        return t, solution

    def run_simulation_sde(self, initial_state, time_span, dt=0.02, sigma=0.05, seed=None):
        # Solves the SDE using Euler-Maruyama method
        rng = np.random.default_rng(seed)
        steps = int(time_span / dt) + 1
        t = np.linspace(0.0, time_span, steps)
        states = np.zeros((steps, 2))
        states[0] = np.array(initial_state, dtype=float)

        for i in range(steps - 1):
            B, K = states[i]
            dBdt, dKdt = self.derivatives([B, K], t[i])
            noise = sigma * rng.normal(0.0, np.sqrt(dt))
            B_next = max(0.0, B + dBdt * dt + noise)
            K_next = max(0.0, K + dKdt * dt)
            states[i + 1] = [B_next, K_next]

        return t, states


def plot_dynamics(t, solution, strategy_label):
    B_series = solution[:, 0]
    K_series = solution[:, 1]

    plt.figure(figsize=(12, 10))

    plt.subplot(2, 1, 1)
    plt.plot(t, B_series, label='Biological Negentropy (B)', color='#2ecc71', linewidth=2.5)
    plt.plot(t, K_series, label='Digital Capital (K)', color='#e74c3c', linewidth=2.5)
    plt.title(f"Neuro-Entropic Extraction Dynamics (Strategy: {strategy_label})", fontsize=16)
    plt.ylabel("Magnitude")
    plt.xlabel("Time (t)")
    plt.legend()
    plt.axhline(y=0.3, color='gray', linestyle='--', alpha=0.5, label='Collapse Threshold')

    plt.subplot(2, 1, 2)
    plt.plot(B_series, K_series, color='#8e44ad', linewidth=2)
    plt.title("Phase Space: Cognitive State vs. Capital Accumulation", fontsize=16)
    plt.xlabel("Biological Negentropy (B)")
    plt.ylabel("Digital Capital (K)")
    plt.grid(True, linestyle=':')
    plt.scatter(B_series[0], K_series[0], color='green', s=100, label='Start')
    plt.scatter(B_series[-1], K_series[-1], color='red', s=100, label='End')
    plt.legend()

    plt.tight_layout()
    plt.show()


def sensitivity_analysis(base_params, y0, t_max, alpha_min=0.1, alpha_max=5.0, n=40):
    # Scans alpha parameter space to find optimal exploitation threshold
    alphas = np.linspace(alpha_min, alpha_max, n)
    k_finals = []

    for alpha in alphas:
        params = dict(base_params)
        params['alpha'] = float(alpha)
        model = NeuroEntropicModel(params)
        _, sol = model.run_simulation(y0, t_max)
        k_finals.append(sol[-1, 1])

    k_finals = np.array(k_finals)
    peak_idx = int(np.argmax(k_finals))
    peak_alpha = alphas[peak_idx]
    peak_k = k_finals[peak_idx]

    plt.figure(figsize=(8, 5))
    plt.plot(alphas, k_finals, color='#2980b9', linewidth=2.2)
    plt.scatter([peak_alpha], [peak_k], color='red', s=80, zorder=5, label=f'peak α≈{peak_alpha:.2f}')
    plt.title("Sensitivity: α vs. K_final", fontsize=15)
    plt.xlabel("α (Penetration Rate)")
    plt.ylabel("K_final")
    plt.legend()
    plt.grid(True, linestyle=':')
    plt.tight_layout()
    plt.show()

    return peak_alpha, peak_k


def main():
    params = {
        'r': 0.8,
        'epsilon': 0.5,
        'delta': 0.15,
        'alpha': 1.5,
        'beta': 0.8,
        'strategy': 'adaptive'
    }

    model = NeuroEntropicModel(params)
    y0 = [1.0, 0.1]
    t_max = 50

    t, result = model.run_simulation(y0, t_max)
    plot_dynamics(t, result, params['strategy'])

    peak_alpha, peak_k = sensitivity_analysis(
        base_params=params,
        y0=y0,
        t_max=t_max,
        alpha_min=0.1,
        alpha_max=5.0,
        n=40
    )
    print(f"[Sensitivity] K_final peak at α≈{peak_alpha:.3f}, K_final≈{peak_k:.3f}")

    t_sde, sol_sde = model.run_simulation_sde(
        initial_state=y0,
        time_span=t_max,
        dt=0.02,
        sigma=0.05,
        seed=42
    )
    plot_dynamics(t_sde, sol_sde, strategy_label=f"{params['strategy']} + noise")


if __name__ == "__main__":
    main()
