# coding: shift-jis

"""
SimpleRadarSimulator.py

User can operate a target by inputting velosity and yawrate.
This program can simulate a static/dynamic target detection.
Distance, horizontal angle, velosity on range and angle direction.

How to use:
    

Author: Shisato Yano

Last Update: 2018/07/11
"""
from math import sin, cos, tan, atan, sqrt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider
import matplotlib.animation as anm

# クラス定義
class ObjectSensingSimulator(object):
    # コンストラクタ
    def __init__(self, deltaTime_s):
        # 刻み時間[s]の設定
        self.deltaTime_s = deltaTime_s

        # センサの検知範囲パラメータ定義
        self.maxRange_mm    = 100000           # 最大検知可能距離[mm]
        self.minRange_mm    = 5000            # 最小検知可能距離[mm]
        self.leftAngle_deg  = 45              # 左側検知可能角度[deg]  
        self.rightAngle_deg = -45             # 右側検知可能角度[deg]

        # 検知範囲を扇形で描画するための角度配列
        angleStep = 1
        leftAngleArray  = np.arange(0, self.leftAngle_deg + angleStep, angleStep)
        rightAngleArray = np.arange(0, self.rightAngle_deg - angleStep, -angleStep)

        # 左側の境界線座標配列
        leftBoundaryX = []
        leftBoundaryX.append([self.maxRange_mm * cos(np.deg2rad(angle)) for angle in leftAngleArray])
        leftBoundaryX = np.append(leftBoundaryX, 0.0)
        leftBoundaryY = []
        leftBoundaryY.append([self.maxRange_mm * sin(np.deg2rad(angle)) for angle in leftAngleArray])
        leftBoundaryY = np.append(leftBoundaryY, 0.0)
        self.leftScanBoundary = np.vstack((leftBoundaryX, leftBoundaryY))

        # 右側の境界線座標配列
        rightBoundaryX = []
        rightBoundaryX.append([self.maxRange_mm * cos(np.deg2rad(angle)) for angle in rightAngleArray])
        rightBoundaryX = np.append(rightBoundaryX, 0.0)
        rightBoundaryY = []
        rightBoundaryY.append([self.maxRange_mm * sin(np.deg2rad(angle)) for angle in rightAngleArray])
        rightBoundaryY = np.append(rightBoundaryY, 0.0)
        self.rightScanBoundary = np.vstack((rightBoundaryX, rightBoundaryY))

        # ターゲットの状態方程式行列A
        self.A = np.array([[1.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0],
                           [0.0, 0.0, 1.0]])
        
        # ターゲットの状態方程式行列B(制御入力)
        self.B = np.zeros((3, 3))

        # ターゲットの初期状態
        truePosX0_mm = 120000 # 位置X座標[mm]
        truePosY0_mm = 0      # 位置Y座標[mm]
        trueYaw0_rad = 0      # 方位角[rad]
        # 真値
        self.trueTarget = np.array([[truePosX0_mm],
                                    [truePosY0_mm],
                                    [trueYaw0_rad]])
        # 観測値
        self.observedTarget = self.trueTarget
        # 観測角度
        self.observedAngle_rad = 0  
    
    # 速度と角速度からターゲットの真値を計算
    def GenerateTrueTarget(self, currentX, inputV, inputOmega):
        """次のサイクルのターゲットの状態を計算
           状態方程式: x(k+1) = A * x(k) + B * u(k)
        引数:
            currentX:現在のターゲットの状態x(k)
            inputV:速度入力[m/s]
            inputOmega:角速度入力[deg/s]
        返り値:
            nextX:次のサイクルのターゲットの状態x(k+1)
            velocityX_mms:ターゲット速度のcos成分
            velosityY_mms:ターゲット速度のsin成分
        """
        # 制御入力
        self.B[0, 0] = inputV * 1000 # [mm/s]
        self.B[1, 1] = inputV * 1000 # [mm/s]
        self.B[2, 2] = np.deg2rad(inputOmega)

        currentYaw_rad = currentX[2, 0] # 移動方位角[rad]
        u = np.array([[self.deltaTime_s * cos(currentYaw_rad)],
                      [self.deltaTime_s * sin(currentYaw_rad)],
                      [self.deltaTime_s]])

        # 次のサイクルの状態    
        nextX = (self.A @ currentX) + (self.B @ u)
        nextX[2, 0] = pi2pi(nextX[2, 0])

        # ターゲット速度のcos成分
        velocityX_mms = inputV * 1000 * cos(nextX[2, 0])
        # ターゲット速度のsin成分
        velocityY_mms = inputV * 1000 * sin(nextX[2, 0])

        return nextX, velocityX_mms, velocityY_mms
    
    # 真値にガウスノイズを付加したターゲットの観測値を計算
    def GenerateObservedTarget(self, trueTarget, velocityX_mms, velocityY_mms):
        """ターゲットの観測状態を計算
            距離と角度に対してそれぞれ5%のガウスノイズを付加
            センサ座標系で計算する
        引数:
            trueTarget:ターゲットの真値[x, y, yaw]
            velocityX_mms:ターゲット速度のcos成分[mm/s]
            velocityY_mms:ターゲット速度のsin成分[mm/s]
        返り値:
            observedRange_mm:観測距離[mm]
            observedAngle_rad:観測角度[rad]
            rangeVelosity_mms:距離方向速度[mm/s]
            angleVelosity_rads:角度方向速度[rad/s]
        """
        # 真値
        truePosX_mm = trueTarget[0, 0]
        truePosY_mm = trueTarget[1, 0]
        trueYaw_rad = trueTarget[2, 0]
        
        # 観測距離を計算
        # 2%のガウスノイズを付加
        trueRange_mm = sqrt( (pow(truePosX_mm,2) + pow(truePosY_mm,2)) )
        observedRange_mm = trueRange_mm + np.random.normal(0, 0.02*trueRange_mm)

        # 観測角度を計算
        trueAngle_rad = atan(truePosY_mm/truePosX_mm)
        # 2%のガウスノイズを付加
        observedAngle_rad = trueAngle_rad + np.random.normal(0, 0.01) + np.random.normal(0, 0.02*abs(trueAngle_rad)) 

        # ターゲット速度の極座標成分を計算
        # 距離方向速度
        rangeVelosity_mms = velocityX_mms * cos(observedAngle_rad) + velocityY_mms * sin(observedAngle_rad)
        # 角度方向速度
        angleVelosity_rads = (observedAngle_rad - self.observedAngle_rad)/self.deltaTime_s
        self.observedAngle_rad = observedAngle_rad

        return trueRange_mm, trueAngle_rad, observedRange_mm, observedAngle_rad, rangeVelosity_mms, angleVelosity_rads
    
    # 検知範囲の内外判定をする関数
    def CheckInOutSensorCoverage(self, targetRange_mm, targetAngle_rad):
        """扇形の内外判定アルゴリズム
        引数:
            targetRange_mm:ターゲットの距離[mm]
            targetAngle_rad:ターゲットの角度[rad]
        返り値:
            insideFlag:検知範囲内ならTrue, 逆ならFalse
        """
        # ステップ1:検知可能距離を半径とする円の外か判定
        if targetRange_mm > self.maxRange_mm:
            return False
        
        # ステップ2:扇形の境界角度より外側にあるか判定
        # 左側の判定
        if targetAngle_rad > np.deg2rad(self.leftAngle_deg):
            return False
        # 右側の判定
        if targetAngle_rad < np.deg2rad(self.rightAngle_deg):
            return False
        
        # 上記の条件をクリアしたら検知範囲内にいると判定
        return True

    
    # シミュレーションのメイン処理関数
    def SimulationMain(self, inputV, inputOmega):
        """ターゲットの真値と観測値の生成
        引数:
            inputV:速度入力[m/s]
            yawRateInput_degs:角速度入力[deg/s]
        返り値:
            trueTarget:ターゲットの真値[x, y, yaw]
            observedTarget:ターゲットの観測値[x, y, yaw]
        """
        # ターゲットの真値を計算
        self.trueTarget, velocityX_mms, velocityY_mms = self.GenerateTrueTarget(self.trueTarget, inputV, inputOmega)

        # ターゲットの観測値を計算
        trueRange_mm, trueAngle_rad, observedRange_mm, observedAngle_rad, rangeVelosity_mms, angleVelosity_rads = self.GenerateObservedTarget(self.trueTarget, velocityX_mms, velocityY_mms)

        # 検知範囲の内外判定
        insideFlag = self.CheckInOutSensorCoverage(trueRange_mm, trueAngle_rad)

        return self.trueTarget, observedRange_mm, observedAngle_rad, rangeVelosity_mms, angleVelosity_rads, insideFlag

