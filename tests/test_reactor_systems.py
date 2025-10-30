try:
    from Nuclear_Reactor_Power_Plant_Simulator.reactor import Reactor
except:
    from reactor import Reactor

def test_scram_3120_nomelt():
    reactor = Reactor()

    reactor.toggle_reactor()

    while reactor.temperature < 3120:
        reactor.update()

    reactor.scram()

    reactor.pumpA = True
    reactor.pumpAspeed = 1
    reactor.pumpB = True
    reactor.pumpBspeed = 1
    reactor.toggle_coolant_valve()

    assert reactor.scramEngaged == True

    while reactor.scramFrame < reactor.scramFail and reactor.temperature > reactor.meltdownSafety:
        reactor.update()

    assert reactor.inMeltdown == False
    assert reactor.temperature == 20
    assert reactor.powerOutput == 0
    assert reactor.controlRodPosition == 100
    assert reactor.isActive == False
    assert reactor.scramFrame == 0
    assert reactor.meltdownReactivity == 0.0
    assert reactor.scramEngaged == False

def test_scram_4000_nomelt():
    reactor = Reactor()

    reactor.toggle_reactor()

    while reactor.temperature < 4000:
        reactor.update()

    reactor.scram()

    reactor.pumpA = True
    reactor.pumpAspeed = 1
    reactor.pumpB = True
    reactor.pumpBspeed = 1
    reactor.toggle_coolant_valve()
    reactor.controlRodPosition = 100

    assert reactor.scramEngaged == True # Scram

    while reactor.scramFrame < reactor.scramFail and reactor.temperature > reactor.meltdownSafety:
        reactor.update()

    assert reactor.inMeltdown == False # Not in meltdown
    assert reactor.temperature == 20
    assert reactor.powerOutput == 0
    assert reactor.controlRodPosition == 100
    assert reactor.isActive == False
    assert reactor.scramFrame == 0
    assert reactor.meltdownReactivity == 0.0
    assert reactor.scramEngaged == False

def test_scram_5000_melt():
    reactor = Reactor()

    reactor.toggle_reactor()

    while reactor.temperature < 5000:
        reactor.update()

    reactor.scram()

    reactor.pumpA = True
    reactor.pumpAspeed = 1
    reactor.pumpB = True
    reactor.pumpBspeed = 1
    reactor.toggle_coolant_valve()

    assert reactor.scramEngaged == True

    while reactor.scramFrame < reactor.scramFail and reactor.temperature > reactor.meltdownSafety:
        reactor.update()

    assert reactor.inMeltdown == True
    assert reactor.controlRodPosition == 100
    assert reactor.isActive == True
    assert reactor.scramEngaged == True

def test_reactor_startup_and_shutdown():
    reactor = Reactor()

    # Initial state checks
    assert reactor.isActive == False
    assert reactor.temperature == 20
    assert reactor.powerOutput == 0
    assert reactor.controlRodPosition == 100

    # Start the reactor
    reactor.toggle_reactor()
    assert reactor.isActive == True
    assert reactor.inStartup == True
    assert reactor.controlRodPosition == 100

    # Simulate startup phase
    while reactor.temperature < 1420: # Simulate enough updates to reach 1420
        reactor.update()
    
    assert reactor.temperature >= 625
    assert reactor.inStartup == False

    reactor.controlRodPosition = 55 # Adjust control rods for normal operation
    reactor.pumpA = True
    reactor.pumpAspeed = 1
    reactor.pumpB = True
    reactor.pumpBspeed = 1
    reactor.toggle_coolant_valve()

    assert reactor.pumpA
    assert reactor.pumpB
    assert reactor.cvOpen

    # Simulate normal operation for a few updates
    for _ in range(10):
        reactor.update()
    
    assert reactor.powerOutput > 0

    # Move control rods to shutdown the reactor
    reactor.controlRodPosition = 95.0  # Almost fully inserted
    while reactor.temperature != 20:
        reactor.update()

    reactor.update()
    
    assert reactor.isActive == False
    assert reactor.temperature < 100
    assert reactor.powerOutput == 0.0
    assert reactor.controlRodPosition == 100.0

def test_normal_op_no_delta():
    reactor = Reactor()

    # Initial state checks
    assert reactor.isActive == False
    assert reactor.temperature == 20
    assert reactor.powerOutput == 0
    assert reactor.controlRodPosition == 100.0

    # Start the reactor
    reactor.toggle_reactor()
    assert reactor.isActive == True
    assert reactor.inStartup == True
    assert reactor.controlRodPosition == 100.0

    # Simulate startup phase
    while reactor.temperature < 1420: # Simulate enough updates to reach 1420
        reactor.update()
    
    assert reactor.temperature >= 625
    assert reactor.inStartup == False

    reactor.controlRodPosition = 55 # Adjust control rods for normal operation
    reactor.pumpA = True
    reactor.pumpAspeed = 1
    reactor.pumpB = True
    reactor.pumpBspeed = 1
    reactor.toggle_coolant_valve()

    assert reactor.pumpA
    assert reactor.pumpB
    assert reactor.cvOpen

    reactor.update()

    temp = reactor.temperature

    reactor.randomDelta = 0

    # Simulate normal operation for a while
    for _ in range(10000):
        reactor.update()
    
    assert reactor.temperature == temp