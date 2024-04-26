import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from sklearn import metrics
 
#f = 'datos/standerdscaler/standersscalerattackbeforeprediction0.csv'
f = 'datos/bothnormalization/bothnormailzerattackbeforeprediction2.csv'
df = pd.read_csv(f, sep=",") 
a = df.values
datos_entrada = a[:, 1:]
 
#f = 'datos/standerdscaler/standersscalerattackpredicted0.csv'
f = 'datos/bothnormalization/bothnormailzerattackpredicted2.csv'
df = pd.read_csv(f, sep=",") 
a = df.values
datos_salida = a[:, 1:]
 
print(datos_entrada.shape)
print(datos_salida.shape)
 
mse_attack = np.sum((datos_entrada - datos_salida)**2, axis=1)
print(mse_attack.shape)
 
mse_plot = mse_attack[mse_attack<100]
 
binwidth = 0.2
plt.figure(figsize=(18, 6))
plt.subplot(1, 3, 1)
plt.hist(mse_plot, bins=np.arange(np.min(mse_plot), np.max(mse_plot) + binwidth, binwidth))
plt.axis([0, 10, 0, 10000])
plt.title("Attack")
 
x = np.arange(0, 100, 0.1)[:, None]
kde = KernelDensity(kernel="gaussian", bandwidth=0.25).fit(mse_plot[:, None])
log_dens_attack = kde.score_samples(x)
 
plt.plot(x, mse_plot.shape[0]*binwidth*np.exp(log_dens_attack), linewidth=2)
 
#f = 'datos/standerdscaler/standersscalernormalbeforeprediction0.csv'
f = 'datos/bothnormalization/bothnormailzernormalbeforeprediction2.csv'
df = pd.read_csv(f, sep=",") 
a = df.values
datos_entrada = a[:, 1:]
 
#f = 'datos/standerdscaler/standersscalernormalpredicted0.csv'
f = 'datos/bothnormalization/bothnormailzernormalpredicted2.csv'
df = pd.read_csv(f, sep=",") 
a = df.values
datos_salida = a[:, 1:]
 
print(datos_entrada.shape)
print(datos_salida.shape)
 
mse_normal = np.sum((datos_entrada - datos_salida)**2, axis=1)
print(mse_normal.shape)
 
mse_plot = mse_normal[mse_normal<100]
 
plt.subplot(1, 3, 2)
plt.hist(mse_plot, bins=np.arange(np.min(mse_plot), np.max(mse_plot) + binwidth, binwidth))
plt.axis([0, 10, 0, 10000])
plt.title("Normal")
 
kde = KernelDensity(kernel="gaussian", bandwidth=0.25).fit(mse_plot[:, None])
log_dens_normal = kde.score_samples(x)
 
plt.plot(x, mse_plot.shape[0]*binwidth*np.exp(log_dens_normal), linewidth=2)
 
plt.subplot(1, 3, 3)
plt.plot(x, np.exp(log_dens_attack), linewidth=2)
plt.plot(x, np.exp(log_dens_normal), linewidth=2)
plt.axis([0, 10, 0, 0.5])
plt.legend(["attack", "normal"])
 
 
mse = np.concatenate((mse_normal, mse_attack))
target = np.concatenate((np.zeros_like(mse_normal), np.ones_like(mse_attack)))
print(mse.shape)
print(target.shape)
 
 
fpr, tpr, thresholds = metrics.roc_curve(target, mse, pos_label=1)
auc = metrics.roc_auc_score(target, mse)
plt.figure()
plt.plot(fpr, tpr)
plt.grid(True)
plt.title(f"AUC = {auc}")
plt.xlabel("FPR")
plt.ylabel("TPR")
 
precision, recall, thresholds = metrics.precision_recall_curve(target, mse, pos_label=1)
auc = metrics.auc(recall, precision)
plt.figure()
plt.plot(recall, precision)
plt.grid(True)
plt.title(f"AUC = {auc}")
plt.xlabel("recall")
plt.ylabel("precision")
 
 
plt.show()