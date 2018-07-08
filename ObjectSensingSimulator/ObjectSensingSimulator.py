# coding: shift-jis

"""
SimpleRadarSimulator.py

User can operate a target by inputting velosity and yawrate.
This program can simulate a static/dynamic target detection.
Distance, horizontal angle, velosity on range and angle direction.

Author: Shisato Yano
Last Update: 2018/07/04
"""

from math import sin, cos, tan, atan, sqrt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider

# �N���X��`
class ObjectSensingSimulator(object):
    # �R���X�g���N�^
    def __init__(self, deltaTime_s):
        # ���ݎ���[s]�̐ݒ�
        self.deltaTime_s = deltaTime_s

        # �Z���T�̌��m�͈̓p�����[�^��`
        self.maxRange_mm    = 80000           # �ő匟�m�\����[mm]
        self.minRange_mm    = 5000            # �ŏ����m�\����[mm]
        self.leftAngle_rad  = np.deg2rad(45)  # �������m�\�p�x[rad]  
        self.rightAngle_rad = np.deg2rad(-45) # �E�����m�\�p�x[rad]

        # ���m�͈͂̋��E���z����`
        self.centerArray     = np.arange(0, self.maxRange_mm, 2000)        # ���S��
        self.rightBoundArray = self.centerArray * tan(self.rightAngle_rad) # �E�����E��
        self.leftBoundArray  = self.centerArray * tan(self.leftAngle_rad)  # �������E��
        # ���E������I�_��ǉ�
        self.centerArray     = np.append(self.centerArray, (self.maxRange_mm + 10000))
        self.rightBoundArray = np.append(self.rightBoundArray, 0)
        self.leftBoundArray  = np.append(self.leftBoundArray, 0)

        # �^�[�Q�b�g�̏�ԕ������s��A
        self.A = np.array([[1.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0],
                           [0.0, 0.0, 1.0]])
        
        # �^�[�Q�b�g�̏�ԕ������s��B(�������)
        self.B = np.zeros((3, 3))

        # �^�[�Q�b�g�̏������
        truePosX0_mm = 100000 # �ʒuX���W[mm]
        truePosY0_mm = 0      # �ʒuY���W[mm]
        trueYaw0_rad = 0      # ���ʊp[rad]
        # �^�l
        self.trueTarget = np.array([[truePosX0_mm],
                                    [truePosY0_mm],
                                    [trueYaw0_rad]])
        # �ϑ��l
        self.observedTarget = self.trueTarget
        # �ϑ��p�x
        self.observedAngle_rad = 0  
    
    # ���x�Ɗp���x����^�[�Q�b�g�̐^�l���v�Z
    def GenerateTrueTarget(self, currentX, inputV, inputOmega):
        """���̃T�C�N���̃^�[�Q�b�g�̏�Ԃ��v�Z
           ��ԕ�����: x(k+1) = A * x(k) + B * u(k)
        ����:
            currentX:���݂̃^�[�Q�b�g�̏��x(k)
            inputV:���x����[m/s]
            inputOmega:�p���x����[deg/s]
        �Ԃ�l:
            nextX:���̃T�C�N���̃^�[�Q�b�g�̏��x(k+1)
            velocityX_mms:�^�[�Q�b�g���x��cos����
            velosityY_mms:�^�[�Q�b�g���x��sin����
        """
        # �������
        self.B[0, 0] = inputV * 1000 # [mm/s]
        self.B[1, 1] = inputV * 1000 # [mm/s]
        self.B[2, 2] = np.deg2rad(inputOmega)

        currentYaw_rad = currentX[2, 0] # �ړ����ʊp[rad]
        u = np.array([[self.deltaTime_s * cos(currentYaw_rad)],
                      [self.deltaTime_s * sin(currentYaw_rad)],
                      [self.deltaTime_s]])

        # ���̃T�C�N���̏��    
        nextX = (self.A @ currentX) + (self.B @ u)
        nextX[2, 0] = pi2pi(nextX[2, 0])

        # �^�[�Q�b�g���x��cos����
        velocityX_mms = inputV * 1000 * cos(nextX[2, 0])
        # �^�[�Q�b�g���x��sin����
        velocityY_mms = inputV * 1000 * sin(nextX[2, 0])

        return nextX, velocityX_mms, velocityY_mms
    
    # �^�l�ɃK�E�X�m�C�Y��t�������^�[�Q�b�g�̊ϑ��l���v�Z
    def GenerateObservedTarget(self, trueTarget, velocityX_mms, velocityY_mms):
        """�^�[�Q�b�g�̊ϑ���Ԃ��v�Z
            �����Ɗp�x�ɑ΂��Ă��ꂼ��5%�̃K�E�X�m�C�Y��t��
            �Z���T���W�n�Ōv�Z����
        ����:
            trueTarget:�^�[�Q�b�g�̐^�l[x, y, yaw]
            velocityX_mms:�^�[�Q�b�g���x��cos����[mm/s]
            velocityY_mms:�^�[�Q�b�g���x��sin����[mm/s]
        �Ԃ�l:
            observedRange_mm:�ϑ�����[mm]
            observedAngle_rad:�ϑ��p�x[rad]
            rangeVelosity_mms:�����������x[mm/s]
            angleVelosity_rads:�p�x�������x[rad/s]
        """
        # �^�l
        truePosX_mm = trueTarget[0, 0]
        truePosY_mm = trueTarget[1, 0]
        trueYaw_rad = trueTarget[2, 0]
        
        # �ϑ��������v�Z
        # 2%�̃K�E�X�m�C�Y��t��
        trueRange_mm = sqrt( (pow(truePosX_mm,2) + pow(truePosY_mm,2)) )
        observedRange_mm = trueRange_mm + np.random.normal(0, 0.02*trueRange_mm)

        # �ϑ��p�x���v�Z
        trueAngle_rad = atan(truePosY_mm/truePosX_mm)
        # 2%�̃K�E�X�m�C�Y��t��
        observedAngle_rad = trueAngle_rad + np.random.normal(0, 0.01) + np.random.normal(0, 0.02*abs(trueAngle_rad)) 

        # �^�[�Q�b�g���x�̋ɍ��W�������v�Z
        # �����������x
        rangeVelosity_mms = velocityX_mms * cos(observedAngle_rad) + velocityY_mms * sin(observedAngle_rad)
        # �p�x�������x
        angleVelosity_rads = (observedAngle_rad - self.observedAngle_rad)/self.deltaTime_s
        self.observedAngle_rad = observedAngle_rad

        return trueRange_mm, trueAngle_rad, observedRange_mm, observedAngle_rad, rangeVelosity_mms, angleVelosity_rads
    
    # ���m�͈͂̓��O���������֐�
    def CheckInOutSensorCoverage(self, targetRange_mm, targetAngle_rad):
        """��`�̓��O����A���S���Y��
        ����:
            targetRange_mm:�^�[�Q�b�g�̋���[mm]
            targetAngle_rad:�^�[�Q�b�g�̊p�x[rad]
        �Ԃ�l:
            insideFlag:���m�͈͓��Ȃ�True, �t�Ȃ�False
        """
        # �X�e�b�v1:���m�\�����𔼌a�Ƃ���~�̊O������
        if targetRange_mm > self.maxRange_mm:
            return False
        
        # �X�e�b�v2:��`�̋��E�p�x���O���ɂ��邩����
        # �����̔���
        if targetAngle_rad > self.leftAngle_rad:
            return False
        # �E���̔���
        if targetAngle_rad < self.rightAngle_rad:
            return False
        
        # ��L�̏������N���A�����猟�m�͈͓��ɂ���Ɣ���
        return True

    
    # �V�~�����[�V�����̃��C�������֐�
    def SimulationMain(self, inputV, inputOmega):
        """�^�[�Q�b�g�̐^�l�Ɗϑ��l�̐���
        ����:
            inputV:���x����[m/s]
            yawRateInput_degs:�p���x����[deg/s]
        �Ԃ�l:
            trueTarget:�^�[�Q�b�g�̐^�l[x, y, yaw]
            observedTarget:�^�[�Q�b�g�̊ϑ��l[x, y, yaw]
        """
        # �^�[�Q�b�g�̐^�l���v�Z
        self.trueTarget, velocityX_mms, velocityY_mms = self.GenerateTrueTarget(self.trueTarget, inputV, inputOmega)

        # �^�[�Q�b�g�̊ϑ��l���v�Z
        trueRange_mm, trueAngle_rad, observedRange_mm, observedAngle_rad, rangeVelosity_mms, angleVelosity_rads = self.GenerateObservedTarget(self.trueTarget, velocityX_mms, velocityY_mms)

        # ���m�͈͂̓��O����
        insideFlag = self.CheckInOutSensorCoverage(trueRange_mm, trueAngle_rad)

        return self.trueTarget, observedRange_mm, observedAngle_rad, rangeVelosity_mms, angleVelosity_rads, insideFlag

