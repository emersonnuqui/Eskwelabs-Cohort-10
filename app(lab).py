import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns

st.set_page_config(layout = "wide")
sns.set(rc={'axes.facecolor':'#353535', 
            'axes.edgecolor': '#353535',
            'figure.facecolor':'#353535',
            'grid.color': '#353535',
            'text.color': '#ffffff',
            'ytick.color': '#ffffff',
            'xtick.color': '#ffffff',
            'axes.labelcolor': '#ffffff'
            })

def load_data():
    # Load the data for philippines
    data = pd.read_csv(
        "micro_world.csv"
    )

    philippine_data = data[
        data['economy'] == 'Philippines'
        ]

    return philippine_data

def introduction():
    # Write the title and the subheader
    st.title(
        "Financial account ownership in the Philippines"
    )
    st.subheader(
        """
    **Scope/Focus**

    1. FI metric we chose to focus on is the access to account in a financial institution (account_fin).
    
    2. Goal is to find out the profile of Filipinos who don’t have accounts and to find reasons as to why they don’t have accounts in a financial institution.

        """
    )

    # Load data
    philippine_data = load_data()

    # Display data
    st.markdown("**The Data**")
    st.dataframe(philippine_data)
    st.markdown("Source: Global Findex 2017 from World Bank.")

    #Partition the page into 2
    col1, col2, col3, col4 = st.columns(4)

    #Insert image on left side
    col1.image("image1.jpg")

    #Insert header on right side
    col2.write("\n")
    col2.write("\n")
    col2.write("\n")
    col2.header("Filipinos have accounts in financial institutions")


    #Partition the page into 2
    #col1, col2 = st.columns(2)

    col3.image("image2.jpg")

    col4.header("Less than the world average")

def fi_state_ph():
    # Write the title
    st.title(
        "This is the current state of FI in the Philippines."
    )

    # Load data
    data = load_data()

    # Fetch Philippine data
    philippine_data = data[
        data['economy'] == 'Philippines'
        ]

    # Create another column for debit card ownership
    philippine_data['has_debit_card'] = philippine_data['fin2'].apply(
        lambda x: 1 if x == 1 else 0
    )

    # Compute overall debit card ownership
    percent_debit_card_ownership = philippine_data['has_debit_card'].sum() * 100.0 / philippine_data[
        'wpid_random'].count()

    # Partition the page into 2
    col1, col2 = st.columns(2)

    # Display text in column 1
    col1.markdown(
        "In the Philippines, there is still an opportunity to expand access to financial services: "
    )

    # Display metric in column 2
    col2.metric(
        label='% of Population with Debit Card',
        value=percent_debit_card_ownership
    )

    # Display text
    st.markdown("In terms of gender breakdown:")

    # Create another column for gender
    philippine_data['gender'] = philippine_data['female'].apply(
        lambda x: 'male' if x == 1 else 'female'
    )

    # Compute breakdown of access to debit card by gender
    debit_by_gender = philippine_data.groupby('gender').agg(
        total_debit_card_owners=('has_debit_card', 'sum'),
        total_population=('wpid_random', 'count')
    ).reset_index()

    # Compute % debit card ownership
    debit_by_gender['% debit card ownership'] = debit_by_gender['total_debit_card_owners'] * 100.0 / debit_by_gender[
        'total_population']

    # Plot the data
    fig, ax = plt.subplots(figsize=(6, 3), dpi=200)
    ax.bar(
        debit_by_gender["gender"],
        debit_by_gender["% debit card ownership"],
    )
    ax.set_xlabel("Gender")
    ax.set_ylabel("% Debit Card Ownership")

    # Show the data
    st.pyplot(fig)

