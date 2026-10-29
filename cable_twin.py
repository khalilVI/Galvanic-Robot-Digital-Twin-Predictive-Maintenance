import pandas as pd

class CableFatigueSimulator:
    def __init__(self):
        self.total_flex_cycles = 0
        # Corrected: 45 cycles/day * 240 days * 6 years
        self.lifespan_limit = 64800 

    def run_cycle(self):
        self.total_flex_cycles += 1
        
        # Calculate how "tired" the copper wire is
        fatigue_percentage = (self.total_flex_cycles / self.lifespan_limit) * 100
        
        # Determine the health state based on the new 64,800 timeline
        state = "HEALTHY"
        if fatigue_percentage >= 100:
            # 64,800 cycles - The 6-year mark
            state = "CRITICAL_SINGLE_CABLE_SNAP"
        elif fatigue_percentage >= 95:
            # ~61,560 cycles (5.7 years) 
            state = "WARNING_EXPECT_CABLE_FAILURES"
        elif fatigue_percentage >= 80:
            # ~51,840 cycles (4.8 years)
            state = "INFO_HIGH_WEAR_ON_BUNDLE"

        return {
            "Total_Flex_Cycles": self.total_flex_cycles,
            "Fatigue_Percentage": round(min(fatigue_percentage, 100.0), 2),
            "Machine_State": state
        }

# --- GENERATE DATA ---
print("Simulating 6 Years of Cable Carrier Movement (Rosca Schedule)...")

robot = CableFatigueSimulator()
dataset = []

# Fast-forward simulating exactly past the break point
for _ in range(64805):
    dataset.append(robot.run_cycle())

df = pd.DataFrame(dataset)

# Save directly to your PFE folder
df.to_csv(r"C:\Users\vikha\OneDrive\Desktop\stage pfe\rosca_cable_training_data.csv", index=False)

print("rosca_cable_training_data.csv generated successfully.")