# �p�x��-�΁`�΂͈̔͂ɐ�������֐�
def pi2pi(angle_rad):
    """
    ����:
        angle_rad: �p�x[rad]
    �Ԃ�l:
        angle_rad: �p�x[rad]
    """
    PI = np.pi
    angle_rad += PI     # ��U180�x�𑫂��ĉ����l��0�ɂ���
    angle_rad %= (2*PI) # 360�x�Ŋ������ۂ̗]��
    if angle_rad < 0:
        angle_rad += PI
    else:
        angle_rad -= PI
    return angle_rad

# �A�j���[�V���������p�֐�
def SimAnimation(simObject, inputV, inputOmega):
    # �^�[�Q�b�g�̐^�l
    trueTarget, observedRange_mm, observedAngle_rad, rangeVelosity_mms, angleVelosity_rads, insideFlag = simObject.SimulationMain(inputV, inputOmega)

    # �^�[�Q�b�g�̃f�[�^��`��
    trueTargetPlot.set_data(trueTarget[0, 0]/1000, trueTarget[1, 0]/1000)
    # �^�[�Q�b�g�����m�͈͓��Ȃ�ϑ��ʒu���W��`��
    if insideFlag == True:
        # ���W�l���v�Z
        observedPosX_mm = observedRange_mm * cos(observedAngle_rad)
        observedPosY_mm = observedRange_mm * sin(observedAngle_rad)
        # �`��
        observedTargetPlot.set_data(observedPosX_mm/1000, observedPosY_mm/1000)
    else:
        observedTargetPlot.set_data([], [])
    rangeText.set_text('Range = %.2f[m]' % (observedRange_mm/1000))
    angleText.set_text('Angle = %.2f[deg]' % np.rad2deg(observedAngle_rad))
    rangeVelText.set_text('Range Velosity = %.2f[m/s]' % (rangeVelosity_mms/1000))
    angleVelText.set_text('Angle Velosity = %.2f[deg/s]' % np.rad2deg(angleVelosity_rads))

