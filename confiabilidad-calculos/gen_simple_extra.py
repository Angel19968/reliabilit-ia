"""
Genera los datos para los 4 gráficos "simples" restantes de la sección
Confiabilidad Cálculos: Mixture models, Competing risks models,
Optimal replacement time, y QQ/PP plots.

Reutiliza el MISMO dataset sintético (semilla 42) que generó Weibull/KM/NA,
para que las 3 secciones sean consistentes entre sí.

Cada cálculo se genera con la librería `reliability` y se valida cruzando
contra los resultados que la propia librería produce (ver sección AUDITORÍA
al final) antes de aceptarlo para el sitio.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reliability.Distributions import Mixture_Model, Competing_Risks_Model, Weibull_Distribution
from reliability.Nonparametric import KaplanMeier
from reliability.Repairable_systems import optimal_replacement_time
from reliability.Probability_plotting import QQ_plot_semiparametric, PP_plot_semiparametric

np.random.seed(42)

# ---------------------------------------------------------------------------
# Mismo dataset sintético que gen_reliability_data.py (semilla 42)
# ---------------------------------------------------------------------------
N = 40
TRUE_BETA = 2.3
TRUE_ETA = 9200.0
all_times = np.random.weibull(TRUE_BETA, N) * TRUE_ETA
all_times = np.round(all_times, 0)
n_censored = 8
idx = np.arange(N)
np.random.shuffle(idx)
censored_idx = set(idx[:n_censored].tolist())
failures, right_censored = [], []
for i, t in enumerate(all_times):
    if i in censored_idx:
        right_censored.append(round(t * np.random.uniform(0.5, 0.95), 0))
    else:
        failures.append(float(t))
failures = sorted(failures)
right_censored = sorted(right_censored)

BETA_HAT = 2.275467705324058
ETA_HAT = 9348.417416694741
fitted_dist = Weibull_Distribution(alpha=ETA_HAT, beta=BETA_HAT)

out = {}
audit = {}

# ===========================================================================
# 1) MIXTURE MODEL — dos sub-poblaciones de falla:
#    (a) desgaste temprano de un lote con defecto de fabricación (β alto, η bajo)
#    (b) desgaste normal del resto de la población (la Weibull ya ajustada)
#    Proporciones ilustrativas: 15% lote defectuoso, 85% población normal.
# ===========================================================================
early_life = Weibull_Distribution(alpha=2200, beta=3.0)
normal_life = fitted_dist
mixture = Mixture_Model(distributions=[early_life, normal_life], proportions=[0.15, 0.85])

t_grid = np.linspace(0.01, 18000, 150)
mix_sf = mixture.SF(xvals=t_grid, show_plot=False)
mix_cdf = mixture.CDF(xvals=t_grid, show_plot=False)
mix_pdf = mixture.PDF(xvals=t_grid, show_plot=False)

out["mixture"] = {
    "descripcion": "Mezcla ilustrativa: 15% de un lote con defecto de fabricación (falla temprana, Weibull α=2200,β=3.0) + 85% población normal (la Weibull ajustada α=9348,β=2.28).",
    "t": [round(x, 1) for x in t_grid.tolist()],
    "sf": [round(x, 4) for x in mix_sf.tolist()],
    "cdf": [round(x, 4) for x in mix_cdf.tolist()],
    "pdf": [round(x, 6) for x in mix_pdf.tolist()],
    "sub_a_sf": [round(x, 4) for x in early_life.SF(xvals=t_grid, show_plot=False).tolist()],
    "sub_b_sf": [round(x, 4) for x in normal_life.SF(xvals=t_grid, show_plot=False).tolist()],
}
# AUDITORÍA: en t=0 SF debe ser ~1; en t grande SF debe tender a 0; CDF+SF=1 siempre
audit["mixture"] = {
    "sf_at_0_is_1": bool(abs(mix_sf[0] - 1.0) < 0.01),
    "sf_plus_cdf_is_1_maxdev": float(np.max(np.abs((mix_sf + mix_cdf) - 1.0))),
    "sf_monotonic_nonincreasing": bool(np.all(np.diff(mix_sf) <= 1e-9)),
}

# ===========================================================================
# 2) COMPETING RISKS MODEL — dos modos de falla independientes compitiendo:
#    (a) desgaste mecánico progresivo (la Weibull ajustada)
#    (b) falla eléctrica aleatoria ocasional (beta~1, ocurre en cualquier momento)
#    SF resultante = SF_a(t) * SF_b(t) (el primero que ocurra "gana")
# ===========================================================================
mechanical = fitted_dist
electrical = Weibull_Distribution(alpha=35000, beta=1.1)
competing = Competing_Risks_Model(distributions=[mechanical, electrical])

cr_sf = competing.SF(xvals=t_grid, show_plot=False)
cr_cdf = competing.CDF(xvals=t_grid, show_plot=False)
cr_pdf = competing.PDF(xvals=t_grid, show_plot=False)

# validación cruzada manual: SF_competing debe ser exactamente el producto de las SF individuales
sf_a = mechanical.SF(xvals=t_grid, show_plot=False)
sf_b = electrical.SF(xvals=t_grid, show_plot=False)
manual_product = sf_a * sf_b

out["competing_risks"] = {
    "descripcion": "Dos modos de falla independientes compitiendo: desgaste mecánico progresivo (la Weibull ajustada α=9348,β=2.28) y falla eléctrica aleatoria ocasional (Weibull α=35000,β=1.1). Ilustrativo.",
    "t": [round(x, 1) for x in t_grid.tolist()],
    "sf": [round(x, 4) for x in cr_sf.tolist()],
    "cdf": [round(x, 4) for x in cr_cdf.tolist()],
    "pdf": [round(x, 6) for x in cr_pdf.tolist()],
    "mode_a_sf": [round(x, 4) for x in sf_a.tolist()],
    "mode_b_sf": [round(x, 4) for x in sf_b.tolist()],
}
audit["competing_risks"] = {
    "sf_equals_product_of_individual_sf_maxdev": float(np.max(np.abs(cr_sf - manual_product))),
    "competing_sf_leq_each_individual_sf": bool(np.all(cr_sf <= sf_a + 1e-9) and np.all(cr_sf <= sf_b + 1e-9)),
}

# ===========================================================================
# 3) OPTIMAL REPLACEMENT TIME — costo de mantenimiento preventivo (PM) vs.
#    correctivo (CM, tras una falla). Curva de costo/tiempo por unidad de tiempo
#    (modelo de renovación estándar) con el mínimo marcado.
#    Costos ilustrativos: PM = $100 (cambio programado), CM = $1500 (falla + paro no programado).
# ===========================================================================
COST_PM = 100.0
COST_CM = 1500.0
ort = optimal_replacement_time(
    cost_PM=COST_PM, cost_CM=COST_CM,
    weibull_alpha=ETA_HAT, weibull_beta=BETA_HAT,
    show_time_plot=False, show_ratio_plot=False, print_results=False,
)

# curva de costo por unidad de tiempo: C(t) = [Cp*R(t) + Cc*(1-R(t))] / integral(R, 0, t)
from scipy.integrate import quad

def R(t):
    return np.exp(-(t / ETA_HAT) ** BETA_HAT)

def cost_rate(t):
    integral, _ = quad(R, 0, t)
    if integral <= 0:
        return np.nan
    return (COST_PM * R(t) + COST_CM * (1 - R(t))) / integral

t_ort_grid = np.linspace(50, 14000, 300)
costs = np.array([cost_rate(t) for t in t_ort_grid])
best_i = int(np.nanargmin(costs))

out["optimal_replacement"] = {
    "descripcion": f"Costo de mantenimiento por unidad de tiempo, comparando reemplazo preventivo (PM, ${COST_PM:.0f}) vs. reemplazo tras falla (CM, ${COST_CM:.0f}). Curva calculada con el modelo de renovación estándar sobre la Weibull ajustada; el mínimo se validó contra optimal_replacement_time() de la librería reliability. Costos ilustrativos.",
    "cost_pm": COST_PM,
    "cost_cm": COST_CM,
    "t": [round(x, 1) for x in t_ort_grid.tolist()],
    "cost_rate": [round(x, 6) for x in costs.tolist()],
    "ort_t": round(float(t_ort_grid[best_i]), 1),
    "ort_cost": round(float(costs[best_i]), 6),
}
audit["optimal_replacement"] = {
    "library_ORT": float(ort.ORT),
    "library_min_cost": float(ort.min_cost),
    "manual_ORT": float(t_ort_grid[best_i]),
    "manual_min_cost": float(costs[best_i]),
    "ORT_relative_error_pct": float(abs(t_ort_grid[best_i] - ort.ORT) / ort.ORT * 100),
    "min_cost_relative_error_pct": float(abs(costs[best_i] - ort.min_cost) / ort.min_cost * 100),
}

# ===========================================================================
# 4) QQ PLOT (semiparamétrico) — cuantiles empíricos (Kaplan-Meier) vs.
#    cuantiles teóricos (Weibull ajustada). Replica EXACTA del algoritmo
#    interno de reliability.Probability_plotting.QQ_plot_semiparametric
#    (validado contra su salida real, ver auditoría).
# ===========================================================================
km = KaplanMeier(failures=failures, right_censored=right_censored, print_results=False, show_plot=False)
df = km.results
failure_rows = df.loc[df["Censoring code (censored=0)"] == 1.0]
ecdf_km = 1 - np.array(failure_rows["Kaplan-Meier Estimate"].values)

isf_vals = np.array([fitted_dist.inverse_SF(float(q)) for q in ecdf_km])
isf_vals = isf_vals[::-1]
isf_vals[isf_vals == -np.inf] = 0
x_sorted_failures = np.sort(np.array(failures))

out["qq_plot"] = {
    "descripcion": "QQ plot semiparamétrico: cuantiles observados (eje X) vs. cuantiles teóricos de la Weibull ajustada dado el estimador Kaplan-Meier (eje Y). Si el ajuste es bueno, los puntos deberían caer cerca de la diagonal Y=X.",
    "actual": [round(x, 1) for x in x_sorted_failures.tolist()],
    "theoretical": [round(x, 1) for x in isf_vals.tolist()],
}

# validación cruzada: comparar contra la salida real de QQ_plot_semiparametric (extrae del scatter)
fig_qq_params = QQ_plot_semiparametric(
    X_data_failures=failures, X_data_right_censored=right_censored,
    Y_dist=fitted_dist, method="KM",
)
fig = plt.gcf()
ax = fig.axes[0]
lib_scatter = ax.collections[0].get_offsets()
lib_x = np.array([p[0] for p in lib_scatter])
lib_y = np.array([p[1] for p in lib_scatter])
plt.close(fig)

audit["qq_plot"] = {
    "max_abs_diff_actual_x": float(np.max(np.abs(lib_x - x_sorted_failures))),
    "max_abs_diff_theoretical_y": float(np.max(np.abs(lib_y - isf_vals))),
    "library_fit_slope_m": float(fig_qq_params[0]),
}

# ===========================================================================
# 5) PP PLOT (semiparamétrico) — CDF empírica (Kaplan-Meier) vs. CDF teórica
#    (Weibull ajustada), ambas en escala 0-1. Validado contra la salida real
#    de PP_plot_semiparametric (extrae del scatter).
# ===========================================================================
emp_cdf_pp = 1 - np.array(failure_rows["Kaplan-Meier Estimate"].values)  # ya ascendente por construcción de KM.results
theo_cdf_pp = fitted_dist.CDF(xvals=x_sorted_failures, show_plot=False)

out["pp_plot"] = {
    "descripcion": "PP plot semiparamétrico: probabilidad acumulada empírica (Kaplan-Meier, eje X) vs. probabilidad acumulada teórica de la Weibull ajustada (eje Y), ambas de 0 a 1. Sirve como prueba gráfica de bondad de ajuste.",
    "empirical_cdf": [round(x, 5) for x in emp_cdf_pp.tolist()],
    "theoretical_cdf": [round(x, 5) for x in theo_cdf_pp.tolist()],
}

fig_pp = PP_plot_semiparametric(
    X_data_failures=failures, X_data_right_censored=right_censored,
    Y_dist=fitted_dist, method="KM",
)
ax2 = fig_pp.axes[0]
lib_scatter_pp = ax2.collections[0].get_offsets()
lib_x_pp = np.array([p[0] for p in lib_scatter_pp])
lib_y_pp = np.array([p[1] for p in lib_scatter_pp])
plt.close(fig_pp)

audit["pp_plot"] = {
    "max_abs_diff_empirical_x": float(np.max(np.abs(lib_x_pp - emp_cdf_pp))),
    "max_abs_diff_theoretical_y": float(np.max(np.abs(lib_y_pp - theo_cdf_pp))),
}

# ---------------------------------------------------------------------------
with open("/tmp/simple_extra_data.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

with open("/tmp/simple_extra_audit.json", "w", encoding="utf-8") as f:
    json.dump(audit, f, ensure_ascii=False, indent=2)

print(json.dumps(audit, indent=2))
print("OK -> /tmp/simple_extra_data.json, /tmp/simple_extra_audit.json")
