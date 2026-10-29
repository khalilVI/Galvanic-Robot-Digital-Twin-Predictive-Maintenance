import pandas as pd
import random
import numpy as np

class BrakeSimulator:
    def __init__(self):
        # Placeholders until you get the nameplate/inverter data tomorrow
        self.base_running_amps = 1.1
        self.travel_duration = 3.0 # Seconds the hoist actively moves up/down
        self.brake_health = 1.0 # 1.0 is perfect, 0.0 is completely dead

    def run_high_res_cycle(self, cycle_id):
        cycle_data = []
        
        # Calculate degradation: Stopping time increases as health drops
        # Healthy = 0.2s to stop. Critical = 5.0s to stop.
        stopping_time = 0.2 + (1.0 - self.brake_health) * 4.8
        
        # We record for 8 seconds total to ensure we capture the whole 5-second coasting phase
        total_recording_time = 8.0 

        for t in np.arange(0.0, total_recording_time, 0.1):
            t = round(t, 1)
            
            if t < self.travel_duration:
                # Motor is lifting normally
                amps = self.base_running_amps + random.uniform(-0.05, 0.05)
            elif t < (self.travel_duration + stopping_time):
                # Power is cut! Motor is coasting/grinding to a halt
                # Amps gradually drop from the running baseline down to 0
                time_in_stop_phase = t - self.travel_duration
                drop_ratio = 1.0 - (time_in_stop_phase / stopping_time)
                amps = (self.base_running_amps * drop_ratio) + random.uniform(-0.05, 0.05)
            else:
                # Motor has completely stopped
                amps = 0.0
            
            # Determine State
            state = "HEALTHY"
            if self.brake_health <= 0.1:
                state = "CRITICAL_BRAKE"
            elif self.brake_health <= 0.5:
                state = "WARNING_DEGRADED"

            cycle_data.append({
                "Cycle_ID": cycle_id,
                "Time_Seconds": t,
                "Inverter_Amps": round(max(amps, 0.0), 3), # Ensure it doesn't drop below 0
                "Machine_State": state
            })
            
        return cycle_data

# --- GENERATE DATA ---
robot = BrakeSimulator()
all_data = []

print("Simulating New Brake Logic (End-of-Cycle Coasting)...")

# Simulate 3 distinct points in the machine's life
# 1.0 = Brand New, 0.5 = Warning, 0.0 = Critical (coasts for 5s)
health_stages = [1.0, 0.5, 0.0] 

for i, health in enumerate(health_stages):
    robot.brake_health = health
    cycle_id = f"Cycle_Stage_{i+1}"
    data = robot.run_high_res_cycle(cycle_id)
    all_data.extend(data)

# Saving as V2 directly to your PFE folder
df = pd.DataFrame(all_data)
df.to_csv(r"C:\Users\vikha\OneDrive\Desktop\stage pfe\rosca_brake_training_data_V2.csv", index=False)

print("rosca_brake_training_data_V2.csv generated successfully.")