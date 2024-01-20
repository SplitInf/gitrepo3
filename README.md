# Utilizing Github API to assess repository populatrity
By default this package uses Github API to retireve the top 20 repositories with more than 1,000 followers.
The top X repositories can be adjusted using yaml file (see below)

## Instructions
```
#Install ghapi
pip install ghapi

```


## Input:
By default the code prints the top 20 repositories with results more than 1000 followers
*optional* config.yml file can be provided with key:value pair top_n: interger
There is a warning when more than 20 repositories is selected
- example config.yml:
```
top_n: 15
```

- how to run ghapi. Example script
```
#after running pip install ghapi
from ghapi import ghapi_func

#get top_n entries by configuration file
file_path="settings.yaml"
#file_path="" #this gives you default of 15
n=ghapi_func.Analysis.get_top_n(file_path)
print(n)

#get list and preview
t=ghapi_func.Analysis.get_data(n, True)

#plot results as bar chart
ghapi_func.Analysis.get_plot(repo_name=t[0], repo_counts=t[1])
```
## output:
bar plot of top x repositories

