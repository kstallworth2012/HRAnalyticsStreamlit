import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


# from eda_app import run_eda_app
# from ml_app import run_ml_app

#cache
def load_dataset(dataset):
    df =  pd.read_csv('hr_data\\50000-HRA-Records\\'+dataset)
    return df

def main():
        st.title("HR Analytics")
        hr_df = load_dataset('50000 HRA Records.csv')
        # data DICTIONARies
        edu_level = {1:'Below College',
                     2:'College',
                     3:'Bachelor',
                     4:'Masters',
                     5:'Doctor'}
        edu_level_list = ['Below College',
                             'College',
                             'Bachelor',
                             'Masters',
                             'Doctor']
        hr_df['Education'] =hr_df['Education'].map(edu_level)

        EnvironSat_dict = {1:'Low',
                           2:'Medium',
                           3:'High',
                           4:'Very High'}
        EnvironSat_list = ['Low',
                           'Medium',
                           'High',
                           'Very High']
        hr_df['EnvironmentSatisfaction'] =hr_df['EnvironmentSatisfaction'].map(EnvironSat_dict)

        JobInvol_dict= {1:'Low',
                        2:'Medium',
                        3:'High',
                        4:'Very High'}
        JobInvol_list= ['Low',
                        'Medium',
                        'High',
                        'Very High']

        hr_df['JobInvolvement'] =hr_df['JobInvolvement'].map(JobInvol_dict)

        JobSat_dict = {1:'Low',
                       2:'Medium',
                       3:'High',
                       4:'Very High'}
        JobSat_list = ['Low',
                       'Medium',
                       'High',
                       'Very High']

        hr_df['JobSatisfaction'] =hr_df['JobSatisfaction'].map(JobSat_dict)


        PerformRating_dict = {1:'Low',
                           2:'Good',
                           3:'Excellent',
                           4:'Outstanding'}
        PerformRating_list = ['Low',
                              'Good',
                              'Excellent',
                              'Outstanding']
        hr_df['PerformanceRating'] =hr_df['PerformanceRating'].map(PerformRating_dict)

        RelationshipSat_dict = {1:'Low',
                                2:'Medium',
                                3:'High',
                                4:'Very High'}
        RelationshipSat_list = ['Low',
                                'Medium',
                                'High',
                                'Very High']

        hr_df['RelationshipSatisfaction'] =hr_df['RelationshipSatisfaction'].map(RelationshipSat_dict)

        WorkLifeBalance_dict = {1:'Bad',
                                2:'Good',
                                3:'Better',
                                4:'Best'}
        WorkLifeBalance_list = ['Bad',
                                'Good',
                                'Better',
                                'Best']
        hr_df['WorkLifeBalance'] =hr_df['WorkLifeBalance'].map(WorkLifeBalance_dict)




        col1, col2, col3 = st.columns(3)
        col4, col5, col6,col7 = st.columns(4)
        menu = ["HOME","EDA","ML","ABOUT"]
        attr_menu = ['No','Yes']
        over_time = ['All','NO','Yes']
        dept_list = ['Software', 'Human Resources', 'Sales', 'Support', 'Hardware','Research & Development']
        travel_list = ["Non-Travel","Travel_Frequently","Travel_Rarely"]
        marital_status = ['Single','Married','Divorced']
        job_role = ['Sales Executive','Healthcare Representative''Manager','Research Director', 'Research Scientist','Sales Representative','Developer','Manufacturing Director','Human Resources','Laboratory Technician']
        # stockOptLvl = []
        choice=st.sidebar.selectbox("Data Menu",menu)
        attr_choice=st.sidebar.radio("Attrition",attr_menu)
        ot_choice=st.sidebar.radio("Over Time",over_time)
        dept_choice=st.sidebar.selectbox("Department",dept_list)
        marital_choice=st.sidebar.radio("Marital Status",marital_status)
        job_choice=st.sidebar.selectbox("Job Position",job_role)
        travel_choice=st.sidebar.selectbox("Travel",travel_list)
        start_age, end_age = st.sidebar.select_slider(
             'Select a Age range',
             options=[18,25,35,45,55,65,75,85],
             value=(18, 25))

        if choice == "HOME":
            st.header("Home")

            with col1:
                st.selectbox("Education Level",edu_level_list)

        #
            with col2:
                st.selectbox("Environment Satisfaction",EnvironSat_list)

        #
            with col3:
                st.selectbox("Job Satisfaction",JobSat_list)


            with col4:
                st.selectbox("Work Life Balance",WorkLifeBalance_list)

        #
            with col5:
                st.selectbox("Relationship Satisfaction",RelationshipSat_list)

        #
            with col6:
                st.selectbox("Performance Rating",PerformRating_list)

            with col7:
                st.selectbox("Job Involvement",JobInvol_list)

            dept_attr = hr_df[(hr_df['Department']==dept_choice) & (hr_df['Attrition']==attr_choice) & (hr_df['MaritalStatus']==marital_choice)]
            dept_attr_age = dept_attr[dept_attr['Age'].between(int(start_age),int(end_age),inclusive=True)]
            st.metric(label="Attrition:"+attr_choice, value=str(dept_attr_age["Attrition"].count()), delta=None)
            # st.metric(label="Travel:"+attr_choice, value=str(dept_attr["Attrition"].count()), delta=None)
            st.dataframe(dept_attr_age.head())
            st.header("Department:"+dept_choice)
            st.subheader("Attrition: "+attr_choice)
            cent = px.pie(dept_attr_age,names=dept_attr_age.PerformanceRating, values=dept_attr_age.Age,hole = .3)
            # attr_age_index = hr_df.set_index(['Attrition','Age']).head()
            st.dataframe(dept_attr_age)
            st.plotly_chart(cent,use_container_width=True)
            st.subheader('JobSatisfaction')
            st.bar_chart(dept_attr_age['JobSatisfaction'].value_counts())
            st.subheader('Performance Rating')
            st.bar_chart(dept_attr_age['PerformanceRating'].value_counts())
            st.subheader('Business Travel')
            st.bar_chart(dept_attr_age['BusinessTravel'].value_counts())
            st.subheader('Marital Status')
            st.bar_chart(dept_attr_age['MaritalStatus'].value_counts())
            fig = px.line(dept_attr_age, x="YearsAtCompany", y="EmployeeCount")
	           # color="HourlyRate", line_group="Department")
            st.plotly_chart(fig,use_container_width=True)

            _fig = px.scatter(dept_attr_age, x="YearsAtCompany", y="YearsInCurrentRole",
	         size="YearsAtCompany", color="HourlyRate",
                 hover_name="YearsAtCompany", log_x=True, size_max=60)
            st.plotly_chart(_fig)
