# 주어진 시작 날짜와 끝 날짜에 해당하는 데이터가 담긴
# 데이터프레임을 반환하는 모듈입니다.
# 
# 반환되는 데이터프레임에 들어있는 정보는 다음과 같습니다.
#
# Date, weekday, weeknum, kospi_Close, kospi_Volume, kospi_Change
# kosdaq_Close, kosdaq_Volume, kosdaq_Change, nasdaq_Close
# usd_Close, usd_Change, jpy_Close, jpy_Change
# acf_Close, acf_Change, ugb_Close, vix_Close
# btc_Close, btc_Volume, btc_Change, kgb_Close, kgb_Change
#
# 사용 예시 : getData('20200106', '20220429')

# import libraries
import FinanceDataReader as fdr
import pandas as pd
import numpy as np

# getData() 에서 사용되는 함수들---------------------------------------------
# 1. function for columns renaming
def cols_rename(data_set, target_name):
    for i in data_set.columns:
        if i == 'Date':
            pass
        else:
            data_set.rename(columns={i:target_name+'_'+i}, inplace=True)
    return data_set

# 2. function for column renaming
def col_rename(data_set, name_from, name_to):
    for i in data_set.columns:
        if i != name_from:
            pass
        else:
            data_set.rename(columns={i:name_to}, inplace=True)
    return data_set

# 3. function for adjusting friday to sunday data as new friday data
def weekendToFriday(target, idx, col, returnType): # idx: Friday
    if (returnType == 'intType'):
        target.loc[idx, col] = (target.loc[idx, col]//7)*1 + (target.loc[idx+1, col]//7)*2 + (target.loc[idx+2, col]//7)*4
    elif (returnType == 'floatType'):
        target.loc[idx, col] = (target.loc[idx, col]/7)*1 + (target.loc[idx+1, col]/7)*2 + (target.loc[idx+2, col]/7)*4
    return target.loc[idx, col]
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

    # 암호화폐: 비트코인(BitCoin) 추가
    BTC = fdr.DataReader('BTC/KRW',start_date,end_date).reset_index()
    BTC['dayofweek'] = BTC['Date'].dt.dayofweek
    BTC.drop(['Open', 'High', 'Low'], axis=1, inplace=True)
    cols_rename(BTC, 'btc')
    if (BTC.loc[len(BTC)-1, 'btc_dayofweek'] == 5):
        BTC.drop(len(BTC)-1, inplace=True)
    if (BTC.loc[0, 'btc_dayofweek'] == 6):
        BTC.drop(0, inplace=True)
    elif (BTC.loc[0, 'btc_dayofweek'] == 5):
        BTC.drop(0, inplace=True)
        BTC.drop(1, inplace=True)
    for idx in BTC.index:
        if (BTC.loc[idx, 'btc_dayofweek'] == 6):
            BTC.loc[idx-2, 'btc_Close'] = weekendToFriday(BTC, idx-2, 'btc_Close', 'intType')
            BTC.loc[idx-2, 'btc_Volume'] = weekendToFriday(BTC, idx-2, 'btc_Volume', 'floatType')
            BTC.loc[idx-2, 'btc_Change'] = np.ceil(weekendToFriday(BTC, idx-2, 'btc_Change', 'floatType')*1000)/1000
    for idx in BTC.index:
        if (BTC.loc[idx, 'btc_dayofweek'] == 5 or BTC.loc[idx, 'btc_dayofweek'] == 6):
            BTC.drop(idx, inplace=True)
    BTC.drop(['btc_dayofweek'], axis=1, inplace=True)
    BTC.reset_index(inplace=True)
    BTC.drop(['index'], axis=1, inplace=True)
    data = pd.merge(data, BTC, how='outer')

    # 국채: 한국 국채 추가
    KGB = fdr.DataReader('KR10YT=RR', start_date, end_date).reset_index()
    KGB['dayofweek'] = KGB['Date'].dt.dayofweek
    KGB.drop(['Open', 'High', 'Low'], axis=1, inplace=True)
    cols_rename(KGB, 'kgb')
    if (KGB.loc[len(KGB)-1, 'kgb_dayofweek'] == 5):
        KGB.drop(len(KGB)-1, inplace=True)
    if (KGB.loc[0, 'kgb_dayofweek'] == 6):
        KGB.drop(0, inplace=True)
    elif (KGB.loc[0, 'kgb_dayofweek'] == 5):
        KGB.drop(0, inplace=True)
        KGB.drop(1, inplace=True)
    for idx in KGB.index:
        if (KGB.loc[idx, 'kgb_dayofweek'] == 6):
            KGB.loc[idx-2, 'kgb_Close'] = weekendToFriday(KGB, idx-2, 'kgb_Close', 'floatType')
            KGB.loc[idx-2, 'kgb_Change'] = weekendToFriday(KGB, idx-2, 'kgb_Change', 'floatType')
            KGB.loc[idx-2, 'kgb_Change'] = np.ceil(weekendToFriday(KGB, idx-2, 'kgb_Change', 'floatType')*1000)/1000
    for idx in KGB.index:
        if (KGB.loc[idx, 'kgb_dayofweek'] == 5 or KGB.loc[idx, 'kgb_dayofweek'] == 6):
            KGB.drop(idx, inplace=True)
    KGB.drop(['kgb_dayofweek'], axis=1, inplace=True)
    KGB.reset_index(inplace=True)
    KGB.drop(['index'], axis=1, inplace=True)
    data = pd.merge(data, KGB, how='outer')

    # NaN 값은 전일 값으로 대체. 
    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill') # 예외처리

    # 주어진 기간에 해당하는 정보들을 담은 데이터프레임 반환
    return data
    