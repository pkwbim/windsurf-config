---
name: laravel-ddd
description: >
  Domain-Driven Design architecture enforcement for Laravel PHP projects.
  Ensures proper separation of Domain, Application, Infrastructure, and Http layers.
  Use when: (1) Creating a new Laravel project with DDD architecture,
  (2) Adding new features/modules to an existing Laravel DDD project,
  (3) Creating Bounded Contexts, Entities, Value Objects, Actions, Repositories, or Services in Laravel,
  (4) Refactoring Laravel code to follow DDD patterns,
  (5) Working with any Laravel .php files that involve business logic, data access, or API endpoints.
  Prevents common Laravel anti-patterns: Eloquent in Controllers, business logic outside Domain layer,
  skipping Service/Action/Repository layers, cross-context coupling.
  Designed for projects that may scale to microservices.
---

# Laravel DDD

Enforce Domain-Driven Design in Laravel projects. Prevent Eloquent/Active Record anti-patterns and ensure the codebase is microservice-ready.

## Three Iron Rules

1. **Domain layer MUST NOT depend on Laravel** — Domain Models, Actions, Value Objects are pure PHP classes
2. **NEVER write business logic in Controllers** — Follow: Controller → DTO → Service/Action → Repository
3. **Use Interfaces to isolate infrastructure** — Repository Interface in Domain, implementation in Infrastructure

## Directory Structure

Organize by Bounded Context, not by technical role:

```
app/
├── Domain/{Context}/           # Pure PHP business logic
│   ├── Models/                 # Domain Models (NOT Eloquent)
│   ├── ValueObjects/
│   ├── Actions/                # Single-responsibility business operations
│   ├── DTOs/
│   ├── Events/                 # Domain Events
│   ├── Exceptions/
│   └── Contracts/              # Interfaces (Repository, Service)
├── Application/{Context}/      # Orchestration layer
│   └── Services/               # Coordinate multiple Actions
├── Infrastructure/             # Technical implementations
│   ├── Persistence/
│   │   ├── Eloquent/Models/    # Eloquent Models live HERE only
│   │   ├── Eloquent/Repositories/
│   │   └── Mappers/            # Eloquent ↔ Domain conversion
│   ├── External/               # Third-party API integrations
│   └── Providers/              # Service Providers (Interface bindings)
└── Http/                       # Interface layer
    ├── Controllers/
    ├── Requests/               # Form Requests (validation only)
    └── Resources/              # API Resources (response formatting)
```

For full directory structure with examples, see [references/directory-structure.md](references/directory-structure.md).

## Dependency Rules

| Layer | MAY depend on | MUST NOT depend on |
|-------|--------------|-------------------|
| Domain | PHP native, own Domain | Laravel, Eloquent, any framework |
| Application | Domain | Infrastructure concrete classes |
| Infrastructure | Domain, Application, Laravel | — |
| Http | Application, Domain DTOs | Domain internals |

## Call Chain (MUST follow)

Every request MUST flow through this chain. Never skip layers.

```
Controller → FormRequest → DTO → Service/Action → Repository Interface → Eloquent Repository
```

### ❌ NEVER: Eloquent in Controller

```php
// FORBIDDEN — skips all layers, business logic in controller
public function store(Request $request) {
    $order = Order::create($request->all());
    if ($order->total > 1000) {
        $order->discount = $order->total * 0.1;
        $order->save();
    }
    return response()->json($order);
}
```

### ✅ MUST: Proper layered approach

```php
// Controller — only receive, delegate, respond
public function store(CreateOrderRequest $request): OrderResource
{
    $dto = CreateOrderData::fromRequest($request);
    $order = $this->orderService->createOrder($dto);
    return new OrderResource($order);
}
```

For complete code examples of every layer, see [references/code-examples.md](references/code-examples.md).

## Cross-Context Communication

- **NEVER** call another Bounded Context directly from an Action
- **ALWAYS** use Domain Events + Listeners for cross-context communication
- **ALWAYS** use DTOs (not Domain Models) when passing data across contexts

## Eloquent Isolation

Eloquent Models belong ONLY in `Infrastructure/Persistence/Eloquent/Models/`. Use Mappers to convert between Eloquent and Domain Models.

- Domain Models: pure PHP classes, no `extends Model`, no `$fillable`, no `$casts`
- Eloquent Models: suffixed with `Eloquent` (e.g., `OrderEloquent`), only used inside Repository implementations
- Mapper classes handle bidirectional conversion

For Eloquent isolation patterns and Mapper examples, see [references/eloquent-patterns.md](references/eloquent-patterns.md).

## Testing Strategy

- **Domain layer**: Pure PHPUnit tests (no Laravel TestCase), use in-memory repository fakes
- **Infrastructure layer**: Laravel integration tests with `RefreshDatabase`
- **Http layer**: Feature tests for API endpoints

For testing examples, see [references/testing.md](references/testing.md).

## Microservice Readiness

Design every Bounded Context so it can be extracted to a separate service by only:
1. Writing a new Repository implementation (e.g., `ApiOrderRepository`)
2. Changing the Service Provider binding
3. Zero changes to Domain or Application code

Key rules:
- No cross-context Eloquent JOINs
- No shared Eloquent Models between contexts
- Repository Interface in Domain, implementation in Infrastructure

For migration patterns, see [references/microservice-ready.md](references/microservice-ready.md).

## Pre-Commit Checklist

Before completing any feature, verify:

- [ ] Controller only receives, delegates, and responds
- [ ] Business logic lives in Action or Domain Model
- [ ] Data access goes through Repository Interface
- [ ] Eloquent Models only in `Infrastructure/Persistence/Eloquent/Models/`
- [ ] Domain layer has zero Laravel imports
- [ ] Cross-context communication uses Events
- [ ] Unit tests exist for Domain Actions
- [ ] DTOs used for inter-layer data transfer

## Recommended Packages

| Package | Purpose |
|---------|---------|
| `spatie/laravel-data` | DTO management (strongly recommended) |
| `spatie/laravel-event-sourcing` | Event Sourcing (advanced, optional) |
| `lorisleiva/laravel-actions` | Action pattern helpers (optional) |

## References

- [references/directory-structure.md](references/directory-structure.md) — Full directory tree with file-level examples
- [references/code-examples.md](references/code-examples.md) — Complete code for Controller, DTO, Service, Action, Repository, Mapper
- [references/eloquent-patterns.md](references/eloquent-patterns.md) — Eloquent isolation, Mapper pattern, Value Objects
- [references/testing.md](references/testing.md) — Test examples for each layer, test pyramid
- [references/microservice-ready.md](references/microservice-ready.md) — Extraction patterns, Service Provider swapping
