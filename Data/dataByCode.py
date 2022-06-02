# �־��� ���� ��¥�� �� ��¥�� �ش��ϴ� �����Ͱ� ���
# �������������� ��ȯ�ϴ� ����Դϴ�.
# 
# ��ȯ�Ǵ� �����������ӿ� ����ִ� ������ ������ �����ϴ�.
#
# Date, Close, ma5, ma20, ma60
# ma5_Change, ma20_Change, ma60_Change
#
# ��� ���� : getData('000060', '20200106', '20220429')

# import libraries
import FinanceDataReader as fdr
import numpy as np
from datetime import datetime, timedelta
import math

# �־��� �Ⱓ�� �ش��ϴ� ������������ ��ȯ �Լ�
def getData(code, start_date, end_date):

    # �������� �ָ��� ���: ����ó��
    start_datetime = datetime.strptime(start_date, '%Y%m%d')
    if (start_datetime.weekday() == 5): # ����: �����
        start_datetime += timedelta(days=2)
        start_date = start_datetime.strftime('%Y%m%d')
    elif (start_datetime.weekday() == 6): # ����: �Ͽ���
        start_datetime += timedelta(days=1)
        start_date = start_datetime.strftime('%Y%m%d')

    # �����ڵ忡 ���� ���� ������ ����
    data = fdr.DataReader(code, start_date, end_date)
    data.drop(['Open', 'High', 'Low', 'Change', 'Volume'], axis=1, inplace=True)

    # 5/20/60�� �̵���� ���
    ma5 = data['Close'].rolling(window=5).mean()
    data['ma5'] = ma5
    ma20 = data['Close'].rolling(window=20).mean()
    data['ma20'] = ma20
    ma60 = data['Close'].rolling(window=60).mean()
    data['ma60'] = ma60

    # NaN ������ ����: ma5�� Close��, ma20�� ma5��, ma60�� ma20���� ��ü
    for idx in data.index:
        if (math.isnan(data.loc[idx, 'ma5'])):
            data.loc[idx, 'ma5'] = data.loc[idx, 'ma20'] = data.loc[idx, 'ma60'] = data.loc[idx, 'Close']
        if (math.isnan(data.loc[idx, 'ma20'])):
            data.loc[idx, 'ma20'] = data.loc[idx, 'ma60'] = data.loc[idx, 'ma5']
        if (math.isnan(data.loc[idx, 'ma60'])):
            data.loc[idx, 'ma60'] = data.loc[idx, 'ma20']

    # �̵���� ��ȭ��(Change) ���
    data['ma5_Change'] = np.ceil((data['ma5']/data['ma5'].shift(1) - 1) * 100 * 10000)/10000
    data['ma20_Change'] = np.ceil((data['ma20']/data['ma20'].shift(1) - 1) * 100 * 10000)/10000
    data['ma60_Change'] = np.ceil((data['ma60']/data['ma60'].shift(1) - 1) * 100 * 10000)/10000
    data.fillna(method='bfill', inplace=True)
            
    # �̵���� ������Ÿ�� ��ȯ (float to int)
    data['ma5'] = data['ma5'].astype(int)
    data['ma20'] = data['ma20'].astype(int)
    data['ma60'] = data['ma60'].astype(int)

    # �־��� �Ⱓ�� �ش��ϴ� �������� ���� ������������ ��ȯ
    return data