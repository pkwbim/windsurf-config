# Microservice Readiness

## Table of Contents
- [Design Principles](#design-principles)
- [Bounded Context Isolation](#bounded-context-isolation)
- [Repository Swapping Pattern](#repository-swapping-pattern)
- [Cross-Context Communication](#cross-context-communication)
- [Extraction Checklist](#extraction-checklist)
- [Migration Example](#migration-example)

## Design Principles

Every Bounded Context should be extractable to a separate service by:
1. Writing a new Repository implementation
2. Changing the Service Provider binding
3. **Zero changes** to Domain or Application code

## Bounded Context Isolation

### Rules

- **No cross-context Eloquent JOINs** — each context queries its own tables
- **No shared Eloquent Models** — each context has its own Eloquent Models
- **No direct method calls across contexts** — use Events or DTOs
- **No shared database transactions** — each context manages its own

### ❌ NEVER: Cross-context JOIN

```php
// FORBIDDEN — couples Order and User at database level
OrderEloquent::join('users', 'orders.customer_id', '=', 'users.id')
    ->where('users.email', $email)
    ->get();
```

### ✅ MUST: Separate queries

```php
// Each context queries independently
$user = $this->userRepository->findByEmail($email);
$orders = $this->orderRepository->findByCustomer($user->id->toString());
```

## Repository Swapping Pattern

The key to microservice extraction: Repository Interface in Domain, implementation swappable via Service Provider.

### Current State: Monolith (Eloquent)

```php
// Domain — unchanged during extraction
interface OrderRepositoryInterface
{
    public function save(Order $order): void;
    public function findById(OrderId $id): ?Order;
}

// Infrastructure — current implementation
class EloquentOrderRepository implements OrderRepositoryInterface
{
    public function save(Order $order): void
    {
        $eloquent = OrderMapper::toEloquent($order);
        $eloquent->save();
    }

    public function findById(OrderId $id): ?Order
    {
        $eloquent = OrderEloquent::find($id->toString());
        return $eloquent ? OrderMapper::toDomain($eloquent) : null;
    }
}

// Service Provider binding
$this->app->bind(OrderRepositoryInterface::class, EloquentOrderRepository::class);
```

### Future State: Microservice (API)

```php
// Domain — ZERO CHANGES
interface OrderRepositoryInterface
{
    public function save(Order $order): void;
    public function findById(OrderId $id): ?Order;
}

// Infrastructure — NEW implementation calling remote API
class ApiOrderRepository implements OrderRepositoryInterface
{
    public function __construct(
        private readonly HttpClient $client,
        private readonly string $baseUrl,
    ) {}

    public function save(Order $order): void
    {
        $this->client->post("{$this->baseUrl}/orders", [
            'json' => [
                'id' => $order->id->toString(),
                'customer_id' => $order->customerId,
                'status' => $order->status->value,
                'total' => $order->total->amount(),
                'items' => array_map(fn ($item) => [
                    'product_id' => $item->productId,
                    'quantity' => $item->quantity,
                    'price' => $item->price->amount(),
                ], $order->items),
            ],
        ]);
    }

    public function findById(OrderId $id): ?Order
    {
        $response = $this->client->get("{$this->baseUrl}/orders/{$id}");

        if ($response->status() === 404) {
            return null;
        }

        return OrderApiMapper::toDomain($response->json());
    }
}

// Service Provider — ONLY CHANGE: swap binding
$this->app->bind(OrderRepositoryInterface::class, function ($app) {
    return new ApiOrderRepository(
        client: $app->make(HttpClient::class),
        baseUrl: config('services.order.url'),
    );
});
```

## Cross-Context Communication

### In Monolith: Laravel Events

```php
// Order context dispatches event
event(new OrderCreated($order->id, $order->customerId, $order->total));

// Notification context listens
class SendOrderConfirmationListener
{
    public function handle(OrderCreated $event): void
    {
        // Send notification
    }
}

// EventServiceProvider
protected $listen = [
    OrderCreated::class => [
        SendOrderConfirmationListener::class,
    ],
];
```

### In Microservices: Message Queue

```php
// Order service publishes to queue
class QueueEventDispatcher
{
    public function dispatch(OrderCreated $event): void
    {
        $this->queue->publish('order.created', [
            'order_id' => $event->orderId->toString(),
            'customer_id' => $event->customerId,
            'total' => $event->total->amount(),
        ]);
    }
}

// Notification service subscribes
class OrderCreatedSubscriber
{
    public function handle(array $payload): void
    {
        // Send notification
    }
}
```

The Domain Event class (`OrderCreated`) stays the same. Only the dispatch mechanism changes.

## Extraction Checklist

Before extracting a Bounded Context to a microservice, verify:

### Pre-Extraction
- [ ] Context has zero cross-context Eloquent JOINs
- [ ] Context has zero shared Eloquent Models with other contexts
- [ ] All cross-context communication uses Events
- [ ] All data access goes through Repository Interface
- [ ] Context has its own Service Provider
- [ ] All DTOs are self-contained (no references to other context's Domain Models)

### During Extraction
- [ ] Create new service with the Domain and Application layers (copy as-is)
- [ ] Implement new Infrastructure layer (API endpoints, database, etc.)
- [ ] In the monolith, replace `EloquentRepository` with `ApiRepository`
- [ ] Replace Laravel Event dispatch with message queue
- [ ] Update Service Provider binding

### Post-Extraction
- [ ] Domain and Application code unchanged
- [ ] All existing tests pass (update Infrastructure tests)
- [ ] Cross-context Events flow through message queue
- [ ] No direct database access between services

## Migration Example

### Step 1: Identify the Bounded Context to extract

```
app/Domain/Order/          → Move to Order Service
app/Application/Order/     → Move to Order Service
app/Infrastructure/.../Order  → Rewrite for new service
```

### Step 2: Create the new service

```
order-service/
├── app/
│   ├── Domain/Order/          # Copied from monolith (unchanged)
│   ├── Application/Order/     # Copied from monolith (unchanged)
│   ├── Infrastructure/        # New: own DB, own Eloquent
│   └── Http/                  # New: API endpoints
├── database/migrations/       # Own migrations
└── routes/api.php             # Own routes
```

### Step 3: Update the monolith

```php
// Before (monolith)
$this->app->bind(OrderRepositoryInterface::class, EloquentOrderRepository::class);

// After (monolith calls order-service API)
$this->app->bind(OrderRepositoryInterface::class, function ($app) {
    return new ApiOrderRepository(
        client: $app->make(HttpClient::class),
        baseUrl: config('services.order.url'),
    );
});
```

### Step 4: Verify

```bash
# All Domain tests still pass (they use InMemoryRepository)
php artisan test --filter=Unit/Domain

# Update Integration tests to test ApiOrderRepository
php artisan test --filter=Integration

# Feature tests may need API mocking
php artisan test --filter=Feature
```
