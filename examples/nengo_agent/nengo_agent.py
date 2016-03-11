import nengo
import nengo_pygazebo_simulator

from components.motor_area_component import MotorAreaOperator
from components.hippocampus_component import HippocampusOperator
from components.visual_area_component import VisualAreaOperator

# Debug mode
#import logging
#logging.basicConfig(level=logging.DEBUG) 
import os
os.environ['TROLLIUSDEBUG']='1'

model = nengo.Network()
with model:
    visualOperator = VisualAreaOperator()
    hippocampusOperator = HippocampusOperator()
    motorOperator = MotorAreaOperator()
    
    visual = nengo.Node(output=visualOperator.fire, size_in=1, size_out=8)
    hippocampus = nengo.Node(output=hippocampusOperator.fire, size_in=2, size_out=2)
    motor = nengo.Node(output=motorOperator.fire, size_in=10, size_out=2)
    
    nengo.Connection(visual[0:2], hippocampus)
    nengo.Connection(visual[0:8], motor[0:8])
    nengo.Connection(hippocampus, motor[8:10])        

if __name__ == "__main__":
    gazebo_agent = nengo_pygazebo_simulator.SampleAgent(model, dt=0.01)
    gazebo_agent.set_modules(visualOperator, motorOperator)
    gazebo_agent.run(20)
    print "finished"
