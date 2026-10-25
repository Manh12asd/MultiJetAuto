Place each saved map in its own folder, for example:

```text
maps/
  room/
    map.yaml
    map.pgm
```

Use the real saved map and its metadata. In `map.yaml`, set `image: map.pgm`
(or the actual image filename). The image path is relative to the YAML file.
The launch does not create a map; `room` is currently an empty placeholder.

Build the package again after adding maps so they are installed with bringup:

```bash
colcon build --packages-select bringup --symlink-install
source install/setup.bash
ros2 launch bringup load_map.launch.py map_name:=room
```

Run localization separately for each robot:

```bash
ros2 launch bringup localization.launch.py \
  namespace:=robot1 frame_prefix:=robot1/
```

For a map outside the package, pass `map:=/absolute/path/to/map.yaml` to load_map.
Map server parameters are stored in `bringup/config/load_map.yaml`; AMCL
parameters are stored in `bringup/config/localization.yaml`. Each launch accepts
`params_file:=/absolute/path/to/its/config.yaml`.

Run load_map once to publish the shared `/map` topic, even when its nodes have
a namespace. It has its own lifecycle manager managing only map_server.
Localization runs AMCL and a separate lifecycle manager under `/robot1`.
AMCL receives global `/map` and namespaced `/robot1/scan`, and uses global `/tf`
and `/tf_static`. It publishes `map -> robot1/odom` and expects the robot bringup
to provide `robot1/odom -> robot1/base_footprint` and the sensor transforms.
Namespace and frame_prefix are independent: include the trailing `/` in the
prefix and match the frame IDs published by the robot. Leave both empty for
a robot without a namespace or frame prefix. If changing `map_frame`, pass the
same value to both launches so the map header and AMCL global frame agree.

Start the robot bringup separately and set its actual initial pose using RViz's
2D Pose Estimate, targeting `/robot1/initialpose`.
