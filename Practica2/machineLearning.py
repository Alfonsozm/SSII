import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from sklearn import datasets, linear_model, tree
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
from sklearn.datasets import load_iris
from subprocess import call
import graphviz

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
df_data["received"] = received
df_data["clicks"] = clicks
for index, row in df_data.iterrows():
    if row["received"] != 0:
        df_data._set_value(index, "prob_click", row["clicks"] / row["received"])
    else:
        df_data._set_value(index, "prob_click", 0)
df_vuln = pd.DataFrame()
df_vuln["vulnerable"] = vuln
df_data = df_data.to_numpy()

# Use only one feature
df_data = df_data[:, np.newaxis, 2]
# Split the data into training/testing sets
df_data_train = df_data[:-15]
#print(df_data[:-15])
df_data_test = df_data[-15:]
# Split the targets into training/testing sets
df_vuln_train = df_vuln[:-15]
df_vuln_test = df_vuln[-15:]

## Create linear regression object
regr = linear_model.LinearRegression()
# Train the model using the training sets
regr.fit(df_data_train, df_vuln_train)
# Make predictions using the testing set
df_vuln_pred = regr.predict(df_data_test)

# The mean squared error
print("Linear Regression mean squared error: %.2f" % mean_squared_error(df_vuln_test, df_vuln_pred))
#
## Plot outputs
plt.scatter(df_data_test, df_vuln_test, color="black")
plt.plot(df_data_test, df_vuln_pred, color="blue", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()

# Decision Tree
# Split data
X, y = df_data_train, df_vuln_train
clf_model = tree.DecisionTreeClassifier()
clf_model.fit(X, y)

# Random forest
clf = RandomForestClassifier(max_depth=2, random_state=0, n_estimators=10)
clf.fit(X, y.values.ravel())

#Predictions from real data
with open("users_IA_predecir.json", "r") as file:
    data = json.load(file)

usernames = []
received = []
clicks = []
for user in data["usuarios"]:
    usernames = usernames + [user["usuario"]]
    received = received + [user["emails_phishing_recibidos"]]
    clicks = clicks + [user["emails_phishing_clicados"]]

df_data = pd.DataFrame()
df_data["received"] = received
df_data["clicks"] = clicks
for index, row in df_data.iterrows():
    if row["received"] != 0:
        df_data._set_value(index, "prob_click", row["clicks"] / row["received"])
    else:
        df_data._set_value(index, "prob_click", 0)
df_data = df_data.to_numpy()
df_data = df_data[:, np.newaxis, 2]

#Regression
print(regr.predict(df_data))

#Decision tree
print("Decision tree .predict", clf_model.predict(df_data))
# Print plot
dot_data = tree.export_graphviz(clf_model, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("tree")
dot_data = tree.export_graphviz(clf_model, out_file=None,
                                filled=True, rounded=True,
                                special_characters=True)
graph = graphviz.Source(dot_data)
graph.render('tree.gv', view=True).replace('\\', '/')

#Random forest
print("Random forest .predict", clf.predict(df_data))
for i in range(len(clf.estimators_)):
    estimator = clf.estimators_[i]
    export_graphviz(estimator,
                    out_file='forest.dot',
                    rounded=True, proportion=False,
                    precision=2, filled=True)
    call(['dot', '-Tpng', 'forest.dot', '-o', 'forest' + str(i) + '.png', '-Gdpi=600'])

