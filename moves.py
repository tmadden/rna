import json
import pandas as pd


def replay_moves(moves):
    """A generator that will replay the moves from an Eterna user session.
       Each item yielded by this generator is the full RNA sequence at that
       point in the user's progression towards a solution."""
    state = list(moves['begin_from'])
    yield "".join(state)
    for stroke in moves['moves']:
        for element in stroke:
            if 'base' in element:
                state[element['pos'] - 1] = element['base']
            else:
                seq = element['sequence']
                state[:len(seq)] = list(seq)
        yield "".join(state)


def moves_are_valid(json_moves):
    try:
        moves = json.loads(json_moves)
    except:
        # The JSON is invalid (happens for 9 records in the whole dataset).
        return False
    try:
        for _ in replay_moves(moves):
            pass
    except:
        # Processing failed. It seems this tends to happen because of moves
        # that reference positions that are past the end of the sequence.
        # The SentRNA repository also mentions that "For some reason, a lot
        # of the Lab puzzles have solutions that don't match the length of
        # the dot-bracket so they can't be used...", so this could be
        # related. It happens for a little over 1% of the records, so I'm
        # just ignoring these errors as well.
        return False
    return True


df = pd.read_csv(
    "EternaBrain/rna-prediction/movesets/move-set-11-14-2016.txt", sep='\t')

json_moves = df.loc[18]['move_set']
assert moves_are_valid(json_moves)

moves = json.loads(json_moves)
for seq in replay_moves(moves):
    print(seq)
