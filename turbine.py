try:
    from Nuclear_Reactor_Power_Plant_Simulator.syncroscope import Syncroscope
except:
    from syncroscope import Syncroscope

class Turbine:
    def __init__(self, root):
        self.rpm = 0.0 # Revolutions per minute
        self.valve = 0.0
        self.target = 0.0
        self.flow = 0.0
        self.powerOutput = 0.0
        self.hertz = 0.0
        self.syncroscope = Syncroscope(root, self)
        self.synced = False
        self.breakers = False
        self.exploded = False
        self.triped = False
        self.bladeBackups = 2
        self.repairTimer = 0

    def update(self, reactorPower):
        if self.target < self.valve:
            self.valve = round(self.valve - 0.0003, 4)
        elif self.target > self.valve:
            self.valve = round(self.valve + 0.0003, 4)
        if not self.exploded and not self.synced and not self.triped:
            self.flow = ((reactorPower / 1000) * 1.8) * self.valve
            self.rpm += self.flow - (self.rpm / 1000)  # Simplified RPM calculation
            self.powerOutput = 0
            self.hertz = self.rpm / 50
            if self.rpm > 4800:
                self.exploded = True
            if self.flow >= 20:
                self.trip()
        elif self.exploded and self.rpm <= 0:
            if self.repairTimer < 5000 and self.bladeBackups > 0:
                self.rpm = 0
                self.repairTimer += 1
            elif self.repairTimer >= 5000 and self.bladeBackups > 0:
                self.exploded = False
                self.bladeBackups -= 1
                self.repairTimer = 0
        elif self.exploded or self.triped:
            self.valve = 0.0
            self.flow = 0.0
            if self.exploded:
                self.rpm -= 5
            else:
                self.rpm -= 1
            self.powerOutput = 0
            self.hertz = self.rpm / 50
            if self.triped and not self.exploded and self.rpm <= 0:
                self.rpm = 0
                self.triped = False
        elif self.synced:
            self.flow = ((reactorPower / 1000) * 1.8) * self.valve
            self.rpm = 3000
            self.syncroscope.angle = 90
            self.powerOutput = self.flow * (self.rpm / 50)  # Simplified power output calculation
            self.hertz = 60
            if self.powerOutput < 150:
                self.trip()
    
    def set_valve(self, value):
        self.target = value    

    def grid_sync(self):
        if 80 < self.syncroscope.angle < 100 and 2990 < self.rpm < 3010 and not self.triped and not self.exploded:
            self.synced = True
        else:
            self.triped = True
    
    def trip(self):
        self.triped = True
        self.synced = False
        self.close_breaker()
    
    def open_breaker(self):
        if self.synced:
            self.breakers = True
        elif not self.synced:
            self.exploded = True
    
    def close_breaker(self):
        self.breakers = False