from solution import MDProblem

if __name__ == "__main__":
    fh=open("problem.txt")
    problem=MDProblem(fh)
    problem.toString()
    