_robot = _env = None

def init(robot, environment):
    global _robot, _env
    _robot, _env = robot, environment

def read_id():
    for tid, rect in _env.tags.items():
        if rect.collidepoint(_robot.x, _robot.y):
            return tid
    return None