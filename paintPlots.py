import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from sklearn import metrics

DOCUMENTS_PATH = "documents/"
STATS_FILE = "rewritten_spanish_abstracts_stats.txt"

stats_file = open(DOCUMENTS_PATH + STATS_FILE, "r", encoding='utf-8')

original_stats = {
    "Palabras": [],
    "Palabras Distintas": [],
    ",": [],
    ".": [],
    ";": [],
    ":": [],
    "-": [],
    "Frases": [],
}
chatGPT_stats = {
	"Palabras": [],
    "Palabras Distintas": [],
    ",": [],
    ".": [],
    ";": [],
    ":": [],
    "-": [],
    "Frases": [],
}

if __name__ == '__main__':
    stats_rows = stats_file.readlines()
    
    for stats_row in stats_rows:
        stats = json.loads(stats_row[:-2])
        
        original_stats["Palabras"].append(stats["Resumen"]["Palabras"]["Cantidad"])
        original_stats["Palabras Distintas"].append(stats["Resumen"]["Palabras"]["Num_Distintas"])
        original_stats[","].append(stats["Resumen"]["Signos"][","])
        original_stats["."].append(stats["Resumen"]["Signos"]["."])
        original_stats[";"].append(stats["Resumen"]["Signos"][";"])
        original_stats[":"].append(stats["Resumen"]["Signos"][":"])
        original_stats["-"].append(stats["Resumen"]["Signos"]["-"])
        original_stats["Frases"].append(stats["Resumen"]["Frases"]["Cantidad"])
        
        chatGPT_stats["Palabras"].append(stats["Resumen_ChatGPT"]["Palabras"]["Cantidad"])
        chatGPT_stats["Palabras Distintas"].append(stats["Resumen_ChatGPT"]["Palabras"]["Num_Distintas"])
        chatGPT_stats[","].append(stats["Resumen_ChatGPT"]["Signos"][","])
        chatGPT_stats["."].append(stats["Resumen_ChatGPT"]["Signos"]["."])
        chatGPT_stats[";"].append(stats["Resumen_ChatGPT"]["Signos"][";"])
        chatGPT_stats[":"].append(stats["Resumen_ChatGPT"]["Signos"][":"])
        chatGPT_stats["-"].append(stats["Resumen_ChatGPT"]["Signos"]["-"])
        chatGPT_stats["Frases"].append(stats["Resumen_ChatGPT"]["Frases"]["Cantidad"])

# #### Palabras       
# palabras_original = np.array(original_stats["Palabras"])
# palabras_chatGPT = np.array(chatGPT_stats["Palabras"])
# # mse_palabras = np.sum((palabras_original - palabras_chatGPT)**2, axis=1)

# plt.figure()
# plt.title("Numero de palabras")

# plt.plot(palabras_original[:1400], palabras_chatGPT[:1400], 'o', linewidth=2, label="Original")
# plt.plot(palabras_chatGPT, palabras_chatGPT, 'r')
# # plt.plot(palabras_chatGPT, linewidth=2, label="ChatGPT")
# plt.legend()

# ##### Palabras distintas
# distintas_original = np.array(original_stats["Palabras Distintas"])
# distintas_chatGPT = np.array(chatGPT_stats["Palabras Distintas"])
# # mse_palabras = np.sum((palabras_original - palabras_chatGPT)**2, axis=1)

# plt.figure()
# plt.title("Numero de palabras distintas")

# plt.plot(distintas_original, linewidth=2, label="Original")
# plt.plot(distintas_chatGPT, linewidth=2, label="ChatGPT")
# plt.legend()

# #### Frases
# frases_original = np.array(original_stats["Frases"])
# frases_chatGPT = np.array(chatGPT_stats["Frases"])
# # mse_palabras = np.sum((palabras_original - palabras_chatGPT)**2, axis=1)

# plt.figure()
# plt.title("Numero de frases")