if __name__ == '__main__':
    # ���W�I�{�^���p�̔w�i�F��ݒ�
    radioButtonColor = 'lightgoldenrodyellow'
    
    # �V�~�����[�V�����̍��ݎ���[s]
    deltaTime_s = 0.05
    
    # �N���X�̃C���X�^���X��
    simObject = ObjectSensingSimulator(deltaTime_s)

    # �A�j���[�V�����̕`��I�u�W�F�N�g
    fig, axSimPlot = plt.subplots(1, 1,  figsize=(8, 7))
    # ���[�_�̌��m�\�͈͂�`��
    axSimPlot.plot(simObject.centerArray/1000, simObject.leftBoundArray/1000, c='#212121')
    axSimPlot.plot(simObject.centerArray/1000, simObject.rightBoundArray/1000, c='#212121')
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
    yawRateSliderObj = Slider(axYawRateSlider, 'Yaw Rate[deg/s]', -10.0, 10.0, valinit=0.0)
    # ���͑��x�ϐ�
    global yawRateInput_degs
    yawRateInput_degs = 0
    # �X���C�_�̒l���^�[�Q�b�g�ւ̊p���x���͂Ƃ��ĕԂ��֐�
    def ControlTargetYawRateInput(sliderVal):
        global yawRateInput_degs
        yawRateInput_degs = sliderVal
    yawRateSliderObj.on_changed(ControlTargetYawRateInput)

    # �`����X�V���Ă����f�[�^��Plot�I�u�W�F�N�g���`
    trueTargetPlot,     = axSimPlot.plot([], [], '.', c='#2196F3', ms=15) # True Target Position
    observedTargetPlot, = axSimPlot.plot([], [], '.', c='#f44336', ms=15) # Observed Target Position
    rangeText    = axSimPlot.text(0.05, 0.9, '', transform=axSimPlot.transAxes)
    angleText    = axSimPlot.text(0.05, 0.8, '', transform=axSimPlot.transAxes)
    rangeVelText = axSimPlot.text(0.05, 0.7, '', transform=axSimPlot.transAxes)
    angleVelText = axSimPlot.text(0.05, 0.6, '', transform=axSimPlot.transAxes)

    while simRunFlag == True:
        # ���x�Ɗp���x�̓��͂ɉ����ă^�[�Q�b�g�ʒu���X�V
        SimAnimation(simObject, velosityInput_ms, yawRateInput_degs)

        plt.pause(deltaTime_s)