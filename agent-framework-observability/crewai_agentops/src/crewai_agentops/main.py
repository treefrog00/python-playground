from .main_learning_guide import kickoff as learning_guide_kickoff
from .main_poems import kickoff as poems_kickoff

import agentops
agentops.init()

def kickoff():
    learning_guide_kickoff()

if __name__ == "__main__":
    kickoff()
