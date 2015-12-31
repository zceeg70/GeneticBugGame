__author__ = 'Peter'

from eventsConfig import ViewEvents as GameEvents
from eventsConfig import ViewStates as ViewScreen

renderObject = None
# class to control what is being shown in the view.
class CurrentState:
    def __init__(self):
        self.StartState = Start()
        self.LevelEnd = LevelEnd()
        self.LevelRunning = LevelRunning()
        self.GameOver = GameOver()
        self.currentState = self.StartState

    # method to change to change the state.
    # calls the current states end() method, and next states start() method
    def set_state(self, nextState):
        self.currentState.end()
        nextState.start()
        self.currentState = nextState

    def event(self, eventName):
        if self.currentState == self.StartState:
            if eventName == GameEvents.StartButton:
                self.set_state(self.LevelRunning)
        elif self.currentState == self.LevelRunning:
            if eventName == GameEvents.LevelComplete:
                self.set_state(self.LevelEnd)
        elif self.currentState == self.LevelEnd:
            pass
        elif self.currentState == self.GameOver:
            pass

class State:
    def __init__(self,name):
        self.running = False
        self.name = name

    def start(self):
        pass

    def end(self):
        pass

class Start(State):
    def __init__(self):
        super("Start")

    def start(self):
        pass

    def end(self):
        pass

class LevelEnd(State):
    def __init__(self):
        super("LevelEnd")

    def start(self):
        #display result
        pass

class LevelRunning(State):
    def __init__(self):
        super("LevelRunning")

    def start(self):
        if renderObject is not None:
            renderObject.display_state(ViewScreen.LevelRunning)

class GameOver(State):
    def __init__(self):
        super("GameOver")

CurrentState = CurrentState()