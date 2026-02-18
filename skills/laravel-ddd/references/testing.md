# Testing Strategy

## Table of Contents
- [Test Pyramid](#test-pyramid)
- [File Naming Convention](#file-naming-convention)
- [Domain Unit Tests](#domain-unit-tests)
- [In-Memory Repository Fakes](#in-memory-repository-fakes)
- [Infrastructure Integration Tests](#infrastructure-integration-tests)
- [Http Feature Tests](#http-feature-tests)
- [Testing Domain Events](#testing-domain-events)

## Test Pyramid

```
         /    E2E Tests     \         ← Few: full browser/API flow
        /   Feature Tests    \        ← Medium: test API endpoints
       / Integration Tests    \       ← Medium: test Repository + DB
      /  Unit Tests (Domain)   \      ← Many: test business logic (fastest)
```

Priority: Write Domain unit tests first. They are fastest and test the most critical code.

## File Naming Convention

```
tests/
├── Unit/
│   └── Domain/
│       ├── Order/
│       │   ├── Actions/
│       │   │   ├── CreateOrderActionTest.php
│       │   │   └── CancelOrderActionTest.php
│       │   ├── Models/
│       │   │   └── OrderTest.php
│       │   └── ValueObjects/
│       │       ├── MoneyTest.php
│       │       └── OrderIdTest.php
│       └── User/
│           └── Actions/
│               └── RegisterUserActionTest.php
├── Integration/
│   └── Infrastructure/
│       ├── EloquentOrderRepositoryTest.php
│       └── EloquentUserRepositoryTest.php
└── Feature/
    └── Http/
        ├── OrderControllerTest.php
        └── UserControllerTest.php
```

## Domain Unit Tests

Use **PHPUnit TestCase** (NOT Laravel TestCase). Domain tests must run without Laravel.

### Testing an Action

```php
<?php
// tests/Unit/Domain/Order/Actions/CreateOrderActionTest.php

namespace Tests\Unit\Domain\Order\Actions;

use App\Domain\Order\Actions\CreateOrderAction;
use App\Domain\Order\DTOs\CreateOrderData;
use App\Domain\Order\ValueObjects\OrderStatus;
use PHPUnit\Framework\TestCase;
use Tests\Fakes\InMemoryOrderRepository;

class CreateOrderActionTest extends TestCase
{
    private InMemoryOrderRepository $repository;
    private CreateOrderAction $action;

    protected function setUp(): void
    {
        $this->repository = new InMemoryOrderRepository();
        $this->action = new CreateOrderAction($this->repository);
    }

    public function test_creates_order_with_pending_status(): void
    {
        $data = new CreateOrderData(
            customerId: 'cust-1',
            items: [
                ['product_id' => 'p1', 'quantity' => 2, 'price' => 100],
            ],
        );

        $order = $this->action->execute($data);

        $this->assertEquals(OrderStatus::Pending, $order->status);
        $this->assertEquals('cust-1', $order->customerId);
        $this->assertCount(1, $order->items);
    }

    public function test_calculates_total_correctly(): void
    {
        $data = new CreateOrderData(
            customerId: 'cust-1',
            items: [
                ['product_id' => 'p1', 'quantity' => 2, 'price' => 100],
                ['product_id' => 'p2', 'quantity' => 1, 'price' => 500],
            ],
        );

        $order = $this->action->execute($data);

        $this->assertEquals(700, $order->total->amount());
    }

    public function test_persists_order_to_repository(): void
    {
        $data = new CreateOrderData(
            customerId: 'cust-1',
            items: [
                ['product_id' => 'p1', 'quantity' => 1, 'price' => 100],
            ],
        );

        $order = $this->action->execute($data);

        $found = $this->repository->findById($order->id);
        $this->assertNotNull($found);
        $this->assertTrue($order->id->equals($found->id));
    }
}
```

### Testing a Domain Model

```php
<?php
// tests/Unit/Domain/Order/Models/OrderTest.php

namespace Tests\Unit\Domain\Order\Models;

use App\Domain\Order\Exceptions\OrderCannotBeCancelled;
use App\Domain\Order\Models\Order;
use App\Domain\Order\Models\OrderItem;
use App\Domain\Order\ValueObjects\Money;
use App\Domain\Order\ValueObjects\OrderId;
use App\Domain\Order\ValueObjects\OrderStatus;
use PHPUnit\Framework\TestCase;

class OrderTest extends TestCase
{
    private function createOrder(OrderStatus $status = OrderStatus::Pending): Order
    {
        return new Order(
            id: OrderId::generate(),
            customerId: 'cust-1',
            items: [
                new OrderItem('p1', 2, new Money(100, 'TWD')),
            ],
            status: $status,
        );
    }

    public function test_calculate_total(): void
    {
        $order = $this->createOrder();
        $order->calculateTotal();

        $this->assertEquals(200, $order->total->amount());
    }

    public function test_cancel_pending_order(): void
    {
        $order = $this->createOrder(OrderStatus::Pending);
        $order->cancel();

        $this->assertEquals(OrderStatus::Cancelled, $order->status);
    }

    public function test_cannot_cancel_shipped_order(): void
    {
        $order = $this->createOrder(OrderStatus::Shipped);

        $this->expectException(OrderCannotBeCancelled::class);
        $order->cancel();
    }

    public function test_apply_discount(): void
    {
        $order = $this->createOrder();
        $order->calculateTotal();
        $order->applyDiscount(new Money(50, 'TWD'));

        $this->assertEquals(150, $order->total->amount());
    }
}
```

### Testing a Value Object

```php
<?php
// tests/Unit/Domain/Order/ValueObjects/MoneyTest.php

namespace Tests\Unit\Domain\Order\ValueObjects;

use App\Domain\Order\ValueObjects\Money;
use InvalidArgumentException;
use PHPUnit\Framework\TestCase;

class MoneyTest extends TestCase
{
    public function test_cannot_create_negative_amount(): void
    {
        $this->expectException(InvalidArgumentException::class);
        new Money(-100, 'TWD');
    }

    public function test_add_same_currency(): void
    {
        $a = new Money(100, 'TWD');
        $b = new Money(200, 'TWD');
        $result = $a->add($b);

        $this->assertEquals(300, $result->amount());
    }

    public function test_cannot_add_different_currencies(): void
    {
        $a = new Money(100, 'TWD');
        $b = new Money(200, 'USD');

        $this->expectException(InvalidArgumentException::class);
        $a->add($b);
    }
}
```

## In-Memory Repository Fakes

Create fake repositories for Domain unit tests. They implement the same Interface but store data in arrays.

```php
<?php
// tests/Fakes/InMemoryOrderRepository.php

namespace Tests\Fakes;

use App\Domain\Order\Contracts\OrderRepositoryInterface;
use App\Domain\Order\Models\Order;
use App\Domain\Order\ValueObjects\OrderId;

class InMemoryOrderRepository implements OrderRepositoryInterface
{
    /** @var array<string, Order> */
    private array $orders = [];

    public function save(Order $order): void
    {
        $this->orders[$order->id->toString()] = $order;
    }

    public function findById(OrderId $id): ?Order
    {
        return $this->orders[$id->toString()] ?? null;
    }

    public function findByCustomer(string $customerId): array
    {
        return array_filter(
            $this->orders,
            fn (Order $o) => $o->customerId === $customerId,
        );
    }

    public function delete(OrderId $id): void
    {
        unset($this->orders[$id->toString()]);
    }

    // Test helpers
    public function all(): array
    {
        return array_values($this->orders);
    }

    public function count(): int
    {
        return count($this->orders);
    }
}
```

## Infrastructure Integration Tests

Use **Laravel TestCase** with `RefreshDatabase` for testing Eloquent Repositories.

```php
<?php
// tests/Integration/Infrastructure/EloquentOrderRepositoryTest.php

namespace Tests\Integration\Infrastructure;

use App\Domain\Order\Models\Order;
use App\Domain\Order\Models\OrderItem;
use App\Domain\Order\ValueObjects\Money;
use App\Domain\Order\ValueObjects\OrderId;
use App\Domain\Order\ValueObjects\OrderStatus;
use App\Infrastructure\Persistence\Eloquent\Repositories\EloquentOrderRepository;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class EloquentOrderRepositoryTest extends TestCase
{
    use RefreshDatabase;

    private EloquentOrderRepository $repository;

    protected function setUp(): void
    {
        parent::setUp();
        $this->repository = new EloquentOrderRepository();
    }

    public function test_save_and_retrieve(): void
    {
        $order = new Order(
            id: OrderId::generate(),
            customerId: 'cust-1',
            items: [new OrderItem('p1', 2, new Money(100, 'TWD'))],
            status: OrderStatus::Pending,
        );
        $order->calculateTotal();

        $this->repository->save($order);
        $found = $this->repository->findById($order->id);

        $this->assertNotNull($found);
        $this->assertEquals($order->id->toString(), $found->id->toString());
        $this->assertEquals(200, $found->total->amount());
        $this->assertCount(1, $found->items);
    }

    public function test_find_by_customer(): void
    {
        $order1 = $this->createTestOrder('cust-1');
        $order2 = $this->createTestOrder('cust-1');
        $order3 = $this->createTestOrder('cust-2');

        $this->repository->save($order1);
        $this->repository->save($order2);
        $this->repository->save($order3);

        $results = $this->repository->findByCustomer('cust-1');
        $this->assertCount(2, $results);
    }

    public function test_delete(): void
    {
        $order = $this->createTestOrder('cust-1');
        $this->repository->save($order);

        $this->repository->delete($order->id);

        $this->assertNull($this->repository->findById($order->id));
    }

    private function createTestOrder(string $customerId): Order
    {
        $order = new Order(
            id: OrderId::generate(),
            customerId: $customerId,
            items: [new OrderItem('p1', 1, new Money(100, 'TWD'))],
            status: OrderStatus::Pending,
        );
        $order->calculateTotal();
        return $order;
    }
}
```

## Http Feature Tests

Test API endpoints end-to-end with Laravel's HTTP testing.

```php
<?php
// tests/Feature/Http/OrderControllerTest.php

namespace Tests\Feature\Http;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class OrderControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_create_order(): void
    {
        $response = $this->postJson('/api/orders', [
            'customer_id' => 'cust-1',
            'items' => [
                ['product_id' => 'p1', 'quantity' => 2, 'price' => 100],
            ],
        ]);

        $response->assertStatus(201)
            ->assertJsonStructure([
                'data' => ['id', 'customer_id', 'status', 'total', 'items'],
            ])
            ->assertJsonPath('data.status', 'pending')
            ->assertJsonPath('data.total', 200);
    }

    public function test_create_order_validation(): void
    {
        $response = $this->postJson('/api/orders', []);

        $response->assertStatus(422)
            ->assertJsonValidationErrors(['customer_id', 'items']);
    }
}
```

## Testing Domain Events

```php
<?php
// tests/Unit/Domain/Order/Actions/CreateOrderActionTest.php
// (additional test for event dispatching)

use App\Domain\Order\Events\OrderCreated;
use Illuminate\Support\Facades\Event;

public function test_dispatches_order_created_event(): void
{
    Event::fake([OrderCreated::class]);

    $data = new CreateOrderData(
        customerId: 'cust-1',
        items: [['product_id' => 'p1', 'quantity' => 1, 'price' => 100]],
    );

    $this->action->execute($data);

    Event::assertDispatched(OrderCreated::class, function ($event) {
        return $event->customerId === 'cust-1';
    });
}
```

**Note:** Event testing with `Event::fake()` requires Laravel TestCase. For pure Domain unit tests, verify the event was dispatched by checking side effects or using a spy pattern instead.