def edu_employment():
    # Write the title and the subheader

    st.title(
        "Education and Unemployment"
    )

    st.subheader(
        "**Proportion of respondents with account and without account based on educational attainment and employment status**"
    )
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")

    # Load data
    data = load_data()

    philippine_data = data[
        data['economy'] == 'Philippines'
        ]

    geo_cols=["economy","economycode","regionwb"]                             
    feature_cols=["wpid_random","female","age","educ","inc_q","emp_in"]

    #FI Acesss related columns
    fi_account_cols=["account_fin"]
    reasons_cols=["fin11a","fin11b","fin11c","fin11d","fin11e","fin11f","fin11g","fin11h"]
    fi_account_purposes=["fin17a","fin22a","fin27a","fin29a","fin34a","fin39a","fin43a","fin47a"]

    #Renamed Columns
    reasons_cols_new=["Reason_too_far","Reason_too_expensive","Reason_lack_docu","Reason_lack_trust",
                    "Reason_religious","Reason_lack_money","Reason_family_has","Reason_no_need"]

    fi_account_purposes_new= ["Purpose_saved","Purpose_borrowed","Purpose_sent_dom_rem",
                          "Purpose_received_dom_rem","Purpose_received_wage","Purpose_received_govt_transfer",
                          "Purpose_received_agri_payment","Purpose_received_self_employment"]


    #Needed columns
    needed_cols=fi_account_cols+geo_cols+feature_cols+reasons_cols_new+fi_account_purposes_new

    #Rename specified columns, then only include needed columns
    col_rename_dict = {i:j for i,j in zip(reasons_cols+fi_account_purposes,reasons_cols_new+fi_account_purposes_new)}
    philippine_data_2=philippine_data.rename(columns=col_rename_dict)[needed_cols]
    
    col1, col2 = st.columns(2)

    st.markdown("Those with lower educational attainment, as well as the unemployed have a lower proportion of having an account. In relation to the previous slide, bigger proportions of these groups to belong to lower income quartiles.")
    st.markdown("\n")
    st.markdown("\n")

    col1, col2 = st.columns(2)
    proportion_educ = philippine_data_2.groupby(['educ']).agg(
    total_with_acc=('account_fin', 'sum'),
    total_population=('wpid_random', 'count')).reset_index()
    proportion_educ["Proportion"]=proportion_educ.total_with_acc/proportion_educ.total_population
    

    mapping = {
        1:'Primary Education or Less',
        2:'Secondary Education',
        3:'Tertiary Education or Above',
    }

    proportion_educ.replace({"educ":mapping}, inplace=True)
  

    # Set figure size
    plt.figure(figsize=(6,4)  , dpi=200)

    # Run bar plot
    plt.barh(
        proportion_educ['educ'],
        proportion_educ['Proportion'],
        color = "#F46523"
    )

    plt.title('% With Account (Grouped by Educational Attainment)')

    bar = plt.show()

    #Show bar plot 
    col1.pyplot(bar)


    #    This portion shows the percentage of respondents with account in
    #    financial institution grouped by employment status.


    proportion_emp_in = philippine_data_2.groupby(['emp_in']).agg(
    total_with_acc=('account_fin', 'sum'),
    total_population=('wpid_random', 'count')).reset_index()
    proportion_emp_in["Proportion"]=proportion_emp_in.total_with_acc/proportion_emp_in.total_population


    mapping = {
     0:'Unemployed',
     1:'Employed',

    }

    proportion_emp_in.replace({"emp_in":mapping}, inplace=True)
    

    # Set figure size
    plt.figure(figsize=(6,3.25)  , dpi=200)

    # Run bar plot
    plt.barh(
        proportion_emp_in['emp_in'],
        proportion_emp_in['Proportion'],
        color = "#F46523"
    )

    # Set title
    plt.title('% With Account (Grouped by Employment Status)')

    # Set labels
    #plt.xlabel('% Proportion')
    #plt.ylabel('Employment Status')

    # Show figure
    bar = plt.show()

    col2.pyplot(bar)

