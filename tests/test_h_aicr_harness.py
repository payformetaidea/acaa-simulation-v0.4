from experimental.h_aicr_harness import generate_interactions, user_disjoint_split, GROUPS


def test_generation_cardinality():
    rows = generate_interactions(20)
    assert len(rows) == 140
    assert {r.group for r in rows} == set(GROUPS)


def test_user_disjoint_split():
    rows = generate_interactions(20)
    train, test = user_disjoint_split(rows)
    assert {r.user_id for r in train}.isdisjoint({r.user_id for r in test})
    assert len(train) + len(test) == len(rows)
