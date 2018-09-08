sfevent_ods_analysis.py
===============

SFEVENT.txtからODS検知エラーの発報回数を集計する

## Description  
解析するSFEVETNが記録されていたトラックの号機、日付ごとに  
ODS各センサの検知エラーの発生回数をカウントしてグラフ化する。  
自動でグラフを作成して、それらは画像ファイルで保存される。  

## Author
Shisato Yano

## Dependency
Python 3.6.5 :: Anaconda  
以下のモジュールをimportしてください  
モジュール名 自分が動作確認した際のバージョン  
matplotlib 2.2.2  
pandas     0.23.3  
numpy      1.14.2  
tqdm       4.24.0  
tkinter    8.6  
os  

## Usage
1. 解析したSFEVENT.txtを全て一つのディレクトリに置いておく  
![image_alt_text](http://192.168.3.2:8011/yano/FRDataAnalysisTools/blob/master/SfEventOdsAnalysis/image_sample/SFEVENT_Directory.PNG?raw=true)  

2. python sfevent_ods_analysis.pyでツールを起動  

3. ディレクトリを選択するダイアログが開くので、1で作成したディレクトリを選択する  
![image_alt_text](http://192.168.3.2:8011/yano/FRDataAnalysisTools/blob/master/SfEventOdsAnalysis/image_sample/Select_Directory.PNG?raw=true)  

4. データ読み込みと解析が実行され、Completedのメッセージが表示されたら完了(OKを押す)  
![image_alt_text](http://192.168.3.2:8011/yano/FRDataAnalysisTools/blob/master/SfEventOdsAnalysis/image_sample/Run_Completed.PNG?raw=true)  

5. 作成されたグラフの画像はソースファイルと同じディレクトリに保存される(~.png)  

## Result samples
大きく分けて3種類のグラフが作成される。  
1. ある日付において、各エラーがどのトラックで何回起きたか  
![image_alt_text](http://192.168.3.2:8011/yano/FRDataAnalysisTools/blob/master/SfEventOdsAnalysis/image_sample/Error_Count_BarGraph_180801.png?raw=true)  

2. 一つのエラーが、各日付にてどのトラックで何回起きたか  
![image_alt_text](http://192.168.3.2:8011/yano/FRDataAnalysisTools/blob/master/SfEventOdsAnalysis/image_sample/Error_Count_BarGraph_LRL.png?raw=true)  

3. 一台のトラックで、各日付にてどのエラーが何回起きたか  
![image_alt_text](http://192.168.3.2:8011/yano/FRDataAnalysisTools/blob/master/SfEventOdsAnalysis/image_sample/Error_Count_BarGraph_T05.png?raw=true)  

