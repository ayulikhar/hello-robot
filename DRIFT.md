# Hello Robot Stretch 3 Description (MJCF)

## Identity

MuJoCo robot description for the [Hello Robot Stretch 3](https://hello-robot.com/product) — a mobile manipulator with a telescoping arm. The model was provided directly by Hello Robot under Apache 2.0 and converted from URDF to MJCF for use in MuJoCo simulation.

## Stack

- **Simulator:** MuJoCo 3.3.0 or later (hard requirement — earlier versions are not supported)
- **Description format:** MJCF (XML)
- **Source format:** URDF (converted via the pipeline described below)

## Key Files

```
stretch.xml        # Main robot MJCF model
scene.xml          # Scene wrapper: includes robot + textured groundplane, skybox, haze
stretch.png        # Reference render
CHANGELOG.md       # Full version history
```

`scene.xml` is the typical entry point for simulation — load it to get the robot in a complete environment.

## URDF → MJCF Derivation

The model was produced through a documented, reproducible pipeline:

1. `.obj` meshes processed with [`obj2mjcf`](https://github.com/kevinzakka/obj2mjcf)
2. URDF patched with a `<mujoco>` compiler clause before loading:
   ```xml
   <mujoco>
     <compiler discardvisual="false" fusestatic="false" balanceinertia="true"/>
   </mujoco>
   ```
   This preserves visual geometries and prevents inertia errors on near-massless links.
3. URDF loaded into MuJoCo and re-saved as MJCF
4. Common properties extracted into the `<default>` section manually
5. Actuators added
6. `<exclude>` clauses added to suppress self-collision inside the telescoping arm
7. `scene.xml` composed around the robot MJCF
8. XML formatted for readability

## Conventions

- **Collision exclusions:** The telescoping arm segments require explicit `<exclude>` pairs. If you add new arm links, add corresponding `<exclude>` clauses or expect spurious contact forces.
- **Visual geometry:** `discardvisual="false"` is intentional — removing it will strip visual meshes from the compiled model.
- **Static fusion disabled:** `fusestatic="false"` keeps the kinematic tree intact for inspection and debugging; fusing would collapse fixed joints.
- **Inertia balancing:** `balanceinertia="true"` corrects non-physical inertia tensors that can appear in URDF exports.

## Debugging

- **MuJoCo version errors at load time:** Confirm `mujoco.__version__ >= "3.3.0"`. The MJCF uses features not present in earlier releases.
- **Missing visual meshes:** Check that `discardvisual="false"` is present in the `<compiler>` block and that `obj2mjcf` output is on the mesh path.
- **Unexpected contact forces in the arm:** Verify `<exclude>` clauses cover all telescoping segment pairs.
- **Inertia warnings:** `balanceinertia="true"` should suppress these; if they reappear after editing, re-check any manually added links for valid inertia tensors.