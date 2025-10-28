from Nuclear_Reactor_Power_Plant_Simulator.turbine import Turbine
from tkinter import Tk

def test_test1():
    root = Tk()
    turbine = Turbine(root)
    turbine.rpm = 3000
    turbine.hertz = 60
    turbine.syncroscope.angle = 90
    turbine.valve = 0.39

    turbine.grid_sync()

    turbine.update(1420*3)

    assert turbine.synced
    assert turbine.rpm == 3000
    assert turbine.triped == False
    assert turbine.exploded == False