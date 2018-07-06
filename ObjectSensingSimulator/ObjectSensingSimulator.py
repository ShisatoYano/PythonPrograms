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

# ���W�I�{�^���p�̔w�i�F��ݒ�
radioButtonColor = 'lightgoldenrodyellow'

# �V�~�����[�V�������̍��ݎ���[s]
deltaTime_sec = 0.05

# ���[�_�̌��m�\�͈͂��p�����[�^
# ���m�\����
maxRange_mm    = 80000
minRange_mm    = 5000
# ���m�\�p�x
leftAngle_deg  = 45
rightAngle_deg = -45
# ���E���C���`��p�z��
centerArray     = np.arange(0, maxRange_mm, 2000)
leftBoundArray  = centerArray * tan(np.deg2rad(leftAngle_deg))
rightBoundArray = centerArray * tan(np.deg2rad(rightAngle_deg))
# ���E���C������邽�߂ɏI�_��ǉ�
centerArray     = np.append(centerArray, (maxRange_mm + 10000))
leftBoundArray  = np.append(leftBoundArray, 0)
rightBoundArray = np.append(rightBoundArray, 0)

# �V�~�����[�V�����̃��C������
if __name__ == '__main__':

    # �A�j���[�V�����̕`��I�u�W�F�N�g
    fig, axSimPlot = plt.subplots(1, 1,  figsize=(8, 7))
    # ���[�_�̌��m�\�͈͂�`��
    axSimPlot.plot(centerArray/1000, leftBoundArray/1000, c='#212121')
    axSimPlot.plot(centerArray/1000, rightBoundArray/1000, c='#212121')
    axSimPlot.set_xlabel('X [m]')
    axSimPlot.set_ylabel('Y [m]')
    axSimPlot.set_xlim([0, 140])
    axSimPlot.set_ylim([-80, 80])
    axSimPlot.grid()
    fig.tight_layout()
    fig.subplots_adjust(left=0.25, bottom=0.2, right=None, top=None)

    # �V�~�����[�V�������I�������郉�W�I�{�^���I�u�W�F�N�g
    axQuitBttn  = plt.axes([0.05, 0.7, 0.1, 0.1], facecolor=radioButtonColor)
    quitBttnObj = RadioButtons(axQuitBttn, ('Run', 'Quit'))
    # ����t���O���`
    global simRunFlag
    simRunFlag = True
    # �{�^���������ꂽ���̓���𐧌䂷��֐�
    def SwitchSimRunOrQuit(label):
        global simRunFlag
        if label == 'Run':
            simRunFlag = True
        elif label == 'Quit':
            simRunFlag = False
        else:
            simRunFlag = True
    # �{�^���������ꂽ��֐����Ăяo��
    quitBttnObj.on_clicked(SwitchSimRunOrQuit)

    # ���m�^�[�Q�b�g�̈ړ����x�𐧌䂷��X���C�_�I�u�W�F�N�g
    axVelositySlider = plt.axes([0.20, 0.08, 0.7, 0.03])
    velositySliderObj = Slider(axVelositySlider, 'Velosity[m/s]', -5.0, 5.0, valinit=0.0)
    # ���͑��x�ϐ�
    global velosityInput_ms
    velosityInput_ms = 0
    # �X���C�_�̒l���^�[�Q�b�g�ւ̑��x���͂Ƃ��ĕԂ��֐�
    def ControlTargetVelosityInput(sliderVal):
        global velosityInput_ms
        velosityInput_ms = sliderVal
    velositySliderObj.on_changed(ControlTargetVelosityInput)

    # ���m�^�[�Q�b�g�̊p���x���͂𐧌䂷��X���C�_�I�u�W�F�N�g
    axYawRateSlider = plt.axes([0.20, 0.02, 0.7, 0.03])
    yawRateSliderObj = Slider(axYawRateSlider, 'Yaw Rate[deg/s]', -2.0, 2.0, valinit=0.0)
    # ���͑��x�ϐ�
    global yawRateInput_degs
    yawRateInput_degs = 0
    # �X���C�_�̒l���^�[�Q�b�g�ւ̊p���x���͂Ƃ��ĕԂ��֐�
    def ControlTargetYawRateInput(sliderVal):
        global yawRateInput_degs
        yawRateInput_degs = sliderVal
    yawRateSliderObj.on_changed(ControlTargetYawRateInput)

    # �`����X�V���Ă����f�[�^��Plot�I�u�W�F�N�g���`
    axSimPlot.plot([], [], '.', c='#2196F3', ms=5) # Target True Position
    axSimPlot.plot([], [], '.', c='#2196F3', ms=5) # Target Observed Position

    while simRunFlag == True:
        print('Velosity:%.2f YawRate:%.2f' % (velosityInput_ms, yawRateInput_degs))

        plt.pause(deltaTime_sec)