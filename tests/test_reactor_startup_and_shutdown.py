from reactor import Reactor

def test_reactor_startup_and_shutdown():
    reactor = Reactor(meltdownTemperature=3120)

    # Initial state checks
    assert reactor.isActive == False
    assert reactor.temperature == 20
    assert reactor.powerOutput == 0
    assert reactor.controlRodPosition == 100

    # Start the reactor
    reactor.toggle_reactor()
    assert reactor.isActive == True
    assert reactor.inStartup == True
    assert reactor.controlRodPosition == 50

    # Simulate startup phase
    while reactor.temperature < 625: # Simulate enough updates to reach 625C
        reactor.update()
    
    assert reactor.temperature >= 625
    assert reactor.inStartup == False

    reactor.controlRodPosition = 55 # Adjust control rods for normal operation

    # Simulate normal operation for a few updates
    for _ in range(10):
        reactor.update()
    
    assert reactor.powerOutput > 0

    # Move control rods to shutdown the reactor
    reactor.controlRodPosition = 95  # Almost fully inserted
    while reactor.temperature > 100:
        reactor.update()
    
    # Attempt to shut down the reactor
    reactor.toggle_reactor()
    
    assert reactor.isActive == False
    assert reactor.temperature < 100
    assert reactor.powerOutput == 0
    assert reactor.controlRodPosition == 100

