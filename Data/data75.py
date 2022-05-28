# �־��� ���� ��¥�� �� ��¥�� �ش��ϴ� �����Ͱ� ���
# �������������� ��ȯ�ϴ� ����Դϴ�.
# 
# data ��⿡ �ݿ��Ǵ� ������ ��, 
# KOSPI�� �������� �������� 0.75�� �Ѵ� ��ǥ�� �����͵鸸 ��ҽ��ϴ�.
# ��ȯ�Ǵ� �����������ӿ� ����ִ� ������ ������ �����ϴ�.
#
# Date, weekday, weeknum, kospi_Close, kospi_Volume, kospi_Change
# kosdaq_Close, kosdaq_Volume, kosdaq_Change, nasdaq_Close
# jpy_Close, jpy_Change, acf_Close, acf_Change
# btc_Close, btc_Volume, btc_Change
#
# ��� ���� : getData('20200106', '20220429')

# import libraries
import FinanceDataReader as fdr
import pandas as pd
import numpy as np

# getData() ���� ���Ǵ� �Լ���---------------------------------------------
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

# �־��� �Ⱓ�� �ش��ϴ� ������������ ��ȯ �Լ�
def getData(start_date, end_date):

    # make business_days: �ָ� ������
    Business_days = pd.DataFrame(pd.date_range(start_date, end_date, freq='B'), columns = ['Date'])
    Business_days['weekday'] = Business_days.Date.apply(lambda x: x.weekday())
    Business_days['weeknum'] = Business_days.Date.apply(lambda x: x.strftime('%V'))

    # KOSPI �߰�
    KOSPI = fdr.DataReader('KS11', start_date, end_date).reset_index()
    KOSPI = KOSPI.drop(['Open', 'High', 'Low'], axis=1)
    cols_rename(KOSPI, 'kospi')
    data = pd.merge(Business_days, KOSPI, how='outer')

    # KOSDAQ �߰�
    KOSDAQ = fdr.DataReader('KQ11', start_date, end_date).reset_index()
    KOSDAQ = KOSDAQ.drop(['Open', 'High', 'Low'], axis=1)
    cols_rename(KOSDAQ, 'kosdaq')
    data = pd.merge(data, KOSDAQ, how='outer')

    # �̱�����: ������(NASDAQ) �߰�
    NAS = fdr.DataReader('NASDAQCOM', start_date, end_date, data_source='fred').reset_index()
    col_rename(NAS, 'DATE', 'Date')
    col_rename(NAS, 'NASDAQCOM', 'nasdaq_Close')
    data = pd.merge(data, NAS, how='outer')

    # ȯ��: ���޷�(USD) >> ������ 0.75 �̸��̹Ƿ� ����

    # ȯ��: ����(JPY) �߰�
    JPY = fdr.DataReader('JPY/KRW', start_date, end_date).reset_index()
    JPY = JPY.drop(['Open', 'High', 'Low'], axis=1)
    cols_rename(JPY, 'jpy')
    data = pd.merge(data, JPY, how='outer')

    # ȯ��: ȣ�ִ޷�/���������� �߰�
    ACF = fdr.DataReader('AUD/CHF', start_date, end_date).reset_index()
    ACF = ACF.drop(['Open', 'High', 'Low'], axis=1)
    cols_rename(ACF, 'acf')
    data = pd.merge(data, ACF, how='outer')

    # ��ä: �� ��ä 10�� �߰� >> ������ 0.75 �̸��̹Ƿ� ����

    # ������ ���� �߰� >> ������ 0.75 �̸��̹Ƿ� ����

    # ��ȣȭ��: ��Ʈ����(BitCoin) �߰�
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

    # ��ä: �ѱ� ��ä �߰� >> ������ 0.75 �̸��̹Ƿ� ����

    # NaN ���� ���� ������ ��ü. 
    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill') # ����ó��

    # �־��� �Ⱓ�� �ش��ϴ� �������� ���� ������������ ��ȯ
    return data
    