# 角度を-π～πの範囲に制限する関数
def pi2pi(angle_rad):
    """
    引数:
        angle_rad: 角度[rad]
    返り値:
        angle_rad: 角度[rad]
    """
    PI = np.pi
    angle_rad += PI     # 一旦180度を足して下限値を0にする
    angle_rad %= (2*PI) # 360度で割った際の余り
    if angle_rad < 0:
        angle_rad += PI
    else:
        angle_rad -= PI
    return angle_rad

# アニメーション処理用関数
def SimAnimation(simObject, inputV, inputOmega):
    # ターゲットの真値
    trueTarget, observedRange_mm, observedAngle_rad, rangeVelosity_mms, angleVelosity_rads, insideFlag = simObject.SimulationMain(inputV, inputOmega)

    # ターゲットのデータを描画
    x = trueTarget[0, 0]/1000
    y = trueTarget[1, 0]/1000
    trueTargetPlot.set_data(x, y)

    # ターゲットが検知範囲内なら観測位置座標を描画
    if insideFlag == True:
        # 座標値を計算
        observedPosX_mm = observedRange_mm * cos(observedAngle_rad)
        observedPosY_mm = observedRange_mm * sin(observedAngle_rad)
        # 描画
        observedTargetPlot.set_data(observedPosX_mm/1000, observedPosY_mm/1000)
        rangeText.set_text('Range = %.2f[m]' % (observedRange_mm/1000))
        angleText.set_text('Angle = %.2f[deg]' % np.rad2deg(observedAngle_rad))
        rangeVelText.set_text('Range Velosity = %.2f[m/s]' % (rangeVelosity_mms/1000))
        angleVelText.set_text('Angle Velosity = %.2f[deg/s]' % np.rad2deg(angleVelosity_rads))
    else:
        observedTargetPlot.set_data([], [])
        rangeText.set_text('Range = [m]')
        angleText.set_text('Angle = [deg]')
        rangeVelText.set_text('Range Velosity = [m/s]')
        angleVelText.set_text('Angle Velosity = [deg/s]')

