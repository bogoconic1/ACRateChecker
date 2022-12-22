import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests
from pandasql import sqldf
import json
from collections import defaultdict
import streamlit as st

def ac_rate(cf_dataframe, selected_contest, start_time, seconds):
    #end_time = list(selected_contest["startTimeSeconds"])[0] + duration - 1
    end_time = list(selected_contest["startTimeSeconds"])[0] + seconds
    byTimeMemory = cf_dataframe[["creationTimeSeconds","contestId","problem.index","problem.name","programmingLanguage","author.members","verdict","timeConsumedMillis", "memoryConsumedBytes"]].loc[(cf_dataframe["creationTimeSeconds"] >= start_time) & (cf_dataframe["creationTimeSeconds"] <= end_time)]
    byTimeMemory = byTimeMemory.rename(columns = {"timeConsumedMillis": "Time","problem.index":"problem_index","problem.name":"problem_name","author.members":"author_members"})

    #retrieve the name and id of the problems
    problem_header = byTimeMemory[["problem_index","problem_name"]]
    problems = sorted(set(list(byTimeMemory["problem_index"])))
    index_to_name = defaultdict()
    for index,name in problem_header.values:
        index_to_name[index] = name
        if len(index_to_name) == len(problems):
            break
        
    dur_contest = [["Question", "User Accepted", "User Tried", "Total Accepted", "Total Submissions", "Accepted %"]]
    for pindex in problems:
        solved_df = byTimeMemory[(byTimeMemory["problem_index"] == pindex) & (byTimeMemory["verdict"] == "OK")]
        attempted_df = byTimeMemory[(byTimeMemory["problem_index"] == pindex)]
        user_solved = len(set([x[0]["handle"] for x in list(solved_df["author_members"])]))
        user_attempted = len(set([x[0]["handle"] for x in list(attempted_df["author_members"])]))
        total_solved = len(solved_df)
        total_attempted = len(attempted_df)
        acceptance_rate = ((total_solved / total_attempted) * 100)
        dur_contest.append([f'{pindex}. {index_to_name[pindex]}', f'{user_solved:,}', f'{user_attempted:,}' \
            , f'{total_solved:,}', f'{total_attempted:,}', f'{acceptance_rate}'])
    dur_contest = pd.DataFrame(dur_contest)
    style = dur_contest.style.hide_index()
    style.hide_columns()
    st.write(style.to_html(), unsafe_allow_html=True)
    st.write("\n")
    st.write("\n")

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

try:
    assert contest_name != "Select Contest"
    contest = name2id[contest_name]
    
    @st.cache(show_spinner=False)
    def get_contest_snapshots(contest):
        page = "https://codeforces.com/api/contest.status?contestId=" + str(contest) + "&from=1"
        cf_submissions_api = requests.get(page)
        submissions = cf_submissions_api.json()
        cf_dataframe = pd.json_normalize(submissions,['result'])
        
        cf_duration_api = requests.get("https://codeforces.com/api/contest.list?gym=false")
        contests = cf_duration_api.json()
        cf_duration_dataframe = pd.json_normalize(contests,['result'])
        
        selected_contest = cf_duration_dataframe.loc[cf_duration_dataframe["id"] == int(contest)]
        start_time = list(selected_contest["startTimeSeconds"])[0]
        duration = list(selected_contest["durationSeconds"])[0]
    
        return cf_dataframe, selected_contest, start_time, duration
    
    cf_dataframe, selected_contest, start_time, duration = get_contest_snapshots(contest)
    seconds_after_start = st.slider('Select time of Contest Snapshot (in seconds)', 0, duration, duration)
    ac_rate(cf_dataframe, selected_contest, start_time, seconds_after_start)
    
except AssertionError:
    pass