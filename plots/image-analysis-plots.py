import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import numpy as np


data = pd.read_csv("./plots/media_joined_with_tweets-16-dec.csv")
data = data.dropna()

print(data.shape)


a_dict = {}
w_dict = {}
p_dict = {}


for val in data["a_hash"].unique():
    a_dict[val] = 0

for val in data["w_hash"].unique():
    w_dict[val] = 0

for val in data["p_hash"].unique():
    p_dict[val] = 0


for val in data["a_hash"]:
    a_dict[val] += 1

for val in data["w_hash"]:
    w_dict[val] += 1

for val in data["p_hash"]:
    p_dict[val] += 1


a_vals = sorted(a_dict.values(), reverse=True)
w_vals = sorted(w_dict.values(), reverse=True)
p_vals = sorted(p_dict.values(), reverse=True)


print("a_vals:", len(a_vals), sum(a_vals), a_vals[:500])
print("w_vals:", len(w_vals), sum(w_vals), w_vals[:500])
print("p_vals:", len(p_vals), sum(p_vals), p_vals[:500])


rc_params = {
    "pgf.rcfonts": False,
    "pgf.texsystem": "pdflatex",
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": "Times",
}
rc_params["axes.labelsize"] = 30
rc_params["xtick.labelsize"] = 30
rc_params["ytick.labelsize"] = 30
sns.set(rc=rc_params)
sns.set_style("whitegrid")

style = {
"pgf.rcfonts":False,
"pgf.texsystem": "pdflatex",   
"text.usetex": True,                
"font.family": "serif",
"font.serif": "Times"
}
#set
sns.set_style(style)

fig, ax = plt.subplots()


y_a = []
cumulative = 0
for num_of_appearances in a_vals:
    cumulative += num_of_appearances
    y_a.append(cumulative)
plt.plot(y_a, label="aHash", color="#fc4c4c", linewidth=5.05)  # ff2f2f

y_w = []
cumulative = 0
for num_of_appearances in w_vals:
    cumulative += num_of_appearances
    y_w.append(cumulative)
plt.plot(
    y_w, label="wHash", color="#af0000", linewidth=4.75, linestyle="dashed"
)  # 960000

y_p = []
cumulative = 0
for num_of_appearances in p_vals:
    cumulative += num_of_appearances
    y_p.append(cumulative)
plt.plot(
    y_p, label="pHash", color="#e20000", linewidth=4.85, linestyle="dotted"
)  # e10000

ax.axhline(y=167696, linewidth=5, color="#000000")  # color='#676666'
plt.text(2750, 154000, "Total number of images = 167,696", fontsize=46, color="#000000")


ax.legend(fontsize=42, loc="lower right")
plt.xlabel(
    "Rank of image (i.e. unique hash)", fontsize=54, fontweight="bold"
)  # (a unique perceptual hash value)
plt.ylabel("Cumulative \# of matches", fontsize=54, fontweight="bold")

ylabel = [str(0), str(0)]
ylabel += [str(i) + "K" for i in range(25, 200, 25)]
print(ylabel)
ax.set_yticklabels(ylabel, fontsize=44)

xlabel = [str(0), str(0)]
xlabel += [str(i) + "K" for i in range(20, 120, 20)]
print(xlabel)
ax.set_xticklabels(xlabel, fontsize=44)
ax.xaxis.labelpad = 30
ax.yaxis.labelpad = 30

# fig.savefig("./images.pdf", bbox_inches='tight')
plt.show()
