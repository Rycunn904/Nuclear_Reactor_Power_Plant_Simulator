from Nuclear_Reactor_Power_Plant_Simulator.turbine import Turbine
from tkinter import Tk

def test_sync():
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
    assert not turbine.triped
    assert not turbine.exploded

def test_breaker_explode():
    root = Tk()
    turbine = Turbine(root)

    turbine.open_breaker()

    turbine.update(1420*3)

    assert turbine.exploded

def test_miss_sync():
    root = Tk()
    turbine = Turbine(root)
    turbine.rpm = 3000
    turbine.hertz = 60
    turbine.syncroscope.angle = 0
    turbine.valve = 0.39

    turbine.grid_sync()

    turbine.update(1420*3)

    assert turbine.triped

def test_explode():
    root = Tk()
    turbine = Turbine(root)

    turbine.valve = 1.0
    turbine.target = 1.0

    while not turbine.exploded:
        turbine.update(1420*3)
    
    assert turbine.exploded

    while turbine.exploded:
        turbine.update(0)
    
    assert turbine.bladeBackups == 1
    assert turbine.rpm == 0
    assert not turbine.exploded

def test_sync_and_generate():
    root = Tk()
    turbine = Turbine(root)
    turbine.rpm = 3000
    turbine.hertz = 60
    turbine.syncroscope.angle = 90
    turbine.valve = 0.39

    turbine.grid_sync()

    turbine.update(1420*3)

    turbine.open_breaker()

    assert turbine.breakers
    assert turbine.powerOutput > 100