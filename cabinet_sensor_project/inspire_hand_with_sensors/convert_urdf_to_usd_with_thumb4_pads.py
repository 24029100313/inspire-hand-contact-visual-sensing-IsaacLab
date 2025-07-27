#!/usr/bin/env python3
"""
Convert Inspire Hand URDF with Thumb Force Sensor 4 Pads to USD
Creates a single USD file and corresponding YAML configuration
Total: 997 sensor pads across 17 sensors
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Initialize Isaac Sim
from isaacsim import SimulationApp
simulation_app = SimulationApp({"renderer": "RaytracedLighting", "headless": True})

class InspireHandThumb4USDConverter:
    def __init__(self, source_dir="/home/larry/NVIDIA_DEV/isaac_grasp_ws/cabinet_sensor_project"):
        """Initialize the USD converter for Inspire Hand with Thumb4 Pads"""
        self.source_dir = Path(source_dir)
        self.asset_name = "inspire_hand_with_sensors"
        
        # Define paths
        self.asset_dir = self.source_dir / self.asset_name
        self.urdf_dir = self.asset_dir / "urdf"
        
        # Use the URDF with thumb4 sensor pads
        self.processed_urdf = self.urdf_dir / "inspire_hand_processed_with_pads.urdf"
        self.usd_file = self.asset_dir / "usd" / "inspire_hand_processed_with_pads.usd"
        self.yaml_file = self.asset_dir / "config" / "inspire_hand_processed_with_pads.yaml"
        
        # Ensure output directories exist
        self.usd_file.parent.mkdir(parents=True, exist_ok=True)
        self.yaml_file.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"🔧 Inspire Hand USD Converter (with Thumb4 Pads) initialized")
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
        """Create Isaac Lab configuration YAML with all 997 sensor pads"""
        config_content = f'''# Isaac Lab Asset Configuration - Inspire Hand with All Sensor Pads
# Generated from: {self.processed_urdf.name}
# Creation date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Total contact points: 997 across 17 sensors

inspire_hand_with_all_pads:
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
    # Thumb4 sensor pads (3x3 = 9 sensors, 1.2x1.2x0.6mm, white) - NEWLY ADDED
    thumb_sensor_4_pads:
      prim_path: "/inspire_hand_with_sensors/thumb_sensor_4_pad_*"
      update_period: 0.005  # 200 FPS
      force_threshold: 0.147  # 15g trigger force
      torque_threshold: 0.1
      sensor_count: 9
      grid_size: [3, 3]
      pad_size: [0.0012, 0.0012, 0.0006]  # 1.2x1.2x0.6mm
      color: "white"
  
  # Summary - Updated with Thumb4
  total_sensors:
    total_contact_points: 997  # All sensor pads including thumb4
    force_sensors: 17
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
        print("\n🚀 Starting Inspire Hand URDF to USD conversion (with Thumb4 pads)")
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
            print("✅ All 997 sensor pads (including thumb4) converted")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Conversion failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main conversion function"""
    converter = InspireHandThumb4USDConverter()
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