if __name__ == '__main__':
    # ラジオボタン用の背景色を設定
    radioButtonColor = 'lightgoldenrodyellow'
    
    # シミュレーションの刻み時間[s]
    deltaTime_s = 0.05
    
    # クラスのインスタンス化
    simObject = ObjectSensingSimulator(deltaTime_s)

    # アニメーションの描画オブジェクト
    fig, axSimPlot = plt.subplots(1, 1,  figsize=(8, 7))
    # レーダの検知可能範囲を描画
    axSimPlot.plot(simObject.leftScanBoundary[0,:]/1000, simObject.leftScanBoundary[1,:]/1000, c='#212121')
    axSimPlot.plot(simObject.rightScanBoundary[0,:]/1000, simObject.rightScanBoundary[1,:]/1000, c='#212121')
    axSimPlot.set_xlabel('X [m]')
    axSimPlot.set_ylabel('Y [m]')
    axSimPlot.set_xlim([0, 140])
    axSimPlot.set_ylim([-80, 80])
    axSimPlot.grid()
    axSimPlot.axis('equal')
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
    yawRateSliderObj = Slider(axYawRateSlider, 'Yaw Rate[deg/s]', -10.0, 10.0, valinit=0.0)
    # 入力速度変数
    global yawRateInput_degs
    yawRateInput_degs = 0
    # スライダの値をターゲットへの角速度入力として返す関数
    def ControlTargetYawRateInput(sliderVal):
        global yawRateInput_degs
        yawRateInput_degs = sliderVal
    yawRateSliderObj.on_changed(ControlTargetYawRateInput)

    # 描画を更新していくデータのPlotオブジェクトを定義
    trueTargetPlot,     = axSimPlot.plot([], [], '.', c='#2196F3', ms=15) # True Target Position
    observedTargetPlot, = axSimPlot.plot([], [], '.', c='#f44336', ms=15) # Observed Target Position
    rangeText    = axSimPlot.text(0.05, 0.9, '', transform=axSimPlot.transAxes)
    angleText    = axSimPlot.text(0.05, 0.8, '', transform=axSimPlot.transAxes)
    rangeVelText = axSimPlot.text(0.05, 0.7, '', transform=axSimPlot.transAxes)
    angleVelText = axSimPlot.text(0.05, 0.6, '', transform=axSimPlot.transAxes)

    while simRunFlag == True:
        # 速度と角速度の入力に応じてターゲット位置を更新
        SimAnimation(simObject, velosityInput_ms, yawRateInput_degs)

        plt.pause(deltaTime_s)