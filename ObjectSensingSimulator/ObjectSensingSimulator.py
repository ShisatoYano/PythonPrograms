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

# Class Definition
class ObjectSensingSimulator(object):
    # Constructor
    def __init__(self, deltaTime_s):
        # delta Time [s]
        self.deltaTime_s = deltaTime_s

        # Sensor detection coverage parameter
        self.maxRange_mm    = 100000 # Max detect range[mm]
        self.minRange_mm    = 5000   # Min detect range[mm]
        self.leftAngle_deg  = 45     # left side limit angle[deg]  
        self.rightAngle_deg = -45    # right side limit angle[deg]

        # Detection angle array
        angleStep = 1
        leftAngleArray  = np.arange(0, self.leftAngle_deg + angleStep, angleStep)
        rightAngleArray = np.arange(0, self.rightAngle_deg - angleStep, -angleStep)

        # Left side boundary array
        leftBoundaryX = []
        leftBoundaryX.append([self.maxRange_mm * cos(np.deg2rad(angle)) for angle in leftAngleArray])
        leftBoundaryX = np.append(leftBoundaryX, 0.0)
        leftBoundaryY = []
        leftBoundaryY.append([self.maxRange_mm * sin(np.deg2rad(angle)) for angle in leftAngleArray])
        leftBoundaryY = np.append(leftBoundaryY, 0.0)
        self.leftScanBoundary = np.vstack((leftBoundaryX, leftBoundaryY))

        # Right side boundary array
        rightBoundaryX = []
        rightBoundaryX.append([self.maxRange_mm * cos(np.deg2rad(angle)) for angle in rightAngleArray])
        rightBoundaryX = np.append(rightBoundaryX, 0.0)
        rightBoundaryY = []
        rightBoundaryY.append([self.maxRange_mm * sin(np.deg2rad(angle)) for angle in rightAngleArray])
        rightBoundaryY = np.append(rightBoundaryY, 0.0)
        self.rightScanBoundary = np.vstack((rightBoundaryX, rightBoundaryY))

        # State Equation Matrix A
        self.A = np.array([[1.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0],
                           [0.0, 0.0, 1.0]])
        
        # State Equation Matrix B(Control Input)
        self.B = np.zeros((3, 3))

        # Initial state of target object
        truePosX0_mm = 120000 # target position X[mm]
        truePosY0_mm = 0      # target position Y[mm]
        trueYaw0_rad = 0      # Yaw angle[rad]
        # Ground truth
        self.trueTarget = np.array([[truePosX0_mm],
                                    [truePosY0_mm],
                                    [trueYaw0_rad]])
        # Observation
        self.observedTarget = self.trueTarget
        # Observed angle
        self.observedAngle_rad = 0  
    
    # Generate ground truth of target
    def GenerateTrueTarget(self, currentX, inputV, inputOmega):
        """
           State equation: x(k+1) = A * x(k) + B * u(k)
        Input:
            currentX:   Current state x(k)
            inputV:     Input velosity[m/s]
            inputOmega: Input yaw rate[deg/s]
        return:
            nextX:         next state x(k+1)
            velocityX_mms: cos component of velosity
            velosityY_mms: sin component of velosity
        """
        # Control input
        self.B[0, 0] = inputV * 1000 # [mm/s]
        self.B[1, 1] = inputV * 1000 # [mm/s]
        self.B[2, 2] = np.deg2rad(inputOmega)

        currentYaw_rad = currentX[2, 0] # Yaw angle[rad]
        u = np.array([[self.deltaTime_s * cos(currentYaw_rad)],
                      [self.deltaTime_s * sin(currentYaw_rad)],
                      [self.deltaTime_s]])

        # State of next cycle    
        nextX = (self.A @ currentX) + (self.B @ u)
        nextX[2, 0] = pi2pi(nextX[2, 0])

        # cos component of velosity
        velocityX_mms = inputV * 1000 * cos(nextX[2, 0])
        # sin component of velosity
        velocityY_mms = inputV * 1000 * sin(nextX[2, 0])

        return nextX, velocityX_mms, velocityY_mms
    
    # Generate Observation of target 
    def GenerateObservedTarget(self, trueTarget, velocityX_mms, velocityY_mms):
        """
            Each observed value is calculated on sensor coordinate
            2% gaussian noise is add
        Input:
            trueTarget:    Ground truth[x, y, yaw]
            velocityX_mms: cos component of velosity[mm/s]
            velocityY_mms: sin component of velosity[mm/s]
        Return:
            observedRange_mm:   Observed range to target[mm]
            observedAngle_rad:  Observed angle to target[rad]
            rangeVelosity_mms:  Observed velosity on range direction[mm/s]
            angleVelosity_rads: Observed velosity on turning direction[rad/s]
        """
        # Ground truth
        truePosX_mm = trueTarget[0, 0]
        truePosY_mm = trueTarget[1, 0]
        trueYaw_rad = trueTarget[2, 0]
        
        # Calculate observed range
        # add 2% gaussian noise
        trueRange_mm = sqrt( (pow(truePosX_mm,2) + pow(truePosY_mm,2)) )
        observedRange_mm = trueRange_mm + np.random.normal(0, 0.02*trueRange_mm)

        # Calculate observed angle on sensor coordinate
        trueAngle_rad = atan(truePosY_mm/truePosX_mm)
        # add 2% gaussian noise
        observedAngle_rad = trueAngle_rad + np.random.normal(0, 0.01) + np.random.normal(0, 0.02*abs(trueAngle_rad)) 

        # Calculate observed velosity on polar coodinate
        # Range direction
        rangeVelosity_mms = velocityX_mms * cos(observedAngle_rad) + velocityY_mms * sin(observedAngle_rad)
        # Turning direction 
        angleVelosity_rads = (observedAngle_rad - self.observedAngle_rad)/self.deltaTime_s
        self.observedAngle_rad = observedAngle_rad

        return trueRange_mm, trueAngle_rad, observedRange_mm, observedAngle_rad, rangeVelosity_mms, angleVelosity_rads
    
    # Check inside or outside sensor detection area
    def CheckInOutSensorCoverage(self, targetRange_mm, targetAngle_rad):
        """
        Input:
            targetRange_mm:  Range of target[mm]
            targetAngle_rad: Angle of target[rad]
        Return:
            insideFlag: Inside->True, Outside->False
        """
        if targetRange_mm > self.maxRange_mm:
            return False
        
        if targetAngle_rad > np.deg2rad(self.leftAngle_deg):
            return False

        if targetAngle_rad < np.deg2rad(self.rightAngle_deg):
            return False
        
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
    x = trueTarget[0, 0]/1000
    y = trueTarget[1, 0]/1000
    trueTargetPlot.set_data(x, y)

    # �^�[�Q�b�g�����m�͈͓��Ȃ�ϑ��ʒu���W��`��
    if insideFlag == True:
        # ���W�l���v�Z
        observedPosX_mm = observedRange_mm * cos(observedAngle_rad)
        observedPosY_mm = observedRange_mm * sin(observedAngle_rad)
        # �`��
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
    # ���W�I�{�^���p�̔w�i�F��ݒ�
    radioButtonColor = 'lightgoldenrodyellow'
    
    # �V�~�����[�V�����̍��ݎ���[s]
    deltaTime_s = 0.05
    
    # �N���X�̃C���X�^���X��
    simObject = ObjectSensingSimulator(deltaTime_s)

    # �A�j���[�V�����̕`��I�u�W�F�N�g
    fig, axSimPlot = plt.subplots(1, 1,  figsize=(8, 7))
    # ���[�_�̌��m�\�͈͂�`��
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