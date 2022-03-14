
class King(Piece):

    def is_valid_pos(self, pos):

        if pos.x < 3 or pos.x > 5:
            return False

        if (self.side == ChessSide.RED) and pos.y > 2:
            return False

        if (self.side == ChessSide.BLACK) and pos.y < 7:
            return False

        return True

    def is_valid_move(self, pos):

        # 先检查王吃王
        k2 = self.board.get_king(ChessSide.next_side(self.side))

        if ((k2.x, k2.y) == pos()) and self.x == k2.x:
            count = self.board.count_y_line_in(self.x, self.y, k2.y)
            if count == 0:
                return True

        if not self.is_valid_pos(pos):
            return False

        diff = pos.abs_diff(Pos(self.x, self.y))

        return True if ((diff[0] + diff[1]) == 1) else False

    def create_moves(self):
        poss = [Pos(self.x + 1, self.y), Pos(self.x - 1, self.y), Pos(self.x, self.y + 1), Pos(self.x, self.y - 1)]
        curr_pos = Pos(self.x, self.y)
        moves = [(curr_pos, to_pos) for to_pos in poss]
        return filter(self.board.is_valid_move_t, moves)


# -----------------------------------------------------#
# 士
class Advisor(Piece):

    def is_valid_pos(self, pos):
        return True if pos() in advisor_pos[self.side] else False

    def is_valid_move(self, pos):

        if not self.is_valid_pos(pos):
            return False

        if Pos(self.x, self.y).abs_diff(pos) == (1, 1):
            return True

        return False

    def create_moves(self):
        poss = [Pos(self.x + 1, self.y + 1), Pos(self.x + 1, self.y - 1), Pos(self.x - 1, self.y + 1),
                Pos(self.x - 1, self.y - 1)]
        curr_pos = Pos(self.x, self.y)
        moves = [(curr_pos, to_pos) for to_pos in poss]
        return filter(self.board.is_valid_move_t, moves)


# -----------------------------------------------------#
# 象
class Bishop(Piece):
    def is_valid_pos(self, pos):
        return True if pos() in bishop_pos[self.side] else False

    def is_valid_move(self, pos):

        if Pos(self.x, self.y).abs_diff(pos) != (2, 2):
            return False

        # 塞象眼检查
        if self.board.get_fench(Pos(self.x, self.y).middle(pos)) != None:
            return False

        return True

    def create_moves(self):
        poss = [Pos(self.x + 2, self.y + 2), Pos(self.x + 2, self.y - 2), Pos(self.x - 2, self.y + 2),
                Pos(self.x - 2, self.y - 2)]
        curr_pos = Pos(self.x, self.y)
        moves = [(curr_pos, to_pos) for to_pos in poss]
        return filter(self.board.is_valid_move_t, moves)


# -----------------------------------------------------#
# 马
class Knight(Piece):
    def is_valid_move(self, pos):

        if (abs(self.x - pos.x) == 2) and (abs(self.y - pos.y) == 1):

            m_x = (self.x + pos.x) / 2
            m_y = self.y

            # 别马腿检查
            if self.board.get_fench(Pos(m_x, m_y)) == None:
                return True

        if (abs(self.x - pos.x) == 1) and (abs(self.y - pos.y) == 2):

            m_x = self.x
            m_y = (self.y + pos.y) / 2

            # 别马腿检查
            if self.board.get_fench(Pos(m_x, m_y)) == None:
                return True

        return False

    def create_moves(self):
        poss = [Pos(self.x + 1, self.y + 2), Pos(self.x + 1, self.y - 2),
                Pos(self.x - 1, self.y + 2), Pos(self.x - 1, self.y - 2),
                Pos(self.x + 2, self.y + 1), Pos(self.x + 2, self.y - 1),
                Pos(self.x - 2, self.y + 1), Pos(self.x - 2, self.y - 1),
                ]
        curr_pos = Pos(self.x, self.y)
        moves = [(curr_pos, to_pos) for to_pos in poss]
        return filter(self.board.is_valid_move_t, moves)


# -----------------------------------------------------#
# 车
class Rook(Piece):
    def is_valid_move(self, pos):
        if self.x != pos.x:
            # 斜向移动是非法的
            if self.y != pos.y:
                return False

            # 水平移动
            if self.board.count_x_line_in(self.y, self.x, pos.x) == 0:
                return True

        else:
            # 垂直移动
            if self.board.count_y_line_in(self.x, self.y, pos.y) == 0:
                return True

        return False

    def create_moves(self):
        moves = []
        curr_pos = Pos(self.x, self.y)
        for x in range(9):
            for y in range(10):
                if self.x == x and self.y == y:
                    continue
                moves.append((curr_pos, Pos(x, y)))
        return filter(self.board.is_valid_move_t, moves)


# -----------------------------------------------------#
# 炮
class Cannon(Piece):
    def is_valid_move(self, pos):

        if self.x != pos.x:
            # 斜向移动是非法的
            if self.y != pos.y:
                return False

            # 水平移动
            count = self.board.count_x_line_in(self.y, self.x, pos.x)
            if (count == 0) and (self.board.get_fench(pos) == None):
                return True
            if (count == 1) and (self.board.get_fench(pos) != None):
                return True
        else:
            # 垂直移动
            count = self.board.count_y_line_in(self.x, self.y, pos.y)
            if (count == 0) and (self.board.get_fench(pos) == None):
                return True
            if (count == 1) and (self.board.get_fench(pos) != None):
                return True

        return False

    def create_moves(self):
        moves = []
        curr_pos = Pos(self.x, self.y)
        for x in range(9):
            for y in range(10):
                if self.x == x and self.y == y:
                    continue
                moves.append((curr_pos, Pos(x, y)))
        return filter(self.board.is_valid_move_t, moves)


# -----------------------------------------------------#
# 兵/卒
class Pawn(Piece):
    def is_valid_pos(self, pos):

        if (self.side == ChessSide.RED) and pos.y < 3:
            return False

        if (self.side == ChessSide.BLACK) and pos.y > 6:
            return False

        return True

    def is_valid_move(self, pos):

        not_over_river_step = ((0, 1), (0, -1))
        over_river_step = (((-1, 0), (1, 0), (0, 1)), ((-1, 0), (1, 0), (0, -1)))

        step = (pos.x - self.x, pos.y - self.y)

        over_river = self.is_over_river()

        if (not over_river) and (step == not_over_river_step[self.side]):
            return True

        if over_river and (step in over_river_step[self.side]):
            return True

        return False

    def is_over_river(self):
        if (self.side == ChessSide.RED) and (self.y > 4):
            return True

        if (self.side == ChessSide.BLACK) and (self.y < 5):
            return True

        return False

    def create_moves(self):
        moves = []
        curr_pos = Pos(self.x, self.y)
        for x in range(9):
            for y in range(10):
                if self.x == x and self.y == y:
                    continue
                moves.append((curr_pos, Pos(x, y)))
        return filter(self.board.is_valid_move_t, moves)