class Node:
    def __init__(self,node_number, x_coordination, y_coordination, x_constraint, y_constraint):
        self.node_number = node_number
        self.x_coordination = float(x_coordination)
        self.y_coordination = float(y_coordination)
        self.x_constraint = x_constraint
        self.y_constraint = y_constraint
