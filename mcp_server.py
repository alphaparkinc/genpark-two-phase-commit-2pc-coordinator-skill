import sys
import json
from client import TwoPhaseCommitCoordinator

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "coordinate_2pc_transaction",
                        "description": "Simulate and verify distributed Two-Phase Commit (2PC) execution",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "participants": {"type": "array", "items": {"type": "string"}},
                                "failing_nodes": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["participants"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "coordinate_2pc_transaction":
            parts = args["participants"]
            fails = set(args.get("failing_nodes", []))
            plist = [TwoPhaseCommitCoordinator.Participant(p, should_fail=(p in fails)) for p in parts]
            coord = TwoPhaseCommitCoordinator(plist)
            ok, msg = coord.execute_transaction()
            states = {p.node_id: p.state for p in plist}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"success": ok, "coordinator_state": coord.coordinator_state, "participant_states": states})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
