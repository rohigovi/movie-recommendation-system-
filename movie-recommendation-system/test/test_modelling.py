import sys
sys.path.append('..')
import pytest
import Modelling
import numpy as np

#test for process data function
def test_check_traintest():
    train,test=Modelling.process_data()
    assert ['userid','movieid','rating']==list(train.columns)
    assert ['userid','movieid','rating']==list(test.columns)
    assert len(train)>len(test)


def test_check_rmse():
    randnums1= np.random.randint(1,101,20)
    randnums2=np.random.randint(1,101,20)
    assert Modelling.rmse(randnums1,randnums2) is not None
    assert str(type(Modelling.rmse(randnums1,randnums2)))=='<class \'numpy.float64\'>'
    

