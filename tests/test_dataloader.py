import pandas as pd
import pytest
import warnings

from src.dataloader import DataLoader

from pandas.testing import assert_frame_equal


@pytest.fixture
def df_should():
    return pd.DataFrame({
        "Note": [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
        "Anzahl": [3, 4, 10, 5, 4, 12, 10, 17, 24, 22],
        "Prozent": [0.65, 0.87, 2.17, 1.09, 0.87, 2.71, 2.17, 3.7, 5.22, 4.78],
        "Kumuliert": [0.65, 1.52, 3.69, 4.78, 8.26, 10.43, 14.13, 19.35, 24.13, 27.83]
    })


@pytest.fixture
def dataloader():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    return DataLoader("tests/assets/::ECTS_Tab_WS23_24_BA_TEST_DE.pdf")


def test_load_data_return_correct_df(dataloader, df_should):
    dataloader.load_data()
    assert_frame_equal(dataloader.get_df(), df_should)


def test_get_df_return_correct_df(dataloader):
    dataloader.load_data()
    df = dataloader.get_df()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_get_study_return_correct_name(dataloader):
    dataloader.load_data()
    assert dataloader.get_study() == "WS23_24_BA_TEST_DE"
