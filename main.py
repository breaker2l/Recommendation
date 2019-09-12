#Finding similar places
import pandas as pd

r_cols = ["Host_id" ,"Host_Location" , "Rating"]
ratings = pd.read_csv('' , sep='\t' , names=r_cols,usecols=range(3))

m_cols = [""
