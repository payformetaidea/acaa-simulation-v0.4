"""Fail-closed leakage checks for analytical units and temporal ordering."""

def assert_disjoint(*sets):
    seen=set()
    for current in sets:
        overlap=seen.intersection(current)
        if overlap:
            raise RuntimeError("DATA_LEAKAGE_DETECTED")
        seen.update(current)

def assert_user_disjoint(train_users, val_users, test_users):
    assert_disjoint(set(train_users), set(val_users), set(test_users))

def assert_temporal_disjoint(train_end, val_start, val_end, test_start):
    if not (train_end < val_start and val_end < test_start):
        raise RuntimeError("TEMPORAL_LEAKAGE_DETECTED")

def assert_single_cohort(unit_to_groups):
    for unit, groups in unit_to_groups.items():
        if len(set(groups)) != 1:
            raise RuntimeError("COHORT_CONTAMINATION_DETECTED")
