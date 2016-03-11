# A prototype of Nengo controller module for Gazebo

<img width="564" alt="nengo" src="https://cloud.githubusercontent.com/assets/1708549/13658730/39f499fc-e6bd-11e5-9f0d-23d66b31b881.png">

## Installation (Mac, Ubuntu)

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

Install Nengo 2.0
```bash
 pip install nengo
 pip install nengo_gui
```


## Simple Usage

Launch maze world
```
gazebo CognitiveArchitectureLecture/worlds/maze_turtlbot.xml
```
Open new ternminal, 

```
 cd CognitiveArchitectureLecture/examples/brica_agent/
 python brica_agent.py
```

