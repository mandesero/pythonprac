import cowsay as cs
from io import StringIO

cust_mstr = cs.read_dot_cow(StringIO("""
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\'--'//__
         (((""`  `"")))
EOC
"""))




class Game:
    def __init__(self):
        self.field = [[None] * 10 for i in range(10)]
        self.pos = [0, 0]

    def addmon(self, x, y, name, message):
        flag = self.field[x][y] is None
        self.field[x][y] = message, name
        print(f"Added monster {name} to ({x}, {y}) saying {message}")
        if not flag:
            print("Replaced the old monster")

    def move(self, way):

        match way:
            case "up":
                self.pos[1] = (self.pos[1] + 1) % 10
            case "down":
                self.pos[1] = (self.pos[1] - 1) % 10
            case "right":
                self.pos[0] = (self.pos[0] + 1) % 10
            case "left":
                self.pos[0] = (self.pos[0] - 1) % 10

        print(f"Moved to ({self.pos[0]}, {self.pos[1]})")
        self.encounter(self.pos[0], self.pos[1])

    def encounter(self, x, y):
        if monster := self.field[x][y]:
            if monster[1] == "jgsbat":
                print(cs.cowthink(message=monster[0], cowfile=cust_mstr))
            else:
                print(cs.cowsay(message=monster[0], cow=monster[1]))

    def start(self):
        try:
            while True:
                command = input()
                match command.split():
                    case [way]:
                        self.move(way)
                    case "addmon", name, x, y, *message:
                        if name in cs.list_cows() + ['jgsbat']:
                            self.addmon(int(x), int(y), name, " ".join(list(message)))
                        else:
                            print("Cannot add unknown monster")
                    case _:
                        break
        except EOFError:
            pass


def main():
    print("<<< Welcome to Python-MUD 0.1 >>>")
    Game().start()


if __name__ == "__main__":
    main()
