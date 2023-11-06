import matrix

class Main:
    def __init__(self, filepath):
        self.filepath = filepath

    def operate_main(self):
        solve_matrix = matrix.Matrix(self.filepath)
        return solve_matrix.calculate_displacement(),solve_matrix.calculate_element_strength(),solve_matrix.calculate_reactions()

if __name__ == "__main__":
    filepath = "prob1.xlsx"
    solving_class = Main(filepath)
    out_put1, out_put2, out_put3= solving_class.operate_main()
    print(out_put1)
    print(out_put2)
    print(out_put3)