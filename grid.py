import random

class Grid:
    def __init__(self) -> None:
        self.powerIn = 0
        self.minPO = 160
        self.maxPO = 400
        self.time = 0
        self.powerOrder = 0
        self.needsEnergy = False
        self.moe = 20
        self.powerSold = 0
    
    def new_PO(self) -> None:
        self.powerOrder = random.randint(self.minPO, self.maxPO)
        self.time = 2700
        self.needsEnergy = True
    
    def update(self, power) -> None:
        self.powerIn = power
        if self.powerOrder - self.moe <= self.powerIn <= self.powerOrder + self.moe and self.time > 0:
            self.powerSold += (self.powerIn/60)/60
        if self.time <= 0:
            self.new_PO()
    
    def get_PO(self) -> int:
        return self.powerOrder
    
    def get_power_sold(self) -> str:
        return f"{self.powerSold:.0f}"