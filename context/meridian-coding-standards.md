# Meridian Retail — Angular 18 Coding Standards

## Project Context

Meridian Retail is a mid-market EU omnichannel retailer (€1–5B revenue, 1,400 stores). The Angular 18 frontend is a greenfield microservices UI consuming REST APIs from .NET 8 microservices. All Angular code lives in a monorepo under `src/app/`.

---

## Component Rules

### Structure
- All components MUST be standalone (`standalone: true`).
- Change detection MUST be `ChangeDetectionStrategy.OnPush`.
- Components MUST have a selector prefixed `app-`.
- One component per file; file name matches selector (e.g. `product-tile.component.ts`).

### Inputs and Outputs
- Every configurable display value MUST be an `@Input()` with a typed default.
- Business logic side-effects MUST be `@Output() EventEmitter` — never direct service calls from a template event.
- Use `input()` / `output()` signal-based API for new components (Angular 17+).

### Template Rules
- No logic in templates beyond simple ternary and `| async`.
- Loops use `@for` (Angular 17+ control flow), not `*ngFor`.
- Conditionals use `@if` / `@else`, not `*ngIf`.
- All interactive elements (`button`, `a`, custom controls) MUST have `aria-label` or `aria-labelledby`.
- Images MUST have `alt` attributes.

---

## SCSS / Design Tokens

All style values come from the Meridian token library. Never use raw hex, px literals for spacing, or named CSS colors.

```scss
// Colors
$color-primary:      #1A4480;   // brand blue
$color-primary-dark: #0F2B52;
$color-accent:       #E8732A;   // CTA orange
$color-success:      #2D7D46;
$color-warning:      #C17F24;
$color-danger:       #B91C1C;
$color-text:         #1F2937;
$color-text-muted:   #6B7280;
$color-bg:           #F9FAFB;
$color-surface:      #FFFFFF;
$color-border:       #E5E7EB;

// Spacing (8px grid)
$spacing-1: 4px;
$spacing-2: 8px;
$spacing-3: 12px;
$spacing-4: 16px;
$spacing-5: 20px;
$spacing-6: 24px;
$spacing-8: 32px;
$spacing-10: 40px;
$spacing-12: 48px;

// Typography
$font-size-xs:   0.75rem;
$font-size-sm:   0.875rem;
$font-size-base: 1rem;
$font-size-lg:   1.125rem;
$font-size-xl:   1.25rem;
$font-weight-normal: 400;
$font-weight-medium: 500;
$font-weight-bold:   700;

// Border radius
$radius-sm: 4px;
$radius-md: 8px;
$radius-lg: 12px;

// Shadows
$shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
$shadow-md: 0 4px 6px rgba(0,0,0,0.07);
$shadow-lg: 0 10px 15px rgba(0,0,0,0.10);
```

---

## Testing Standards (Jest / Jasmine)

- EVERY `@Input()` must have at least one test verifying it renders or affects behaviour.
- EVERY public method must have at least one test for the happy path.
- Tests for list/collection inputs must cover: empty array, single item, multiple items.
- Use `TestBed.configureTestingModule` with `imports: [ComponentUnderTest]` (standalone).
- Do NOT mock internal Angular pipes or directives — only mock services.
- Arrange / Act / Assert structure; one assertion cluster per `it()`.

### Test file template
```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { XyzComponent } from './xyz.component';

describe('XyzComponent', () => {
  let component: XyzComponent;
  let fixture: ComponentFixture<XyzComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [XyzComponent],
    }).compileComponents();
    fixture = TestBed.createComponent(XyzComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  // ... feature-specific cases
});
```

---

## Barrel Exports

Every component folder MUST have an `index.ts`:
```typescript
export { XyzComponent } from './xyz.component';
```

---

## File Naming Convention

```
src/app/components/<kebab-name>/
  <kebab-name>.component.ts
  <kebab-name>.component.html
  <kebab-name>.component.scss
  <kebab-name>.component.spec.ts
  index.ts
```

---

## What NOT to do

- No `any` in TypeScript — use explicit types or generics.
- No `console.log` in committed code.
- No inline styles in templates.
- No `ngOnChanges` — use computed signals instead.
- No service injection in `constructor` — use `inject()` function.
