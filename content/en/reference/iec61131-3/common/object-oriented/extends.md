---
title: "EXTENDS"
summary: "Single inheritance between FUNCTION_BLOCKs. The derived FB inherits members and methods, may override methods, and reaches the base through SUPER."
weight: 30
iec_chapter: "6.5.5"
construct_kind: "object-oriented"
keywords: ["EXTENDS", "SUPER", "OVERRIDE", "FINAL", "ABSTRACT", "FUNCTION_BLOCK"]
llm_signals:
  - error_pattern: "Unexpected token: 'EXTENDS'"
    where: "FStCompiler"
    diagnosis: "FStCompiler does not yet implement the IEC 61131-3 third-edition OOP layer. FB inheritance is rejected at parse time."
    fix_strategy: "Until OOP support lands, simulate inheritance by composition: declare the would-be base FB as a member of the derived FB (`base : BaseFb;`) and forward calls explicitly. Less ergonomic than EXTENDS but matiec-compatible."
    fix_example: |
      (* before — fails: Unexpected token: 'EXTENDS' *)
      FUNCTION_BLOCK CountingTimer EXTENDS TON
      VAR
          ticks : INT := 0;
      END_VAR
      METHOD PUBLIC OVERRIDE Increment
          ticks := ticks + 1;
          SUPER.Increment();
      END_METHOD
      END_FUNCTION_BLOCK
      (* after — compiles today via composition *)
      FUNCTION_BLOCK CountingTimer
      VAR
          base : TON;
          ticks : INT := 0;
      END_VAR
      VAR_INPUT
          IN : BOOL;
          PT : TIME;
      END_VAR
      VAR_OUTPUT
          Q : BOOL;
          ET : TIME;
      END_VAR
          base(IN := IN, PT := PT);
          Q  := base.Q;
          ET := base.ET;
          ticks := ticks + 1;
      END_FUNCTION_BLOCK
  - error_pattern: "method '...' marked OVERRIDE but base FB has no such method"
    where: "FStAstCxxEmitter (roadmap)"
    diagnosis: "An OVERRIDE method declaration in a derived FB does not match any method in the base FB chain — either the name is misspelled, the signature differs, or the base method is marked FINAL."
    fix_strategy: "Verify the base FB's method signature exactly (name, return type, parameter names + types in order). If the base method is FINAL, the derived FB cannot override it — drop the OVERRIDE and pick a new method name."
  - error_pattern: "cannot extend FINAL FUNCTION_BLOCK '...'"
    where: "FStAstCxxEmitter (roadmap)"
    diagnosis: "The base FB is declared `FINAL`, which forbids further derivation."
    fix_strategy: "Either remove the FINAL marker from the base FB (if you own it) or compose instead of extending."
---

## Definition

`EXTENDS <base_fb>` makes a `FUNCTION_BLOCK` a **derived FB**
of a single named base FB. The derived FB:

1. Inherits all of the base FB's `VAR` / `VAR_INPUT` /
   `VAR_OUTPUT` / `VAR_IN_OUT` members.
2. Inherits all of the base FB's non-`PRIVATE` methods.
3. May add new members and new methods.
4. May `OVERRIDE` any non-`FINAL` inherited method with a
   matching signature.
5. May call the base implementation explicitly via
   `SUPER.<method>(...)` inside an override.

Inheritance is **single only** — an FB extends at most one
base FB. Multiple-inheritance from interfaces is available via
[IMPLEMENTS](../implements/), which is orthogonal: an FB can
both `EXTENDS BaseFb` and `IMPLEMENTS IFoo, IBar`.

## Syntax

```text
FUNCTION_BLOCK [ABSTRACT | FINAL] <derived_name> EXTENDS <base_fb> [IMPLEMENTS <iface>, ...]
    <var_blocks>
    METHOD [PUBLIC | PROTECTED] [OVERRIDE | FINAL] <method_name> [: <return_type>]
        ...
    END_METHOD
    ...
END_FUNCTION_BLOCK
```

- `ABSTRACT` — the derived FB still cannot be instantiated
  (one or more methods remain abstract).
- `FINAL` — no further FB can extend this one.
- `OVERRIDE` — explicit acknowledgement that this method
  overrides a base-class method with the same signature. The
  IEC standard recommends but does not strictly mandate the
  modifier; ForgeIEC's emitter rejects accidental shadowing
  (a method without `OVERRIDE` whose signature matches a base
  method) as a likely error.

