# write your code here
import pandas as pd
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', 8)


file_paths = ['test/general.csv', 'test/prenatal.csv', 'test/sports.csv']
data_sets = {}


def loaddata(file_paths):
    global data_sets
    for path in file_paths:
        data_sets[path] = pd.read_csv(path)

def renamecolumns():
    data_sets["test/prenatal.csv"].rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'}, inplace=True)
    data_sets["test/sports.csv"].rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'}, inplace=True)

def concattables():
    a, b, c = data_sets

    df = pd.concat([data_sets[a], data_sets[b], data_sets[c]], ignore_index=True)
    df.drop(columns=['Unnamed: 0'], inplace=True)
    return df

def gender_deal(data_frame):
    data_frame['gender'].replace(['female', 'woman'],'f', inplace=True)
    data_frame['gender'].replace(['male', 'man'],'m', inplace=True)
    data_frame['gender'].fillna('f',inplace=True)

    colums = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']

    for column in colums:
        data_frame[column].fillna(0, inplace=True)


    data_frame.dropna(axis=0, inplace=True)

    return data_frame

def questions(df):
    a =  df['hospital'].value_counts().idxmax()
    print("The answer to the 1st question is", a)
    a = df.loc[(df['hospital'] == 'general') & (df['diagnosis'] == 'stomach')].shape[0] / df.loc[(df['hospital'] == 'general')].shape[0]
    print("The answer to the 2nd question is", round(a, 3))
    a = df.loc[(df['hospital'] == 'sports') & (df['diagnosis'] == 'dislocation')].shape[0] / df.loc[(df['hospital'] == 'sports')].shape[0]
    print("The answer to the 3nd question is", round(a, 3))
    a = df.loc[df['hospital'] == 'general', 'age'].median() - df.loc[df['hospital'] == 'sports', 'age'].median()
    print("The answer to the 4nd question is", round(a))
    otv = {}
    hospital_names = ['general', 'sports', 'prenatal']
    for hospital_name in hospital_names:
        otv[hospital_name] = df.loc[(df['hospital'] == hospital_name) & (df['blood_test'] == 't')].count()[0]

    max_blood = max(otv.values())
    for hospital_name in hospital_names:
        if otv[hospital_name] == max_blood:
            print(f'The answer to the 5th question is {hospital_name}, {max_blood} blood tests')


def visual(df):
    #df.plot(y=['age'], kind='hist', bins=8, alpha=0.5)
    df['age'].plot(kind='hist')
    plt.savefig('age_pic.jpg')
    plt.show()
    df['diagnosis'].value_counts().plot(kind='pie')
    plt.savefig('diagnosis_pic.jpg')
    plt.show()
    dd = df['height']
    plt.violinplot(dataset=dd)
    plt.savefig('violin_pic.jpg')
    plt.show()

    print('''The answer to the 1st question: 15-35
The answer to the 2nd question: pregnancy
The answer to the 3rd question: It's because..''')











loaddata(file_paths)
renamecolumns()

data_frame = gender_deal(concattables())



#questions(data_frame)

visual(data_frame)

#print(data_frame.diagnosis.unique())
#print(data_frame.sample(n=10, random_state=30))
