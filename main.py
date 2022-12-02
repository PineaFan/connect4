import math as maths
import msvcrt


class Player:
    def __init__(self, name: str, symbol: str, score: int = 0) -> None:
        self.name = name
        self.score = score
        self.symbol = symbol

    def __str__(self) -> str:
        return self.symbol

    def display_name(self) -> str:
        return f"{self.name} ({self.score})"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, Player):
            return False
        return self.name == other.name

    def __bool__(self):
        return True

class NoPlayer(Player):
    def __init__(self) -> None:
        super().__init__(symbol=" ", name="null", score=-1)

    def __bool__(self) -> bool:
        return False


class Connect4:
    def __init__(self,
            players: list[Player],
            height: int = 6,
            width: int = 7
    ) -> None:

        self.board = [([NoPlayer()] * width) for _ in range(height)]
        self.players = players
        self.turn = 0
        self.width = width
        self.height = height
        self.selected_column = width // 2
        self.last_played = [None, None]

    def _pad(self, s, l):
        return f"{str(s):^{l}}"

    def _is_column_full(self, column: int) -> bool:
        return self.board[column][-1] != NoPlayer()

    def _colour_coded_column(self, col, mc):
        code = ""
        if col == self.selected_column:
            if self._is_column_full(col):
                code = "\x1b[31m"
            else:
                code = "\x1b[32m"
        return f"{code}{self._pad(col + 1, mc)}\033[0m"

    def __str__(self) -> str:
        mr = maths.ceil(maths.log(self.width + 1, 10))  # Max rows to show a number (width)
        mc = maths.ceil(maths.log(self.height + 1, 10))  # Max columns to show a number (height)
        horizontal = "─" * (mc + 2)  # Define a horizontal line
        # Top row
        out = "┌" + (f"{horizontal}┬" * (self.height + 1))[:-1] + "┐\n"
        # For each row
        for row in range(self.width - 1, -1, -1):
            # Print the row number, then the player in that position
            out += f"│ {self._pad(row + 1, mr)} │ {' │ '.join([self._pad(self.board[col][row], mc) for col in range(self.height)])} │\n"
        # Print the middle line above the column numbers
        out += "├" + "┼".join([horizontal] * (self.height + 1)) + "┤\n"
        # Print the column numbers, in the colour they need to be highlighted in
        out += f"│ {self._pad(self.players[self.turn], mc)} │ " + " │ ".join([
            self._colour_coded_column(col, mc) for col in range(self.height)
        ]) + " │\n"
        # Print the bottom line
        out += "└" + (f"{horizontal}┴" * (self.height + 1))[:-1] + "┘\n"
        return out

    def _wait_for_character_input(self, validCharacters: list[str]) -> str:
        # Don't block ctrl c, z and y
        validCharacters += ["\x03", "\x1a", "\x19"]
        while True:
            char = str(msvcrt.getch().decode("utf-8"))
            if char in validCharacters:
                if char == "\x03":
                    raise KeyboardInterrupt
                elif char == "\r":
                    return "enter"
                return char

    def _check(self, x: int | None, y: int | None) -> int:
        if x and y:
            # Check for a diagonal line through x, y

            upRightStarts = []
            upLeftStarts = []
            for n in range(-3, 1):  # Check for a diagonal line through x, y, from the bottom left to the square itself
                if x - n < 0 or x + n > self.width or \
                   y - n < 0 or y + n > self.height:
                    continue
                upRightStarts.append((x - n, y - n))
                upLeftStarts.append((x + n, y - n))
            
        if x:
            # Check for the longest line in column x
            currentLongest = [NoPlayer(), 0]
            currentTotal = [None, 0]
            for y in range(self.height):
                if self.board[y][x] == currentTotal[0]:
                    currentTotal[1] += 1
                else:
                    currentTotal = [self.board[y][x], 1]
                if currentTotal[1] > currentLongest[1]:
                    currentLongest = currentTotal
            if currentLongest[1] >= 4:
                return currentLongest[0]
        if y:
            # Check for the longest line in row y
            currentLongest = [NoPlayer(), 0]
            currentTotal = [None, 0]
            for x in range(self.width):
                print(x, y, len(self.board), len(self.board[0]))
                if self.board[y][x] == currentTotal[0]:
                    currentTotal[1] += 1
                else:
                    currentTotal = [self.board[y][x], 1]
                if currentTotal[1] > currentLongest[1]:
                    currentLongest = currentTotal
            if currentLongest[1] >= 4:
                return currentLongest[0]

    def _get_winner(self) -> Player:
        if self.last_played == [None, None]:
            return NoPlayer()
        # Check for a vertical line in the last played column
        columnWinner = self._check(None, self.last_played[0])
        rowWinner = self._check(self.last_played[1], None)
        if columnWinner or rowWinner:
            return columnWinner or rowWinner
        
        return NoPlayer()


    def play_turn(self):
        columnSelected = False
        while not columnSelected:
            print(game)
            char = self._wait_for_character_input(["K", "M", "\r"])
            if char == "K":
                self.selected_column = max(0, self.selected_column - 1)
            elif char == "M":
                self.selected_column = min(self.width, self.selected_column + 1)
            elif char == "enter":
                if not self._is_column_full(self.selected_column):
                    columnSelected = True
        # Find the first empty space in the column
        for row in range(self.height):
            if self.board[self.selected_column][row] == NoPlayer():
                self.board[self.selected_column][row] = self.players[self.turn]
                self.last_played = [self.selected_column, row]
                break
        self.turn = (self.turn + 1) % len(self.players)

    def play(self):
        while not self._get_winner():
            self.play_turn()
        print(self._get_winner(), "wins!")


game = Connect4([
    Player("Player 1", "X"), Player("Player 2", "O")
], 7, 6)
game.play()
