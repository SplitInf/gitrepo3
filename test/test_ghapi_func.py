import pytest
from ghapi import ghapi_func

#test whether default is returned when file path is not found
def test_get_top_n_default():
  assert ghapi_func.Analysis.get_top_n("") == 20

#test when non int arguement is provided to get_data
def test_get_data_non_int_arguments():
  with pytest.raises(TypeError):
    ghapi_func.Analysis.get_data("BLAH", False)

