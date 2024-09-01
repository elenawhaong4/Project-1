import pandas as pd
import streamlit as st
# import seaborn as sns
# from sklearn.metrics import mean_squared_error
# from statsmodels.formula.api import ols
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.tree import plot_tree
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
# import matplotlib.pyplot as plt
# import numpy as np
st.title("SHAPE project by Elena")

# Data
df = pd.read_csv('smmh.csv')
cols = ["Timestamp", "Age", "Gender", "Relationship", "Occupation", "Affiliation", "SocialMedia", "Types", "Time", "WithoutPurpose", "Distracted", "Restless", "drop1", "Worry", "drop2", "Compare", "drop3", "Validation","Depressed", "drop4", "Sleep"]
df.columns = cols
# df.set_axis(["Timestamp", "Age", "Gender", "Relationship", "Occupation", "Affiliation", "SocialMedia", "Types", "Time", "WithoutPurpose", "Distracted", "Restless", "drop1", "Worry", "drop2", "Compare", "drop3", "Validation","Depressed", "drop4", "Sleep"], axis = "columns", inplace = True)
df = df.drop(["drop1", "drop2", "drop3", "drop4", "SocialMedia", "Timestamp", "Affiliation", "Worry"], axis = 1)
df = df.sort_values(by = ["Age", "Gender", "Time"], ascending = [True, False, True]).reset_index(drop = True)
df.Time = df.Time.str.replace("More than 5 hours", "5.5").values
df.Time = df.Time.str.replace("Between 2 and 3 hours", "2.5").values
df.Time = df.Time.str.replace("Between 3 and 4 hours", "3.5").values
df.Time = df.Time.str.replace("Between 4 and 5 hours", "4.5").values
df.Time = df.Time.str.replace("Between 1 and 2 hours", "1.5").values
df.Time = df.Time.str.replace("Less than an Hour", "0.5").values
df = df[:480:]

malefilter = df.Gender == "Male"
femalefilter = df.Gender == "Female"
df = df[(malefilter|femalefilter)].reset_index(drop = True)

df_1 = df[["Age","Sleep"]]
insta = df.Types.str.contains("Instagram")
yt = df.Types.str.contains("YouTube")
disc = df.Types.str.contains("Discord")
red = df.Types.str.contains("Reddit")
twit = df.Types.str.contains("Twitter")
pint = df.Types.str.contains("Pinterest")
snap = df.Types.str.contains("Snapchat")
face = df.Types.str.contains("Facebook")
tik = df.Types.str.contains("TikTok")
type_series = pd.DataFrame({"Instagram":insta, "YouTube":yt, "Discord":disc, "Reddit":red, "Twitter":twit, "Pinterest": pint, "Snapchat": snap, "Facebook":face, "TikTok":tik})
boolean_df = pd.concat([df, type_series], axis = 1).drop(["Types"], axis=1)

channels = pd.get_dummies(df.Types.str.replace(" ","",regex=True).str.split(",").explode())

df_2 = pd.concat([df_1,channels],axis=1)
df_2 = df_2.set_index(["Age","Sleep"]).stack().reset_index()
df_2= df_2[df_2.iloc[:,-1]==1]
df_2 = df_2.reset_index(drop = True).drop(0, axis = 1)

df = pd.merge(df, df_2, how = "inner").drop("Types", axis = 1)
df = df.rename({"level_2":"Platform"}, axis = 1)

# Display data
if st.checkbox("Show raw data"):
  st.subheader("Raw data")
  st.write(df)
