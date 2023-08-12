import streamlit as st
from streamlit_extras.colored_header import colored_header
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import requests
import json
from collections import defaultdict
import streamlit as st
from stqdm import stqdm

colored_header(
    label="ACRateChecker",
    description="A tool to find the acceptance rate of contest problems, and summarise verdicts from contest submissions",
    color_name="violet-70",
)

st.set_option("deprecation.showPyplotGlobalUse", False)


@st.cache_data(show_spinner=False)
def get_contest_snapshots(contest):
    for _ in stqdm(range(1), desc="Fetching data"):
        page = (
            "https://codeforces.com/api/contest.status?contestId="
            + str(contest)
            + "&from=1"
        )
        cf_submissions_api = requests.get(page)
        submissions = cf_submissions_api.json()
        cf_dataframe = pd.json_normalize(submissions, ["result"])

        cf_duration_api = requests.get(
            "https://codeforces.com/api/contest.list?gym=false"
        )
        contests = cf_duration_api.json()
        cf_duration_dataframe = pd.json_normalize(contests, ["result"])

        selected_contest = cf_duration_dataframe.loc[
            cf_duration_dataframe["id"] == int(contest)
        ]
        start_time = list(selected_contest["startTimeSeconds"])[0]
        duration = list(selected_contest["durationSeconds"])[0]

    return cf_dataframe, selected_contest, start_time, duration


def write_dataframe(df):
    style = df.style.hide(axis="index")
    # style.hide_columns()
    st.write(style.to_html(), unsafe_allow_html=True)
    st.write("\n")
    st.write("\n")


# read json files
with open("name2id.json") as j:
    name2id = json.load(j)

with open("name2probs.json") as j:
    name2probs = json.load(j)

# name2probs["Select Contest"] = []
# name2id["Select Contest"] = -1

st.write()

contest_name = st.selectbox(
    "Step 1: Select Contest", ["Select Contest"] + list(name2probs.keys())
)