# -------------------------------------------------------------------------------------------------------------
            st.subheader('Attrition by Department')
            attr_soft = len(hr_df[(hr_df['Department']=='Software') & (hr_df['Attrition']=='Yes')])
            attr_hr =len(hr_df[(hr_df['Department']=='Human Resources') & (hr_df['Attrition']=='Yes')])
            attr_sales  =len(hr_df[(hr_df['Department']=='Sales') & (hr_df['Attrition']=='Yes')])
            attr_support  =len(hr_df[(hr_df['Department']=='Support') & (hr_df['Attrition']=='Yes')])
            attr_hardware  =len(hr_df[(hr_df['Department']=='Hardware') & (hr_df['Attrition']=='Yes')])
            attr_rd =len(hr_df[(hr_df['Department']=='Research & Development') & (hr_df['Attrition']=='Yes')])
            pie_labels = ['Software','Human Resources','Sales','Support','Hardware','Research & Development']
            pie_values = [attr_soft,attr_hr,attr_sales,attr_support,attr_hardware,attr_rd]
            pie_item = go.Figure(data=[go.Pie(labels=pie_labels,values=pie_values,pull=[0,0,0,0.4,0,0.2])])
            st.plotly_chart(pie_item,use_container_width=True)

# -------------------------------------------------------------------------------------------------------------
        elif choice == "EDA":
            pass
            # run_eda_app()

        elif choice == "ML":
            pass
            # run_ml_app()

        elif choice == "ABOUT":
            st.subheader("About")

        else:
            pass
        #
        # dept_col, travel_col, marital_status_col = st.columns(3)
        #
        # with dept_col:
        #     st.header("Department")
        #     dept_chart = px.pie(hr_df,names="Attrition", values="Department")
        #     st.plotly_chart(dept_chart,use_container_width=True)
        #
        #
        # with travel_col:
        #     st.header("Travel")
        #
        #
        # with marital_status_col:
        #     st.header("marital status")
        #
        #
        # WorkLife_col1, job_level_col2, job_sat_col = st.columns(3)
        #
        # with WorkLife_col1:
        #     st.header("Work Life Balance")
        #
        #
        # with job_level_col2:
        #     st.header("Job Level")
        #
        #
        # with job_sat_col:
        #     st.header("Job Job Satisfaction")
        #
        #
        # job_role_col1, job_involve_col2, stockOptLvlcol3 = st.columns(3)
        #
        # with job_role_col1:
        #     st.header("Job Role")
        #
        #
        # with job_involve_col2:
        #     st.header("Job Job Involvement")
        #
        #
        # with stockOptLvlcol3:
        #     st.header("Stock Option Level")


        # col1, col2, col3 = st.columns(3)
        #
        # with col1:
        #     st.header("A cat")
        #     st.image("https://static.streamlit.io/examples/cat.jpg")
        #
        # with col2:
        #     st.header("A dog")
        #     st.image("https://static.streamlit.io/examples/dog.jpg")
        #
        # with col3:
        #     st.header("An owl")
        #     st.image("https://static.streamlit.io/examples/owl.jpg")



if __name__ == '__main__':
        main()
