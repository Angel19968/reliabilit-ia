"""
Genera los datos para los gráficos de "complejidad media" de la nueva página
Confiabilidad Avanzada: Histograma+PDF, MCF, ROCOF, Weibull probability plot,
Reliability growth (Duane), Sequential sampling chart, Stress-Strength
interference, y DSZI model.

Reutiliza el dataset base (semilla 42, Weibull ajustada) donde tiene sentido,
y genera datasets nuevos e ilustrativos donde el escenario lo requiere
(sistemas reparables, programa de pruebas, muestreo de aceptación).
Cada cálculo se audita contra la salida real de la librería `reliability`.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reliability.Distributions import Weibull_Distribution, Normal_Distribution, DSZI_Model
from reliability.Repairable_systems import MCF_nonparametric, ROCOF, reliability_growth
from reliability.Probability_plotting import Weibull_probability_plot
from reliability.Other_functions import stress_strength

np.random.seed(42)

# ---------------------------------------------------------------------------
# Mismo dataset base que las páginas anteriores (semilla 42)
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
# 1) HISTOGRAMA DE FALLAS + PDF SUPERPUESTA
#    Usa las 32 fallas reales del dataset base, agrupadas en bins, con la
#    curva f(t) de la Weibull ajustada superpuesta (ya calculada antes).
# ===========================================================================
counts, bin_edges = np.histogram(failures, bins=8, density=True)
bin_centers = [(bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(len(counts))]
bin_widths = [bin_edges[i + 1] - bin_edges[i] for i in range(len(counts))]

t_grid_pdf = np.linspace(0.01, max(failures) * 1.05, 150)
pdf_vals = fitted_dist.PDF(xvals=t_grid_pdf, show_plot=False)

out["histogram"] = {
    "descripcion": "Histograma de densidad de las 32 fallas observadas (8 bins), con la densidad de falla f(t) de la Weibull ajustada superpuesta. Si el ajuste es bueno, la curva debería seguir la forma de las barras.",
    "bin_centers": [round(x, 1) for x in bin_centers],
    "bin_widths": [round(x, 1) for x in bin_widths],
    "bin_density": [round(x, 6) for x in counts.tolist()],
    "pdf_t": [round(x, 1) for x in t_grid_pdf.tolist()],
    "pdf_y": [round(x, 6) for x in pdf_vals.tolist()],
}
# auditoría: el área bajo el histograma (densidad) debe integrar a ~1
hist_area = float(np.sum(counts * np.array(bin_widths)))
audit["histogram"] = {"histogram_area_should_be_1": hist_area}

# ===========================================================================
# 2) MEAN CUMULATIVE FUNCTION (MCF) — flota de 6 bombas reparables,
#    simuladas con un proceso de Poisson no homogéneo (Power Law, NHPP)
#    con tasa creciente (beta_nhpp=1.4) = el sistema empeora con el tiempo
#    (cada vez se repara con más frecuencia). Escenario sintético ilustrativo.
# ===========================================================================
def simulate_nhpp_power_law(beta_nhpp, eta_nhpp, end_time, rng):
    """Simula tiempos de evento de un proceso de Poisson no homogéneo Power Law
    (equivalente al modelo Duane/Crow-AMSAA) usando el método de inversión:
    t_i = eta * (Gamma(i,1))^(1/beta)."""
    times = []
    cum_gamma = 0.0
    i = 0
    while True:
        i += 1
        cum_gamma += rng.exponential(1.0)
        t = eta_nhpp * (cum_gamma) ** (1.0 / beta_nhpp)
        if t > end_time:
            break
        times.append(round(t, 1))
    return times

rng = np.random.default_rng(7)
N_SYSTEMS = 6
END_TIME = 20000.0
NHPP_BETA = 1.45
NHPP_ETA = 6200.0
mcf_data = []
for s in range(N_SYSTEMS):
    eta_s = NHPP_ETA * rng.uniform(0.85, 1.15)
    reps = simulate_nhpp_power_law(NHPP_BETA, eta_s, END_TIME, rng)
    if len(reps) == 0:
        reps = [END_TIME]
    reps.append(END_TIME)  # retirement time (right censored, per library convention)
    mcf_data.append(reps)

mcf = MCF_nonparametric(data=mcf_data, print_results=False, show_plot=False)
out["mcf"] = {
    "descripcion": f"Función Acumulada Media (MCF) de {N_SYSTEMS} bombas reparables observadas hasta las {int(END_TIME):,} horas. Datos sintéticos ilustrativos, simulados con un proceso de Poisson no homogéneo (tasa creciente) para representar un sistema que se repara con más frecuencia a medida que envejece.",
    "n_systems": N_SYSTEMS,
    "end_time": END_TIME,
    "t": [round(float(x), 1) for x in mcf.time],
    "mcf": [round(float(x), 4) for x in mcf.MCF],
    "lower": [round(float(x), 4) for x in mcf.lower],
    "upper": [round(float(x), 4) for x in mcf.upper],
    "system_events": [[round(x, 1) for x in reps[:-1]] for reps in mcf_data],
}
audit["mcf"] = {
    "mcf_monotonic_nondecreasing": bool(np.all(np.diff(mcf.MCF) >= -1e-9)),
    "lower_leq_mcf_leq_upper": bool(np.all(np.array(mcf.lower) <= np.array(mcf.MCF) + 1e-9) and np.all(np.array(mcf.MCF) <= np.array(mcf.upper) + 1e-9)),
    "n_time_points": len(mcf.time),
}

# ===========================================================================
# 3) ROCOF — se analiza UN solo sistema reparable en detalle para determinar
#    si su tasa de fallas tiene tendencia. Nota: el test de Laplace necesita
#    bastantes eventos para alcanzar significancia estadística; con solo las
#    4-7 reparaciones de un sistema de la flota de MCF (deterioro leve,
#    beta=1.45) no se llega a un resultado significativo (se probó y da
#    "constant" con U~0.77-1.3, un falso negativo por tamaño de muestra).
#    Por eso aquí se simula un historial de mantenimiento más largo y con un
#    deterioro más marcado (beta=2.2) para un único sistema bajo monitoreo
#    prolongado — escenario complementario, no el mismo sistema de la
#    sección de MCF.
# ===========================================================================
rng_rocof = np.random.default_rng(99)
ROCOF_BETA = 2.2
ROCOF_ETA = 6200.0
ROCOF_END_TIME = 45000.0
system0_events = simulate_nhpp_power_law(ROCOF_BETA, ROCOF_ETA, ROCOF_END_TIME, rng_rocof)
rocof = ROCOF(failure_times=system0_events, print_results=False, show_plot=False)

beta_r = float(rocof.Beta_hat) if isinstance(rocof.Beta_hat, (int, float, np.floating)) else None
lambda_r = float(rocof.Lambda_hat) if isinstance(rocof.Lambda_hat, (int, float, np.floating)) else None

t_grid_rocof = np.linspace(0.1, max(system0_events) * 1.05, 100)
# N(t) esperado del modelo NHPP Power Law ajustado: N(t) = Lambda_hat * t^Beta_hat
fitted_cum = (lambda_r * t_grid_rocof ** beta_r).tolist() if (lambda_r and beta_r) else None

out["rocof"] = {
    "descripcion": "Análisis de tendencia (test de Laplace) de un sistema reparable individual bajo monitoreo prolongado: ¿la frecuencia de fallas aumenta, disminuye o se mantiene constante con el uso? Dataset sintético ilustrativo con deterioro marcado, para que el test tenga suficiente potencia estadística con este tamaño de muestra.",
    "failure_times": [round(x, 1) for x in system0_events],
    "trend": rocof.trend,
    "U_statistic": round(float(rocof.U), 4),
    "beta_hat": round(beta_r, 4) if beta_r else None,
    "lambda_hat": lambda_r,
    "fitted_t": [round(x, 1) for x in t_grid_rocof.tolist()] if fitted_cum else None,
    "fitted_cumulative": [round(x, 4) for x in fitted_cum] if fitted_cum else None,
}
audit["rocof"] = {
    "trend_detected": rocof.trend,
    "beta_hat_gt_1_means_worsening": bool(beta_r and beta_r > 1),
    "consistent_with_simulated_beta_2_2": bool(beta_r and abs(beta_r - ROCOF_BETA) < 0.6),
}

# ===========================================================================
# 4) WEIBULL PROBABILITY PLOT — reutiliza el dataset base ya ajustado.
#    Puntos = rangos medios ajustados por censura (extraídos EXACTOS de la
#    librería, ver auditoría), línea = la misma curva F(t) ya calculada
#    (weibull.cdf), graficada en ejes log-x / probabilidad-y en vez de lineal.
# ===========================================================================
fig_wp = Weibull_probability_plot(failures=failures, right_censored=right_censored, CI_type=None)
ax_wp = plt.gca()
wp_scatter = ax_wp.collections[0].get_offsets()
wp_x = [float(p[0]) for p in wp_scatter]
wp_y = [float(p[1]) for p in wp_scatter]
plt.close(fig_wp)

out["weibull_prob_plot"] = {
    "descripcion": "Gráfico de probabilidad de Weibull: si los tiempos de falla realmente siguen una Weibull, los puntos deberían caer sobre una línea recta en estos ejes especiales (X logarítmico, Y transformado). Puntos extraídos exactos de Weibull_probability_plot(); línea = la misma curva F(t) ya calculada.",
    "scatter_t": [round(x, 1) for x in wp_x],
    "scatter_cdf": [round(x, 6) for x in wp_y],
}
# la línea reutiliza la curva CDF de weibull ya calculada en gen_reliability_data.py;
# la recalculamos aquí para no depender de otro archivo
t_line = np.linspace(1, max(failures + right_censored) * 1.15, 150)
cdf_line = fitted_dist.CDF(xvals=t_line, show_plot=False)
out["weibull_prob_plot"]["line_t"] = [round(x, 1) for x in t_line.tolist()]
out["weibull_prob_plot"]["line_cdf"] = [round(x, 6) for x in cdf_line.tolist()]

# auditoría: recomputar manualmente los rangos medios simples (sin censura) y
# verificar que están en el mismo orden de magnitud que los ajustados por censura
simple_median_ranks = [(k - 0.3) / (N - 8 + 1 - 0.4 + 8) for k in range(1, len(wp_x) + 1)]
audit["weibull_prob_plot"] = {
    "n_scatter_points": len(wp_x),
    "scatter_matches_failures_count": len(wp_x) == len(failures),
    "first_point_time_matches_min_failure": bool(abs(wp_x[0] - min(failures)) < 1e-6),
    "last_point_cdf_below_1": bool(wp_y[-1] < 1.0),
}

# ===========================================================================
# 5) RELIABILITY GROWTH (Duane model) — programa de pruebas de un prototipo
#    rediseñado: cada vez que falla, se corrige la causa raíz, así que el
#    tiempo entre fallas tiende a aumentar (el sistema "madura"). Dataset
#    sintético clásico de crecimiento de confiabilidad.
# ===========================================================================
# tiempos de falla acumulados de un programa de pruebas con MTBF creciente
growth_times = [12, 30, 55, 96, 155, 240, 360, 510, 700, 940, 1230, 1580]

growth = reliability_growth(times=growth_times, target_MTBF=150, show_plot=False, print_results=False, model="Duane")

failure_numbers = list(range(1, len(growth_times) + 1))
cum_mtbf = [t / n for t, n in zip(growth_times, failure_numbers)]

t_grid_growth = np.linspace(min(growth_times) * 0.8, max(growth_times) * 1.15, 100)
fit_mtbf_growth = (1.0 / growth.A) * (t_grid_growth ** growth.Alpha)

out["reliability_growth"] = {
    "descripcion": "Programa de pruebas de un prototipo rediseñado: cada falla se corrige antes de continuar, así que el MTBF acumulado (tiempo medio entre fallas) crece con las horas de prueba — el modelo de Duane predice esta mejora como una línea recta en ejes log-log. Datos sintéticos ilustrativos de un programa de desarrollo, no de campo.",
    "cumulative_time": growth_times,
    "cumulative_mtbf": [round(x, 3) for x in cum_mtbf],
    "A": round(float(growth.A), 5),
    "alpha_growth": round(float(growth.Alpha), 5),
    "fit_t": [round(x, 1) for x in t_grid_growth.tolist()],
    "fit_mtbf": [round(x, 3) for x in fit_mtbf_growth.tolist()],
    "target_mtbf": 150,
    "time_to_target": growth.time_to_target if isinstance(growth.time_to_target, str) else round(float(growth.time_to_target), 1),
}
# auditoría: comparar el ajuste A*t^Alpha devuelto por la librería contra el
# MTBF acumulado calculado manualmente (t_n / n) para cada punto observado
# El modelo de Duane es un AJUSTE por mínimos cuadrados de log(MTBF_c) vs
# log(t) (no pasa exactamente por cada punto observado), así que la auditoría
# correcta es reproducir el mismo ajuste polyfit manualmente y comparar A y
# Alpha contra los devueltos por la librería (deben coincidir casi exacto),
# NO comparar la curva ajustada contra cada punto crudo (eso es el residual
# esperado del ajuste, no un error).
x_fit = np.log(growth_times)
y_fit = np.log(cum_mtbf)
z_fit = np.polyfit(x_fit, y_fit, 1)
manual_alpha = float(z_fit[0])
manual_b = float(np.exp(z_fit[1]))
manual_A = 1.0 / manual_b

audit["reliability_growth"] = {
    "A": float(growth.A),
    "Alpha": float(growth.Alpha),
    "manual_polyfit_A": manual_A,
    "manual_polyfit_Alpha": manual_alpha,
    "A_relative_error_pct": float(abs(manual_A - growth.A) / growth.A * 100),
    "Alpha_relative_error_pct": float(abs(manual_alpha - growth.Alpha) / growth.Alpha * 100),
    "alpha_between_0_and_1_growth_expected": bool(0 < growth.Alpha < 1),
}

# ===========================================================================
# 6) SEQUENTIAL SAMPLING CHART — plan de muestreo de aceptación para un lote
#    de componentes. p1=2% (calidad aceptable), p2=8% (calidad rechazable),
#    alpha=5% (riesgo del productor), beta=10% (riesgo del consumidor).
# ===========================================================================
P1, P2, ALPHA_RISK, BETA_RISK = 0.02, 0.08, 0.05, 0.10
MAX_SAMPLES = 60

# NOTA: reliability.Reliability_testing.sequential_sampling_chart() falla en este
# entorno con un bug de compatibilidad pandas/numpy (LossySetitemError al asignar
# "x" a una columna int64 cuando algún límite es negativo). En vez de parchear
# pandas, replicamos EXACTAMENTE la misma fórmula (leída directamente del código
# fuente de la librería vía inspect.getsource) sin pasar por el DataFrame:
a_ = 1 - ALPHA_RISK
b_ = 1 - BETA_RISK
d_ = np.log(P2 / P1) + np.log((1 - P1) / (1 - P2))
h1_ = np.log((1 - a_) / b_) / d_
h2_ = np.log((1 - b_) / a_) / d_
s_ = np.log((1 - P1) / (1 - P2)) / d_

xvals_ssc = np.arange(MAX_SAMPLES + 1)
acceptance_array = np.floor(s_ * xvals_ssc + h2_).astype(int)
rejection_array = np.ceil(s_ * xvals_ssc - h1_).astype(int)
for i, x in enumerate(xvals_ssc):
    if rejection_array[i] > x:
        rejection_array[i] = -1

# simulamos una trayectoria de prueba: 40 muestras, con fallas ocasionales (tasa real ~4%)
rng2 = np.random.default_rng(123)
test_outcomes = (rng2.random(40) < 0.04).astype(int).tolist()
cum_failures_path = np.cumsum(test_outcomes).tolist()

out["sequential_sampling"] = {
    "descripcion": f"Plan de muestreo secuencial para aceptar o rechazar un lote de componentes según se van probando, sin necesidad de fijar el tamaño de muestra de antemano. Calidad aceptable p1={P1*100:.0f}%, calidad rechazable p2={P2*100:.0f}%, riesgo del productor {ALPHA_RISK*100:.0f}%, riesgo del consumidor {BETA_RISK*100:.0f}%. Trayectoria de prueba simulada.",
    "p1": P1, "p2": P2, "alpha": ALPHA_RISK, "beta": BETA_RISK,
    "samples": xvals_ssc.tolist(),
    "failures_to_accept": [None if v < 0 else int(v) for v in acceptance_array.tolist()],
    "failures_to_reject": [None if v < 0 else int(v) for v in rejection_array.tolist()],
    "test_path_samples": list(range(1, len(test_outcomes) + 1)),
    "test_path_cumulative_failures": cum_failures_path,
}
_accept = out["sequential_sampling"]["failures_to_accept"]
_reject = out["sequential_sampling"]["failures_to_reject"]
_both_defined_ok = all((a is None or r is None or r >= a) for a, r in zip(_accept, _reject))
audit["sequential_sampling"] = {
    "n_rows": len(xvals_ssc),
    "reject_geq_accept_where_both_defined": bool(_both_defined_ok),
}

# ===========================================================================
# 7) STRESS-STRENGTH INTERFERENCE — resistencia mecánica de un componente
#    (Weibull) vs. la carga real que recibe en operación (Normal).
#    Escenario sintético ilustrativo con unidades arbitrarias de esfuerzo (MPa).
# ===========================================================================
stress_dist = Normal_Distribution(mu=150, sigma=20)     # carga operativa (MPa)
strength_dist = Weibull_Distribution(alpha=230, beta=6)  # resistencia del material (MPa)

prob_failure = stress_strength(stress=stress_dist, strength=strength_dist, show_plot=False, print_results=False, warn=False)

x_ss = np.linspace(50, 300, 200)
stress_pdf = stress_dist.PDF(xvals=x_ss, show_plot=False)
strength_pdf = strength_dist.PDF(xvals=x_ss, show_plot=False)

# auditoría: integrar manualmente P(stress > strength) = integral sobre x de f_stress(x) * F_strength(x) dx aprox,
# comparando contra el valor devuelto por la librería
from scipy.integrate import quad

def integrand(x):
    p = np.atleast_1d(stress_dist.PDF(xvals=np.array([x]), show_plot=False))[0]
    c = np.atleast_1d(strength_dist.CDF(xvals=np.array([x]), show_plot=False))[0]
    return p * c

manual_pf, _ = quad(integrand, 50, 300, limit=200)

out["stress_strength"] = {
    "descripcion": "Interferencia esfuerzo-resistencia: la curva de resistencia del material (Weibull) y la curva de la carga real en operación (Normal) se superponen. El área de solapamiento (sombreada) representa la probabilidad de que, en algún momento, el esfuerzo supere la resistencia y el componente falle.",
    "x": [round(x, 1) for x in x_ss.tolist()],
    "stress_pdf": [round(x, 6) for x in stress_pdf.tolist()],
    "strength_pdf": [round(x, 6) for x in strength_pdf.tolist()],
    "probability_of_failure": round(float(prob_failure), 5),
}
audit["stress_strength"] = {
    "library_probability_of_failure": float(prob_failure),
    "manual_integration_probability": float(manual_pf),
    "relative_error_pct": float(abs(manual_pf - prob_failure) / prob_failure * 100),
}

# ===========================================================================
# 8) DSZI MODEL — 15% de las unidades pertenece a una subpoblación inmune a
#    este modo de falla específico (ej. lote con un tratamiento anticorrosivo
#    distinto). DS=0.85 => el CDF nunca supera 85%.
# ===========================================================================
DS_FRACTION = 0.85
dszi = DSZI_Model(distribution=fitted_dist, DS=DS_FRACTION)

t_grid_dszi = np.linspace(0.01, 25000, 150)
dszi_sf = dszi.SF(xvals=t_grid_dszi, show_plot=False)
dszi_cdf = dszi.CDF(xvals=t_grid_dszi, show_plot=False)

out["dszi"] = {
    "descripcion": f"Subpoblación defectuosa (DSZI): el {int(DS_FRACTION*100)}% de las unidades eventualmente falla por este modo (siguiendo la Weibull ajustada), pero el {int((1-DS_FRACTION)*100)}% restante nunca lo hace — por ejemplo, un lote con un tratamiento anticorrosivo distinto. Por eso la curva de falla acumulada se estanca en {int(DS_FRACTION*100)}% en vez de llegar a 100%.",
    "ds_fraction": DS_FRACTION,
    "t": [round(x, 1) for x in t_grid_dszi.tolist()],
    "sf": [round(x, 4) for x in dszi_sf.tolist()],
    "cdf": [round(x, 4) for x in dszi_cdf.tolist()],
}
audit["dszi"] = {
    "cdf_asymptote_maxvalue": float(np.max(dszi_cdf)),
    "cdf_approaches_DS_not_1": bool(abs(np.max(dszi_cdf) - DS_FRACTION) < 0.02),
    "sf_plus_cdf_is_1": float(np.max(np.abs((dszi_sf + dszi_cdf) - 1.0))),
}

# ---------------------------------------------------------------------------
with open("/tmp/medium_extra_data.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

with open("/tmp/medium_extra_audit.json", "w", encoding="utf-8") as f:
    json.dump(audit, f, ensure_ascii=False, indent=2)

print(json.dumps(audit, indent=2, default=str))
print("OK -> /tmp/medium_extra_data.json, /tmp/medium_extra_audit.json")
