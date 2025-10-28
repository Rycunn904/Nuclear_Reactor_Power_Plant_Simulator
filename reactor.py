import random

class Reactor:
    def __init__(self, meltdownTemperature=3120, meltdownSafety=325):
        self.status = "Offline"

        self.randomDelta = random.uniform(-0.001, 0.001) # Small random fluctuation
        self.stable = False

        self.reactivity = 0.0 # Initial reactivity
        self.meltdownReactivity = 0.0 # Additional reactivity during meltdown

        self.temperature = 20 # Initial temperature in Celsius
        self.powerOutput = 0 # Initial power output in MW

        self.controlRodPosition = 100.0 # Control rods fully inserted (0-100%)
        self.rodsCanMove = False
        self.coolantFlowRate = 100.0 # Coolant flow rate percentage (0-100%)

        self.pumpA = False
        self.pumpAspeed = 0

        self.pumpB = False
        self.pumpBspeed = 0

        self.cvOpen = False
        self.rodMovementRate = "IDLE" # Direction of rod movement

        self.isActive = False # Reactor is initially off
        self.inStartup = False # Reactor is not in startup phase

        self.heatLoss = 5.0 # W/°C, heat loss to environment

        self.meltdownTemperature = meltdownTemperature # Meltdown temperature in Celsius
        self.meltdownWarning = 2120 # Temperature to trigger warning
        self.meltdownSafety = meltdownSafety # Temperature to successfully SCRAM
        self.inMeltdown = False

        self.scramEngaged = False
        self.scramFrame = 0
        self.scramFail = 10000 # Frames until meltdown after SCRAM failure
    
    def toggle_coolant_valve(self):
        self.cvOpen = not self.cvOpen
    
    def toggle_pump_alpha(self):
        self.pumpA = not self.pumpA
    
    def toggle_pump_beta(self):
        self.pumpB = not self.pumpB

    def toggle_move_rods_up(self):
        """Move control rods up (insert more)."""
        if self.rodsCanMove:
            if self.rodMovementRate == "UP":
                self.rodMovementRate = "IDLE"
                self.controlRodPosition = int(self.controlRodPosition)
            elif self.rodMovementRate == "IDLE":
                self.rodMovementRate = "DOWN"

    def toggle_move_rods_down(self):
        """Move control rods down (withdraw less)."""
        if self.rodsCanMove:
            if self.rodMovementRate == "DOWN":
                self.rodMovementRate = "IDLE"
                self.controlRodPosition = int(self.controlRodPosition)
            elif self.rodMovementRate == "IDLE":
                self.controlRodPosition += 0.5
                self.rodMovementRate = "UP"
            
    
    def toggle_reactor(self):
        """Toggle the reactor's active state."""
        if self.isActive:
            if self.temperature < 100 and self.controlRodPosition > 90:
                self.temperature = 20
                self.powerOutput = 0
                self.controlRodPosition = 100.0
                self.isActive = False
        else:
            self.inStartup = True
            self.isActive = True
    
    def update(self):
        # Coolant pump speed
        if self.pumpA and self.pumpAspeed < 1:
            self.pumpAspeed = round(self.pumpAspeed + 0.001, 3)
        elif self.pumpA and self.pumpAspeed >= 1:
            self.pumpAspeed = 1
        elif not self.pumpA and self.pumpAspeed > 0:
            self.pumpAspeed = round(self.pumpAspeed - 0.001, 3)
        elif not self.pumpA and self.pumpAspeed <= 0:
            self.pumpAspeed = 0

        if self.pumpB and self.pumpBspeed < 1:
            self.pumpBspeed = round(self.pumpBspeed + 0.001, 3)
        elif self.pumpB and self.pumpBspeed >= 1:
            self.pumpBspeed = 1
        elif not self.pumpB and self.pumpBspeed > 0:
            self.pumpBspeed = round(self.pumpBspeed - 0.001, 3)
        elif not self.pumpB and self.pumpBspeed <= 0:
            self.pumpBspeed = 0

        # Control Rod Movement
        if not self.rodsCanMove:
            self.rodMovementRate = "N/A"
        elif self.rodMovementRate == "N/A":
            self.rodMovementRate = "IDLE"
        if self.rodMovementRate == "DOWN":
            if self.controlRodPosition >= 100.0:
                self.controlRodPosition = 100.0
            else:
                self.controlRodPosition = round(self.controlRodPosition + 0.02, 2)
        elif self.rodMovementRate == "UP":
            if self.controlRodPosition <= 0.0:
                self.controlRodPosition = 0.0
            else:
                self.controlRodPosition = round(self.controlRodPosition - 0.02, 2)

        # Reactor Status Update
        if self.scramEngaged:
            self.status = "SCRAM"
        elif self.inMeltdown:
            self.status = "Temp Critical"
        elif self.temperature >= self.meltdownWarning:
            self.status = "Temp High"
        elif self.inStartup:
            self.status = "Ignition"
        elif self.isActive:
            self.status = "Online"
        else:
            self.status = "Offline"

        # Update coolant based off Pump stations and CV status
        self.coolantFlowRate = ((self.pumpAspeed * 50) + (self.pumpBspeed * 50)) * (1 if self.cvOpen else 0)
        
        # heat up or cool down based on rod position and coolant flow, uses a reactivity model.
        if self.inStartup:
            self.temperature += 1
            self.powerOutput = self.temperature * 3
            if self.temperature >= 625:
                self.inStartup = False
                self.rodsCanMove = True
        elif self.isActive:
            self.reactivity = (100 - int(self.controlRodPosition) - ((self.coolantFlowRate / 2) - self.heatLoss)) / 500
            self.temperature += ((self.reactivity + self.meltdownReactivity) * 10)/2
            self.powerOutput = self.temperature * 3

            if self.reactivity == 0:
                if not self.stable:
                    self.randomDelta = random.uniform(-0.001, 0.001)
                    self.stable = True
                self.temperature += self.randomDelta # Minor fluctuations when stable
            else:
                self.stable = False

            # Power output is proportional to reactivity and temperature
        else:
            self.powerOutput = 0
            if self.temperature > 20:
                self.temperature -= 1 # Cool down when off
            else:
                self.temperature = 20 # Ambient temperature
        
        if self.temperature > self.meltdownTemperature and not self.inMeltdown:
            self.inMeltdown = True
            self.meltdownReactivity = 0.1 # Increase reactivity during meltdown
        
        # SCRAM procedure
        if self.scramEngaged:
            if self.temperature > self.meltdownSafety:
                self.inMeltdown = True
                self.controlRodPosition = 100
                self.meltdownReactivity = 0.0
            elif self.temperature <= self.meltdownSafety and self.scramFrame < self.scramFail:
                self.inMeltdown = False
                self.scramEngaged = False
                self.temperature = 20
                self.powerOutput = 0
                self.controlRodPosition = 100
                self.isActive = False
                self.scramFrame = 0
                self.meltdownReactivity = 0.0
        
        if self.inMeltdown:
            self.scramFrame += 1
            print(self.scramFrame, "out of", self.scramFail, "frames until MELTDOWN!", self.temperature, "/", self.meltdownSafety)
            if self.scramFrame >= self.scramFail:
                self.meltdownReactivity = 1.0

    
    def scram(self):
        self.scramEngaged = True