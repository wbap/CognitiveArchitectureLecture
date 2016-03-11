
import brica1
import brical
import pygazebo_agent
import numpy as np

from components.motor_area_component import MotorAreaComponent
from components.hippocampus_component import HippocampusComponent
from components.visual_area_component import VisualAreaComponent

import logging
logging.basicConfig()

use_brica_lang = True

if __name__ == "__main__":
    scheduler = brica1.RealTimeSyncScheduler(0.01)

    if use_brica_lang:
        li = brical.LanguageInterpreter()
        fp = open('language/architecture.json', 'r')
        module = li.load_file(fp)
        agent = li.create_agent(scheduler)

        visual_comp = module["Base.InputModule"] \
            .get_component("Base.InputModule")
        motor_comp = module["Base.OutputModule"] \
            .get_component("Base.OutputModule")

    else:
        agent = brica1.Agent(scheduler)

        visual_comp = VisualAreaComponent()
        motor_comp = MotorAreaComponent()
        hipp_comp = HippocampusComponent()

        CompSet = brica1.ComponentSet()
        CompSet.add_component("visual_area_component", visual_comp, 0)
        CompSet.add_component("hippocampus_component", hipp_comp, 1)
        CompSet.add_component("motor_area_component", motor_comp, 2)

        main_module = brica1.Module()
        main_module.add_component("component_set", CompSet)

        # visual to hippocampus
        visual_comp.set_state("out_body_position",
                              np.zeros(2, dtype=np.short))
        visual_comp.make_out_port("out_body_position", 2)
        hipp_comp.make_in_port("in_body_position", 2)
        brica1.connect((visual_comp, "out_body_position"),
                       (hipp_comp, "in_body_position"))

        # visual to motor
        motor_comp.make_in_port("in_body_position", 2)
        brica1.connect((visual_comp, "out_body_position"),
                       (motor_comp, "in_body_position"))
        visual_comp.set_state("out_body_velocity",
                              np.zeros(2, dtype=np.float32))
        visual_comp.make_out_port("out_body_velocity", 2)
        motor_comp.make_in_port("in_body_velocity", 2)
        brica1.connect((visual_comp, "out_body_velocity"),
                       (motor_comp, "in_body_velocity"))
        visual_comp.set_state("out_body_orientation",
                              np.zeros(4, dtype=np.float32))
        visual_comp.make_out_port("out_body_orientation", 4)
        motor_comp.make_in_port("in_body_orientation", 4)
        brica1.connect((visual_comp, "out_body_orientation"),
                       (motor_comp, "in_body_orientation"))

        # hippocampus to motor
        hipp_comp.set_state("out_target_position", np.zeros(2, dtype=np.short))
        hipp_comp.make_out_port("out_target_position", 2)
        motor_comp.make_in_port("in_target_position", 2)
        brica1.connect((hipp_comp, "out_target_position"),
                       (motor_comp, "in_target_position"))

        agent.add_submodule("main_module", main_module)

    gazebo_agent = pygazebo_agent.SampleAgent(agent, visual_comp, motor_comp)
    gazebo_agent.run()
