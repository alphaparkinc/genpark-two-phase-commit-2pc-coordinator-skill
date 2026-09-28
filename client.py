"""Two-Phase Commit (2PC) Distributed Coordinator Engine.
100% Python Standard Library.
"""

class TwoPhaseCommitCoordinator:
    """Two-Phase Commit (2PC) atomic transaction coordinator."""
    class Participant:
        def __init__(self, node_id, should_fail=False):
            self.node_id = node_id
            self.should_fail = should_fail
            self.state = "INIT"

        def prepare(self):
            if self.should_fail:
                self.state = "ABORTED"
                return False
            self.state = "PREPARED"
            return True

        def commit(self):
            self.state = "COMMITTED"
            return True

        def abort(self):
            self.state = "ABORTED"
            return True

    def __init__(self, participants):
        self.participants = participants
        self.coordinator_state = "INIT"

    def execute_transaction(self):
        votes = [p.prepare() for p in self.participants]
        if all(votes):
            self.coordinator_state = "GLOBAL_COMMIT"
            for p in self.participants:
                p.commit()
            return True, "TRANSACTION_COMMITTED"
        else:
            self.coordinator_state = "GLOBAL_ABORT"
            for p in self.participants:
                p.abort()
            return False, "TRANSACTION_ABORTED"
