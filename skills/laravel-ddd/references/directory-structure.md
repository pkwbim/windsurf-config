# Directory Structure

## Table of Contents
- [Full Directory Tree](#full-directory-tree)
- [Domain Layer](#domain-layer)
- [Application Layer](#application-layer)
- [Infrastructure Layer](#infrastructure-layer)
- [Http Layer](#http-layer)
- [Shared Domain](#shared-domain)
- [Namespace Configuration](#namespace-configuration)

## Full Directory Tree

```
app/
├── Domain/
│   ├── Order/                           # Bounded Context: Order
│   │   ├── Models/
│   │   │   ├── Order.php                # Domain Model (pure PHP)
│   │   │   └── OrderItem.php
│   │   ├── ValueObjects/
│   │   │   ├── OrderId.php
│   │   │   ├── Money.php
│   │   │   └── OrderStatus.php          # Enum
│   │   ├── Actions/
│   │   │   ├── CreateOrderAction.php
│   │   │   ├── CancelOrderAction.php
│   │   │   └── ApplyDiscountAction.php
│   │   ├── DTOs/
│   │   │   ├── CreateOrderData.php
│   │   │   └── OrderSummaryData.php
│   │   ├── Events/
│   │   │   ├── OrderCreated.php
│   │   │   └── OrderCancelled.php
│   │   ├── Exceptions/
│   │   │   ├── OrderCannotBeCancelled.php
│   │   │   └── InsufficientStockException.php
│   │   └── Contracts/
│   │       ├── OrderRepositoryInterface.php
│   │       └── OrderPricingServiceInterface.php
│   │
│   ├── User/                            # Bounded Context: User
│   │   ├── Models/
│   │   │   └── User.php
│   │   ├── ValueObjects/
│   │   │   ├── UserId.php
│   │   │   └── Email.php
│   │   ├── Actions/
│   │   │   ├── RegisterUserAction.php
│   │   │   └── UpdateProfileAction.php
│   │   ├── DTOs/
│   │   │   └── RegisterUserData.php
│   │   ├── Events/
│   │   │   └── UserRegistered.php
│   │   └── Contracts/
│   │       └── UserRepositoryInterface.php
│   │
│   └── Shared/                          # Cross-context shared code
│       ├── ValueObjects/
│       │   ├── Money.php
│       │   └── Currency.php
│       └── Contracts/
│           └── DomainEventInterface.php
│
├── Application/
│   ├── Order/
│   │   └── Services/
│   │       └── OrderService.php         # Orchestrates Order Actions
│   └── User/
│       └── Services/
│           └── UserService.php
│
├── Infrastructure/
│   ├── Persistence/
│   │   ├── Eloquent/
│   │   │   ├── Models/
│   │   │   │   ├── OrderEloquent.php    # Eloquent Model
│   │   │   │   ├── OrderItemEloquent.php
│   │   │   │   └── UserEloquent.php
│   │   │   └── Repositories/
│   │   │       ├── EloquentOrderRepository.php
│   │   │       └── EloquentUserRepository.php
│   │   └── Mappers/
│   │       ├── OrderMapper.php          # Eloquent ↔ Domain
│   │       ├── OrderItemMapper.php
│   │       └── UserMapper.php
│   ├── External/
│   │   ├── PaymentGateway/
│   │   │   └── StripePaymentService.php
│   │   └── Notification/
│   │       └── MailNotificationService.php
│   └── Providers/
│       ├── RepositoryServiceProvider.php
│       ├── OrderServiceProvider.php
│       └── UserServiceProvider.php
│
└── Http/
    ├── Controllers/
    │   └── Api/
    │       ├── OrderController.php
    │       └── UserController.php
    ├── Requests/
    │   ├── CreateOrderRequest.php
    │   └── RegisterUserRequest.php
    └── Resources/
        ├── OrderResource.php
        └── UserResource.php
```

## Domain Layer

Rules:
- Zero Laravel imports — no `use Illuminate\...`
- No Eloquent, no DB facade, no Query Builder
- Pure PHP classes only
- Business rules and invariants enforced here

### File Naming

| Type | Convention | Example |
|------|-----------|---------|
| Domain Model | `{Name}.php` | `Order.php` |
| Value Object | `{Name}.php` | `Money.php` |
| Action | `{Verb}{Noun}Action.php` | `CreateOrderAction.php` |
| DTO | `{Verb}{Noun}Data.php` | `CreateOrderData.php` |
| Event | `{Noun}{PastVerb}.php` | `OrderCreated.php` |
| Exception | `{Description}Exception.php` | `InsufficientStockException.php` |
| Interface | `{Name}Interface.php` | `OrderRepositoryInterface.php` |

## Application Layer

Rules:
- Orchestrate Domain Actions — do NOT contain business logic
- Handle transactions (`DB::transaction()` wraps here)
- May dispatch jobs/queues
- One Service per Bounded Context

### File Naming

| Type | Convention | Example |
|------|-----------|---------|
| Service | `{Context}Service.php` | `OrderService.php` |

## Infrastructure Layer

Rules:
- Implement Domain Contracts (Interfaces)
- Eloquent Models live here, suffixed with `Eloquent`
- Mapper classes convert between Eloquent ↔ Domain Models
- Service Providers bind Interface → Implementation

### File Naming

| Type | Convention | Example |
|------|-----------|---------|
| Eloquent Model | `{Name}Eloquent.php` | `OrderEloquent.php` |
| Repository | `Eloquent{Name}Repository.php` | `EloquentOrderRepository.php` |
| Mapper | `{Name}Mapper.php` | `OrderMapper.php` |
| Provider | `{Context}ServiceProvider.php` | `OrderServiceProvider.php` |

## Http Layer

Rules:
- Controllers: receive request, delegate to Service/Action, return response
- FormRequests: validation only, no business logic
- Resources: response formatting only

### File Naming

| Type | Convention | Example |
|------|-----------|---------|
| Controller | `{Name}Controller.php` | `OrderController.php` |
| Request | `{Verb}{Name}Request.php` | `CreateOrderRequest.php` |
| Resource | `{Name}Resource.php` | `OrderResource.php` |

## Shared Domain

Use `Domain/Shared/` sparingly for truly cross-cutting concerns:
- Common Value Objects (Money, Currency)
- Shared Interfaces (DomainEventInterface)
- Base classes if absolutely necessary

**NEVER** put context-specific logic in Shared.

## Namespace Configuration

Add to `composer.json` autoload:

```json
{
    "autoload": {
        "psr-4": {
            "App\\": "app/",
            "App\\Domain\\": "app/Domain/",
            "App\\Application\\": "app/Application/",
            "App\\Infrastructure\\": "app/Infrastructure/"
        }
    }
}
```

Register Service Providers in `config/app.php`:

```php
'providers' => [
    // ...
    App\Infrastructure\Providers\RepositoryServiceProvider::class,
    App\Infrastructure\Providers\OrderServiceProvider::class,
    App\Infrastructure\Providers\UserServiceProvider::class,
],
```
