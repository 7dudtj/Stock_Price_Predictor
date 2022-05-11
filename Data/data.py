# 주어진 시작 날짜와 끝 날짜에 해당하는 데이터가 담긴
# 데이터프레임을 반환하는 모듈입니다.
# 
# 반환되는 데이터프레임에 들어있는 정보는 다음과 같습니다.
#
# Date, weekday, weeknum, kospi_Close, kospi_Volume, kospi_Change
# kosdaq_Close, kosdaq_Volume, kosdaq_Change, nasdaq_Close
# usd_Close, usd_Change, jpy_Close, jpy_Change
# acf_Close, acf_Change, ugb_Close, vix_Close
#
# 사용 예시 : getData('20200106', '20220429')

# import libraries
import FinanceDataReader as fdr
import pandas as pd

# getData() 에서 사용되는 함수들---------------------------------------------
# 1. columns rename function
def cols_rename(data_set, target_name):
    for i in data_set.columns:
        if i == 'Date':
            pass
        else:
            data_set.rename(columns={i:target_name+'_'+i}, inplace=True)
    return data_set

# 2. column rename function
def col_rename(data_set, name_from, name_to):
    for i in data_set.columns:
        if i != name_from:
            pass
        else:
            data_set.rename(columns={i:name_to}, inplace=True)
    return data_set
# --------------------------------------------------------------------------


# 주어진 기간에 해당하는 데이터프레임 반환 함수
def getData(start_date, end_date):

    # make business_days: 주말 미포함
    Business_days = pd.DataFrame(pd.date_range(start_date, end_date, freq='B'), columns = ['Date'])
    Business_days['weekday'] = Business_days.Date.apply(lambda x: x.weekday())
    Business_days['weeknum'] = Business_days.Date.apply(lambda x: x.strftime('%V'))

    # KOSPI 추가
    KOSPI = fdr.DataReader('KS11', start_date, end_date).reset_index()
    KOSPI = KOSPI.drop(['Open', 'High', 'Low'], axis=1)
    cols_rename(KOSPI, 'kospi')
    data = pd.merge(Business_days, KOSPI, how='outer')

    # KOSDAQ 추가
    KOSDAQ = fdr.DataReader('KQ11', start_date, end_date).reset_index()
    KOSDAQ = KOSDAQ.drop(['Open', 'High', 'Low'], axis=1)
    cols_rename(KOSDAQ, 'kosdaq')
    data = pd.merge(data, KOSDAQ, how='outer')

    # 미국증시: 나스닥(NASDAQ) 추가
    NAS = fdr.DataReader('NASDAQCOM', start_date, end_date, data_source='fred').reset_index()
    col_rename(NAS, 'DATE', 'Date')
    col_rename(NAS, 'NASDAQCOM', 'nasdaq_Close')
    data = pd.merge(data, NAS, how='outer')

    # 환율: 원달러(USD) 추가
    USD = fdr.DataReader('USD/KRW', start_date, end_date).reset_index()
    USD = USD.drop(['Open', 'High', 'Low'], axis=1)
    cols_rename(USD, 'usd')
    data = pd.merge(data, USD, how='outer')

    # 환율: 원엔(JPY) 추가
    JPY = fdr.DataReader('JPY/KRW', start_date, end_date).reset_index()
    JPY = JPY.drop(['Open', 'High', 'Low'], axis=1)
    cols_rename(JPY, 'jpy')
    data = pd.merge(data, JPY, how='outer')

    # 환율: 호주달러/스위스프랑 추가
    ACF = fdr.DataReader('AUD/CHF', start_date, end_date).reset_index()
    ACF = ACF.drop(['Open', 'High', 'Low'], axis=1)
    cols_rename(ACF, 'acf')
    data = pd.merge(data, ACF, how='outer')

    # 국채: 미 국채 10년 추가
    UGB = fdr.DataReader('DGS10', start_date, end_date, data_source='fred').reset_index()
    col_rename(UGB, 'DATE', 'Date')
    col_rename(UGB, 'DGS10', 'ugb_Close')
    data = pd.merge(data, UGB, how='outer')

    # 변동성 지수 추가
    VIX = fdr.DataReader('VIXCLS', start_date, end_date, data_source='fred').reset_index()
    col_rename(VIX, 'DATE', 'Date')
    col_rename(VIX, 'VIXCLS', 'vix_Close')
    data = pd.merge(data, VIX, how='outer')

    # NaN 값은 전일 값으로 대체. 
    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill') # 예외처리

    # 주어진 기간에 해당하는 정보들을 담은 데이터프레임 반환
    return data


