import data_generator
import math
import numpy as np

class Matrix:
    def __init__(self, filepath):
        self.filepath = filepath
        self.nodes_list, self.elements_list, self.external_force_list = self.operate_data_generator()

    def operate_data_generator(self):
        generator = data_generator.Data_generator(self.filepath)
        nodes_list = generator.generate_nodes_list()
        elements_list = generator.generate_elements_list()
        external_force_list = generator.generate_external_force()
        return nodes_list, elements_list, external_force_list
    
    def create_stiffness_matrix(self, element):
        cos = math.cos(element.phi)
        sin = math.sin(element.phi)
        k_matrix = (element.cross_section_area*element.elastic_modulus/element.length) * np.array([[cos*cos, cos*sin, -cos*cos, -cos*sin],
                                                                                                   [cos*sin, sin*sin, -cos*sin, -sin*sin],
                                                                                                   [-cos*cos, -cos*sin, cos*cos, cos*sin],
                                                                                                   [-cos*sin, -sin*sin, cos*sin, sin*sin]])
        return k_matrix
    
    def create_system_force_vector(self):
        system_force_vector = np.zeros((len(self.nodes_list)*2,1))
        for i in range(len(self.external_force_list)):
            node_num = self.external_force_list[i].applied_node_num
            system_force_vector[(node_num*2)-2] = self.external_force_list[i].x_force
            system_force_vector[(node_num*2)-1] = self.external_force_list[i].y_force
        return system_force_vector
    
    def deformer_to_system_matrix(self, element):
        base = np.zeros((len(self.nodes_list)*2,len(self.nodes_list)*2))
        k_stiffness = self.create_stiffness_matrix(element)
        node1 = element.node1.node_number
        node2 = element.node2.node_number
        base[node1*2-2][node1*2-2] = k_stiffness[0][0]
        base[node1*2-2][node1*2-1] = k_stiffness[0][1]
        base[node1*2-2][node2*2-2] = k_stiffness[0][2]
        base[node1*2-2][node2*2-1] = k_stiffness[0][3]
        base[node1*2-1][node1*2-2] = k_stiffness[1][0]
        base[node1*2-1][node1*2-1] = k_stiffness[1][1]
        base[node1*2-1][node2*2-2] = k_stiffness[1][2]
        base[node1*2-1][node2*2-1] = k_stiffness[1][3]
        base[node2*2-2][node1*2-2] = k_stiffness[2][0]
        base[node2*2-2][node1*2-1] = k_stiffness[2][1]
        base[node2*2-2][node2*2-2] = k_stiffness[2][2]
        base[node2*2-2][node2*2-1] = k_stiffness[2][3]
        base[node2*2-1][node1*2-2] = k_stiffness[3][0]
        base[node2*2-1][node1*2-1] = k_stiffness[3][1]
        base[node2*2-1][node2*2-2] = k_stiffness[3][2]
        base[node2*2-1][node2*2-1] = k_stiffness[3][3]
        return base

    def assemble_system_matrixs(self):
        assembled_system_matrix = np.zeros((len(self.nodes_list)*2,len(self.nodes_list)*2))
        for element in self.elements_list:
            assembled_system_matrix += self.deformer_to_system_matrix(element)
        return assembled_system_matrix

    def reflect_constraint(self,assembled_system_matrix):
        x_constraint_nodes = [node.node_number for node in self.nodes_list if node.x_constraint]
        y_constraint_nodes = [node.node_number for node in self.nodes_list if node.y_constraint]
        for i in x_constraint_nodes:
            assembled_system_matrix[i*2-2][:] = 0
        for i in y_constraint_nodes:
            assembled_system_matrix[i*2-1][:] = 0
        for i in range(len(assembled_system_matrix)):
            if assembled_system_matrix[i][i] == 0:
                assembled_system_matrix[i][i] = 1
        return assembled_system_matrix

    def calculate_displacement(self):
        system_force_vector = self.create_system_force_vector()
        final_system_matrix = self.reflect_constraint(self.assemble_system_matrixs())
        k_inverse_matrix = np.linalg.inv(final_system_matrix)
        displacment_matrix = k_inverse_matrix.dot(system_force_vector)
        return displacment_matrix
    
    def calculate_element_node_strength(self):
        displacement_matrix = self.calculate_displacement()
        node_strength_matrix_list = []
        for i in self.elements_list:
            each_displacement_matrix = displacement_matrix[[i.node1.node_number*2-2,
                                                            i.node1.node_number*2-1,
                                                            i.node2.node_number*2-2,
                                                            i.node2.node_number*2-1]]
            k_stiffness = self.create_stiffness_matrix(i)
            each_strengh_matrix = k_stiffness.dot(each_displacement_matrix)
            node_strength_matrix_list.append(each_strengh_matrix)
        return node_strength_matrix_list
    
    def calculate_reactions(self):
        node_reaction_list = np.zeros((len(self.nodes_list)*2,1))
        node_strength_matrix_list = self.calculate_element_node_strength()
        for i in self.elements_list:
            node_reaction_list[i.node1.node_number*2-2] += node_strength_matrix_list[self.elements_list.index(i)][0]
            node_reaction_list[i.node1.node_number*2-1] += node_strength_matrix_list[self.elements_list.index(i)][1]
            node_reaction_list[i.node2.node_number*2-2] += node_strength_matrix_list[self.elements_list.index(i)][2]
            node_reaction_list[i.node2.node_number*2-1] += node_strength_matrix_list[self.elements_list.index(i)][3]
        external_force = self.create_system_force_vector()
        node_reaction_list -= external_force
        return node_reaction_list
            
    def calculate_element_strength(self):
        node_strength_matrix_list = self.calculate_element_node_strength()
        element_strength_list = []
        for nodes_strength in node_strength_matrix_list:
            node1_strength = (nodes_strength[0]**2 + nodes_strength[1]**2)**(1/2)
            node2_strength = (nodes_strength[2]**2 + nodes_strength[3]**2)**(1/2)
            each_total_strength = (node1_strength + node2_strength) / 2
            element_strength_list.append(each_total_strength)
        return element_strength_list
        

if __name__ == "__main__":
    matrix = Matrix.create_stiffness_matrix(3)