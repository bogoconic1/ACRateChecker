# SystemTestsPassed

SystemTestsPassed is a web-based data analytics solution to help users find the overall acceptance and contest acceptance rate of any codeforces problem.

# Problem Statement

The problem ratings in codeforces have a floor of 800. However, it is not always true that all 800 difficulty problems are suitable for beginners. Around 80-90% of problem A in a normal division 2 round have that same rating. It does not take into account whether the problem is mistake prone or the average time taken to solve the problem itself.

Example, problem A (user accepted/tried) ratio of 10000/10500 and 7000/7200 both have the same rating. However, most users on the latter problem have at least one incorrect submission and takes twice the time before getting accepted since the problem is not so straightforward as thought. For new members, previous implementations for recommendations do not take this into account and as such, there is a chance that newbies struggle more to solve such problems without knowing that it is actually harder. 

# Built with

- Streamlit [https://streamlit.io/]
- Pandas
- Python 

# Requirements and Installation

Streamlit is required to open the tool in a web browser.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install streamlit.

```bash
pip install streamlit
```

# Usage

Run the below command
```bash
streamlit run SystemTestsPassed.py
```

The following should show up in the terminal
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: (in this format) http://xxx.xxx.xxx.xxx:8501 
```
