animation_player.py
===============

GUI Tool to playback recorded data as animation.

## Description  
Read csv file as pandas data frame.  
You can playback the data with matplotlib.  
You can switch start/stop playback and playback speed is chanageable.  

## Author
Shisato Yano

## Dependency
Python 3.6.4 :: Anaconda  
Please import the following module    
matplotlib 2.1.2  
pandas     0.22.0  
datetime     

## Usage
1. Start this application: python animation_player    

2. This application read sample csv data file "nmea_gpgga_data_frame.csv" automatically  

3. GUI figure will be displayed as follow.  
![image_alt_text](https://github.com/ShisatoYano/PythonPrograms/blob/master/Animation_Player/animation_player_demo.gif?raw=true)  

4. Radia button "Stop" is selected as default. You can start playback data by selecting "Start".  

5. You can fast forward or rewind the animation by operating the bottom slider.  

6. There are 5 patterns of playback speed,"Normal", "2X", "1.5X", "0.75X", "0.5X". You can select pattern you prefer.  

## X-Y GPS Position Plot  
Black line is GPS trajectory and Blue/Red point marker is position at current time.  
Ploit color blue means GPS quality is stand alone. Red color means differential GPS.  

## Datetime - HDOP graph
The upper right graph is HDOP graph at each datetime. 

## Datetime - Satellite Num graph
The lower right graph is satellite num graph at each datetime.

