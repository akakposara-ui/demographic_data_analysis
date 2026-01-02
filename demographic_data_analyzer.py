
import pandas as pd
import numpy as np

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = None
    
    df = pd.read_csv('adult_data.csv')
    
    df.rename(columns={'native-country':'native_country'}, inplace=True)

    df.rename(columns={'education-num':'education_num'}, inplace=True)

    df.rename(columns={'marital-status':'marital_status'}, inplace=True)

    df.rename(columns={'capital-gain':'capital_gain'}, inplace=True)

    df.rename(columns={'capital-loss':'capital_loss'}, inplace=True)

    df.rename(columns={'hours-per-week':'hours_per_week'}, inplace=True)
    

    df['workclass'].replace('?', np.nan,inplace=True)

    df['occupation'].replace('?', np.nan,inplace=True)

    df['native_country'].replace('?', np.nan,inplace=True)
    
    
    df['workclass'].fillna(df['workclass'].mode()[0], inplace=True)

    df['occupation'].fillna(df['occupation'].mode()[0], inplace=True)

    df['native_country'].fillna(df['native_country'].mode()[0], inplace=True)


    
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(df[df['sex']=='Male']['age'].mean(),1)

    # What is the percentage of people who have a Bachelor's degree?
    bachelor = df[df['education']=='Bachelors']
    
    percentage_bachelors = round(len(df[df['education'] == 'Bachelors']) / len(df) * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    lower_education = df[ (df['education'].str.contains('HS-grad|11th|9th|Some-college|Assoc-acdm|Assoc-voc|7th-8th|Prof-school|5th-6th|10th|1st-4th|Preschool|12th'))]

    # percentage with salary >50K
    higher_education_rich_count = len(higher_education[higher_education['salary'] == '>50K'])
    lower_education_rich_count = len(lower_education[lower_education['salary'] == '>50K'])

    higher_education_rich = round(higher_education_rich_count / len(higher_education) * 100, 1)
    lower_education_rich = round(lower_education_rich_count / len(lower_education) * 100, 1)
    
    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours =  df.hours_per_week.min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[df['hours_per_week'] == min_work_hours]
    rich_num_min_workers = len(num_min_workers[num_min_workers['salary'] == '>50K'])
    rich_percentage = round(rich_num_min_workers / len(num_min_workers) * 100, 1)
    
    # What country has the highest percentage of people that earn >50K?
    person_per_country = df.native_country.value_counts()
    high_salary = df['salary']=='>50K'
    high_salary_person = df[high_salary]['native_country'].value_counts()
    high_salary_percentage = round(((high_salary_person / person_per_country) *100).fillna(0),1)
    highest_earning_country = high_salary_percentage.idxmax()
    
    
    highest_earning_country_percentage = round(high_salary_percentage.max(),1)

    # Identify the most popular occupation for those who earn >50K in India.
    india_high = df[(df['native_country']=='India') & (df['salary']=='>50K')]
    
    top_IN_occupation = india_high['occupation'].value_counts().idxmax()

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
