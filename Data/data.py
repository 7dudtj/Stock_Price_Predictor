# �־��� ���� ��¥�� �� ��¥�� �ش��ϴ� �����Ͱ� ���
# �������������� ��ȯ�ϴ� ����Դϴ�.
# 
# ��ȯ�Ǵ� �����������ӿ� ����ִ� ������ ������ �����ϴ�.
#
# Date, weekday, weeknum, kospi_Close, kospi_Volume, kospi_Change
# kosdaq_Close, kosdaq_Volume, kosdaq_Change, nasdaq_Close
# usd_Close, usd_Change, jpy_Close, jpy_Change
# acf_Close, acf_Change, ugb_Close, vix_Close
#
# ��� ���� : getData('20200106', '20220429')

# import libraries
import FinanceDataReader as fdr
import pandas as pd

# getData() ���� ���Ǵ� �Լ���---------------------------------------------
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

    # ȯ��: ���޷�(USD) �߰�
    USD = fdr.DataReader('USD/KRW', start_date, end_date).reset_index()
    USD = USD.drop(['Open', 'High', 'Low'], axis=1)
    cols_rename(USD, 'usd')
    data = pd.merge(data, USD, how='outer')

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

    # ��ä: �� ��ä 10�� �߰�
    UGB = fdr.DataReader('DGS10', start_date, end_date, data_source='fred').reset_index()
    col_rename(UGB, 'DATE', 'Date')
    col_rename(UGB, 'DGS10', 'ugb_Close')
    data = pd.merge(data, UGB, how='outer')

    # ������ ���� �߰�
    VIX = fdr.DataReader('VIXCLS', start_date, end_date, data_source='fred').reset_index()
    col_rename(VIX, 'DATE', 'Date')
    col_rename(VIX, 'VIXCLS', 'vix_Close')
    data = pd.merge(data, VIX, how='outer')

    # NaN ���� ���� ������ ��ü. 
    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill') # ����ó��

    # �־��� �Ⱓ�� �ش��ϴ� �������� ���� ������������ ��ȯ
    return data


