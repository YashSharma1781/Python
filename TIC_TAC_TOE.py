import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - AI")
        self.root.geometry("400x500")
        self.root.configure(bg="#1e1e1e")

        self.board = [""] * 9
        self.user = "X"
        self.ai = "O"

        self.user_score = 0
        self.ai_score = 0

        self.score_label = tk.Label(
            root,
            text="You: 0 | AI: 0",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="white"
        )
        self.score_label.pack(pady=10)

        self.status = tk.Label(
            root,
            text="Your Turn",
            font=("Arial", 14),
            bg="#1e1e1e",
            fg="cyan"
        )
        self.status.pack()

        self.frame = tk.Frame(root, bg="#1e1e1e")
        self.frame.pack(pady=20)

        self.buttons = []

        for i in range(9):
            btn = tk.Button(
                self.frame,
                text="",
                width=6,
                height=3,
                font=("Arial", 24, "bold"),
                bg="#333333",
                fg="white",
                command=lambda i=i: self.player_move(i)
            )

            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self.buttons.append(btn)

        tk.Button(
            root,
            text="New Game",
            font=("Arial", 14),
            command=self.reset_board
        ).pack(pady=10)

    def player_move(self, index):
        if self.board[index] == "":
            self.board[index] = self.user
            self.buttons[index].config(text=self.user)

            if self.check_winner(self.user):
                self.user_score += 1
                self.update_score()
                messagebox.showinfo("Game Over", "You Win!")
                self.reset_board()
                return

            if "" not in self.board:
                messagebox.showinfo("Game Over", "Draw!")
                self.reset_board()
                return

            self.status.config(text="AI Thinking...")
            self.root.after(500, self.ai_move)

    def ai_move(self):
        best_score = -float("inf")
        best_move = None

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.ai
                score = self.minimax(self.board, 0, False)
                self.board[i] = ""

                if score > best_score:
                    best_score = score
                    best_move = i

        self.board[best_move] = self.ai
        self.buttons[best_move].config(text=self.ai)

        if self.check_winner(self.ai):
            self.ai_score += 1
            self.update_score()
            messagebox.showinfo("Game Over", "AI Wins!")
            self.reset_board()
            return

        if "" not in self.board:
            messagebox.showinfo("Game Over", "Draw!")
            self.reset_board()
            return
    
        self.status.config(text="Your Turn")

    def minimax(self, board, depth, is_maximizing):

        if self.check_winner(self.ai):
            return 1
        

        if self.check_winner(self.user):
            return -1

        if "" not in board:
            return 0

        if is_maximizing:
            best_score = -float("inf")

            for i in range(9):
                if board[i] == "":
                    board[i] = self.ai
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)

            return best_score

        else:
            best_score = float("inf")

            for i in range(9):
                if board[i] == "":
                    board[i] = self.user
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)

            return best_score

    def check_winner(self, player):
        wins = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]

        for combo in wins:
            if all(self.board[i] == player for i in combo):
                return True

        return False

    def update_score(self):
        self.score_label.config(
            text=f"You: {self.user_score} | AI: {self.ai_score}"
        )

    def reset_board(self):
        self.board = [""] * 9

        for btn in self.buttons:
            btn.config(text="")

        self.status.config(text="Your Turn")


root = tk.Tk()
game = TicTacToe(root)
root.mainloop()