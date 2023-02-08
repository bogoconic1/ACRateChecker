import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
from collections import defaultdict
import streamlit as st

st.header("**AC Rate of a Codeforces Problem**")

#read json files
with open("name2id.json") as j:
    name2id = json.load(j)
    
with open("name2probs.json") as j:
    name2probs = json.load(j)
    
    
name2probs["Select Contest"] = []
name2id["Select Contest"] = -1

contest_name = st.selectbox(
    'Select Contest',
    ["Select Contest"] + list(name2probs.keys()))

contest = name2id[contest_name]

question = st.selectbox(
    'Select Problem',
    ["Select Problem"] + name2probs[contest_name])
  
if question != "Select Problem":
    question_idx = question.split("-")[0][:-1]
    page = "https://codeforces.com/api/contest.status?contestId=" + str(contest) + "&from=1"
    st.write(f'Fetching statistics...')
    cf_submissions_api = requests.get(page)
    submissions = cf_submissions_api.json()
    cf_dataframe = pd.json_normalize(submissions,['result'])

    cf_duration_api = requests.get("https://codeforces.com/api/contest.list?gym=false")
    contests = cf_duration_api.json()
    cf_duration_dataframe = pd.json_normalize(contests,['result'])

    total_subs = len(cf_dataframe[cf_dataframe["problem.index"] == question_idx])
    total_accepted = len(cf_dataframe[(cf_dataframe["problem.index"] == question_idx) & (cf_dataframe["verdict"] == "OK")])
    st.markdown('**Total**')
    total = []
    total.append(['Accepted', f'{total_accepted:,}'])
    total.append(['Submissions', f'{total_subs:,}'])
    total.append(['Accepted %', f'{round((total_accepted/total_subs)*100):,}'])
    total = pd.DataFrame(total)
    style = total.style.hide_index()
    style.hide_columns()
    st.write(style.to_html(), unsafe_allow_html=True)
    st.write("\n")
    st.write("\n")
    
    selected_contest = cf_duration_dataframe.loc[cf_duration_dataframe["id"] == int(contest)]
    start_time = list(selected_contest["startTimeSeconds"])[0]
    duration = list(selected_contest["durationSeconds"])[0]
    end_time = list(selected_contest["startTimeSeconds"])[0] + duration - 1
    contest_df = cf_dataframe.loc[(cf_dataframe["creationTimeSeconds"] >= start_time) & (cf_dataframe["creationTimeSeconds"] <= end_time)]
    contest_df = contest_df.rename(columns = {"timeConsumedMillis": "Time","problem.index":"problem_index","problem.name":"problem_name","author.members":"author_members"})

    solved_df = contest_df[(contest_df["problem_index"] == question_idx) & (contest_df["verdict"] == "OK")]
    attempted_df = contest_df[(contest_df["problem_index"] == question_idx)]
    user_solved = len(set([x[0]["handle"] for x in list(solved_df["author_members"])]))
    user_attempted = len(set([x[0]["handle"] for x in list(attempted_df["author_members"])]))
    total_solved = len(solved_df)
    total_attempted = len(attempted_df)
    try:
        difficulty = list(contest_df[(contest_df["problem_index"] == question_idx)]['problem.rating'])[0]
    except:
        difficulty = "Not released yet"
    acceptance_rate = round((total_solved / total_attempted) * 100)
    
    st.markdown('**During Contest**')
    dur_contest = []
    dur_contest.append(["User Accepted",  f'{user_solved:,}'])
    dur_contest.append(["User Tried",  f'{user_attempted:,}'])
    dur_contest.append(["Total Accepted",  f'{total_solved:,}'])
    dur_contest.append(["Total Submissions",  f'{total_attempted:,}'])
    dur_contest.append(["Difficulty",  f'{difficulty}'])
    dur_contest.append(["Accepted %",  f'{acceptance_rate}'])
    dur_contest = pd.DataFrame(dur_contest)
    style = dur_contest.style.hide_index()
    style.hide_columns()
    st.write(style.to_html(), unsafe_allow_html=True)
    
#except AssertionError:
#    pass
#except IndexError:
#    st.write("Question number does not exist. Please re-check input")  
#except KeyError:
#    st.write("Question number does not exist. Please re-check input")  
