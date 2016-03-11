# Brain Simulator controls TurtleBot in Gazebo
GoodAI's Brain Simulator V0.4 controls TurtleBot on Gazebo Environment.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=TRSP8eudr8s
" target="_blank"><img src="http://img.youtube.com/vi/TRSP8eudr8s/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>

Tcp connection nodes in Brain Simulator communicate with python server and this server controls TurtleBot via PyGazebo.

This prototype modules are red boxes(Brain Simulator's nodes(Sensor and Motor) and python sever)
<img width="796" alt="system" src="https://cloud.githubusercontent.com/assets/1708549/13660986/4b3ea904-e6d2-11e5-8f5a-c46e00819211.png">

# Quickstart
## Run
Prepare two machines and connect same network.

 - Brain Simulator Machine
  - 64-bit Windows 7, 8, 8.1 or 10
  - NVIDIA CUDA-enabled graphics card
 - Gazebo Machine
  - recommended Ubuntu or Mac (we used Ubuntu14.04)
  
  
###  Gazebo Machine(Ubuntu or Mac)
Install Gazebo ([Ubuntu](http://gazebosim.org/tutorials?tut=install_ubuntu), [Mac](http://gazebosim.org/tutorials?tut=install_on_mac)).

Install pygazebo:

```
# Do not use version 3.0.0-2014.1 
git clone https://github.com/jpieper/pygazebo.git
cd pygazebo
git checkout 3eaac84
python setup.py install
cd ../
```

Install BriCA V1:

```
https://github.com/wbap/BriCA1.git
git clone https://github.com/wbap/BriCA1.git
cd BriCA1
git checkout 0261df0
python setup.py install
cd ../
```

Launch maze world:

```
git clone https://github.com/masayoshi-nakamura/CognitiveArchitectureLecture.git
gazebo CognitiveArchitectureLecture/worlds/maze_turtlbot.xml
```

Open new ternminal, start brainsimulator_agent.py

```
cd CognitiveArchitectureLecture/examples/brica_brainsimulator_agent/
python brainsimulator_agent.py
```

### Brain Simulator Machine(Windows) 
[Install Brain Simulator](http://www.goodai.com/#!brain-simulator/c81c).

Load CognitiveArchitectureLecture/examples/brainsimulator_agent/brica_sample_agent.brain.
<img width="796" src="https://cloud.githubusercontent.com/assets/1708549/13658146/c3beda0e-e6b7-11e5-8030-2c95be61fea5.png">

Double click "Sensor" node and change TCP_IP variable to your Gazebo Machine's IP and
double click "Motor"  node and change TCP_IP variable to your Gazebo Machine's IP.   

Then click start button(or F5 key), you can control TurtleBot by changing "Motor_input" node slider bar.

 
