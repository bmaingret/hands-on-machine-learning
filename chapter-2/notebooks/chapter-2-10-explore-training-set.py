# %%
from re import M
from chapter2.data import make_dataset
from chapter2 import conf
import matplotlib.pyplot as plt
import seaborn as sns


# %%
housing_train = make_dataset.load_data(
    conf.ROOT_DATA_DIR, conf.DataDirectory.INTERIM, "housing_train.csv"
)
housing_train = housing_train.drop("index", axis=1)
housing_train.describe()

# %%[markdown]

# ## Target variables

# %%
housing_train["median_house_value"].value_counts().sort_values(
    ascending=False
).nlargest(20)

# %%[markdown]

# ## Focus on most promising variables

# %%
housing_train.corr()["median_house_value"].sort_values(ascending=False)

# %%
sns.pairplot(
    housing_train.loc[
        :, ["median_house_value", "median_income", "total_rooms", "housing_median_age"]
    ]
)

# %%[markdown]

# ### Median income
# %%
plt.figure(figsize=(15, 15))
sns.scatterplot(data=housing_train, x="median_income", y="median_house_value")

# %%[markdown]

# ### Median age

# %%
plt.figure(figsize=(15, 15))
sns.histplot(data=housing_train, x="housing_median_age")

# %%[markdown]

# ## Geographic variables

# %%
plt.figure(figsize=(15, 15))
sns.scatterplot(
    data=housing_train,
    x="longitude",
    y="latitude",
    hue="ocean_proximity",
    size="median_house_value",
    sizes=(10, 400),
    alpha=0.5,
)


# %%
ax = sns.boxplot(x="ocean_proximity", y="median_house_value", data=housing_train)
val_count = housing_train["ocean_proximity"].value_counts()
new_xticks = [
    f"{xtick.get_text()} \n ({val_count[xtick.get_text()]} obs)"
    for xtick in ax.get_xticklabels()
]
ax.set_xticklabels(new_xticks)
plt.tight_layout()

# %%
ax = sns.histplot(x="ocean_proximity", y="median_house_value", data=housing_train)

# %%
