# %% 
from re import M
from chapter2.data import make_dataset
from chapter2 import conf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_regression
from sklearn.impute import SimpleImputer
import pandas as pd


# %%
housing_train = make_dataset.load_data(conf.ROOT_DATA_DIR, conf.DataDirectory.INTERIM, "housing_train.csv")
housing_train = housing_train.drop("index", axis=1)
housing_train.describe().transpose()

# %%[markdown]

# ## Rooms and bedrooms

# %%

housing_train["rooms_per_household"] = housing_train["total_rooms"]/housing_train["households"]
housing_train["bedrooms_per_household"] = housing_train["total_bedrooms"]/housing_train["households"]
housing_train["bedrooms_room_ratio"] = housing_train["total_bedrooms"]/housing_train["total_rooms"]
housing_train.corr()["median_house_value"].abs().sort_values(ascending=False)
# %%
sns.pairplot(housing_train.loc[:, ["median_house_value", "median_income", "bedrooms_room_ratio", "rooms_per_household"]])

# %%[markdown]

# ## Numerical vs Categorical

# %%
num_cols = [col for col in housing_train.columns if housing_train[col].dtype in ["int64","float64"]]
cat_cols = [col for col in housing_train.columns if housing_train[col].dtype == "object"]
y_name = "median_house_value"
y = housing_train[y_name]

num_df = housing_train[num_cols]
cat_df = housing_train[cat_cols]

# %%
num_df.nunique()


# %%[markdown]

# ## Missing value_counts

# %%
housing_train.isna().sum()

# %%
mask = housing_train.isna()["total_bedrooms"]

fig, ax = plt.subplots(1,1)
sns.kdeplot(housing_train["median_house_value"], ax=ax)
sns.kdeplot(housing_train.loc[mask, "median_house_value"], ax=ax)
fig.legend(["full data", "missing total_bedrooms"])

# %%
imputer = SimpleImputer(strategy="median")
num_df_imputed = pd.DataFrame(imputer.fit_transform(num_df), columns=num_df.columns)


# %%[markdown]

# ## Univariate feature model_selection

# %%
def mir_score(X, y, discrete_features=False):
    mir_score = mutual_info_regression(X, y, discrete_features=discrete_features, random_state=0)
    mir_score = pd.Series(mir_score, name="MIR_SCORE", index=X.columns)
    mir_score = mir_score.sort_values(ascending=False)
    return mir_score

# %%

mir_num = mir_score(num_df_imputed.drop(y_name, axis=1), y)
mir_num

# %%
mir_cat = mir_score(cat_df["ocean_proximity"].factorize(), y, discrete_features=True)
mir_cat

# %%
pd.get_dummies(cat_df["ocean_proximity"])
mir_cat = mir_score(, y, discrete_features=True)
mir_cat

# %%
