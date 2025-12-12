import pytest
import data_clean as d

def test_validate_date():
    # Valid Cases
    assert d.validate_date("2022-09-24T13:53:14") == True
    
    # Invalid Cases
    assert d.validate_date("24-09-2022T13:53:14") == False 
    assert d.validate_date("2022-09-2413:53:14") == False 
    assert d.validate_date("2022-18-24T13:53") == False
    assert d.validate_date("134") == False  
    assert d.validate_date("RandomString") == False  

def test_validate_integer():
    # Valid Cases
    assert d.validate_integer("10") == True

    # Invalid Cases
    assert d.validate_integer("10.0") == False
    assert d.validate_integer("-10") == False
    assert d.validate_integer("abcde") == False
    assert d.validate_integer("10abc") == False


def test_validate_request():
    # Valid Cases
    assert d.validate_request('GET /data/m/lust_+caution+2007/121.mpg') == True
    assert d.validate_request('GET /rate/philomena+2013=3') == True

    # Invalid Cases
    assert d.validate_request('GET /rate/philomena+2013=-3') == False
    assert d.validate_request('GET /rate/philomena+2013=15') == False
    assert d.validate_request('GET /rate/philomena+2013') == False
    assert d.validate_request('GET /ratesd/philomena+2013=-3') == False
    assert d.validate_request('GET //philomena+2013=-3') == False 
    assert d.validate_request('GET /fjaedata/m/lust_+caution+2007/121.mpg') == False
    assert d.validate_request('GET /data/m/lust_+caution+2007/-1121.mpg') == False
    

def test_data_quality_check():
    # Valid Cases
    assert d.data_quality_check('2022-09-24T13:53:17,336391,GET /data/m/the+swell+season+2011/38.mpg') == True
    assert d.data_quality_check('2022-09-24T13:53:17,198934,GET /rate/carandiru+2003=4') == True
    
    # Invalid Cases
    assert d.data_quality_check('2022-09-24T13:53:17,,GET /data/m/the+swell+season+2011/38.mpg') == False
    assert d.data_quality_check('2022-09-24T13:53:17,336391,') == False
    assert d.data_quality_check(',336391,GET /data/m/the+swell+season+2011/38.mpg') == False
    assert d.data_quality_check('2022-09-24T13:53:17,,GET /rate/carandiru+2003=4') == False 
    assert d.data_quality_check('2022-09-24T13:53:17,198934,') == False
    assert d.data_quality_check(',198934,GET /rate/carandiru+2003=4') == False 
    assert d.data_quality_check('Gibberish Text') == False

    
# def test_data_clean():