### Example (roadmap — not yet compilable)

```iec-st
FUNCTION_BLOCK SavingsAccount EXTENDS BankAccount
VAR
    interestRate : LREAL := 0.02;
END_VAR

METHOD PUBLIC AddInterest
    balance := balance * (1.0 + interestRate);   (* inherited member *)
END_METHOD

METHOD PUBLIC OVERRIDE Withdraw : BOOL
VAR_INPUT
    amount : LREAL;
END_VAR
    (* Savings: refuse to overdraft. Delegate to base for the
       balance update, then enforce the no-overdraft policy. *)
    IF balance < amount THEN
        Withdraw := FALSE;
    ELSE
        Withdraw := SUPER.Withdraw(amount := amount);
    END_IF;
END_METHOD
END_FUNCTION_BLOCK
```

## Semantics

- **Member layout** — the derived FB's data layout starts with
  the base FB's members, in their declaration order, followed
  by the derived FB's own members. This guarantees that a
  reference to the base FB can address an instance of the
  derived FB without offset adjustment.
- **Method dispatch** — when a derived FB overrides a base
  method, the override wins at every call site that addresses
  the derived FB instance, *including* calls through a base-
  typed or interface-typed reference. This is dynamic dispatch.
- **SUPER** — only legal inside a method body. Calls the base
  FB's version of a method by name, bypassing the override
  resolution. Useful for "do the base behaviour and add
  something on top" patterns.
- **Initialization** — the base FB's initial-value list runs
  before the derived FB's. The derived FB cannot change the
  base's initial values inline; if it needs different starting
  values, it must reset them in the cycle body or via an
  initialisation method.
- **Type compatibility** — a variable of base-FB type may
  point at any derived-FB instance. The reverse (base
  instance assigned to a derived-typed variable) is illegal
  unless you go through an explicit downcast (a third-edition
  feature not yet in the keyword tables above).

## IEC reference

IEC 61131-3 third edition (2013), clause **6.5.5** —
"Inheritance". The keyword `EXTENDS` is reserved. `SUPER`,
`OVERRIDE`, `FINAL`, `ABSTRACT` are reserved (clauses 6.5.5.2
through 6.5.5.5).

## matiec conformance

❌ **Not supported.** matiec's grammar treats `EXTENDS` as an
unknown identifier. The parser breaks on the FB header line.
For matiec-compatible code, replace inheritance with the
composition workaround in the first `llm_signals` block: the
derived FB carries the base FB as a member and forwards calls
manually. You lose dynamic dispatch and override sugar; you
keep matiec compatibility.

## ForgeIEC notes

- **Cycle behaviour vs OO behaviour** — the implicit FB-cycle
  (the body that runs every task cycle when the FB is named as
  a step in a task's POU list) is *not* a virtual method. A
  derived FB's body runs in place of the base's body; there
  is no `SUPER`-call on the implicit cycle. If you need
  layered cycle behaviour, declare an explicit method called
  e.g. `Cycle` and call `SUPER.Cycle()` from the override.
  The implicit cycle body is then a stub that calls
  `THIS.Cycle()`.
- **C++ codegen mapping** — the roadmap maps a `FUNCTION_BLOCK
  Derived EXTENDS Base` to `class GenDerived : public
  GenBase { ... }`. Override methods carry `override`;
  `FINAL` carries `final`; `ABSTRACT` makes the method pure
  virtual. Multiple-interface implementation adds further
  base-class entries (`class GenDerived : public GenBase,
  public IFoo, public IBar`); since interfaces are
  state-free, the diamond problem does not arise.
- **Migration path from composition** — the workaround in the
  `llm_signals` block (composition over inheritance) is
  forward-compatible. Once the OOP codegen lands, you can
  convert each `base : BaseFb;` member + forwarder
  boilerplate to an actual `EXTENDS BaseFb` declaration with
  a mechanical refactor. Behaviour stays the same; the call
  sites get cleaner.

## See also

- [METHOD](../method/) — method declarations, including the
  `OVERRIDE` / `FINAL` / `ABSTRACT` modifiers.
- [INTERFACE](../interface/) — multiple-interface
  implementation via [IMPLEMENTS](../implements/), orthogonal
  to FB inheritance.
- [IMPLEMENTS](../implements/) — the keyword that pairs with
  `EXTENDS` when an FB both inherits and implements
  interfaces.
