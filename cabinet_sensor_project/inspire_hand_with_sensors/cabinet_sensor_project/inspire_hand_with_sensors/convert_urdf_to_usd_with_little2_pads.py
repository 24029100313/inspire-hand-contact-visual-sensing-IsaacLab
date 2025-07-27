#!/usr/bin/env python3
"""
Convert Inspire Hand URDF with Little Force Sensor 2 Pads to USD
Creates a single USD file and corresponding YAML configuration
Total: 952 sensor pads
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Initialize Isaac Sim
from isaacsim import SimulationApp
simulation_app = SimulationApp({"renderer": "RaytracedLighting", "headless": True})

class InspireHandLittle2USDConverter:
    def __init__(self, source_dir="/home/larry/NVIDIA_DEV/isaac_grasp_ws/cabinet_sensor_project"):
        """Initialize the USD converter for Inspire Hand with Little2 Pads"""
        self.source_dir = Path(source_dir)
        self.asset_name = "inspire_hand_with_sensors"
        
        # Define paths
        self.asset_dir = self.source_dir / self.asset_name
        self.urdf_dir = self.asset_dir / "urdf"
        
        # Use the URDF with little2 sensor pads
        self.processed_urdf = self.urdf_dir / "inspire_hand_processed_with_pads.urdf"
        self.usd_file = self.asset_dir / "usd" / "inspire_hand_processed_with_pads.usd"
        self.yaml_file = self.asset_dir / "config" / "inspire_hand_processed_with_pads.yaml"
        
        # Ensure output directories exist
        self.usd_file.parent.mkdir(parents=True, exist_ok=True)
        self.yaml_file.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"🔧 Inspire Hand USD Converter (with Little2 Pads) initialized")
        print(f"📁 Source directory: {self.source_dir}")
        print(f"📄 Source URDF: {self.processed_urdf}")
        print(f"📄 Target USD: {self.usd_file}")
        print(f"📄 Target YAML: {self.yaml_file}")

    def convert_to_usd(self):
        """Convert URDF to USD using Isaac Sim"""
        print(f"\n🔄 Converting URDF to USD...")
        print(f"📄 Input: {self.processed_urdf}")
        print(f"📄 Output: {self.usd_file}")
        
        if not self.processed_urdf.exists():
            raise FileNotFoundError(f"Source URDF not found: {self.processed_urdf}")
        
        try:
            import omni.kit.commands
            from omni.isaac.core.utils.extensions import enable_extension
            import omni.usd
            
            # Enable necessary extensions
            enable_extension("isaacsim.asset.importer.urdf")
            
            print("🔧 Executing URDF import...")
            
            # Create URDF import configuration
            status, import_config = omni.kit.commands.execute("URDFCreateImportConfig")
            
            # Configure import settings
            import_config.merge_fixed_joints = False
            import_config.convex_decomp = False
            import_config.import_inertia_tensor = True
            import_config.self_collision = False
            import_config.create_physics_scene = True
            import_config.distance_scale = 1.0
            
            # Import URDF
            status, import_result = omni.kit.commands.execute(
                "URDFParseAndImportFile",
                urdf_path=str(self.processed_urdf),
                import_config=import_config,
            )
            
            if not status:
                raise RuntimeError("Failed to import URDF")
            
            print("✅ URDF import successful")
            
            # Get the current stage and export it
            from omni.usd import get_context
            usd_context = get_context()
            stage = usd_context.get_stage()
            
            # Export the stage to USD
            stage.Export(str(self.usd_file))
            print(f"✅ USD export successful: {self.usd_file}")
            
        except ImportError as e:
            print(f"❌ Isaac Sim import error: {e}")
            print("Please ensure this script is run with Isaac Sim's Python environment")
            raise
        except Exception as e:
            print(f"❌ Conversion error: {e}")
            raise

    def create_isaac_lab_config(self):
        """Create Isaac Lab configuration YAML with Little2 pads"""
        config_content = f'''# Isaac Lab Asset Configuration - Inspire Hand with Little Force Sensor 2 Pads
# Generated from: {self.processed_urdf.name}
# Creation date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Total contact points: 952 (including 80 little2 pads)

inspire_hand_with_little2_pads:
  class_type: RigidObject
  
  # USD file path
  usd_path: "{self.usd_file}"
  
  # Physics properties
  physics:
    rigid_body_enabled: true
    kinematic_enabled: false
    disable_gravity: false
    
  # Contact sensor configuration - Uniform 0.6mm thickness
  contact_sensors:
    # Palm sensor pads (14x8 = 112 sensors, 3.0x3.0x0.6mm, green)
    palm_sensor_pads:
      prim_path: "/inspire_hand_with_sensors/palm_sensor_pad_*"
      update_period: 0.005  # 200 FPS 
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 112
      grid_size: [14, 8]
      pad_size: [0.003, 0.003, 0.0006]  # 3.0x3.0x0.6mm
      color: "green"
      
    # Thumb1 sensor pads (8x12 = 96 sensors, 1.2x1.2x0.6mm, blue)
    thumb_sensor_1_pads:
      prim_path: "/inspire_hand_with_sensors/thumb_sensor_1_pad_*"
      update_period: 0.005  # 200 FPS
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 96
      grid_size: [8, 12]
      pad_size: [0.0012, 0.0012, 0.0006]  # 1.2x1.2x0.6mm
      color: "blue"
      
    # Thumb2 sensor pads (2x4 = 8 sensors, 1.2x1.2x0.6mm, orange)
    thumb_sensor_2_pads:
      prim_path: "/inspire_hand_with_sensors/thumb_sensor_2_pad_*"
      update_period: 0.005  # 200 FPS
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 8
      grid_size: [2, 4]
      pad_size: [0.0012, 0.0012, 0.0006]  # 1.2x1.2x0.6mm
      color: "orange"
      
    # Thumb3 sensor pads (8x12 = 96 sensors, 1.2x1.2x0.6mm, purple)
    thumb_sensor_3_pads:
      prim_path: "/inspire_hand_with_sensors/thumb_sensor_3_pad_*"
      update_period: 0.005  # 200 FPS
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 96
      grid_size: [8, 12]
      pad_size: [0.0012, 0.0012, 0.0006]  # 1.2x1.2x0.6mm
      color: "purple"
      
    # Index1 sensor pads (8x10 = 80 sensors, 1.2x1.2x0.6mm, red)
    index_sensor_1_pads:
      prim_path: "/inspire_hand_with_sensors/index_sensor_1_pad_*"
      update_period: 0.005  # 200 FPS
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 80
      grid_size: [8, 10]
      pad_size: [0.0012, 0.0012, 0.0006]  # 1.2x1.2x0.6mm
      color: "red"
      
    # Index2 sensor pads (8x10 = 80 sensors, 1.2x1.2x0.6mm, light_red)
    index_sensor_2_pads:
      prim_path: "/inspire_hand_with_sensors/index_sensor_2_pad_*"
      update_period: 0.005  # 200 FPS
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 80
      grid_size: [8, 10]
      pad_size: [0.0012, 0.0012, 0.0006]  # 1.2x1.2x0.6mm
      color: "light_red"
      
    # Middle1 sensor pads (10x8 = 80 sensors, 1.2x1.2x0.6mm, cyan)
    middle_sensor_1_pads:
      prim_path: "/inspire_hand_with_sensors/middle_sensor_1_pad_*"
      update_period: 0.005  # 200 FPS
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 80
      grid_size: [10, 8]
      pad_size: [0.0012, 0.0012, 0.0006]  # 1.2x1.2x0.6mm
      color: "cyan"
      
    # Middle2 sensor pads (8x10 = 80 sensors, 1.2x1.2x0.6mm, light_cyan)
    middle_sensor_2_pads:
      prim_path: "/inspire_hand_with_sensors/middle_sensor_2_pad_*"
      update_period: 0.005  # 200 FPS
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 80
      grid_size: [8, 10]
      pad_size: [0.0012, 0.0012, 0.0006]  # 1.2x1.2x0.6mm
      color: "light_cyan"
      
    # Ring1 sensor pads (8x10 = 80 sensors, 1.2x1.2x0.6mm, magenta)
    ring_sensor_1_pads:
      prim_path: "/inspire_hand_with_sensors/ring_sensor_1_pad_*"
      update_period: 0.005  # 200 FPS
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 80
      grid_size: [8, 10]
      pad_size: [0.0012, 0.0012, 0.0006]  # 1.2x1.2x0.6mm
      color: "magenta"
      
    # Ring2 sensor pads (8x10 = 80 sensors, 1.2x1.2x0.6mm, light_magenta)
    ring_sensor_2_pads:
      prim_path: "/inspire_hand_with_sensors/ring_sensor_2_pad_*"
      update_period: 0.005  # 200 FPS
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 80
      grid_size: [8, 10]
      pad_size: [0.0012, 0.0012, 0.0006]  # 1.2x1.2x0.6mm
      color: "light_magenta"
      
    # Little1 sensor pads (8x10 = 80 sensors, 1.2x1.2x0.6mm, yellow)
    little_sensor_1_pads:
      prim_path: "/inspire_hand_with_sensors/little_sensor_1_pad_*"
      update_period: 0.005  # 200 FPS
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 80
      grid_size: [8, 10]
      pad_size: [0.0012, 0.0012, 0.0006]  # 1.2x1.2x0.6mm
      color: "yellow"
      
    # Little2 sensor pads (8x10 = 80 sensors, 1.2x1.2x0.6mm, light_yellow)
    little_sensor_2_pads:
      prim_path: "/inspire_hand_with_sensors/little_sensor_2_pad_*"
      update_period: 0.005  # 200 FPS
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 80
      grid_size: [8, 10]
      pad_size: [0.0012, 0.0012, 0.0006]  # 1.2x1.2x0.6mm
      color: "light_yellow"
  
  # Summary
  total_sensors:
    palm_pads: 112
    thumb1_pads: 96
    thumb2_pads: 8
    thumb3_pads: 96
    index1_pads: 80
    index2_pads: 80
    middle1_pads: 80
    middle2_pads: 80
    ring1_pads: 80
    ring2_pads: 80
    little1_pads: 80
    little2_pads: 80  # NEW: Little force sensor 2
    total_contact_points: 952  # 112+96+8+96+80+80+80+80+80+80+80+80
    force_sensors: 12
    uniform_thickness: 0.6  # mm
    
  # Sensor specifications
  sensor_specs:
    trigger_force: 15  # grams
    force_range: 20    # Newtons
    sample_rate: 200   # FPS
    thickness: 0.6     # mm (unified)
'''

        # Write configuration to file
        with open(self.yaml_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"✅ Isaac Lab config created: {self.yaml_file}")

    def convert(self):
        """Execute the complete conversion process"""
        print("\n🚀 Starting Inspire Hand URDF to USD conversion (with Little2 pads)")
        print("=" * 70)
        
        try:
            # Convert URDF to USD
            self.convert_to_usd()
            
            # Create Isaac Lab config
            self.create_isaac_lab_config()
            
            # Display results
            if self.usd_file.exists():
                size_mb = self.usd_file.stat().st_size / (1024 * 1024)
                print(f"\n📊 USD file size: {size_mb:.1f} MB")
            
            if self.yaml_file.exists():
                size_kb = self.yaml_file.stat().st_size / 1024
                print(f"📊 YAML file size: {size_kb:.1f} KB")
            
            print("\n🎉 Conversion completed successfully!")
            print(f"✅ USD file: {self.usd_file}")
            print(f"✅ YAML config: {self.yaml_file}")
            print("✅ All 952 sensor pads (including little2) converted")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Conversion failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main conversion function"""
    converter = InspireHandLittle2USDConverter()
    success = converter.convert()
    
    # Close Isaac Sim
    simulation_app.close()
    
    if success:
        print("\n✅ All operations completed successfully!")
        return 0
    else:
        print("\n❌ Conversion failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 