def reason_unbanking():
    st.title(
        "Reason for Unbanking"
    )

    #load the data
    data = load_data()

    philippine_data = data[
        data['economy'] == 'Philippines'
        ]

    geo_cols=["economy","economycode","regionwb"]                             
    feature_cols=["wpid_random","female","age","educ","inc_q","emp_in"]

    #FI Acesss related columns
    fi_account_cols=["account_fin"]
    reasons_cols=["fin11a","fin11b","fin11c","fin11d","fin11e","fin11f","fin11g","fin11h"]
    fi_account_purposes=["fin17a","fin22a","fin27a","fin29a","fin34a","fin39a","fin43a","fin47a"]

    #Renamed Columns
    reasons_cols_new=["Reason_too_far","Reason_too_expensive","Reason_lack_docu","Reason_lack_trust",
                    "Reason_religious","Reason_lack_money","Reason_family_has","Reason_no_need"]

    fi_account_purposes_new= ["Purpose_saved","Purpose_borrowed","Purpose_sent_dom_rem",
                          "Purpose_received_dom_rem","Purpose_received_wage","Purpose_received_govt_transfer",
                          "Purpose_received_agri_payment","Purpose_received_self_employment"]


    #Needed columns
    needed_cols=fi_account_cols+geo_cols+feature_cols+reasons_cols_new+fi_account_purposes_new

    #Rename specified columns, then only include needed columns
    col_rename_dict = {i:j for i,j in zip(reasons_cols+fi_account_purposes,reasons_cols_new+fi_account_purposes_new)}
    philippine_data_2=philippine_data.rename(columns=col_rename_dict)[needed_cols]

    label = ['Lack of Money', 'Too Expensive', 'Lack Documentation', 'No Need',
         'Bank Too Far', 'Family Has One',
         'Lack of Trust', 'Religious Reason']

    unbanked_respondents = philippine_data_2[philippine_data_2['account_fin'] == 0]
    reasons_unbanked_respondents = philippine_data_2[(philippine_data_2['Reason_too_far'] == 1) |
                                         (philippine_data_2['Reason_too_expensive'] == 1) |
                                         (philippine_data_2['Reason_lack_docu'] == 1) |
                                         (philippine_data_2['Reason_lack_trust'] == 1) |
                                         (philippine_data_2['Reason_religious'] == 1) |
                                         (philippine_data_2['Reason_lack_money'] == 1) |
                                         (philippine_data_2['Reason_family_has'] == 1) |
                                         (philippine_data_2['Reason_no_need'] == 1)]

    long_reasons_unbanked = pd.melt(reasons_unbanked_respondents, 
                                id_vars = 'account_fin',
                                value_vars = reasons_cols_new)
    unbanked_chart_data = long_reasons_unbanked[long_reasons_unbanked['value'] == 1]\
                        .groupby(['variable']).count().reset_index().sort_values('account_fin', ascending = False)

    plt.figure(figsize=(6,3), dpi=200)


    #create a bar plot
    g = sns.barplot(
        unbanked_chart_data['account_fin'], 
        unbanked_chart_data['variable'],
        color = "#F46523")

    g.set_yticklabels(label)

    plot = plt.show()

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(plot)


def recommendations():
    # Write the title
    st.title(
        "What We Can Do"
    )


def the_team():
    # Write the title
    st.title(
        "The Team"
    )


list_of_pages = [
    "Towards Financial Inclusion",
    "Income quartiles and accounts",
    "Education and unemployment",
    "Reasons for Unbanking",
    "What We Can Do",
    "The Team"
]

st.sidebar.title('Main Pages')
selection = st.sidebar.radio("Go to: ", list_of_pages)

if selection == "Towards Financial Inclusion":
    introduction()

elif selection == "Income quartiles and accounts":
    fi_state_ph()

elif selection == "Education and unemployment":
    edu_employment()

elif selection == "Reasons for Unbanking":
    reason_unbanking()

elif selection == "What We Can Do":
    recommendations()

elif selection == "The Team":
    the_team()
