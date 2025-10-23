class Turbine:
    def __init__(self):
        self.rpm = 0.0 # Revolutions per minute
        self.valve = 0.0
        self.flow = 0.0
        self.powerOutput = 0.0

    def update(self, reactorPower):
        self.flow = ((reactorPower / 1000) * 1.8) * self.valve
        self.rpm += self.flow - (self.rpm / 1000)  # Simplified RPM calculation
        self.powerOutput = self.rpm * 0.05  # Simplified power output calculation
        # print(f"Turbine RPM: {self.rpm:.2f}\nPower Output: {self.powerOutput:.2f} MW")