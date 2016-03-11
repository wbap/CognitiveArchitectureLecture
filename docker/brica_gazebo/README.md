

# Quickstart
[Install Docker](https://docs.docker.com/engine/installation/).

If you are using Mac, find the "Docker Quickstart Terminal" and double-click to launch it and work within it.

build container:

```
git clone https://github.com/masayoshi-nakamura/CognitiveArchitectureLecture.git
cd CognitiveArchitectureLecture/docker/brica_gazebo
docker build --tag=brica-gazebo .
```

run docker container:

```
docker run -it -p 8888:8888 -p 8080:8080 -p 7681:7681 brica-gazebo
```

After that, you are in docker container. Start gazebo server and gazebo web server:

```
# in docker container
/root/gzweb/start_gzweb.sh && gzserver /root/CognitiveArchitectureLecture/worlds/maze_turtlbot.xml &
```

You'll now be able to access http://[your docker IP]:8080. 
 - Ubuntu: [http://localhost:8080/](http://localhost:8080/)
 - Mac and using "Docker Quickstart Terminal": access to IP displayed when "Docker Quickstart Terminal" started.
 
<img src="https://cloud.githubusercontent.com/assets/1708549/13484633/fd0aa402-e142-11e5-8b4a-cd4be83954e4.png" width=400/>


Run a BriCA sample agent in the container:

```
# in docker container
cd ~/CognitiveArchitectureLecture/examples/brica_agent 
python brica_agent.py
```



If you want to create your code, use [IPython Jupyter](http://ipython.org/):

```
# in docker container
cd ~/CognitiveArchitectureLecture/examples/brica_agent
jupyter notebook --no-browser --port 8888 --ip=*
```

You'll now be able to access http://[your docker IP]:8888/ 


<img src="https://cloud.githubusercontent.com/assets/1708549/13484604/d72e9cf2-e142-11e5-8ac9-e4eb9e8978c1.png" width=400/>



