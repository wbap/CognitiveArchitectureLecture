
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
