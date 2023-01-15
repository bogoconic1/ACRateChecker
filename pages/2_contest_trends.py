import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
from collections import defaultdict
import streamlit as st

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

def write_dataframe(df):
    
    style = df.style.hide_index()
    style.hide_columns()
    st.write(style.to_html(), unsafe_allow_html=True)
    st.write("\n")
    st.write("\n")

#read json files
with open("name2id.json") as j:
    name2id = json.load(j)
    
with open("name2probs.json") as j:
    name2probs = json.load(j)

#name2probs["Select Contest"] = []
#name2id["Select Contest"] = -1



st.header("**Contest Snapshot Visualizer**")

contest_name = st.selectbox(
    'Select Contest',
    ["Select Contest"] + list(name2probs.keys()))

if contest_name != "Select Contest":
    contest = name2id[contest_name]

    cf_dataframe, selected_contest, start_time, duration = get_contest_snapshots(contest)
    minutes_after_start = st.slider('Minutes after contest started', 0, duration // 60, duration // 60)


    #end_time = list(selected_contest["startTimeSeconds"])[0] + duration - 1
    seconds_after_start = minutes_after_start * 60
    end_time = list(selected_contest["startTimeSeconds"])[0] + seconds_after_start
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
        
    dur_contest = [["Problem", "User Accepted", "User Tried", "Total Accepted", "Total Submissions", "Accepted %"]]
    for pindex in problems:
        solved_df = byTimeMemory[(byTimeMemory["problem_index"] == pindex) & (byTimeMemory["verdict"] == "OK")]
        attempted_df = byTimeMemory[(byTimeMemory["problem_index"] == pindex)]
        user_solved = len(set([x[0]["handle"] for x in list(solved_df["author_members"])]))
        user_attempted = len(set([x[0]["handle"] for x in list(attempted_df["author_members"])]))
        total_solved = len(solved_df)
        total_attempted = len(attempted_df)
        acceptance_rate = round(((total_solved / total_attempted) * 100),2)
        dur_contest.append([f'{pindex}. {index_to_name[pindex]}', f'{user_solved:,}', f'{user_attempted:,}' \
            , f'{total_solved:,}', f'{total_attempted:,}', f'{acceptance_rate}'])
    dur_contest = pd.DataFrame(dur_contest)
    write_dataframe(dur_contest)
    
    st.markdown("Verdict Snapshot Visualiser")
    
    verdict_prob, verdict_lang = st.columns(2)
    
    with verdict_prob:
        selected_problem = st.selectbox(
                            'Select Problem',
                            ["Select Problem"] + problems)
        
    with verdict_lang:
        prog_langs = sorted(list(set(cf_dataframe.programmingLanguage)))
        selected_language = st.selectbox(
                            'Select Language',
                            ["Select Language"] + prog_langs)
        
        
    if selected_problem != 'Select Problem' and selected_language != 'Select Language':
        compressed_df = cf_dataframe[(cf_dataframe.programmingLanguage == selected_language) & \
            (cf_dataframe["problem.index"] == selected_problem) & (cf_dataframe["creationTimeSeconds"] <= end_time)]
        compressed_df["temp"] = compressed_df["verdict"].apply(lambda x: x.capitalize().replace("_", " ").replace("Ok", "Accepted"))
        compressed_df["passedTestCount"] += 1
        compressed_df["passedTestCount"] = compressed_df["passedTestCount"].astype(str)
        verdicts_with_test_no = ["Wrong answer", "Time limit exceeded", "Memory limit exceeded", "Idleness limit exceeded", "Runtime error"]
        conditions = [compressed_df["temp"] == "Wrong answer",
                    compressed_df["temp"] == "Time limit exceeded", \
                    compressed_df["temp"] == "Memory limit exceeded", \
                    compressed_df["temp"] == "Idleness limit exceeded", \
                    compressed_df["temp"] == "Runtime error"]
        choices = [compressed_df["temp"] + " on test " + compressed_df["passedTestCount"], \
                compressed_df["temp"] + " on test " + compressed_df["passedTestCount"], \
                compressed_df["temp"] + " on test " + compressed_df["passedTestCount"],\
                compressed_df["temp"] + " on test " + compressed_df["passedTestCount"],\
                compressed_df["temp"] + " on test " + compressed_df["passedTestCount"]]
        compressed_df["final_verdict"] = np.select(conditions, choices, default = compressed_df["temp"])
        
        v_counts = compressed_df["final_verdict"].value_counts()
        verdict = []
        for x in v_counts.keys():
            verdict.append((x,v_counts[x]))
        verdict_df = pd.DataFrame(verdict, columns = ["Verdict", "Submissions"])
        write_dataframe(verdict_df)
        
        
    
    
#except AssertionError:
    #pass