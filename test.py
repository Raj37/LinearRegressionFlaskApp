"""
 Created on 9:37 PM 7/14/2020 using PyCharm
 
 @author: Raj
"""
import pickle
import pandas as pd
loaded_model = pickle.load(open("finalized_model.pickle", 'rb')) # loading the model file from the storage
scalar = pickle.load(open('scalar_model.pickle', 'rb')) # loading the scalar model file from the storage
# predictions using the loaded model file
input_variables = pd.DataFrame([[337,118,4,4.5,4.5,9.65,1]],
                                    columns=['GRE Score','TOEFL Score','University Rating','SOP','LOR','CGPA','Research'],
                                    dtype=float)
prediction = loaded_model.predict(scalar.transform(input_variables))
print(prediction)