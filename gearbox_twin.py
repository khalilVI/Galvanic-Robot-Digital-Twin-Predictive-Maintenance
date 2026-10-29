import pandas as pd
import random

class GalvanicHoist:
    def __init__(self):
        # 1. The Baseline (Healthy State for a 750W Motor)
        self.cycle_count = 0
        self.base_current_amps = 1.1 
        self.gearbox_friction = 0.0   

    def run_cycle(self):
        self.cycle_count += 1
        
        # 2. The Lifespan Math (12,000 cycles = ~1 year)
        # To reach a critical friction level of 0.25 right around 11,500 cycles:
        # 0.25 / 11500 = 0.0000217
        self.gearbox_friction += 0.0000217 
        
        # 3. The Inverter Output during Steps 22 & 30 (Horizontal Moves)
        friction_penalty = self.gearbox_friction * 1.6 
        electrical_noise = random.uniform(-0.05, 0.05) 
        
        simulated_amps = self.base_current_amps + friction_penalty + electrical_noise
        
 # 4. Define the Machine's True State 
        if simulated_amps >= 1.5:
            status = "CRITICAL_FAILURE"
        elif simulated_amps >= 1.3:
            status = "WARNING_HIGH_FRICTION"
        else:
            status = "HEALTHY"

        return {
            "Cycle_Number": self.cycle_count,
            "Inverter_Current_Amps": round(simulated_amps, 3),
            "Machine_State": status
        }

# --- THE DATA GENERATOR ---
print("Starting Digital Twin Simulation for 1 Year (12,000 Cycles)...")

robot = GalvanicHoist()
dataset = []

for _ in range(12000):
    cycle_data = robot.run_cycle()
    dataset.append(cycle_data)

df = pd.DataFrame(dataset)

# Saving directly to your PFE folder
df.to_csv(r"C:\Users\vikha\OneDrive\Desktop\stage pfe\rosca_gearbox_training_data.csv", index=False)

print("Simulation Complete. rosca_gearbox_training_data.csv generated with 12,000 rows.")