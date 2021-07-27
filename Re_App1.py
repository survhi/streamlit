# Core Pkg
import streamlit as st
import streamlit.components.v1 as stc

# Load EDA
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer 
from PIL import Image   

# Load our Dataset
df = pd.read_excel(r"C:/Users/shree/OneDrive/Desktop/New folder/Cluster_dataset2.xlsx")

tfidf = TfidfVectorizer(stop_words = "english")
tfidf_matrix = tfidf.fit_transform(df.Insurance_Provider_Name)
cosine_sim_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
    
# Recommendation sys
def get_recommendations(policy_select, num_of_recc=5):   
    
    policy_index = pd.Series(df.index, index = df['Insurance_Provider_Name']).drop_duplicates()
    policy_id = policy_index[policy_select]
    
    policy_id = policy_index[policy_select]
    cosine_scores = list(enumerate(cosine_sim_matrix[policy_id]))
    
    cosine_scores = sorted(cosine_scores, key=lambda x:x[1], reverse = True)
    cosine_scores_N = cosine_scores[0: num_of_recc]
    
    policy_idx  =  [i[0] for i in cosine_scores_N]
    policy_scores =  [i[1] for i in cosine_scores_N]
    
    policy_similar_show = pd.DataFrame(columns=["Insurance_Provider_Name", "Score"])
    policy_similar_show["Insurance_Provider_Name"] = df.loc[policy_idx, "Insurance_Provider_Name"]
    policy_similar_show["Score"] = policy_scores
    policy_similar_show.reset_index(inplace = True)  
    
    policy_similar_show.drop(["index"], axis=1, inplace=True)
    print (policy_similar_show)
    
    # Get the dataframe & title 
    result_df = df.iloc[policy_idx]
    final_recc = result_df[['Insurance_Provider_Name','Premium']]
    return final_recc

# CSS Style 
RESULT_TEMP = """
<div style="width:90%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 60px;
box-shadow:0 0 15px 5px #ccc; background-color: #a8f0c6;
  border-left: 5px solid #6c6c6c;">
<h4>{}</h4>
<p style="color:blue;"><span style="color:black;">💲Premium:: </span>{}</p>
</div>
"""
img = Image.open("C:/Users/shree/OneDrive/Desktop/New folder/innodatatics.png")
st.image(img)

def main():
    html_temp = """
<div style="background-color:tomato;padding:10px">
<h2 style="color:white;text-align:center;"> Group Health Insurance Policy Recommendation App </h2>
</div>
"""
    st.markdown(html_temp,unsafe_allow_html=True)
    
    menu = ["Home", "Recommend Policies", "About"]
    options = st.sidebar.selectbox("Menu", menu)
    
    if options =="Home":
        st.subheader("Home")
    
    elif options == "Recommend Policies":
        st.subheader("Recommend Policies")
        feature_name = st.selectbox("Select a Feature", ("Select ","Premium"))
        policy_select = st.selectbox("Select Your Previous Policy", (df.Insurance_Provider_Name))
        num_of_recc = st.sidebar.number_input("Number", 1, 5, 1)
        if st.button("Recommend"):
            if feature_name == "Premium":
                try:
                    results = get_recommendations(policy_select, num_of_recc)
                    for row in results.iterrows():
                        rec_title = row[1][0]
                        rec_prem = row[1][1]
                    
                        #st.write("Insurance Provider Name and Product", rec_title)
                        stc.html(RESULT_TEMP.format(rec_title, rec_prem), height=120)
                    
                except:
                    results = "Not Found"
                
                
    else:
        st.subheader("Built with Streamlit")
           
if __name__ == '__main__':
    main()

