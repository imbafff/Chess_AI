class Figure:
    def __init__(self, name, team, enemies):
        self.name = name
        self.point_x = 0
        self.point_z = 0
        self.team = team
        self.checking = ()
        self.enemies = enemies

    def fire_lines(self):
        fire_lines = []
        for sign_x, sign_z in self.checking:
            if self.point_x + sign_x < 0 or self.point_z + sign_z < 0 or \
                    self.point_x + sign_x > 7 or self.point_z + sign_z > 7:
                continue
            fire_lines.append((self.point_x + sign_x, self.point_z + sign_z))
        return fire_lines

    def moving(self):
        team = tuple((i.point_x, i.point_z) for i in self.team)
        return list(filter(lambda i: i not in team, self.fire_lines()))


class King(Figure):
    def __init__(self, name, team, enemies):
        super().__init__(name, team, enemies)
        self.checking = ((1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1), (0, 1), (1, 1), (-1, 1))

    def moving(self):
        enemy_fire = []
        team = list((i.point_x, i.point_z) for i in self.team)
        for i in self.enemies:
            enemy_fire += i.fire_lines()
        return list(filter(lambda x: x not in enemy_fire and x not in team, self.fire_lines()))


class Knight(Figure):
    def __init__(self, name, team, enemies):
        super().__init__(name, team, enemies)
        self.checking = ((-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2))


class Pawn(Figure):
    def __init__(self, name, team, enemies):
        super().__init__(name, team, enemies)
        self.checking = ((-1, -1), (-1, 1))

    def fire_lines(self):
        if self.point_x == 7 or self.point_x == 0:
            king = tuple(filter(lambda i: isinstance(i, King), self.enemies))[0]
            self.checking = ((-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2))
            knight_fl = Knight.fire_lines(self)
            self.checking = ((-1, -1), (-1, 1))
            if (king.point_x, king.point_z) in knight_fl:
                return knight_fl
            return Queen.fire_lines(self)
        return super().fire_lines()

    def moving(self):
        moving_lines = []
        if (turn_num == 1 and self.name == 'P') or (turn_num == 0 and self.name == 'p'):
            if matrix[self.point_x - 1][self.point_z] == '.':
                moving_lines.append((self.point_x - 1, self.point_z))
            if self.point_x == 1 and matrix[self.point_x - 2][self.point_z] == '.':
                moving_lines.append((self.point_x - 2, self.point_z))
            for i in ((-1, 1), (-1, -1)):
                try:
                    if matrix[self.point_x + i[0]][self.point_z + i[1]] in self.enemies:
                        moving_lines.append((self.point_x + i[0], self.point_z + i[1]))
                except IndexError:
                    continue
        else:
            if matrix[self.point_x + 1][self.point_z] == '.':
                moving_lines.append((self.point_x + 1, self.point_z))
            if self.point_x == 6 and matrix[self.point_x + 2][self.point_z] == '.':
                moving_lines.append((self.point_x + 2, self.point_z))
            for i in ((1, 1), (1, -1)):
                try:
                    if matrix[self.point_x + i[0]][self.point_z + i[1]] in self.enemies:
                        moving_lines.append((self.point_x + i[0], self.point_z + i[1]))
                except IndexError:
                    continue
        return moving_lines


class Rook(Figure):
    def __init__(self, name, team, enemies):
        super().__init__(name, team, enemies)

    def fire_lines(self):
        fire_lines = []

        for xx in range(self.point_x + 1, 8):
            cell = matrix[xx][self.point_z]
            if cell in self.enemies:
                fire_lines.append((xx, self.point_z))
                if isinstance(cell, King):
                    continue
                break
            elif cell == '.':
                fire_lines.append((xx, self.point_z))
            else:
                fire_lines.append((xx, self.point_z))
                break

        for x in range(self.point_x - 1, -1, -1):
            cell = matrix[x][self.point_z]
            if cell in self.enemies:
                fire_lines.append((x, self.point_z))
                if isinstance(cell, King):
                    continue
                break
            elif cell == '.':
                fire_lines.append((x, self.point_z))
            else:
                fire_lines.append((x, self.point_z))
                break

        for zz in range(self.point_z + 1, 8):
            cell = matrix[self.point_x][zz]
            if cell in self.enemies:
                fire_lines.append((self.point_x, zz))
                if isinstance(cell, King):
                    continue
                break
            elif cell == '.':
                fire_lines.append((self.point_x, zz))
            else:
                fire_lines.append((self.point_x, zz))
                break

        for z in range(self.point_z - 1, -1, -1):
            cell = matrix[self.point_x][z]
            if cell in self.enemies:
                fire_lines.append((self.point_x, z))
                if isinstance(cell, King):
                    continue
                break
            elif cell == '.':
                fire_lines.append((self.point_x, z))
            else:
                fire_lines.append((self.point_x, z))
                break
        return fire_lines


