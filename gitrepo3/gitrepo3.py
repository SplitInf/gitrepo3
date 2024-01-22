import requests #set http request to github
import json #used to interpret results by github
from pprint import pprint # pretty print
import matplotlib.pyplot as plt # plotting
import logging # error handling
import yaml # import (optional) yaml file
#import pandas as pd
import numpy as np

import os.path
import os



#create class
#https://www.programiz.com/python-programming/property
#https://stackoverflow.com/questions/25158930/how-to-return-objects-from-methods-in-python

class Analysis():
  def __init__(self, config_file):

    ##verify parameters##
    #get directory
    cur_dir=os.getcwd()
    os.chdir(cur_dir)

    #check if file path exist
    if os.path.isfile("configs/"+config_file):
      with open("configs/"+config_file, "r") as yaml_f:
        try:
            config = yaml.safe_load(yaml_f) 
        except yaml.YAMLError as exc:
            print(exc)
    else:
      logging.warning(f'No config_file detected. Using default settings.')
      default_config_path="configs/system_config.yml"
      with open(default_config_path, "r") as yaml_f:
        try:
            config = yaml.safe_load(yaml_f) 
        except yaml.YAMLError as exc:
            print(exc)

    # parameter check
    top_n=config['top_n']
    try:
      str(top_n).isnumeric()
    except ValueError:
      logging.error(f'Parameter top_n must be integer! {top_n} provided')

    if top_n > 20:
      logging.warning(f'When parameter top_n is > 20 the plot may not be legible')
    
    #return config
    self.config = config

   

  def load_data(self) -> tuple:
    """ Function to retrieve top X repo from github
    returns tuple containing repo name and stargazer count

    Parameters
    ----------
    top_n : int
      the top X repo to retrieve

    config : dict
      dictionary of load_data and plot_data settings

    Returns
    ----------
    returns tuple of repo_name and stargazer_count

    """

    #settings
    top_n = self.config['top_n']

    # retrieve secrets
    token = self.config['gh_token']

    
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

    print(r_json)
    for item in r_json['items'][:top_n]:
      repo_name.append(item['name'])
      repo_counts.append(item['stargazers_count'])
   
    #return values
    tuple_plt = (repo_name, repo_counts)
    self.data = tuple_plt

  # def compute_analysis(repo_name: list, repo_counts: list, ) -> None:
  def plot_data(self) -> None:
    """ Function to create bar plot based on name and count lists
    returns bar plot from matplotlib based on provided lists

    Parameters
    ----------
    repo_name : list
      list of names to be plotted. From self.data[0]
    repo_counts : list
      list of counts. From self.data[1]
    plot_settings : list
      array of plot settings. From self.config

    Returns
    ----------
    matplot lib barplot in location specified in save_path

    """
    ## plot ##

    #get data
    repo_name = self.data[0]
    repo_counts = self.data[1]

    #get plot settings
    plot_settings = self.config
    plt_color= plot_settings["plt_color"]
    plt_title= plot_settings["plt_title"]
    plt_x_title= plot_settings["plt_x_title"]
    plt_y_title= plot_settings["plt_y_title"]
    fig_size= plot_settings["fig_size"]
    save_path = plot_settings["save_path"]


    #make sure the lengths are the same
    assert len(repo_name)==len(repo_counts), "length of two lists don't match"
    top_n=len(repo_name)

    final_plt_title = plt_title + "( top " + str(top_n) + ")"
    # Plot bar chart
    print(f'Plotting top {top_n} repo')

    plt.figure(figsize=fig_size)
    plt.bar(repo_name, repo_counts, color=plt_color)
    plt.title(f"{final_plt_title}")

    plt.xlabel(plt_x_title)
    plt.ylabel(plt_y_title)

    plt.xticks(rotation=90)
    plt.savefig(save_path+"/"+'barplot.png')
    plt.show()


  def compute_analysis(self) -> None:
    """ Function to find out what the most frequent character is from github repos
    returns list of top characters, sorted along with number of times observed.

    Parameters
    ----------
    repo_name : list
      list of names to be plotted. From self.data[0]

    Returns
    ----------
    list of top characters, sorted along with number of times observed.

    """

    #get repo names and concat to string
    string = ''.join(self.data[0])
    char_list = []
    for letter in string:
      char_list.append(letter)

    #count most freq char
    char_freq={}

    for i in char_list:
        if i in char_freq:
            char_freq[i]=char_freq[i]+1
        else:
            char_freq[i] = 1
    #sort
    print('the most freq characters are calculated')
    result = sorted(char_freq.items(), key=lambda x:x[1], reverse= True)
    return result

