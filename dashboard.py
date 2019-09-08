import pandas as pd
import panel as pn
from config import db

pn.extension()
pd.options.display.float_format = '{:,.2f}'.format

query = """ SELECT Assignments.Client_Name, Assignments.Director, Assignments.Manager, 
                    Time.Hours, Time.Billed, Time.Sheet_Date 
                    FROM Assignments 
                    LEFT JOIN Time ON Assignments.Client_ID=Time.Client_ID"""


def create_dashboard():
    mgrDir_list = ['Manager', 'Director']

    mgrDirWidget = pn.interact(mgrDir, ManagerDirector = mgrDir_list)
    assignmentsWidget = pn.interact(chooseAssignmentLevel, 
            Quarter_Detail=['With_Quarters','Without_Quarters'],
            ManagerDirector = mgrDir_list)
    managerJobsWidget = pn.interact(displayManagerJobs, 
            Manager = df['Manager'].unique(),
            ManagerDirector = mgrDir_list)

    gspec = pn.GridSpec(sizing_mode='stretch_both', max_height=800)

    gspec[0, :2] = pn.Row("# Novak Francella Manager/Partner Hours")
    gspec[1:4, 0] = mgrDirWidget
    gspec[1:6, 1] = pn.Column('')
    gspec[1:3, 2] = assignmentsWidget
    gspec[1:6, 3] = pn.Column('')   
    gspec[1:6, 4] = managerJobsWidget
    

    return gspec

# Returns a grouped DF by either manager or director. ManagerDirector must be "Manager" or "Director"
def mgrDir(ManagerDirector="Manager"):
    temp_df = df.groupby([ManagerDirector,'Quarter']).sum()
    temp_df['Hourly_Rate'] = temp_df['Billed'] / temp_df['Hours']
    return temp_df


def hours(df,Quarter_Detail,ManagerDirector):
    if (Quarter_Detail == 'With_Quarters'):
        return df.sort_values('Hours', ascending=False)
    else:
        df = df.reset_index(level=1, drop=True)
        return df.groupby(ManagerDirector).sum().sort_values('Hours', ascending=False)


def chooseAssignmentLevel(Quarter_Detail, ManagerDirector):
    return hours(mgrDir(ManagerDirector),Quarter_Detail, ManagerDirector)


def displayManagerJobs(Manager):
    temp_df = df[df.Manager == Manager].groupby('Client_Name').sum()
    temp_df['Hourly_Rate'] = temp_df['Billed'] / temp_df['Hours']
    return(temp_df[['Hours','Billed','Hourly_Rate']].sort_values(by='Billed',ascending=False))


# Read tables from SQLite Database to pandas dataframes
df = pd.read_sql(query, db)
df['Sheet_Date'] = pd.to_datetime(df['Sheet_Date'], format='%m/%d/%y', errors='coerce')
df['Quarter'] = df['Sheet_Date'].dt.quarter

dashboard = create_dashboard()
dashboard.servable();


if __name__ =="__main__":
    dashboard.show()
