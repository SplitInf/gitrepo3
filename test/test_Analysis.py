import pytest
from gitrepo3 import Analysis


#test when non int arguement is provided to load_data
def test_load_data_non_str_arguments():
  with pytest.raises(TypeError):
    Analysis.Analysis(12341234)
