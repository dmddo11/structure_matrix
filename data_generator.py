import pandas as pd
import basic_components.node_class as node_class
import basic_components.element_class as element_class
import basic_components.external_force_class as external_force_class

class Data_generator:
    def __init__(self, filepath):
        self.filepath = filepath
        
    def generate_nodes_list(self):
        data_file = pd.read_excel(self.filepath, sheet_name='node_properties')
        nodes_list = []
        for i in range(len(data_file)):
            node_data = data_file.iloc[i]
            node = node_class.Node(node_data['Node No.'],node_data['x_coordination'],node_data['y_coordination'],node_data['x_constraint'],node_data['y_constraint'])
            nodes_list.append(node)
        return nodes_list

    def generate_elements_list(self):
        data_file = pd.read_excel(self.filepath, sheet_name='element_properties')
        nodes_list = self.generate_nodes_list()
        elements_list = []
        for i in range(len(data_file)):
            element_data = data_file.iloc[i]
            element = element_class.Element(element_data['Element No.'],nodes_list[int(element_data['node1'])-1],nodes_list[int(element_data['node2'])-1],element_data['Elastic_modulus'],element_data['cross-section-area'])
            elements_list.append(element)
        return elements_list 

    def generate_external_force(self):
        data_file = pd.read_excel(self.filepath, sheet_name='external_forces')
        force_list = []
        for i in range(len(data_file)):
            force_data = data_file.iloc[i]
            node = external_force_class.External_force(force_data['Applied node num.'],force_data['x_force'],force_data['y_force'])
            force_list.append(node)
        return force_list


if __name__ == "__main__":
    #df = Data_generator("data_excel_file.xlsx")
    df = Data_generator("example_excel_file.xlsx")
    nodelist = df.generate_nodes_list()
    print("###",nodelist[2].x_coordination)

    elementlist = df.generate_elements_list()
    print(type(elementlist[0].elastic_modulus))

    external_force_list = df.generate_external_force()
    print(external_force_list[0].y_force)