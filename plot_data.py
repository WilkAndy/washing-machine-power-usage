import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read data
df = pd.read_csv("data.csv")

# Categories in the required plotting order:
# (cycle, temperature, label)
categories = [
    ("Super quick 15", None, "Super quick 15"),
    ("Super quick 30", None, "Super quick 30"),
    ("Mix eco",       30,   "Mix eco, 30degC"),
    ("Mix speed",     30,   "Mix speed, 30degC"),
    ("Cotton eco",    30,   "Cotton eco, 30degC"),
    ("Mix eco",       40,   "Mix eco, 40degC"),
    ("Mix speed",     40,   "Mix speed, 40degC"),
    ("Cotton eco",    40,   "Cotton eco, 40degC"),
    ("Cotton speed",  40,   "Cotton speed, 40degC"),
    ("Cotton speed",  60,   "Cotton speed, 60degC"),
]

data = []
labels = []

for cycle, temperature, label in categories:

    mask = df["Cycle"].eq(cycle)

    if temperature is not None:
        mask &= df["Temperature degC"].eq(temperature)

    # Ignore missing measurements
    values = df.loc[mask, "Power usage kWh"].dropna().to_numpy()

    data.append(values)
    labels.append(f"{label}.  n={len(values)}")


fig, ax = plt.subplots(figsize=(6, 6))

# ------------------------------------------------------------
# Background shading by temperature
# ------------------------------------------------------------

ax.axvspan(0.5, 2.5, color="royalblue", alpha=0.10, zorder=0)
ax.axvspan(2.5, 5.5, color="mediumpurple", alpha=0.10, zorder=0)
ax.axvspan(5.5, 9.5, color="lightcoral", alpha=0.10, zorder=0)
ax.axvspan(9.5, 10.5, color="red", alpha=0.10, zorder=0)

# ------------------------------------------------------------
# Box and whisker plots
# ------------------------------------------------------------

ax.boxplot(
    data,
    tick_labels=labels,
    widths=0.8,

    # Mean
    showmeans=True,
    meanline=True,
    meanprops=dict(
        color="red",
        linewidth=2
    ),

    # Median
    medianprops=dict(
        color="blue",
        linewidth=2
    ),

    # Box and whiskers
    boxprops=dict(
        color="black"
    ),
    whiskerprops=dict(
        color="black"
    ),
    capprops=dict(
        color="black"
    ),

    # Outliers
    showfliers=False,
)


# ------------------------------------------------------------
# Plot every individual sample as a black dot
# ------------------------------------------------------------

rng = np.random.default_rng(12345)

for x, values in enumerate(data, start=1):
    jitter = (0 if len(values) < 10 else 0.02)
    jitter = rng.uniform(-jitter, jitter, size=len(values))

    ax.scatter(
        x + jitter,
        values,
        marker="o",
        s=10,
        facecolor="black",
        edgecolor="black",
        zorder=3
    )


# ------------------------------------------------------------
# Axis labels
# ------------------------------------------------------------

ax.set_xticks(range(1, len(labels) + 1))
ax.set_xticklabels(
    labels,
    rotation=45,
    ha="right"
)

ax.set_ylabel("Power (kWh)")
ax.set_ylim([0, ax.get_ylim()[1]])

ax.grid(axis="y", alpha=0.25)

plt.title("Bosch washing machine power usage")
plt.tight_layout()
plt.savefig("plot_data.png", bbox_inches="tight")
plt.show()



# ------------------------------------------------------------
# Statistical comparison: Mix speed vs Mix eco at 40 degC
# ------------------------------------------------------------
from scipy import stats

eco = df.loc[
    df["Cycle"].eq("Mix eco") & df["Temperature degC"].eq(40),
    "Power usage kWh"
].dropna()

speed = df.loc[
    df["Cycle"].eq("Mix speed") & df["Temperature degC"].eq(40),
    "Power usage kWh"
].dropna()

mean_eco = eco.mean()
mean_speed = speed.mean()
sd_eco = eco.std(ddof=1)
sd_speed = speed.std(ddof=1)

# Welch's t-test
test = stats.ttest_ind(speed, eco, equal_var=False)

# Difference and 95% CI: speed - eco
diff = mean_speed - mean_eco
se = np.sqrt(sd_speed**2 / len(speed) + sd_eco**2 / len(eco))

df_welch = (
    (sd_speed**2 / len(speed) + sd_eco**2 / len(eco))**2
    / (
        (sd_speed**2 / len(speed))**2 / (len(speed) - 1)
        + (sd_eco**2 / len(eco))**2 / (len(eco) - 1)
    )
)

tcrit = stats.t.ppf(0.975, df_welch)
ci_low = diff - tcrit * se
ci_high = diff + tcrit * se

print("\nMix speed vs Mix eco at 40degC")
print(f"Mix speed: mean = {mean_speed:.3f} kWh, SD = {sd_speed:.3f}, n = {len(speed)}")
print(f"Mix eco:   mean = {mean_eco:.3f} kWh, SD = {sd_eco:.3f}, n = {len(eco)}")
print(f"Difference in means (speed - eco) = {diff:.3f} kWh")
print(f"95% CI for difference = [{ci_low:.3f}, {ci_high:.3f}] kWh")
print(f"Welch t-test: t = {test.statistic:.3f}, df = {df_welch:.1f}, p = {test.pvalue:.4g}")
