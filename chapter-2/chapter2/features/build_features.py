from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(handle_unknown='ignore')
encoder.fit(housing_train[["ocean_proximity"]])
encoder.categories_
