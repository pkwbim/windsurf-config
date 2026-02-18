# Code Examples

Complete code examples for every layer in the call chain.

## Table of Contents
- [Controller](#controller)
- [Form Request](#form-request)
- [DTO](#dto)
- [Application Service](#application-service)
- [Domain Action](#domain-action)
- [Domain Model](#domain-model)
- [Value Object](#value-object)
- [Repository Interface](#repository-interface)
- [Eloquent Repository](#eloquent-repository)
- [Eloquent Model](#eloquent-model)
- [Mapper](#mapper)
- [Domain Event](#domain-event)
- [Service Provider](#service-provider)
- [API Resource](#api-resource)

## Controller

```php
<?php
// app/Http/Controllers/Api/OrderController.php

namespace App\Http\Controllers\Api;

use App\Application\Order\Services\OrderService;
use App\Domain\Order\DTOs\CreateOrderData;
use App\Http\Controllers\Controller;
use App\Http\Requests\CreateOrderRequest;
use App\Http\Resources\OrderResource;

class OrderController extends Controller
{
    public function __construct(
        private readonly OrderService $orderService,
    ) {}

    // Controller does THREE things only: receive, delegate, respond
    public function store(CreateOrderRequest $request): OrderResource
    {
        $dto = CreateOrderData::fromRequest($request);
        $order = $this->orderService->createOrder($dto);
        return new OrderResource($order);
    }

    public function show(string $id): OrderResource
    {
        $order = $this->orderService->getOrder($id);
        return new OrderResource($order);
    }

    public function cancel(string $id): OrderResource
    {
        $order = $this->orderService->cancelOrder($id);
        return new OrderResource($order);
    }
}
```

## Form Request

```php
<?php
// app/Http/Requests/CreateOrderRequest.php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class CreateOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    // Validation ONLY — no business logic
    public function rules(): array
    {
        return [
            'customer_id' => ['required', 'string'],
            'items' => ['required', 'array', 'min:1'],
            'items.*.product_id' => ['required', 'string'],
            'items.*.quantity' => ['required', 'integer', 'min:1'],
            'items.*.price' => ['required', 'integer', 'min:0'],
            'coupon_code' => ['nullable', 'string'],
        ];
    }
}
```

## DTO

```php
<?php
// app/Domain/Order/DTOs/CreateOrderData.php

namespace App\Domain\Order\DTOs;

use App\Http\Requests\CreateOrderRequest;

final readonly class CreateOrderData
{
    public function __construct(
        public string $customerId,
        public array $items,
        public ?string $couponCode = null,
    ) {}

    public static function fromRequest(CreateOrderRequest $request): self
    {
        return new self(
            customerId: $request->validated('customer_id'),
            items: $request->validated('items'),
            couponCode: $request->validated('coupon_code'),
        );
    }

    public static function fromArray(array $data): self
    {
        return new self(
            customerId: $data['customer_id'],
            items: $data['items'],
            couponCode: $data['coupon_code'] ?? null,
        );
    }
}
```

### DTO with spatie/laravel-data (recommended)

```php
<?php
// app/Domain/Order/DTOs/CreateOrderData.php

namespace App\Domain\Order\DTOs;

use Spatie\LaravelData\Data;

class CreateOrderData extends Data
{
    public function __construct(
        public string $customerId,
        /** @var array<OrderItemData> */
        public array $items,
        public ?string $couponCode = null,
    ) {}
}
```

## Application Service

```php
<?php
// app/Application/Order/Services/OrderService.php

namespace App\Application\Order\Services;

use App\Domain\Order\Actions\CancelOrderAction;
use App\Domain\Order\Actions\CreateOrderAction;
use App\Domain\Order\Actions\ApplyDiscountAction;
use App\Domain\Order\Contracts\OrderRepositoryInterface;
use App\Domain\Order\DTOs\CreateOrderData;
use App\Domain\Order\Models\Order;
use App\Domain\Order\ValueObjects\OrderId;
use Illuminate\Support\Facades\DB;

class OrderService
{
    public function __construct(
        private readonly CreateOrderAction $createOrderAction,
        private readonly ApplyDiscountAction $applyDiscountAction,
        private readonly CancelOrderAction $cancelOrderAction,
        private readonly OrderRepositoryInterface $orderRepository,
    ) {}

    // Orchestrate Actions, handle transactions
    public function createOrder(CreateOrderData $data): Order
    {
        return DB::transaction(function () use ($data) {
            $order = $this->createOrderAction->execute($data);

            if ($data->couponCode) {
                $order = $this->applyDiscountAction->execute($order, $data->couponCode);
            }

            return $order;
        });
    }

    public function getOrder(string $id): Order
    {
        return $this->orderRepository->findById(new OrderId($id));
    }

    public function cancelOrder(string $id): Order
    {
        return DB::transaction(function () use ($id) {
            $order = $this->orderRepository->findById(new OrderId($id));
            return $this->cancelOrderAction->execute($order);
        });
    }
}
```

## Domain Action

```php
<?php
// app/Domain/Order/Actions/CreateOrderAction.php

namespace App\Domain\Order\Actions;

use App\Domain\Order\Contracts\OrderRepositoryInterface;
use App\Domain\Order\DTOs\CreateOrderData;
use App\Domain\Order\Events\OrderCreated;
use App\Domain\Order\Models\Order;
use App\Domain\Order\Models\OrderItem;
use App\Domain\Order\ValueObjects\Money;
use App\Domain\Order\ValueObjects\OrderId;
use App\Domain\Order\ValueObjects\OrderStatus;

class CreateOrderAction
{
    public function __construct(
        private readonly OrderRepositoryInterface $orderRepository,
    ) {}

    public function execute(CreateOrderData $data): Order
    {
        $items = array_map(
            fn (array $item) => new OrderItem(
                productId: $item['product_id'],
                quantity: $item['quantity'],
                price: new Money($item['price'], 'TWD'),
            ),
            $data->items,
        );

        $order = new Order(
            id: OrderId::generate(),
            customerId: $data->customerId,
            items: $items,
            status: OrderStatus::Pending,
        );

        $order->calculateTotal();

        $this->orderRepository->save($order);

        event(new OrderCreated(
            orderId: $order->id,
            customerId: $order->customerId,
            total: $order->total,
        ));

        return $order;
    }
}
```

## Domain Model

```php
<?php
// app/Domain/Order/Models/Order.php

namespace App\Domain\Order\Models;

use App\Domain\Order\Exceptions\OrderCannotBeCancelled;
use App\Domain\Order\ValueObjects\Money;
use App\Domain\Order\ValueObjects\OrderId;
use App\Domain\Order\ValueObjects\OrderStatus;

// Pure PHP class — NO extends Model, NO traits, NO Laravel imports
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

    public function calculateTotal(): void
    {
        $sum = 0;
        foreach ($this->items as $item) {
            $sum += $item->price->amount() * $item->quantity;
        }
        $this->total = new Money($sum, 'TWD');
    }

    public function cancel(): void
    {
        if ($this->status !== OrderStatus::Pending) {
            throw new OrderCannotBeCancelled(
                "Order {$this->id} cannot be cancelled in status {$this->status->value}"
            );
        }
        $this->status = OrderStatus::Cancelled;
    }

    public function applyDiscount(Money $discount): void
    {
        $this->total = $this->total->subtract($discount);
    }
}
```

## Value Object

```php
<?php
// app/Domain/Order/ValueObjects/OrderId.php

namespace App\Domain\Order\ValueObjects;

use InvalidArgumentException;

final readonly class OrderId
{
    public function __construct(
        private string $value,
    ) {
        if (empty($value)) {
            throw new InvalidArgumentException('OrderId cannot be empty');
        }
    }

    public static function generate(): self
    {
        return new self(uniqid('ord_', true));
    }

    public function toString(): string
    {
        return $this->value;
    }

    public function equals(self $other): bool
    {
        return $this->value === $other->value;
    }

    public function __toString(): string
    {
        return $this->value;
    }
}
```

```php
<?php
// app/Domain/Order/ValueObjects/Money.php

namespace App\Domain\Order\ValueObjects;

use InvalidArgumentException;

final readonly class Money
{
    public function __construct(
        private int $amount,      // Store in smallest unit (cents)
        private string $currency,
    ) {
        if ($amount < 0) {
            throw new InvalidArgumentException('Money amount cannot be negative');
        }
    }

    public function amount(): int
    {
        return $this->amount;
    }

    public function currency(): string
    {
        return $this->currency;
    }

    public function add(self $other): self
    {
        $this->assertSameCurrency($other);
        return new self($this->amount + $other->amount, $this->currency);
    }

    public function subtract(self $other): self
    {
        $this->assertSameCurrency($other);
        return new self($this->amount - $other->amount, $this->currency);
    }

    private function assertSameCurrency(self $other): void
    {
        if ($this->currency !== $other->currency) {
            throw new InvalidArgumentException("Cannot operate on different currencies");
        }
    }
}
```

```php
<?php
// app/Domain/Order/ValueObjects/OrderStatus.php

namespace App\Domain\Order\ValueObjects;

enum OrderStatus: string
{
    case Pending = 'pending';
    case Confirmed = 'confirmed';
    case Shipped = 'shipped';
    case Delivered = 'delivered';
    case Cancelled = 'cancelled';
}
```

## Repository Interface

```php
<?php
// app/Domain/Order/Contracts/OrderRepositoryInterface.php

namespace App\Domain\Order\Contracts;

use App\Domain\Order\Models\Order;
use App\Domain\Order\ValueObjects\OrderId;

interface OrderRepositoryInterface
{
    public function save(Order $order): void;
    public function findById(OrderId $id): ?Order;
    public function findByCustomer(string $customerId): array;
    public function delete(OrderId $id): void;
}
```

## Eloquent Repository

```php
<?php
// app/Infrastructure/Persistence/Eloquent/Repositories/EloquentOrderRepository.php

namespace App\Infrastructure\Persistence\Eloquent\Repositories;

use App\Domain\Order\Contracts\OrderRepositoryInterface;
use App\Domain\Order\Models\Order;
use App\Domain\Order\ValueObjects\OrderId;
use App\Infrastructure\Persistence\Eloquent\Models\OrderEloquent;
use App\Infrastructure\Persistence\Mappers\OrderMapper;

class EloquentOrderRepository implements OrderRepositoryInterface
{
    public function save(Order $domainOrder): void
    {
        $eloquentOrder = OrderMapper::toEloquent($domainOrder);
        $eloquentOrder->save();

        // Save order items
        $eloquentOrder->items()->delete();
        foreach ($domainOrder->items as $item) {
            $eloquentOrder->items()->create([
                'product_id' => $item->productId,
                'quantity' => $item->quantity,
                'price' => $item->price->amount(),
            ]);
        }
    }

    public function findById(OrderId $id): ?Order
    {
        $eloquent = OrderEloquent::with('items')->find($id->toString());
        return $eloquent ? OrderMapper::toDomain($eloquent) : null;
    }

    public function findByCustomer(string $customerId): array
    {
        return OrderEloquent::with('items')
            ->where('customer_id', $customerId)
            ->get()
            ->map(fn ($e) => OrderMapper::toDomain($e))
            ->all();
    }

    public function delete(OrderId $id): void
    {
        OrderEloquent::destroy($id->toString());
    }
}
```

## Eloquent Model

```php
<?php
// app/Infrastructure/Persistence/Eloquent/Models/OrderEloquent.php

namespace App\Infrastructure\Persistence\Eloquent\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class OrderEloquent extends Model
{
    protected $table = 'orders';

    protected $keyType = 'string';
    public $incrementing = false;

    protected $fillable = [
        'id',
        'customer_id',
        'status',
        'total',
    ];

    public function items(): HasMany
    {
        return $this->hasMany(OrderItemEloquent::class, 'order_id');
    }
}
```

## Mapper

```php
<?php
// app/Infrastructure/Persistence/Mappers/OrderMapper.php

namespace App\Infrastructure\Persistence\Mappers;

use App\Domain\Order\Models\Order;
use App\Domain\Order\Models\OrderItem;
use App\Domain\Order\ValueObjects\Money;
use App\Domain\Order\ValueObjects\OrderId;
use App\Domain\Order\ValueObjects\OrderStatus;
use App\Infrastructure\Persistence\Eloquent\Models\OrderEloquent;

class OrderMapper
{
    public static function toDomain(OrderEloquent $eloquent): Order
    {
        $items = $eloquent->items->map(fn ($item) => new OrderItem(
            productId: $item->product_id,
            quantity: $item->quantity,
            price: new Money($item->price, 'TWD'),
        ))->all();

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

## Domain Event

```php
<?php
// app/Domain/Order/Events/OrderCreated.php

namespace App\Domain\Order\Events;

use App\Domain\Order\ValueObjects\Money;
use App\Domain\Order\ValueObjects\OrderId;
use DateTimeImmutable;

class OrderCreated
{
    public readonly DateTimeImmutable $occurredAt;

    public function __construct(
        public readonly OrderId $orderId,
        public readonly string $customerId,
        public readonly Money $total,
    ) {
        $this->occurredAt = new DateTimeImmutable();
    }
}
```

## Service Provider

```php
<?php
// app/Infrastructure/Providers/RepositoryServiceProvider.php

namespace App\Infrastructure\Providers;

use App\Domain\Order\Contracts\OrderRepositoryInterface;
use App\Domain\User\Contracts\UserRepositoryInterface;
use App\Infrastructure\Persistence\Eloquent\Repositories\EloquentOrderRepository;
use App\Infrastructure\Persistence\Eloquent\Repositories\EloquentUserRepository;
use Illuminate\Support\ServiceProvider;

class RepositoryServiceProvider extends ServiceProvider
{
    public array $bindings = [
        OrderRepositoryInterface::class => EloquentOrderRepository::class,
        UserRepositoryInterface::class => EloquentUserRepository::class,
    ];
}
```

## API Resource

```php
<?php
// app/Http/Resources/OrderResource.php

namespace App\Http\Resources;

use App\Domain\Order\Models\Order;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class OrderResource extends JsonResource
{
    public function __construct(
        private readonly Order $order,
    ) {
        parent::__construct($order);
    }

    public function toArray(Request $request): array
    {
        return [
            'id' => $this->order->id->toString(),
            'customer_id' => $this->order->customerId,
            'status' => $this->order->status->value,
            'total' => $this->order->total->amount(),
            'items' => array_map(fn ($item) => [
                'product_id' => $item->productId,
                'quantity' => $item->quantity,
                'price' => $item->price->amount(),
            ], $this->order->items),
        ];
    }
}
```
