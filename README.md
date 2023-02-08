# ACRateChecker

https://bogoconic1-acratechecker-main-fddjqv.streamlit.app/

ACRateChecker is a web-based data analytics solution to help users find the overall acceptance and contest acceptance rate of any codeforces problem, added on with a verdict classifier for contests

# Problem Statement

During a codeforces virtual contest, many contestants occasionally look at the submission verdicts to a problem for various reasons (such as deciding the language to use etc). 

Submission **verdicts** are public to the contestant, and for the user to view the submission verdicts, they have to click on Status and key in the problem and language in the drop down boxes. Even by doing that, the search results can retrieve thousands of records that will be difficult to analyze under contest pressure

![image](https://user-images.githubusercontent.com/100673850/214788853-31e13002-b6e3-44f1-af6a-8bc12a37aee3.png)
<p style="text-align: center;"> Figure 1: Example of the "Status" page DURING a contest </p>

An example:
![image](https://user-images.githubusercontent.com/100673850/214785248-08d6bb62-78e6-4e79-adfb-6d48fe8a8603.png)
<p style="text-align: center;"> Figure 2: Example of the "Status" page AFTER a contest </p>

The large runtime (extremely close to the time limit) (Figure 2) of these submissions in the python language, accompanied with the vast majority of solutions having "Time limit exceeded on pretest 3" could imply that the problem is extremely difficult to pass in python and as such the user may use C++ without wasting time writing a python solution which has high chances of getting time limit exceeded.

The "Contest Snapshots" function aims to provide a live summary of the verdicts in the "Status" tab which is public and can be viewed in the contest (see Figure 1).


# Built with

- Streamlit [https://streamlit.io/]
- Pandas
- Python 


# Some screenshots of ACRateChecker

![image](https://user-images.githubusercontent.com/100673850/215093277-51dcda52-87ca-4054-8134-c182d9bfc9a7.png)
![image](https://user-images.githubusercontent.com/100673850/215093344-c4638958-29be-4e19-af82-efaf0a3f9ad0.png)
![image](https://user-images.githubusercontent.com/100673850/215093363-db125e57-084d-47ad-94c7-08c76c651c6a.png)

