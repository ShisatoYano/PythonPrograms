# coding: shift-jis

"""
SimpleRadarSimulator.py

User can operate a target by inputting velosity and yawrate.
This program can simulate a static/dynamic target detection.
Distance, horizontal angle, velosity on range and angle direction.

Author: Shisato Yano
Last Update: 2018/07/04
"""

from math import sin, cos, tan
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider

# ラジオボタン用の背景色を設定
radioButtonColor = 'lightgoldenrodyellow'

# シミュレーション中の刻み時間[s]
deltaTime_sec = 0.05

# レーダの検知可能範囲をパラメータ
# 検知可能距離
maxRange_mm    = 80000
minRange_mm    = 5000
# 検知可能角度
leftAngle_deg  = 45
rightAngle_deg = -45
# 境界ライン描画用配列
centerArray     = np.arange(0, maxRange_mm, 2000)
leftBoundArray  = centerArray * tan(np.deg2rad(leftAngle_deg))
rightBoundArray = centerArray * tan(np.deg2rad(rightAngle_deg))
# 境界ラインを閉じるために終点を追加
centerArray     = np.append(centerArray, (maxRange_mm + 10000))
leftBoundArray  = np.append(leftBoundArray, 0)
rightBoundArray = np.append(rightBoundArray, 0)

# シミュレーションのメイン処理
if __name__ == '__main__':

    # アニメーションの描画オブジェクト
    fig, axSimPlot = plt.subplots(1, 1,  figsize=(8, 7))
    # レーダの検知可能範囲を描画
    axSimPlot.plot(centerArray/1000, leftBoundArray/1000, c='#212121')
    axSimPlot.plot(centerArray/1000, rightBoundArray/1000, c='#212121')
    axSimPlot.set_xlabel('X [m]')
    axSimPlot.set_ylabel('Y [m]')
    axSimPlot.set_xlim([0, 140])
    axSimPlot.set_ylim([-80, 80])
    axSimPlot.grid()
    fig.tight_layout()
    fig.subplots_adjust(left=0.25, bottom=0.2, right=None, top=None)

    # シミュレーションを終了させるラジオボタンオブジェクト
    axQuitBttn  = plt.axes([0.05, 0.7, 0.1, 0.1], facecolor=radioButtonColor)
    quitBttnObj = RadioButtons(axQuitBttn, ('Run', 'Quit'))
    # 動作フラグを定義
    global simRunFlag
    simRunFlag = True
    # ボタンが押された時の動作を制御する関数
    def SwitchSimRunOrQuit(label):
        global simRunFlag
        if label == 'Run':
            simRunFlag = True
        elif label == 'Quit':
            simRunFlag = False
        else:
            simRunFlag = True
    # ボタンが押されたら関数を呼び出す
    quitBttnObj.on_clicked(SwitchSimRunOrQuit)

    # 検知ターゲットの移動速度を制御するスライダオブジェクト
    axVelositySlider = plt.axes([0.20, 0.08, 0.7, 0.03])
    velositySliderObj = Slider(axVelositySlider, 'Velosity[m/s]', -5.0, 5.0, valinit=0.0)
    # 入力速度変数
    global velosityInput_ms
    velosityInput_ms = 0
    # スライダの値をターゲットへの速度入力として返す関数
    def ControlTargetVelosityInput(sliderVal):
        global velosityInput_ms
        velosityInput_ms = sliderVal
    velositySliderObj.on_changed(ControlTargetVelosityInput)

    # 検知ターゲットの角速度入力を制御するスライダオブジェクト
    axYawRateSlider = plt.axes([0.20, 0.02, 0.7, 0.03])
    yawRateSliderObj = Slider(axYawRateSlider, 'Yaw Rate[deg/s]', -2.0, 2.0, valinit=0.0)
    # 入力速度変数
    global yawRateInput_degs
    yawRateInput_degs = 0
    # スライダの値をターゲットへの角速度入力として返す関数
    def ControlTargetYawRateInput(sliderVal):
        global yawRateInput_degs
        yawRateInput_degs = sliderVal
    yawRateSliderObj.on_changed(ControlTargetYawRateInput)

    # 描画を更新していくデータのPlotオブジェクトを定義
    axSimPlot.plot([], [], '.', c='#2196F3', ms=5) # Target True Position
    axSimPlot.plot([], [], '.', c='#2196F3', ms=5) # Target Observed Position

    while simRunFlag == True:
        print('Velosity:%.2f YawRate:%.2f' % (velosityInput_ms, yawRateInput_degs))

        plt.pause(deltaTime_sec)