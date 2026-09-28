from client import TwoPhaseCommitCoordinator

p1 = TwoPhaseCommitCoordinator.Participant("shard-1", should_fail=False)
p2 = TwoPhaseCommitCoordinator.Participant("shard-2", should_fail=False)
coord = TwoPhaseCommitCoordinator([p1, p2])

ok, msg = coord.execute_transaction()
print(f"Transaction Result: {ok} -> {msg}, State: {coord.coordinator_state}")
