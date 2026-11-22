# Donation State Transitions

Define allowed transitions between draft, published, matched, assigned, picked up, delivered, expired, and cancelled states.

Reject transitions that skip required checks. For example, a donation should not be marked delivered before pickup is confirmed. Record the actor, timestamp, and reason for each transition.