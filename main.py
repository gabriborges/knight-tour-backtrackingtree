import sys

solutions = []

class Node:
    def __init__(self, position, board):
        self.position = position
        self.board = board
        self.next = None
        self.previous = None
        self.moves_left = []

    def create_child(self, new_position):
        new_board = [row[:] for row in self.board]
        new_board[new_position[0]][new_position[1]] = 0
        return Node(new_position, new_board)
    
    def check_board(self):
        for row in self.board:
            if 1 in row:
                return False
        return True

    def possible_move(self, move):
        new_x, new_y = self.position[0] + move[0], self.position[1] + move[1]
        if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board[0]) and self.board[new_x][new_y] == 1:
            return True, self.create_child([new_x, new_y])
        return False, self.position

    def print_nodes(self):
        node = self
        node_number = len(node.board)**2
        while node is not None:
            solutions.append(node.position)
            print(f'Node: {node.position}, Node number: {node_number}')
            print_board(node.board)
            print()
            node_number -= 1
            node = node.previous
    
    def create_numbered_board(self, solution):
        numbered_board = [row[:] for row in self.board]
        size = len(numbered_board)**2
        for position in solution:
            x, y = position
            numbered_board[x][y] = size
            size -= 1
        return numbered_board

#o tour é recursivo, e a cada chamada ele vai criando um novo nó, que é o próximo movimento do cavalo
#se a lista de movimentos de um cavalo se esgorar, ele volta para o nó anterior e tenta outros movimento do cavalo anterior
def tour(node, knight_moves):

    #se um hora o nó for Nulo, quer dizer que todos os movimentos de todos os cavalos foram testados
    #assim o nó anterior do nó raiz será None, então o programa termina
    if node is None:
        return False
    #se o tabuleiro estiver completo, o programa termina
    elif node.check_board():
        print("-------------------------------------------------------------------------")
        node.print_nodes()
        print("Solution found!!!!!!!!!!!!!!!!!!!!!! You can chek the steps right above or bellow.")
        print(f"Solution: {solutions} , Root--> {solutions[-1]}" )
        print("\nNumbered board: ")
        print_board(node.create_numbered_board(solutions)) 
        print("--------------------------------------------------------------------------")
        sys.exit()
    #se a lista de movimentos de um cavalo se esgotar, ele volta para o nó anterior e tenta outro movimento com o cavalo anterior
    elif node.moves_left == [] and not node.check_board():
        node = node.previous
        node.next = None
        tour(node, knight_moves)
    #criação dos nós filhos
    else:
        moves_left_copy = node.moves_left.copy()
        for i in range(len(moves_left_copy)):
            is_possible, new_node = node.possible_move(moves_left_copy[i])
            if is_possible:
                new_node.moves_left = knight_moves.copy()
                new_node.previous = node
                node.moves_left = node.moves_left[i+1:].copy() 
                tour(new_node, knight_moves)
                return
        
        if node.previous is not None:
            tour(node.previous, knight_moves)
    
    return False

def print_board(board):
    for row in board:
        print(row)

if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    size = 5
    board = [[1 for _ in range(size)] for _ in range(size)]
    knight_moves = [[2, 1], [2, -1], [-2, 1],
                    [-2, -1], [1, 2], [-1, 2], [1, -2], [-1, -2]]
    
    #itera sobre todas as posições do tabuleiro, com cada umas das posições do tabuleiro sendo a raiz da árvore
    for i in range(size):
        for j in range(size):
            try:
                aux_board = [row[:] for row in board]
                root_tree = Node([i, j], aux_board)
                root_tree.moves_left = knight_moves
                root_tree.board[i][j] = 0
                solutions = []
                print("\nCurrent Root:", root_tree.position)
                print_board(root_tree.board)
                print("Searching for a solution...")
                if tour(root_tree, knight_moves):
                    pass
                sys.exit()
            except:
                pass    
    print("\nEnd of search.")