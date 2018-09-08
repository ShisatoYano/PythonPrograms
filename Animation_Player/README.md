sfevent_ods_analysis.py
===============

SFEVENT.txt����ODS���m�G���[�̔���񐔂��W�v����

## Description  
��͂���SFEVETN���L�^����Ă����g���b�N�̍��@�A���t���Ƃ�  
ODS�e�Z���T�̌��m�G���[�̔����񐔂��J�E���g���ăO���t������B  
�����ŃO���t���쐬���āA�����͉摜�t�@�C���ŕۑ������B  

## Author
Shisato Yano

## Dependency
Python 3.6.5 :: Anaconda  
�ȉ��̃��W���[����import���Ă�������  
���W���[���� ����������m�F�����ۂ̃o�[�W����  
matplotlib 2.2.2  
pandas     0.23.3  
numpy      1.14.2  
tqdm       4.24.0  
tkinter    8.6  
os  

## Usage
1. ��͂���SFEVENT.txt��S�Ĉ�̃f�B���N�g���ɒu���Ă���  
![image_alt_text](http://192.168.3.2:8011/yano/FRDataAnalysisTools/blob/master/SfEventOdsAnalysis/image_sample/SFEVENT_Directory.PNG?raw=true)  

2. python sfevent_ods_analysis.py�Ńc�[�����N��  

3. �f�B���N�g����I������_�C�A���O���J���̂ŁA1�ō쐬�����f�B���N�g����I������  
![image_alt_text](http://192.168.3.2:8011/yano/FRDataAnalysisTools/blob/master/SfEventOdsAnalysis/image_sample/Select_Directory.PNG?raw=true)  

4. �f�[�^�ǂݍ��݂Ɖ�͂����s����ACompleted�̃��b�Z�[�W���\�����ꂽ�犮��(OK������)  
![image_alt_text](http://192.168.3.2:8011/yano/FRDataAnalysisTools/blob/master/SfEventOdsAnalysis/image_sample/Run_Completed.PNG?raw=true)  

5. �쐬���ꂽ�O���t�̉摜�̓\�[�X�t�@�C���Ɠ����f�B���N�g���ɕۑ������(~.png)  

## Result samples
�傫��������3��ނ̃O���t���쐬�����B  
1. ������t�ɂ����āA�e�G���[���ǂ̃g���b�N�ŉ���N������  
![image_alt_text](http://192.168.3.2:8011/yano/FRDataAnalysisTools/blob/master/SfEventOdsAnalysis/image_sample/Error_Count_BarGraph_180801.png?raw=true)  

2. ��̃G���[���A�e���t�ɂĂǂ̃g���b�N�ŉ���N������  
![image_alt_text](http://192.168.3.2:8011/yano/FRDataAnalysisTools/blob/master/SfEventOdsAnalysis/image_sample/Error_Count_BarGraph_LRL.png?raw=true)  

3. ���̃g���b�N�ŁA�e���t�ɂĂǂ̃G���[������N������  
![image_alt_text](http://192.168.3.2:8011/yano/FRDataAnalysisTools/blob/master/SfEventOdsAnalysis/image_sample/Error_Count_BarGraph_T05.png?raw=true)  

