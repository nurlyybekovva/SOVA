def evaluate(events: list[dict]) -> list[dict]:
    """Turn ML events into violations. TODO: load rules/kz_compliance_rules.json
    from participant #1 and match event types against verified rules."""
    return [
        {
            "type": "possible_cash_handling_violation",
            "timecode_sec": e["evidence_timestamp"],
            "description": e["description"],
        }
        for e in events
    ]