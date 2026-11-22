# Donation Status Model

Suggested lifecycle: DRAFT -> AVAILABLE -> RESERVED -> PICKUP_CONFIRMED -> COLLECTED -> DELIVERED. Terminal alternatives include CANCELLED and EXPIRED. Every transition should record actor, timestamp, and reason. Prevent duplicate reservation and do not allow a delivered donation to return to AVAILABLE without an explicit administrative correction.