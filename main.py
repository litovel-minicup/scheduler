from functools import partial
from itertools import product, combinations, permutations
from collections import deque, namedtuple
from operator import contains
from random import randint

TEAMS = range(1, 12 + 1)

TEAMS_MINIMAL_ROUND = {
    1: 5, # kostelec po 15:00
    2: 2,  # chodov po 13:00
}

RESET_ROUNDS = {12, 26}

MATCHES = list((combinations(TEAMS, 2)))


class Schedule(list):
    MATCHES_IN_ROUND = 2

    def is_team_in_last_n_rounds_including_partial_round(self, team, n=1):
        if not self:
            return False

        last = self[-n:]

        if len(last[-1]) < self.MATCHES_IN_ROUND:
            last = self[-n - 1:]

        return any(team in match for round_ in last for match in round_)

    def append_match(self, match: set):
        if not self:
            self.append([match, ])
            return
        last = self[-1]
        if len(last) < self.MATCHES_IN_ROUND:
            last.append(match)
            return
        self.append([match, ])

    def pop_match(self):
        if not self:
            raise ValueError
        last = self[-1]
        match = last.pop()
        if not last:
            self.pop()
        return match

    @property
    def rounds_count(self):
        return len(self) - (len(self[-1]) < self.MATCHES_IN_ROUND if self else 0)

    def __str__(self):
        return '\n'.join(
            '\n'.join(
                '\t'.join(map(str, (match[::-1] if randint(0, 1) else match)))
                for match in round_
            )
            for round_ in self
        )


s = Schedule()
assert not s.is_team_in_last_n_rounds_including_partial_round(5)
s.append(({1, 2}, {3, 4}))
assert s.is_team_in_last_n_rounds_including_partial_round(2)
assert not s.is_team_in_last_n_rounds_including_partial_round(5)
s.append(({5, 6}, {7, 8}))
assert s.is_team_in_last_n_rounds_including_partial_round(5)
assert not s.is_team_in_last_n_rounds_including_partial_round(2)
del s


def could_play_in_next_round(schedule: Schedule, team):
    next_round_i = schedule.rounds_count + 1
    if TEAMS_MINIMAL_ROUND.get(team, 0) >= next_round_i:
        return False
    if next_round_i in RESET_ROUNDS and not schedule.is_team_in_last_n_rounds_including_partial_round(team, 0):
        return True
    if schedule.is_team_in_last_n_rounds_including_partial_round(team):
        return False
    return True


def main():
    schedule = Schedule()
    before = None
    while MATCHES:
        match = MATCHES.pop(randint(0, len(MATCHES) - 1))
        if before == match:
            MATCHES.insert(0, schedule.pop_match())

        t1, t2 = match
        if could_play_in_next_round(schedule, t1) and could_play_in_next_round(schedule, t2):
            schedule.append_match(match)
            continue

        before = match
        MATCHES.insert(randint(0, len(MATCHES)), match)
        print(match)

    return schedule


print(main())