if contest_name != "Select Contest":
    if contest_name in name2id:
        contest = name2id[contest_name]

    cf_dataframe, selected_contest, start_time, duration = get_contest_snapshots(
        contest
    )
    minutes_after_start = st.slider(
        "Minutes after contest started", 0, duration // 60, duration // 60
    )

    # end_time = list(selected_contest["startTimeSeconds"])[0] + duration - 1
    seconds_after_start = minutes_after_start * 60
    end_time = list(selected_contest["startTimeSeconds"])[0] + seconds_after_start
    byTimeMemory = cf_dataframe[
        [
            "creationTimeSeconds",
            "contestId",
            "problem.index",
            "problem.name",
            "programmingLanguage",
            "author.members",
            "verdict",
            "timeConsumedMillis",
            "memoryConsumedBytes",
        ]
    ].loc[
        (cf_dataframe["creationTimeSeconds"] >= start_time)
        & (cf_dataframe["creationTimeSeconds"] <= end_time)
    ]
    byTimeMemory = byTimeMemory.rename(
        columns={
            "timeConsumedMillis": "Time",
            "problem.index": "problem_index",
            "problem.name": "problem_name",
            "author.members": "author_members",
        }
    )

    # retrieve the name and id of the problems
    problem_header = byTimeMemory[["problem_index", "problem_name"]]
    problems = sorted(set(list(byTimeMemory["problem_index"])))
    index_to_name = defaultdict()
    for index, name in problem_header.values:
        index_to_name[index] = name
        if len(index_to_name) == len(problems):
            break

    dur_contest = []
    for i in stqdm(range(len(problems)), desc="Calculating AC rates"):
        pindex = problems[i]
        solved_df = byTimeMemory[
            (byTimeMemory["problem_index"] == pindex)
            & (byTimeMemory["verdict"] == "OK")
        ]
        attempted_df = byTimeMemory[(byTimeMemory["problem_index"] == pindex)]
        user_solved = len(
            set([x[0]["handle"] for x in list(solved_df["author_members"])])
        )
        user_attempted = len(
            set([x[0]["handle"] for x in list(attempted_df["author_members"])])
        )
        total_solved = len(solved_df)
        total_attempted = len(attempted_df)
        acceptance_rate = round(((total_solved / total_attempted) * 100), 2)
        dur_contest.append(
            [
                f"{pindex}. {index_to_name[pindex]}",
                f"{user_solved:,}",
                f"{user_attempted:,}",
                f"{total_solved:,}",
                f"{total_attempted:,}",
                f"{acceptance_rate}",
            ]
        )
    dur_contest = pd.DataFrame(
        dur_contest,
        columns=[
            "Problem",
            "User Accepted",
            "User Tried",
            "Total Accepted",
            "Total Submissions",
            "Accepted %",
        ],
    )
    write_dataframe(dur_contest)

    st.markdown("Verdict Snapshot Visualiser")

    verdict_prob, verdict_lang = st.columns(2)

    with verdict_prob:
        selected_problem = st.selectbox(
            "Step 2: Select Problem", ["Select Problem"] + problems
        )

    with verdict_lang:
        prog_langs = sorted(list(set(cf_dataframe.programmingLanguage)))
        selected_language = st.selectbox(
            "Step 3: Select Language",
            ["Select Language"] + ["All Languages"] + prog_langs,
        )

    compressed_df = None

    if selected_problem != "Select Problem" and selected_language != "Select Language":
        if selected_language == "All Languages":
            compressed_df = cf_dataframe[
                (cf_dataframe["problem.index"] == selected_problem)
                & (cf_dataframe["creationTimeSeconds"] <= end_time)
            ]
        else:
            compressed_df = cf_dataframe[
                (cf_dataframe.programmingLanguage == selected_language)
                & (cf_dataframe["problem.index"] == selected_problem)
                & (cf_dataframe["creationTimeSeconds"] <= end_time)
            ]
        compressed_df["temp"] = compressed_df["verdict"].apply(
            lambda x: x.capitalize().replace("_", " ").replace("Ok", "Accepted")
        )
        compressed_df["passedTestCount"] += 1
        compressed_df["passedTestCount"] = compressed_df["passedTestCount"].astype(str)
        verdicts_with_test_no = [
            "Wrong answer",
            "Time limit exceeded",
            "Memory limit exceeded",
            "Idleness limit exceeded",
            "Runtime error",
        ]
        conditions = [
            compressed_df["temp"] == "Wrong answer",
            compressed_df["temp"] == "Time limit exceeded",
            compressed_df["temp"] == "Memory limit exceeded",
            compressed_df["temp"] == "Idleness limit exceeded",
            compressed_df["temp"] == "Runtime error",
        ]
        choices = [
            compressed_df["temp"] + " on test " + compressed_df["passedTestCount"],
            compressed_df["temp"] + " on test " + compressed_df["passedTestCount"],
            compressed_df["temp"] + " on test " + compressed_df["passedTestCount"],
            compressed_df["temp"] + " on test " + compressed_df["passedTestCount"],
            compressed_df["temp"] + " on test " + compressed_df["passedTestCount"],
        ]
        compressed_df["final_verdict"] = np.select(
            conditions, choices, default=compressed_df["temp"]
        )

        v_counts = compressed_df["final_verdict"].value_counts()
        verdict = []
        for x in v_counts.keys():
            verdict.append((x, v_counts[x]))
        verdict_df = pd.DataFrame(verdict, columns=["Verdict", "Submissions"])
        write_dataframe(verdict_df)

    if compressed_df is not None:
        runtime_df = compressed_df[compressed_df["final_verdict"] == "Accepted"][
            ["timeConsumedMillis", "memoryConsumedBytes"]
        ]

        runtime_df = runtime_df.rename(columns={"timeConsumedMillis": "Time(ms)"})
        runtime_df["Memory(KB)"] = runtime_df["memoryConsumedBytes"] // 1000

        # Create the histogram figure
        fig = go.Figure(data=[go.Histogram(x=runtime_df["Time(ms)"])])

        # Customize the plot
        fig.update_layout(
            title="Runtime Distribution (ms)",
            xaxis_title="Runtime (ms)",
            yaxis_title="Frequency (Log Scale)",
            bargap=0.1,  # Adjust the gap between bars
            bargroupgap=0.2,  # Adjust the gap between groups of bars
            showlegend=False,  # Hide the legend
        )

        fig.update_yaxes(type="log")

        # Show the plot
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        # Create the histogram figure
        fig = go.Figure(
            data=[
                go.Histogram(x=runtime_df["Memory(KB)"], marker=dict(color="darkblue"))
            ]
        )

        # Customize the plot
        fig.update_layout(
            title="Memory Distribution (KB)",
            xaxis_title="Memory Used (KB)",
            yaxis_title="Frequency (Log Scale)",
            bargap=0.1,  # Adjust the gap between bars
            bargroupgap=0.2,  # Adjust the gap between groups of bars
            showlegend=False,  # Hide the legend
        )

        fig.update_yaxes(type="log")

        # Show the plot
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)


# except AssertionError:
# pass
