# Demo: How to trigger the AI Factory

Copy the issue body below into a new GitHub Issue on your factory repo, then add the label `ai-generate`.

---

## Issue title

```
Click-and-collect slot picker — store + time selection
```

## Issue body

```markdown
## Feature: Click-and-Collect Slot Picker

### Context
Meridian customers can reserve items online and collect in-store.
During checkout, they must pick a store and a collection time slot.

### Component requirements

**Selector:** `app-slot-picker`

**Inputs:**
- `stores: Store[]` — list of available stores. Each store has `{ id: string; name: string; address: string }`.
- `slots: TimeSlot[]` — list of available time slots for the selected store. Each slot: `{ id: string; label: string; available: boolean }`.
- `selectedStoreId: string | null` — currently selected store (default: null).
- `selectedSlotId: string | null` — currently selected slot (default: null).

**Outputs:**
- `storeSelected: EventEmitter<string>` — emits the store id when user picks a store.
- `slotSelected: EventEmitter<string>` — emits the slot id when user picks a slot.

**Behaviour:**
- Show a dropdown/list of stores.
- When a store is selected, show the time slots for that store.
- Unavailable slots must be visually greyed out and not selectable.
- Selected store and slot should be highlighted.
- If `stores` is empty, show the message "No stores available in your area."
- If `slots` is empty after a store is selected, show "No slots available for this store."

**Accessibility:**
- All interactive elements must be keyboard-navigable.
- Screen reader must announce the selected store and slot.

**Visual:**
- Use Meridian design tokens for all colours and spacing.
- Mobile-first; single-column layout.
- CTA button "Confirm selection" is disabled until both store and slot are selected.
```

---

## Expected output

After labelling this issue `ai-generate`, within ~60 seconds GitHub Actions should:

1. Run `agents/factory/agent.py`
2. Open a PR titled `feat(slot-picker): SlotPickerComponent [AI generated]`
3. The PR contains:
   - `src/app/components/slot-picker/slot-picker.component.ts`
   - `src/app/components/slot-picker/slot-picker.component.html`
   - `src/app/components/slot-picker/slot-picker.component.scss`
   - `src/app/components/slot-picker/slot-picker.component.spec.ts`
   - `src/app/components/slot-picker/index.ts`
4. The Review Agent fires and posts an inline review

This is the primary demo scenario for the AI/RUN Mission 2026 submission.
