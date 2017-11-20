class GameState:
    def __init__(self, state):
        self.enter = state.enter
        self.exit = state.exit
        self.pause = state.pause
        self.resume = state.resume
        self.handle_events = state.handle_events
        self.update = state.update
        self.draw = state.draw



class TestGameState:

    def __init__(self, name):
        self.name = name

    def enter(self):
        print("State [%s] Entered" % self.name)

    def exit(self):
        print("State [%s] Exited" % self.name)

    def pause(self):
        print("State [%s] Paused" % self.name)

    def resume(self):
        print("State [%s] Resumed" % self.name)

    def handle_events(self):
        print("State [%s] handle_events" % self.name)

    def update(self):
        print("State [%s] update" % self.name)

    def draw(self):
        print("State [%s] draw" % self.name)



running = None
stack = None


def change_state(state): # 현재 상태를 없애고 Top에서 실행
    global stack
    pop_state()
    stack.append(state)
    state.enter()



def push_state(state): # 쌓아두면서 차근차근 실행하다가 Top에서 실행
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(state)
    state.enter()



def pop_state():
    global stack
    if (len(stack) > 0):
        # execute the current state's exit function
        stack[-1].exit()
        # remove the current state
        stack.pop()

    # execute resume function of the previous state
    if (len(stack) > 0):
        stack[-1].resume()



def quit():
    global running
    running = False


def run(start_state):
    global running, stack
    running = True
    stack = [start_state] # stack은 넣고 빼는것밖에 못하는(특정 자리에 넣을 수 없고 입출력에 제한있는) 리스트
                          # 뺄 때 맨 마지막에 있는 것만 가져올 수 있음
                          # 리스트는 자료 집합
    start_state.enter()
    while (running):
        stack[-1].handle_events() # -1은 맨 마지막
        stack[-1].update()
        stack[-1].draw() # Top에서 handle, update,draw반복하다 push_state 들어오면 한 단 추가, 맨 위가 Top됨
                         # change면 밑에 있는 것들 다 지우고 맨 위가 Top
    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].exit() # 스택에 있는 상태들을 계속 exit하고
        stack.pop()


def test_game_framework():
    start_state = TestGameState('StartState')
    run(start_state)



if __name__ == '__main__':
    test_game_framework()