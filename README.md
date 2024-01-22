# Utilizing Github API to assess repository populatrity
By default this package uses Github API to retireve the top 20 repositories with more than 1,000 followers.
The top X repositories can be adjusted using yaml file (see below)

## Input:
By default the code prints the top 20 repositories with results more than 1000 followers
*optional* user_config.yml file can be provided with key:value pair top_n: interger (and other plot settings)
There is a warning when more than 20 repositories is selected
- example user_config.yml:
```
gh_token: "github_pat_somethingsomething"
top_n: 15
plt_color: "red"
plt_title: "barbplot"
plt_x_title: "Top Github Repo"
plt_y_title: "Stargazer Counts"
fig_size: [10,6]
save_path: "/content"
```

- how to run gitrepo3 Analysis. Example script
```
# !pip install git+https://github.com/SplitInf/gitrepo3
# from gitrepo3 import Analysis

# analysis_obj = Analysis.Analysis('config.yml')
# analysis_obj.load_data()

# analysis_output = analysis_obj.compute_analysis()
# print(analysis_output)

# analysis_figure = analysis_obj.plot_data()
```

## output:
bar plot of top x repositories in the location determined by 'save_path' in yaml file

