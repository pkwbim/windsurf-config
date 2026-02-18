# Eloquent Isolation Patterns

## Table of Contents
- [The Core Problem](#the-core-problem)
- [Anti-Patterns (NEVER DO)](#anti-patterns-never-do)
- [Correct Patterns (MUST DO)](#correct-patterns-must-do)
- [Mapper Pattern](#mapper-pattern)
- [Value Object Patterns](#value-object-patterns)
- [Query Scopes in DDD](#query-scopes-in-ddd)
- [Relationships](#relationships)

## The Core Problem

Laravel Eloquent is Active Record. It merges data access with domain logic:

```php
// Eloquent encourages this — FORBIDDEN in DDD
$order = Order::create(['customer_id' => 'c1', 'total' => 100]);
$order->total = 200;
$order->save();
```

In DDD, Domain Models must be pure PHP. Eloquent Models are infrastructure concerns.

## Anti-Patterns (NEVER DO)

### 1. Domain Model extending Eloquent

```php
// ❌ FORBIDDEN
namespace App\Domain\Order\Models;

use Illuminate\Database\Eloquent\Model;

class Order extends Model  // Domain coupled to Laravel
{
    protected $fillable = ['customer_id', 'total'];
}
```

### 2. Using Eloquent directly in Actions

```php
// ❌ FORBIDDEN
namespace App\Domain\Order\Actions;

use App\Domain\Order\Models\Order;

class CreateOrderAction
{
    public function execute(array $data): Order
    {
        return Order::create($data);  // Eloquent call in Domain
    }
}
```

### 3. Using DB Facade in Domain

```php
// ❌ FORBIDDEN
namespace App\Domain\Order\Actions;

use Illuminate\Support\Facades\DB;

class CreateOrderAction
{
    public function execute(array $data): void
    {
        DB::table('orders')->insert($data);  // Infrastructure in Domain
    }
}
```

### 4. Returning Eloquent Models from Repository

```php
// ❌ FORBIDDEN
interface OrderRepositoryInterface
{
    public function findById(string $id): \Illuminate\Database\Eloquent\Model;
}
```

### 5. Using Eloquent casts/accessors as business logic

```php
// ❌ FORBIDDEN — business logic hidden in Eloquent
class OrderEloquent extends Model
{
    public function getTotalWithDiscountAttribute(): float
    {
        return $this->total * 0.9;  // Business rule in infrastructure
    }
}
```

## Correct Patterns (MUST DO)

### Domain Model — Pure PHP

```php
<?php
namespace App\Domain\Order\Models;

use App\Domain\Order\ValueObjects\Money;
use App\Domain\Order\ValueObjects\OrderId;
use App\Domain\Order\ValueObjects\OrderStatus;

class Order
{
    public Money $total;

    public function __construct(
        public readonly OrderId $id,
        public readonly string $customerId,
        public array $items,
        public OrderStatus $status,
    ) {
        $this->total = new Money(0, 'TWD');
    }

    // Business logic lives HERE
    public function calculateTotal(): void
    {
        $sum = 0;
        foreach ($this->items as $item) {
            $sum += $item->subtotal()->amount();
        }
        $this->total = new Money($sum, 'TWD');
    }

    public function canBeCancelled(): bool
    {
        return $this->status === OrderStatus::Pending;
    }
}
```

### Eloquent Model — Infrastructure Only

```php
<?php
namespace App\Infrastructure\Persistence\Eloquent\Models;

use Illuminate\Database\Eloquent\Model;

class OrderEloquent extends Model
{
    protected $table = 'orders';
    protected $keyType = 'string';
    public $incrementing = false;

    protected $fillable = ['id', 'customer_id', 'status', 'total'];

    // Only Eloquent relationships and DB concerns here
    public function items()
    {
        return $this->hasMany(OrderItemEloquent::class, 'order_id');
    }
}
```

## Mapper Pattern

Mappers convert between Eloquent and Domain Models. They live in Infrastructure.

### Basic Mapper

```php
<?php
namespace App\Infrastructure\Persistence\Mappers;

use App\Domain\Order\Models\Order;
use App\Domain\Order\ValueObjects\{Money, OrderId, OrderStatus};
use App\Infrastructure\Persistence\Eloquent\Models\OrderEloquent;

class OrderMapper
{
    public static function toDomain(OrderEloquent $eloquent): Order
    {
        $items = $eloquent->items->map(
            fn ($item) => OrderItemMapper::toDomain($item)
        )->all();

        $order = new Order(
            id: new OrderId($eloquent->id),
            customerId: $eloquent->customer_id,
            items: $items,
            status: OrderStatus::from($eloquent->status),
        );
        $order->total = new Money($eloquent->total, 'TWD');

        return $order;
    }

    public static function toEloquent(Order $domain): OrderEloquent
    {
        $eloquent = OrderEloquent::findOrNew($domain->id->toString());
        $eloquent->id = $domain->id->toString();
        $eloquent->customer_id = $domain->customerId;
        $eloquent->status = $domain->status->value;
        $eloquent->total = $domain->total->amount();
        return $eloquent;
    }
}
```

### Mapper with Nested Relations

```php
<?php
namespace App\Infrastructure\Persistence\Mappers;

use App\Domain\Order\Models\OrderItem;
use App\Domain\Order\ValueObjects\Money;
use App\Infrastructure\Persistence\Eloquent\Models\OrderItemEloquent;

class OrderItemMapper
{
    public static function toDomain(OrderItemEloquent $eloquent): OrderItem
    {
        return new OrderItem(
            productId: $eloquent->product_id,
            quantity: $eloquent->quantity,
            price: new Money($eloquent->price, 'TWD'),
        );
    }

    public static function toArray(OrderItem $domain): array
    {
        return [
            'product_id' => $domain->productId,
            'quantity' => $domain->quantity,
            'price' => $domain->price->amount(),
        ];
    }
}
```

## Value Object Patterns

### ID Value Object

```php
<?php
namespace App\Domain\Order\ValueObjects;

final readonly class OrderId
{
    public function __construct(private string $value)
    {
        if (empty($value)) {
            throw new \InvalidArgumentException('OrderId cannot be empty');
        }
    }

    public static function generate(): self
    {
        return new self(uniqid('ord_', true));
    }

    public function toString(): string { return $this->value; }
    public function equals(self $other): bool { return $this->value === $other->value; }
    public function __toString(): string { return $this->value; }
}
```

### Money Value Object

```php
<?php
namespace App\Domain\Shared\ValueObjects;

final readonly class Money
{
    public function __construct(
        private int $amount,       // Smallest unit (cents/分)
        private string $currency,
    ) {
        if ($amount < 0) {
            throw new \InvalidArgumentException('Amount cannot be negative');
        }
    }

    public function amount(): int { return $this->amount; }
    public function currency(): string { return $this->currency; }

    public function add(self $other): self
    {
        $this->assertSameCurrency($other);
        return new self($this->amount + $other->amount, $this->currency);
    }

    public function subtract(self $other): self
    {
        $this->assertSameCurrency($other);
        $result = $this->amount - $other->amount;
        if ($result < 0) {
            throw new \InvalidArgumentException('Result cannot be negative');
        }
        return new self($result, $this->currency);
    }

    public function multiply(int $factor): self
    {
        return new self($this->amount * $factor, $this->currency);
    }

    private function assertSameCurrency(self $other): void
    {
        if ($this->currency !== $other->currency) {
            throw new \InvalidArgumentException('Currency mismatch');
        }
    }
}
```

### Enum Value Object

```php
<?php
namespace App\Domain\Order\ValueObjects;

enum OrderStatus: string
{
    case Pending = 'pending';
    case Confirmed = 'confirmed';
    case Shipped = 'shipped';
    case Delivered = 'delivered';
    case Cancelled = 'cancelled';

    public function canTransitionTo(self $target): bool
    {
        return match ($this) {
            self::Pending => in_array($target, [self::Confirmed, self::Cancelled]),
            self::Confirmed => in_array($target, [self::Shipped, self::Cancelled]),
            self::Shipped => $target === self::Delivered,
            default => false,
        };
    }
}
```

## Query Scopes in DDD

Eloquent scopes stay in Infrastructure. Domain defines what queries are needed via Repository Interface.

```php
// Domain: defines WHAT queries exist
interface OrderRepositoryInterface
{
    public function findPendingByCustomer(string $customerId): array;
    public function findByDateRange(DateTimeImmutable $from, DateTimeImmutable $to): array;
}

// Infrastructure: implements HOW using Eloquent
class EloquentOrderRepository implements OrderRepositoryInterface
{
    public function findPendingByCustomer(string $customerId): array
    {
        return OrderEloquent::where('customer_id', $customerId)
            ->where('status', 'pending')
            ->get()
            ->map(fn ($e) => OrderMapper::toDomain($e))
            ->all();
    }
}
```

## Relationships

Cross-context relationships MUST NOT use Eloquent relationships. Use separate queries.

```php
// ❌ FORBIDDEN — cross-context Eloquent relationship
class OrderEloquent extends Model
{
    public function customer()
    {
        return $this->belongsTo(UserEloquent::class);  // Couples Order to User context
    }
}

// ✅ CORRECT — query separately via Repository
class OrderService
{
    public function getOrderWithCustomer(string $orderId): array
    {
        $order = $this->orderRepository->findById(new OrderId($orderId));
        $customer = $this->userRepository->findById($order->customerId);
        return ['order' => $order, 'customer' => $customer];
    }
}
```

Within the same Bounded Context, Eloquent relationships are acceptable:

```php
// ✅ OK — same context (Order → OrderItem)
class OrderEloquent extends Model
{
    public function items()
    {
        return $this->hasMany(OrderItemEloquent::class, 'order_id');
    }
}
```