# plt.plot(frases_original, linewidth=2, label="Original")
# plt.plot(frases_chatGPT, linewidth=2, label="ChatGPT")
# plt.legend()

original = np.array(original_stats["Palabras"][:1400])
chatGPT = np.array(chatGPT_stats["Palabras"][:1400])
binwidth = 10
# mse_normal = np.sum((palabras_original - palabras_chatGPT)**2, axis=1)


plt.figure()
plt.hist(original, bins=np.arange(0, 600, binwidth))
plt.title("Original")

x = np.arange(0, 600, binwidth)[:, None]
kde = KernelDensity(kernel="gaussian", bandwidth=10).fit(original[:, None])
log_dens_original = kde.score_samples(x)

plt.plot(x, binwidth * 1400 * np.exp(log_dens_original))

plt.figure()
plt.hist(chatGPT, bins=np.arange(0, 600, binwidth))
plt.title("ChatGPT")

kde = KernelDensity(kernel="gaussian", bandwidth=10).fit(chatGPT[:, None])
log_dens_chatGPT = kde.score_samples(x)

plt.plot(x, binwidth * 1400 * np.exp(log_dens_chatGPT))

plt.figure()
plt.plot(x, binwidth * 1400 * np.exp(log_dens_original), label="original")
plt.plot(x, binwidth * 1400 * np.exp(log_dens_chatGPT), label="chatGPT")
plt.legend()

plt.show()

# #f = 'datos/standerdscaler/standersscalernormalbeforeprediction0.csv'
# f = 'datos/bothnormalization/bothnormailzernormalbeforeprediction2.csv'
# df = pd.read_csv(f, sep=",") 
# a = df.values
# datos_entrada = a[:, 1:]
 
# #f = 'datos/standerdscaler/standersscalernormalpredicted0.csv'
# f = 'datos/bothnormalization/bothnormailzernormalpredicted2.csv'
# df = pd.read_csv(f, sep=",") 
# a = df.values
# datos_salida = a[:, 1:]
 
# print(datos_entrada.shape)
# print(datos_salida.shape)
 
# mse_normal = np.sum((datos_entrada - datos_salida)**2, axis=1)
# print(mse_normal.shape)
 
# mse_plot = mse_normal[mse_normal<100]
 
# plt.subplot(1, 3, 2)
# plt.hist(mse_plot, bins=np.arange(np.min(mse_plot), np.max(mse_plot) + binwidth, binwidth))
# plt.axis([0, 10, 0, 10000])
# plt.title("Normal")
 
# kde = KernelDensity(kernel="gaussian", bandwidth=0.25).fit(mse_plot[:, None])
# log_dens_normal = kde.score_samples(x)
 
# plt.plot(x, mse_plot.shape[0]*binwidth*np.exp(log_dens_normal), linewidth=2)
 
# plt.subplot(1, 3, 3)
# plt.plot(x, np.exp(log_dens_attack), linewidth=2)
# plt.plot(x, np.exp(log_dens_normal), linewidth=2)
# plt.axis([0, 10, 0, 0.5])
# plt.legend(["attack", "normal"])
 
 
# mse = np.concatenate((mse_normal, mse_palabras))
# target = np.concatenate((np.zeros_like(mse_normal), np.ones_like(mse_palabras)))
# print(mse.shape)
# print(target.shape)
 
 
# fpr, tpr, thresholds = metrics.roc_curve(target, mse, pos_label=1)
# auc = metrics.roc_auc_score(target, mse)
# plt.figure()
# plt.plot(fpr, tpr)
# plt.grid(True)
# plt.title(f"AUC = {auc}")
# plt.xlabel("FPR")
# plt.ylabel("TPR")
 
# precision, recall, thresholds = metrics.precision_recall_curve(target, mse, pos_label=1)
# auc = metrics.auc(recall, precision)
# plt.figure()
# plt.plot(recall, precision)
# plt.grid(True)
# plt.title(f"AUC = {auc}")
# plt.xlabel("recall")
# plt.ylabel("precision")
 
 
# plt.show()