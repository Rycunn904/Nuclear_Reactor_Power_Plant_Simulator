from reactor import Reactor

def test_scram_after_5000():
    reactor = Reactor()

    reactor.toggle_reactor()

    while reactor.temperature < 5000:
        reactor.update()

    reactor.scram()

    assert reactor.scramEngaged == True

    while reactor.scramFrame < reactor.scramFail and reactor.temperature > reactor.meltdownSafety:
        reactor.update()

    assert reactor.inMeltdown == True
    assert reactor.controlRodPosition == 100
    assert reactor.isActive == True
    assert reactor.scramEngaged == True