---
title: "IMPLEMENTS"
summary: "Declare that a FUNCTION_BLOCK conforms to one or more INTERFACE contracts. The compiler enforces that every interface method has a matching METHOD implementation."
weight: 40
iec_chapter: "6.5.5"
construct_kind: "object-oriented"
keywords: ["IMPLEMENTS", "INTERFACE", "OVERRIDE", "METHOD", "PROPERTY"]
llm_signals:
  - error_pattern: "Unexpected token: 'IMPLEMENTS'"
    where: "FStCompiler"
    diagnosis: "FStCompiler does not yet implement the IEC 61131-3 third-edition OOP layer. Interface implementation declarations are rejected at parse time."
    fix_strategy: "Until OOP support lands, model 'I implement interface X' as a comment + naming convention. Implementer FBs name their methods to match X's signatures; call sites use the concrete FB type instead of an interface-typed reference. No dynamic dispatch — every call site picks the FB type explicitly. Track the OOP roadmap on the section landing page."
  - error_pattern: "FB '...' implements '...' but is missing method '...'"
    where: "FStAstCxxEmitter (roadmap)"
    diagnosis: "An FB declared `IMPLEMENTS IFoo` does not provide a METHOD body for one of IFoo's required methods. The emitter cannot generate the FB class because the C++ class would be abstract."
    fix_strategy: "Add the missing METHOD declarations with `OVERRIDE`, matching IFoo's signatures exactly (return type, parameter names + types in order)."
  - error_pattern: "method '...' in FB '...' has signature mismatch with interface '...'"
    where: "FStAstCxxEmitter (roadmap)"
    diagnosis: "An IMPLEMENTS method's signature does not match the interface's. Typically return type or parameter type drift."
    fix_strategy: "Open the interface declaration, copy the exact METHOD signature into the FB, then write the body. The interface and the FB must agree byte-for-byte on signatures."
  - error_pattern: "ambiguous method '...' from interfaces '...' and '...'"
    where: "FStAstCxxEmitter (roadmap)"
    diagnosis: "Two interfaces an FB implements both declare a method with the same name but incompatible signatures. The compiler cannot pick one implementation to satisfy both contracts."
    fix_strategy: "Rename the method on one of the interfaces (if you control it) or refactor the FB into two separate FBs that each implement one interface."
---

## Definition

`IMPLEMENTS <iface_list>` declares that a `FUNCTION_BLOCK`
honours one or more `INTERFACE` contracts. The FB must provide
a `METHOD` body for every method declared on every named
interface, with **exactly matching signatures**.

`IMPLEMENTS` is orthogonal to [EXTENDS](../extends/): an FB
can extend zero or one base FBs and implement zero or more
interfaces simultaneously. Multiple interface implementation
(e.g. `IMPLEMENTS IFoo, IBar, IBaz`) is the IEC 61131-3 escape
from the single-inheritance restriction on FBs.

## Syntax

```text
FUNCTION_BLOCK <name> [EXTENDS <base_fb>] IMPLEMENTS <iface_1>, <iface_2>, ...
    <var_blocks>
    METHOD PUBLIC OVERRIDE <iface_method> [: <return_type>]
        <var_blocks_for_method>
        <statement_list>
    END_METHOD
    ...
END_FUNCTION_BLOCK
```