class Bishop(Figure):
    def fire_lines(self):
        fire_lines = []
        for top_left in range(1, min(self.point_x, self.point_z) + 1):
            cell = matrix[self.point_x - top_left][self.point_z - top_left]
            if cell in self.enemies:
                fire_lines.append((self.point_x - top_left, self.point_z - top_left))
                if isinstance(cell, King):
                    continue
                break
            elif cell == '.':
                fire_lines.append((self.point_x - top_left, self.point_z - top_left))
                continue
            else:
                fire_lines.append((self.point_x - top_left, self.point_z - top_left))
                break

        for bottom_left in range(1, min(7 - self.point_x, self.point_z) + 1):
            try:
                cell = matrix[self.point_x + bottom_left][self.point_z - bottom_left]
            except IndexError:
                continue
            if cell in self.enemies:
                fire_lines.append((self.point_x + bottom_left, self.point_z - bottom_left))
                if isinstance(cell, King):
                    continue
                break
            elif cell == '.':
                fire_lines.append((self.point_x + bottom_left, self.point_z - bottom_left))
                continue
            else:
                fire_lines.append((self.point_x + bottom_left, self.point_z - bottom_left))
                break

        for top_left in range(1, min(8 - self.point_x, 8 - self.point_z)):
            cell = matrix[self.point_x + top_left][self.point_z + top_left]
            if cell in self.enemies:
                fire_lines.append((self.point_x + top_left, self.point_z + top_left))
                if isinstance(cell, King):
                    continue
                break
            elif cell == '.':
                fire_lines.append((self.point_x + top_left, self.point_z + top_left))
                continue
            else:
                fire_lines.append((self.point_x + top_left, self.point_z + top_left))
                break

        for top_left in range(1, min(self.point_x, 7 - self.point_z) + 1):
            cell = matrix[self.point_x - top_left][self.point_z + top_left]
            if cell in self.enemies:
                fire_lines.append((self.point_x - top_left, self.point_z + top_left))
                if isinstance(cell, King):
                    continue
                break
            elif cell == '.':
                fire_lines.append((self.point_x - top_left, self.point_z + top_left))
                continue
            else:
                fire_lines.append((self.point_x - top_left, self.point_z + top_left))
                break
        return fire_lines


class Queen(Figure):
    def fire_lines(self):
        return list(set(King.fire_lines(self) + Bishop.fire_lines(self) + Rook.fire_lines(self)))


with open('input.txt', 'r') as file:
    matrix = []
    turn_num = int(file.readline())
    for line in file:
        matrix.append(list(line.rstrip()))

white_team = []
black_team = []

figures = {'N': Knight, 'R': Rook, 'K': King, 'Q': Queen, 'P': Pawn, 'B': Bishop}
for x, line in enumerate(matrix):
    for z, figure in enumerate(line):
        if figure == '.':
            continue
        if figure.isupper():
            figure = figures[figure](figure, white_team, black_team)
            white_team.append(figure)
        else:
            figure = figures[figure.upper()](figure, black_team, white_team)
            black_team.append(figure)
        matrix[x][z] = figure
        figure.point_x, figure.point_z = x, z

moves = []
if turn_num == 0:
    turn = (black_team, white_team)
else:
    turn = (white_team, black_team)
for figure in turn[0]:
    for move in figure.moving():
        team_king = tuple(filter(lambda i: isinstance(i, King), turn[0]))[0]
        reserve_points = (figure.point_x, figure.point_z)
        reserve_figure = matrix[move[0]][move[1]]
        if reserve_figure != '.':
            turn[1].remove(reserve_figure)
        matrix[figure.point_x][figure.point_z] = '.'
        matrix[move[0]][move[1]] = figure
        figure.point_x, figure.point_z = move
        king = tuple(filter(lambda i: isinstance(i, King), turn[1]))[0]
        fire_lines = []
        for fire in turn[1]:
            fire_lines += fire.fire_lines()
        fire_lines_team = []
        for fire in turn[0]:
            fire_lines_team += fire.fire_lines()
        if king.moving() == list() and ((team_king.point_x, team_king.point_z) not in fire_lines) and ((king.point_x, king.point_z) in fire_lines_team):
            for figure_enemy in turn[1]:
                for move_enemy in figure_enemy.moving():
                    reserve_points_enemy = (figure_enemy.point_x, figure_enemy.point_z)
                    reserve_figure_enemy = matrix[move_enemy[0]][move_enemy[1]]
                    if reserve_figure_enemy != '.':
                        turn[0].remove(reserve_figure_enemy)
                    matrix[figure_enemy.point_x][figure_enemy.point_z] = '.'
                    matrix[move_enemy[0]][move_enemy[1]] = figure_enemy
                    figure_enemy.point_x, figure_enemy.point_z = move_enemy
                    fire_lines = []
                    for fire in turn[0]:
                        fire_lines += fire.fire_lines()
                    if (king.point_x, king.point_z) in fire_lines:
                        matrix[figure_enemy.point_x][figure_enemy.point_z] = reserve_figure_enemy
                        matrix[reserve_points_enemy[0]][reserve_points_enemy[1]] = figure_enemy
                        if reserve_figure_enemy != '.':
                            turn[0].append(reserve_figure_enemy)
                        figure_enemy.point_x, figure_enemy.point_z = reserve_points_enemy
                    else:
                        matrix[figure_enemy.point_x][figure_enemy.point_z] = reserve_figure_enemy
                        matrix[reserve_points_enemy[0]][reserve_points_enemy[1]] = figure_enemy
                        if reserve_figure_enemy != '.':
                            turn[0].append(reserve_figure_enemy)
                        figure_enemy.point_x, figure_enemy.point_z = reserve_points_enemy
                        break
                else:
                    continue
                break
            else:
                with open('output.txt', 'w') as f:
                    f.write(str('ABCDEFGH'[reserve_points[1]]) + str(8 - reserve_points[0]) + ' ')
                    f.write(str('ABCDEFGH'[figure.point_z]) + str(8 - figure.point_x))
                break
        matrix[figure.point_x][figure.point_z] = reserve_figure
        matrix[reserve_points[0]][reserve_points[1]] = figure
        if reserve_figure != '.':
            turn[1].append(reserve_figure)
        figure.point_x, figure.point_z = reserve_points
    else:
        continue
    break