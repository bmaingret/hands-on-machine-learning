# %% 
import pandas as pd
from chapter2.data import make_dataset
from chapter2 import conf
import matplotlib.pyplot as plt
import seaborn as sns


# %%
housing = make_dataset.load_data(conf.ROOT_DATA_DIR, conf.DataDirectory.RAW, "housing.csv")

# %%
housing.head()

# %%
housing.info()

# %%[markdown]

# Only numerical columns except `ocean_proximity`

# %%
housing["ocean_proximity"].value_counts()

# %%[markdown]

# 5 distinct values, with `ISLAND` having only 5 occurences over 20640 observations.

# %%
housing.describe()

# %%[markdown]

# Bedrooms and rooms are global values by district.
# 
# Median income is probably in k$.

# %%
housing.hist(bins=50, figsize=(20,15))

# %%
train, test = make_dataset.train_test_split(housing)
fig, ax = plt.subplots(nrows=len(train.columns), figsize=(8, 20))

for ix, column in enumerate(train.drop("ocean_proximity", axis=1).columns):
    sns.kdeplot(train[column], ax=ax.flat[ix])
    sns.kdeplot(test[column], ax=ax.flat[ix])
    
(pd.DataFrame({
    "train":train["ocean_proximity"].value_counts(normalize=True),
    "test":test["ocean_proximity"].value_counts(normalize=True)})
    .reset_index().rename(columns={"index":"ocean_proximity"})
    .pipe((pd.melt, "frame"), id_vars="ocean_proximity", var_name="train_test", value_name="percentage")
    .pipe((sns.barplot, "data"), hue="train_test", x="ocean_proximity", y="percentage", ax=ax.flat[-1], log=True)
)
ax.flat[-1].set_title("Log of percentage of value counts for ocean_proximity")
plt.tight_layout()

# %%
