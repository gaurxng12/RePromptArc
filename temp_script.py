class NQueensOptimized:
    def __init__(self, n):
        self.n = n
        self.solutions = []

    def solve(self):
        """Solve the N-Queens problem and store all solutions."""
        stack = [(0, set(), set(), set())]
        while stack:
            row, cols, diag1, diag2 = stack.pop()

            if row == self.n:
                self.reconstruct_solution(cols)
                continue

            for col in range(self.n):
                if (col in cols) or ((row - col) in diag1) or ((row + col) in diag2):
                    continue

                new_cols = cols | {col}
                new_diag1 = diag1 | {row - col}
                new_diag2 = diag2 | {row + col}
                stack.append((row + 1, new_cols, new_diag1, new_diag2))

        return self.solutions

    def reconstruct_solution(self, cols):
        """Reconstruct the board solution from the given columns."""
        solution = []
        for row in range(self.n):
            for col in cols:
                if len(solution) == row:
                    solution.append(col)
                    break
        self.solutions.append(solution)

    def solve_memory_efficient(self):
        """Solve the N-Queens problem and yield each solution one at a time."""
        stack = [(0, set(), set(), set())]
        while stack:
            row, cols, diag1, diag2 = stack.pop()

            if row == self.n:
                yield self.reconstruct_yield(cols)
                continue

            for col in range(self.n):
                if (col in cols) or ((row - col) in diag1) or ((row + col) in diag2):
                    continue

                new_cols = cols | {col}
                new_diag1 = diag1 | {row - col}
                new_diag2 = diag2 | {row + col}
                stack.append((row + 1, new_cols, new_diag1, new_diag2))

    def reconstruct_yield(self, cols):
        """Reconstruct the board solution for yielding."""
        return [col for col in sorted(cols)]

    @staticmethod
    def print_solution(solution):
        """Print the solution in a readable format."""
        n = len(solution)
        board = [['.' for _ in range(n)] for _ in range(n)]
        for row, col in enumerate(solution):
            board[row][col] = 'Q'

        for line in board:
            print(' '.join(line))
        print()

def benchmark(n):
    print(f"Benchmarking for n={n}")

    # Standard solve method
    solver = NQueensOptimized(n)
    solutions = solver.solve()
    print(f"Total solutions found (standard): {len(solutions)}")

    if solutions:
        print("First solution (standard):")
        solver.print_solution(solutions[0])

    # Memory efficient solve method
    solver = NQueensOptimized(n)
    solutions_gen = solver.solve_memory_efficient()
    solutions_count = sum(1 for _ in solutions_gen)
    solutions_gen = solver.solve_memory_efficient()  # Recreate generator to get the 1st solution again

    print(f"Total solutions found (memory-efficient): {solutions_count}")

    first_solution = next(solutions_gen)
    print("First solution (memory-efficient):")
    solver.print_solution(first_solution)

if __name__ == "__main__":
    benchmark(8)
