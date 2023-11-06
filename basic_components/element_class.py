import math

class Element:
    def __init__(self, element_number, node1, node2, elastic_modulus, cross_section_area):
        self.element_number = element_number
        self.node1 = node1
        self.node2 = node2
        self.elastic_modulus = float(elastic_modulus)
        self.cross_section_area = float(cross_section_area)
        self.length = self.calculate_element_length() 
        self.phi = self.calculate_element_phi()


    def calculate_element_length(self):
        length = ((self.node1.x_coordination-self.node2.x_coordination)**2 + (self.node1.y_coordination-self.node2.y_coordination)**2)**(1/2)
        return length
    
    def calculate_element_phi(self):
        x_length = self.node1.x_coordination - self.node2.x_coordination
        y_length = self.node1.y_coordination - self.node2.y_coordination
        if x_length == 0:
            if self.node1.y_coordination - self.node2.y_coordination > 0:
                phi = math.radians(270)
            else:
                phi = math.radians(90)
        else:
            phi = math.atan(y_length / x_length)
        return phi
    
