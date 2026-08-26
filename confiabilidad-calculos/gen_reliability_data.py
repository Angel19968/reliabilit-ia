"""
Genera datos precalculados (JSON) para la nueva sección "Confiabilidad Cálculos"
del sitio RELIABILIT-IA, usando la librería Python `reliability`.

Datos sintéticos ilustrativos: tiempos de falla (en horas de operación) de una
población simulada de un componente rotativo (ej. rodamiento), declarados como
tales en la página — misma convención que el resto del sitio.

Curvas generadas (las 3 "simples": curva única o escalón, ejes lineales):
  1. Weibull — ajuste paramétrico: función de confiabilidad R(t), probabilidad
     de falla acumulada F(t) y densidad de falla f(t).
  2. Kaplan-Meier — estimador no paramétrico de supervivencia (función escalón),
     incluye datos censurados (equipos que siguen operando sin haber fallado).
  3. Nelson-Aalen — estimador no paramétrico de riesgo acumulado (función escalón).

Salida: reliability_data.json
"""
import json
import numpy as np

np.random.seed(42)

from reliability.Fitters import Fit_Weibull_2P
from reliability.Nonparametric import KaplanMeier, NelsonAalen

# ---------------------------------------------------------------------------
# 1) Datos sintéticos: 40 unidades, tiempos de falla (horas) simulados a partir
#    de una Weibull real (beta=2.3, eta=9200h) típica de desgaste mecánico
#    progresivo, más un 20% de datos censurados (equipos aún en operación).
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

failures = []
right_censored = []
for i, t in enumerate(all_times):
    if i in censored_idx:
        # unidad retirada/observada antes de fallar -> tiempo censurado algo menor
        ct = round(t * np.random.uniform(0.5, 0.95), 0)
        right_censored.append(float(ct))
    else:
        failures.append(float(t))

failures = sorted(failures)
right_censored = sorted(right_censored)

# ---------------------------------------------------------------------------
# 2) Ajuste Weibull (paramétrico) con censura
# ---------------------------------------------------------------------------
fit = Fit_Weibull_2P(failures=failures, right_censored=right_censored, show_probability_plot=False, print_results=False)
beta_hat = float(fit.beta)
eta_hat = float(fit.alpha)

t_grid = np.linspace(0.01, max(failures + right_censored) * 1.15, 120)
R = np.exp(-(t_grid / eta_hat) ** beta_hat)          # confiabilidad / supervivencia
F = 1 - R                                             # probabilidad de falla acumulada
f = (beta_hat / eta_hat) * (t_grid / eta_hat) ** (beta_hat - 1) * R  # densidad de falla

weibull_curve = {
    "beta": round(beta_hat, 3),
    "eta": round(eta_hat, 1),
    "t": [round(x, 1) for x in t_grid.tolist()],
    "reliability": [round(x, 4) for x in R.tolist()],
    "cdf": [round(x, 4) for x in F.tolist()],
    "pdf": [round(x, 6) for x in f.tolist()],
}

# ---------------------------------------------------------------------------
# 3) Kaplan-Meier (no paramétrico, con censura)
# ---------------------------------------------------------------------------
km = KaplanMeier(failures=failures, right_censored=right_censored, print_results=False, show_plot=False)
km_time = [0.0] + [float(x) for x in km.xvals]
km_surv = [1.0] + [float(x) for x in km.SF]
km_lower = [1.0] + [float(x) if x == x else None for x in km.SF_lower]
km_upper = [1.0] + [float(x) if x == x else None for x in km.SF_upper]

kaplan_meier = {
    "t": km_time,
    "survival": km_surv,
    "ci_lower": km_lower,
    "ci_upper": km_upper,
    "censor_times": right_censored,
}

# ---------------------------------------------------------------------------
# 4) Nelson-Aalen (no paramétrico, riesgo acumulado, con censura)
# ---------------------------------------------------------------------------
na = NelsonAalen(failures=failures, right_censored=right_censored, print_results=False, show_plot=False)
na_time = [0.0] + [float(x) for x in na.xvals]
na_cumhaz = [0.0] + [float(x) for x in na.CHF]

nelson_aalen = {
    "t": na_time,
    "cumulative_hazard": na_cumhaz,
    "censor_times": right_censored,
}

# ---------------------------------------------------------------------------
out = {
    "meta": {
        "descripcion": "Datos sintéticos ilustrativos (no productivos reales): 40 unidades simuladas de un componente rotativo, tiempos de falla en horas de operación. Calculado con la librería Python 'reliability' (scipy-based), precalculado offline y graficado a mano en SVG.",
        "n_unidades": N,
        "n_fallas": len(failures),
        "n_censurados": len(right_censored),
    },
    "weibull": weibull_curve,
    "kaplan_meier": kaplan_meier,
    "nelson_aalen": nelson_aalen,
}

with open("/tmp/reliability_data.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)

print("beta_hat=", beta_hat, "eta_hat=", eta_hat)
print("failures:", len(failures), "censored:", len(right_censored))
print("KM points:", len(km_time), "NA points:", len(na_time))
print("OK -> /tmp/reliability_data.json")
