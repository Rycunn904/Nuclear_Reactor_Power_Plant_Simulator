from reactor import Reactor

def test_scram():
    reactor = Reactor()

    reactor.toggle_reactor()

    while reactor.temperature < 3120:
        reactor.update()

    reactor.scram()

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