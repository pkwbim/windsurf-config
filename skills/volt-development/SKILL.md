---
name: volt-development
description: "Develops single-file Livewire components with Volt. Activates when creating Volt components, converting Livewire to Volt, working with license: MIT
metadata:
  author: laravel
---
# Volt Development

## When to Apply

Activate this skill when:

- Creating Volt single-file components
- Converting traditional Livewire components to Volt
- Testing Volt components

## Documentation

Use `search-docs` for detailed Volt patterns and documentation.

## Basic Usage

Create components with `[project-specific]`.

Important: Check existing Volt components to determine if they use functional or class-based style before creating new ones.

### Functional Components

```php
@<?php
use function Livewire\Volt\{state, computed};

state(['count' => 0]);

$increment = fn () => $this->count++;
$double = computed(fn () => $this->count * 2);
?>

<div>
    <h1>Count: @{{ $count }} (Double: @{{ $this->double }})</h1>
    <button wire:click="increment">+</button>
</div>
@```

### Class-Based Components

```php
use Livewire\Volt\Component;

new class extends Component {
    public int $count = 0;

    public function increment(): void
    {
        $this->count++;
    }
} ?>

<div>
    <h1>@{{ $count }}</h1>
    <button wire:click="increment">+</button>
</div>
```

## Testing

Tests go in existing Volt test directory or `tests/Feature/Volt`:

```php
use Livewire\Volt\Volt;

test('counter increments', function () {
    Volt::test('counter')
        ->assertSee('Count: 0')
        ->call('increment')
        ->assertSee('Count: 1');
});
```

## Verification

1. Check existing components for functional vs class-based style
2. Test component with `Volt::test()`

## Common Pitfalls

- Not checking existing style (functional vs class-based) before creating
- Forgetting `- Missing `--test` or `--pest` flag when tests are needed