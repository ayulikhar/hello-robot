import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path('kitchen_scene.xml')
data = mujoco.MjData(model)

# MjData starts at the model's qpos0 (the origin, inside the island).  Apply
# the scene keyframe so every launch begins at the intended clear floor pose.
robot_start = model.key('robot_start').id
mujoco.mj_resetDataKeyframe(model, data, robot_start)
mujoco.mj_forward(model, data)

mujoco.viewer.launch(model, data)