The `OVERRIDE` modifier on each implementing method is
recommended (and required by ForgeIEC's emitter) so that
typos in method names are caught early — without `OVERRIDE`,
a misnamed method silently adds a new method to the FB
without satisfying the interface contract, and the missing-
method error appears only at the call site.

### Example (roadmap — not yet compilable)

```iec-st
INTERFACE ILogger
    METHOD Log
    VAR_INPUT
        msg : STRING;
    END_VAR
    END_METHOD
END_INTERFACE

INTERFACE IPersistent
    METHOD Save : BOOL
    END_METHOD

    METHOD Load : BOOL
    END_METHOD
END_INTERFACE

(* SavingsAccount inherits from BankAccount and additionally
   implements two unrelated interfaces. *)
FUNCTION_BLOCK SavingsAccount EXTENDS BankAccount IMPLEMENTS ILogger, IPersistent
VAR
    interestRate : LREAL := 0.02;
    persistPath  : STRING := 'savings.dat';
END_VAR

METHOD PUBLIC OVERRIDE Log
VAR_INPUT
    msg : STRING;
END_VAR
    (* ... write to recent-logs sink ... *)
END_METHOD

METHOD PUBLIC OVERRIDE Save : BOOL
    (* ... serialise balance to persistPath ... *)
    Save := TRUE;
END_METHOD

METHOD PUBLIC OVERRIDE Load : BOOL
    (* ... read balance from persistPath ... *)
    Load := TRUE;
END_METHOD
END_FUNCTION_BLOCK

(* Call sites can target either interface independently: *)
VAR
    acc : SavingsAccount;
    log : REFERENCE TO ILogger;
    psv : REFERENCE TO IPersistent;
END_VAR
log REF= acc;
psv REF= acc;
log.Log(msg := 'opened account');
psv.Save();
```

## Semantics

- **Interface satisfaction** is checked at compile time. Every
  method on every implemented interface must have a body in the
  implementing FB (directly, or inherited from an
  `EXTENDS`-base that itself implemented the method). Methods
  not declared in any implemented interface are simply
  additional methods on the FB.
- **Multiple-interface methods with the same name** must have
  compatible signatures — same return type, same parameter
  list. If they conflict, the compiler refuses the FB. There
  is no IEC mechanism for "implement Foo of IFoo and Foo of
  IBar separately"; the FB has one Foo method that satisfies
  both interface obligations.
- **Dynamic dispatch** flows through interface references
  exactly as for [EXTENDS](../extends/): a `REFERENCE TO
  ILogger` pointing at a `SavingsAccount` instance calls
  `SavingsAccount.Log`, even though the call site sees only
  the `ILogger` type.
- **Interface inheritance compatibility** — when an interface
  extends another (`INTERFACE IDerived EXTENDS IBase`),
  implementing `IDerived` automatically signs the contract for
  `IBase` too. An FB that `IMPLEMENTS IDerived` does not also
  need to list `IBase`.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.5.5** —
"Inheritance" covers both `EXTENDS` and `IMPLEMENTS`. Cross-
reference [INTERFACE](../interface/) for the contract side
of the relationship.

## matiec conformance

❌ **Not supported.** matiec's grammar does not recognise
`IMPLEMENTS`; the parser stops on the FB header line. The
workaround is exactly the same as for `EXTENDS`: use naming
conventions and explicit FB types at every call site so
polymorphism is unnecessary. Switching to the C++-codegen
target is the supported upgrade path once that emitter
covers OOP (roadmap).

## ForgeIEC notes

- **C++ codegen mapping** — the roadmap maps `IMPLEMENTS
  IFoo, IBar` to public C++ inheritance from each interface's
  abstract base class. Since interfaces declare no state, the
  diamond problem in classical C++ multiple inheritance does
  not arise. Each interface method becomes a `virtual`
  function override.
- **Property implementation** — interfaces may declare
  `PROPERTY` accessors (`GET` and `SET` blocks); an FB that
  `IMPLEMENTS` such an interface must provide the
  corresponding `PROPERTY` blocks with bodies. This is on
  the same TS-ST-Cleanup Phase 2 sprint queue as METHOD /
  INTERFACE.
- **Editor library-picker filter** — the planned Library-
  Help-Panel will let you filter FBs by interface, so that
  "find me all FBs that implement `IPersistent`" is a
  one-click action. Until then, search the FB catalogue
  manually by inspecting each FB's `IMPLEMENTS` clause.

## See also

- [INTERFACE](../interface/) — the contract side.
- [METHOD](../method/) — the bodies that satisfy interface
  contracts; required `OVERRIDE` modifier.
- [EXTENDS](../extends/) — orthogonal mechanism; an FB may
  extend a base and implement interfaces in the same header.
