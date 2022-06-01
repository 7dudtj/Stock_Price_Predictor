# �־��� ���� ��¥�� �� ��¥�� �ش��ϴ� �����Ͱ� ���
# �������������� ��ȯ�ϴ� ����Դϴ�.
# 
# ��ȯ�Ǵ� �����������ӿ� ����ִ� ������ ������ �����ϴ�.
#
# Date, Close, ma5, ma20, ma60
# ma5_Change, ma20_Change, ma60_Change
#
# ��� ���� : getData('20200106', '20220429', '000060')

# import libraries
import FinanceDataReader as fdr
import numpy as np
from datetime import datetime, timedelta

# �־��� �Ⱓ�� �ش��ϴ� ������������ ��ȯ �Լ�
def getData(start_date, end_date, code):

    # �������� �ָ��� ���: ����ó��
    start_datetime = datetime.strptime(start_date, '%Y%m%d')
    if (start_datetime.weekday() == 5): # ����: �����
        start_datetime += timedelta(days=2)
        start_date = start_datetime.strftime('%Y%m%d')
    elif (start_datetime.weekday() == 6): # ����: �Ͽ���
        start_datetime += timedelta(days=1)
        start_date = start_datetime.strftime('%Y%m%d')

    # start_data�� �����Ͽ� ma ��꿡 �ʿ��� ���� ������ Ȯ��
    new_start_datetime = start_datetime - timedelta(weeks=14)
    new_start_date = new_start_datetime.strftime('%Y%m%d')

    # �����ڵ忡 ���� ���� ������ ����
    data = fdr.DataReader(code, new_start_date, end_date).reset_index()
    data.drop(['Open', 'High', 'Low', 'Change', 'Volume'], axis=1, inplace=True)

    # 5/20/60�� �̵���� ���
    ma5 = data['Close'].rolling(window=5).mean()
    data['ma5'] = ma5
    ma20 = data['Close'].rolling(window=20).mean()
    data['ma20'] = ma20
    ma60 = data['Close'].rolling(window=60).mean()
    data['ma60'] = ma60

    # �̵���� ��ȭ��(Change) ���
    data['ma5_Change'] = np.ceil((data['ma5']/data['ma5'].shift(1) - 1) * 100 * 10000)/10000
    data['ma20_Change'] = np.ceil((data['ma20']/data['ma20'].shift(1) - 1) * 100 * 10000)/10000
    data['ma60_Change'] = np.ceil((data['ma60']/data['ma60'].shift(1) - 1) * 100 * 10000)/10000

    # Nan ������ ����
    for idx in data.index:
        if (data.loc[idx, 'Date'].to_pydatetime().strftime('%Y%m%d') != start_date):
            data.drop(idx, inplace=True)
        else:
            break
    data.reset_index(inplace=True)
    data.drop(['index'], axis=1, inplace=True)

    # �̵���� ������Ÿ�� ��ȯ (float to int)
    data['ma5'] = data['ma5'].astype(int)
    data['ma20'] = data['ma20'].astype(int)
    data['ma60'] = data['ma60'].astype(int)

    # �־��� �Ⱓ�� �ش��ϴ� �������� ���� ������������ ��ȯ
    return data