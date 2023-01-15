# ACRateChecker

ACRateChecker is a web-based data analytics solution to help users find the overall acceptance and contest acceptance rate of any codeforces problem.

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
streamlit run main.py
```

The following should show up in the terminal
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: (in this format) http://xxx.xxx.xxx.xxx:8501 
  
```

# The Interface

The main page will be shown when the URL is opened
![image](https://user-images.githubusercontent.com/100673850/209146368-48942d7d-e5c0-4a4e-9a73-34bd1651d0b3.png)

**Function 1: Find the acceptance rate of a question**
![image](https://user-images.githubusercontent.com/100673850/209146554-fcec621b-ee81-4735-9aff-8a4a0c6d7dab.png)

Step 1: Choose a contest
![image](https://user-images.githubusercontent.com/100673850/209146765-d8079c18-8895-412a-80bd-edd801c85988.png)

Step 2: Choose a question
![image](https://user-images.githubusercontent.com/100673850/209146904-35135df0-15d0-4232-90e0-32da3f60e3dd.png)

Within **15 seconds**, output is shown
![image](https://user-images.githubusercontent.com/100673850/209147047-794c4514-6ab1-439c-89e2-23ff13bbafc4.png)

**Function 2: Track contest acceptance rate across time**
![image](https://user-images.githubusercontent.com/100673850/209147188-9b167e22-c590-4c86-8912-55de0741161c.png)

Step 1: Choose a contest
![image](https://user-images.githubusercontent.com/100673850/209147346-8c32d7ab-4265-4091-b4b2-a296dbb99885.png)

Step 2: Drag the slider to to find the acceptance rate at a specific time in the contest
![image](https://user-images.githubusercontent.com/100673850/209147480-bc0bf1a6-9d5d-4186-9fa2-b1d4c4af6c61.png)

