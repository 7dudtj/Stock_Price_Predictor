# Stock Price Predictor  

- 다음주의 주식은 오를까요? 내릴까요?
- 다음주의 주식 가격 추이를 예측해보고, 투자에 활용해보세요!
- <ins>**모든 투자의 책임은 본인에게 있습니다.**</ins>

---

## What is Stock Price Predictor?

<p align="center">
  <img width="400" src="https://user-images.githubusercontent.com/67851701/174953510-297cbdc5-46db-4100-8271-993b4325ecd7.jpg">  
</p>
  
주식의 가격이 낮을 때 매수하고 높을 때 매도한다면 얼마나 좋을까요?  
하지만 현실은 녹록치 않습니다.  
내가 사면 가격이 떨어지고, 내가 팔면 가격이 오르는 일을 종종 경험할 수 있습니다.  
일반인 투자자 입장에서, 정보가 부족하기 때문에 주식으로 낭패를 보는 일이 많이 있습니다.  

그러나, 미래의 주식 가격을 예측할 수 있다면 어떠할까요?  
다음주 주식 가격의 추이를 알 수 있다면 투자를 결정하는 데에 큰 도움이 될겁니다!  

**Stock Price Predictor**는 수년간 쌓인 금융 데이터를 기반으로 다음주 가격을 예측합니다!  
KOSPI와 KOSDAQ에 상장되어 있는 주식에 대하여 가격을 예측하며,  
예측 대상 주식은 [주가 예측 주식 목록](https://github.com/7dudtj/Stock_Price_Predictor/blob/main/Data/stock_list.csv) 에서 확인할 수 있습니다.  

그렇다면 **Stock Price Predictor**는 어떻게 주식 가격을 예측할까요?

---

## Idea

**Stock Price Predictor**는 수년간의 주식 및 금융 데이터를 수집하고,  
수집된 시계열 데이터를 모델에 학습시켜서 다음주 주식 가격을 예측합니다.  

KOSPI와 KOSDAQ에 영향을 주는 세계 주요 금융 지표들을 선정하여서 같이 학습하고자 하였고,  
여러 금융 지표들과 국내 시장 간의 상관관계를 분석한 후 상관계수가 높은 지표들을 선발하였습니다.  

<p align="center">
  <img width="640" src="https://github.com/7dudtj/Stock_Price_Predictor/blob/main/Data/DataAnalysis/Result/NAS_Analysis.png">
</p>  

위의 사진은 미국 NASDAQ 지수와 한국 KOSPI & KOSDAQ 지수의 상관관계를 분석한 결과입니다.   
전일 NASDAQ 지수와 국내 증시가 높은 상관관계를 보이는 것을 통해,  
국내 증시가 미국 증시에 큰 영향을 받음을 알 수 있습니다.  

이처럼 세계 주요 금융지표 및 자산과 국내 시장 간의 상관관계를 분석하였고,  
분석 결과 높은 상관계수를 보인 지표를 선정하여 학습 데이터로 사용하였습니다.  

더 자세한 분석 결과를 보고 싶으시다면, [상관관계 분석 결과](https://github.com/7dudtj/Stock_Price_Predictor/blob/main/Data/DataAnalysis/CorrelationCoefficient.ipynb) 에서 확인할 수 있습니다.

---

## How to use?

1. **Stock Price Predictor**를 clone하고, requirements를 설치합니다.  
```
git clone https://github.com/7dudtj/Stock_Price_Predictor.git # clone
cd Stock_Price_Predictor
pip install -r requirements.txt # install
```
2. 모델을 고르고, 예측하고자 하는 날짜에 맞춰서 'end_date'를 변경합니다.
```
Code 폴더에 여러 모델이 있습니다. Code/LinearRegression0603/FCPriceDiff.ipynb를 추천하며,  
예측은 월~금 단위로 진행해야 합니다.
22년 5월 23일(월) ~ 22년 5월 27일(금) 기간의 가격을 예측하고 싶을 경우,
end_date를 예측 마지막 날인 '20220527'로 설정해야 합니다.
```
3. 학습을 진행하면, 예측 결과를 받아볼 수 있습니다.
```
.ipynb 파일을 실행하세요. 학습이 완료되면, 예측 결과는 submission.csv 파일에 저장됩니다.
```

---

## Warning

<p align="center">
  <img width="400" src="https://user-images.githubusercontent.com/67851701/174976264-43524462-13e8-4dda-b66d-2278297aa9a4.jpg">
</p> 

<ins>**모든 투자의 책임은 본인에게 있습니다.**</ins>  
**Stock Price Predictor**는 주식 가격을 정확하게 예측할 수 없습니다.  
또한, 주식 가격의 추이 또한 정확하게 예측할 수 없습니다.  
그 누구도, 그 어떤 프로그램도 미래의 주식을 정확하게 예측할 수 없습니다.  

주식 투자로 발생하는 모든 손실은 본인의 책임이며,  
**Stock Price Predictor**는 참고용으로만 사용하시길 바랍니다.  

---

## Copyleft / End User License
<details>
<summary>
내용 보기
</summary>
<div markdown="1">
<img align="right" src="http://opensource.org/trademarks/opensource/OSI-Approved-License-100x137.png">

The class is licensed under the [MIT License](http://opensource.org/licenses/MIT):

Copyright &copy; 2022 [7dudtj](https://github.com/7dudtj), [kgh1030](https://github.com/kgh1030), and [hoyongjungdev](https://github.com/hoyongjungdev).

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  </div>
  </details>