import requests #set http request to github
import json #used to interpret results by github
from pprint import pprint # pretty print
import matplotlib.pyplot as plt # plotting
import logging # error handling
import yaml # import (optional) yaml file
import os.path



class Analysis():

  def __init__(self, config_file):
    self.config_file = config_file

  #set return annotation to be dict for checking
  def get_top_n(config_file: str) -> int:

    """ Function to retrieve the top X based on user provided yaml config file
    returns int based on yaml file. If file is not found, the default of 20 is returned

    Parameters
    ----------
    config_file : str
      where yaml file is located

    Returns
    ----------
    top_n

    """
    if os.path.isfile(config_file):
      with open(config_file, "r") as yaml_f:
        try:
            top_n_yaml = yaml.safe_load(yaml_f)
            top_n = top_n_yaml['top_n'] # by default expects 'top_n' as key
        except yaml.YAMLError as exc:
            print(exc)
    else:
      logging.warning(f'No config_file detected. Using default 20.')
      top_n=20 # default top_n value

    # parameter check
    try:
      str(top_n).isnumeric()
    except ValueError:
      logging.error(f'Parameter top_n must be integer! {top_n} provided')

    if top_n > 20:
      logging.warning(f'When parameter top_n is > 20 the plot may not be legible')

    return top_n

  def get_data(top_n: int, preview: bool =True) -> tuple:
    """ Function to retrieve top X repo from github
    returns tuple containing repo name and stargazer count

    Parameters
    ----------
    top_n : int
      the top X repo to retrieve
    preview : bool
      whether to preview the data

    Returns
    ----------
    returns tuple of repo_name and stargazer_count

    """
    # check top_n
    if not isinstance(top_n, int):
      raise TypeError('Please provide a int argument')


    # retrieve secrets
    from google.colab import userdata
    token = userdata.get('ghtoken')
    
    # construct API request #
    #https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-users
    url = 'https://api.github.com/search/repositories?q=followers:>1000&order=desc'  #works
    headers = {'Authorization': 'Bearer ' + token}

    # retrieve using requests
    r = requests.get(url, headers=headers)
    r_json = json.loads(r.text) # .text to access response content

    ## retrieve data ##
    # retrieve name and counts in separate lists
    repo_name = []
    repo_counts = []
    for item in r_json['items'][:top_n]:
      repo_name.append(item['name'])
      repo_counts.append(item['stargazers_count'])

    #print results
    if preview:
      for r, c in zip(repo_name,repo_counts):
        print(f"{r} ({c})")
    
    return repo_name, repo_counts


  def get_plot(repo_name: list, repo_counts: list, ) -> None:
    """ Function to create bar plot based on name and count lists
    returns bar plot from matplotlib based on provided lists

    Parameters
    ----------
    repo_name : list
      list of names to be plotted
    repo_counts : list
      list of counts


    Returns
    ----------
    matplot lib barplot

    """
    ## plot ##

    #make sure the lengths are the same
    assert len(repo_name)==len(repo_counts), "length of two lists don't match"
    top_n=len(repo_name)

    # Plot bar chart
    print(f'Plotting top {top_n} repo')
    plt.bar(repo_name, repo_counts)
    plt.title(f"Top {top_n} Most Starred GitHub Repositories")
    plt.ylabel("Number of starred counts")
    plt.xlabel("Ranks")
    plt.xticks(rotation=90)
    plt.show()



