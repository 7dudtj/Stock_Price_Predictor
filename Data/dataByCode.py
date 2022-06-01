# 주어진 시작 날짜와 끝 날짜에 해당하는 데이터가 담긴
# 데이터프레임을 반환하는 모듈입니다.
# 
# 반환되는 데이터프레임에 들어있는 정보는 다음과 같습니다.
#
# Date, Close, ma5, ma20, ma60
# ma5_Change, ma20_Change, ma60_Change
#
# 사용 예시 : getData('20200106', '20220429', '000060')

# import libraries
import FinanceDataReader as fdr
import numpy as np
from datetime import datetime, timedelta

# 주어진 기간에 해당하는 데이터프레임 반환 함수
def getData(start_date, end_date, code):

    # 시작일이 주말인 경우: 예외처리
    start_datetime = datetime.strptime(start_date, '%Y%m%d')
    if (start_datetime.weekday() == 5): # 시작: 토요일
        start_datetime += timedelta(days=2)
        start_date = start_datetime.strftime('%Y%m%d')
    elif (start_datetime.weekday() == 6): # 시작: 일요일
        start_datetime += timedelta(days=1)
        start_date = start_datetime.strftime('%Y%m%d')

    # start_data를 조정하여 ma 계산에 필요한 여분 데이터 확보
    new_start_datetime = start_datetime - timedelta(weeks=14)
    new_start_date = new_start_datetime.strftime('%Y%m%d')

    # 종목코드에 대한 종가 데이터 수집
    data = fdr.DataReader(code, new_start_date, end_date).reset_index()
    data.drop(['Open', 'High', 'Low', 'Change', 'Volume'], axis=1, inplace=True)

    # 5/20/60일 이동평균 계산
    ma5 = data['Close'].rolling(window=5).mean()
    data['ma5'] = ma5
    ma20 = data['Close'].rolling(window=20).mean()
    data['ma20'] = ma20
    ma60 = data['Close'].rolling(window=60).mean()
    data['ma60'] = ma60

    # 이동평균 변화율(Change) 계산
    data['ma5_Change'] = np.ceil((data['ma5']/data['ma5'].shift(1) - 1) * 100 * 10000)/10000
    data['ma20_Change'] = np.ceil((data['ma20']/data['ma20'].shift(1) - 1) * 100 * 10000)/10000
    data['ma60_Change'] = np.ceil((data['ma60']/data['ma60'].shift(1) - 1) * 100 * 10000)/10000

    # Nan 데이터 제거
    for idx in data.index:
        if (data.loc[idx, 'Date'].to_pydatetime().strftime('%Y%m%d') != start_date):
            data.drop(idx, inplace=True)
        else:
            break
    data.reset_index(inplace=True)
    data.drop(['index'], axis=1, inplace=True)

    # 이동평균 데이터타입 변환 (float to int)
    data['ma5'] = data['ma5'].astype(int)
    data['ma20'] = data['ma20'].astype(int)
    data['ma60'] = data['ma60'].astype(int)

    # 주어진 기간에 해당하는 정보들을 담은 데이터프레임 반환
    return data