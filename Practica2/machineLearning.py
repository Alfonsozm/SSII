import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

with open("users_IA_clases.json", "r") as file:
    data = json.load(file)

usernames = []
received = []
clicks = []
vuln = []
for user in data["usuarios"]:
    usernames = usernames + [user["usuario"]]
    received = received + [user["emails_phishing_recibidos"]]
    clicks = clicks + [user["emails_phishing_clicados"]]
    vuln = vuln + [user["vulnerable"]]

df_data = pd.DataFrame()
df_data["usernames"] = usernames
df_data["received"] = received
df_data["clicks"] = clicks
df_vuln = pd.DataFrame()
df_vuln["vulnerable"] = vuln
df_data= df_data.to_numpy()
print(df_data)
#print(df.loc["sergio.garcia"])


# Use only one feature
#df_data = df_data[:, np.newaxis, 2]
# Split the data into training/testing sets
#df_data_train = df_data[:-20]
#df_data_test = df_data[-20:]
## Split the targets into training/testing sets
#df_vuln_train = df_vuln[:-20]
#df_vuln_test = df_vuln[-20:]
#
## Create linear regression object
#regr = linear_model.LinearRegression()
## Train the model using the training sets
#regr.fit(df_data_train, df_vuln_train)
## Make predictions using the testing set
#df_vuln_pred = regr.predict(df_data_test)
## The mean squared error
#print("Mean squared error: %.2f" % mean_squared_error(df_vuln_test,
#df_vuln_pred))
#
## Plot outputs
#plt.scatter(df_data_test, df_vuln_test, color=
#"black")
#plt.plot(df_data_test, df_vuln_pred, color="blue", linewidth=3)
#plt.xticks(())
#plt.yticks(())
#plt.show()