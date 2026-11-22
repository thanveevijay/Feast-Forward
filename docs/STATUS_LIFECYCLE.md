# Food donation status lifecycle

A donation should move through a controlled lifecycle so donors, volunteers, and recipients see consistent progress.

## Suggested states
- `POSTED`: donor has submitted a donation for review or matching.
- `MATCHED`: a recipient or handoff has been associated with the donation.
- `PICKUP_CONFIRMED`: a volunteer has confirmed the collection plan.
- `PICKED_UP`: the volunteer has confirmed physical collection.
- `DELIVERED`: the recipient handoff has been confirmed.
- `CANCELLED`: the donation will not proceed.

## Transition rules
- A new donation begins in `POSTED`.
- Only a valid match can move a post to `MATCHED`.
- Pickup confirmation requires an assigned volunteer and a valid time window.
- Delivery requires a prior pickup confirmation.
- Cancellation should record a reason and actor.
- Terminal states should not be silently reopened; use an explicit correction workflow if needed.

## Audit information
Record the previous state, new state, actor, timestamp, and optional reason. Enforce transitions on the server and test concurrent updates to avoid conflicting handoff records.
