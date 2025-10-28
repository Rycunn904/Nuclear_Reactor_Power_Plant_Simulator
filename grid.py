import random

class Grid:
    def __init__(self) -> None:
        self.powerIn = 0
        self.minPO = 160
        self.maxPO = 400
        self.minTime = 900
        self.maxTime = 2700
        self.time = 0
        self.powerOrder = 0
        self.needsEnergy = False
        self.moe = 20
    
    def new_PO(self) -> None:
        self.powerOrder = random.randint(self.minPO, self.maxPO)
        self.time = random.randint(self.minTime, self.maxTime)
        self.needsEnergy = True
    
    def update(self, power) -> None:
        self.powerIn = power
        if self.powerOrder - self.moe <= self.powerIn <= self.powerOrder + self.moe and self.time > 0:
            self.time -= 1
        if self.time <= 0:
            self.powerOrder = 0
            self.needsEnergy = False
    
    def get_PO(self) -> int:
        return self.powerOrder
    
    def get_time_left(self) -> str:
        return f"{self.time/60:.1f}"