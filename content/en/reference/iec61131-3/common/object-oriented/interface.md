---
title: "INTERFACE / END_INTERFACE"
summary: "Declare a contract of method signatures that any conforming FUNCTION_BLOCK must implement. Interfaces enable polymorphic dispatch through interface-typed variables."
weight: 20
iec_chapter: "6.5.4"
construct_kind: "object-oriented"
keywords: ["INTERFACE", "END_INTERFACE", "EXTENDS", "METHOD", "PROPERTY"]
llm_signals:
  - error_pattern: "Unexpected token: 'INTERFACE'"
    where: "FStCompiler"
    diagnosis: "FStCompiler does not yet implement the IEC 61131-3 third-edition OOP layer. INTERFACE declarations are rejected at parse time."
    fix_strategy: "Until OOP support lands, model interface contracts as a hand-written set of FUNCTION_BLOCK 'base' types with empty method bodies; require implementers to define an FB with a matching member layout and call sites do dispatch by name. Crude but matiec-compatible. Track the OOP roadmap on the section landing page."
  - error_pattern: "matiec: error: missing 'END_INTERFACE'"
    where: "matiec"
    diagnosis: "matiec's grammar has no INTERFACE production. The error surfaces from the parser drifting after the first unrecognised token."
    fix_strategy: "Same workaround as METHOD. Future: switch codegen.target to 'cxx' once C++-emit covers interfaces (roadmap)."
  - error_pattern: "interface method '...' has no implementation in '<FB>'"
    where: "FStAstCxxEmitter (roadmap)"
    diagnosis: "An FB declared `IMPLEMENTS IFoo` is missing a METHOD declaration for an interface member, or the signature does not match (return type / parameter type / parameter name)."
    fix_strategy: "Add the missing METHOD with `OVERRIDE`, matching the interface signature exactly. The compiler will list every missing method when emission starts."
---

## Definition

An `INTERFACE` declares a **contract**: a set of method
signatures (and optionally property signatures) without any
bodies. Any `FUNCTION_BLOCK` that `IMPLEMENTS` the interface
must provide a body for every interface method with an exactly
matching signature.

Interfaces are the IEC 61131-3 mechanism for **polymorphism by
contract**: a variable typed as the interface can hold *any*
FB instance that implements the interface, and a call through
the interface variable dispatches to the concrete FB's
method at run time.

## Syntax

```text
INTERFACE <interface_name> [EXTENDS <base_interface>, <base_interface>, ...]
    METHOD <method_name> [: <return_type>]
        <var_blocks_no_body>
    END_METHOD
    ...
END_INTERFACE
```

- Interface extension is multiple (`EXTENDS A, B, C`) —
  the third edition allows an interface to extend several
  base interfaces. (FUNCTION_BLOCK `EXTENDS` is single-only;
  see [EXTENDS](../extends/).)
- The method declarations carry signatures only — no
  statement-list, no `VAR` block beyond the parameter blocks.
- Properties (`PROPERTY <name> : <type>` with `GET` / `SET`
  bodies omitted) may appear inside an interface.

### Example (roadmap — not yet compilable)

```iec-st
INTERFACE IAccount
    METHOD Deposit
    VAR_INPUT
        amount : LREAL;
    END_VAR
    END_METHOD

    METHOD Withdraw : BOOL
    VAR_INPUT
        amount : LREAL;
    END_VAR
    END_METHOD

    METHOD GetBalance : LREAL
    END_METHOD
END_INTERFACE

FUNCTION_BLOCK BankAccount IMPLEMENTS IAccount
VAR
    balance : LREAL := 0.0;
END_VAR

METHOD PUBLIC OVERRIDE Deposit
VAR_INPUT
    amount : LREAL;
END_VAR
    balance := balance + amount;
END_METHOD

METHOD PUBLIC OVERRIDE Withdraw : BOOL
VAR_INPUT
    amount : LREAL;
END_VAR
    IF balance >= amount THEN
        balance := balance - amount;
        Withdraw := TRUE;
    ELSE
        Withdraw := FALSE;
    END_IF;
END_METHOD

METHOD PUBLIC OVERRIDE GetBalance : LREAL
    GetBalance := balance;
END_METHOD
END_FUNCTION_BLOCK

(* Caller uses the interface type — accepts any IAccount: *)
VAR
    acc : BankAccount;
    iAcc : REFERENCE TO IAccount;
END_VAR
iAcc REF= acc;
iAcc.Deposit(amount := 100.0);
```

## Semantics

- An interface declaration is **not instantiable** on its own
  — there is no storage layout, no constructor. It only fixes
  the contract that implementers must satisfy.
- A variable of an interface type **must be a reference** —
  IEC 61131-3 declares `REFERENCE TO <interface>`. The
  reference is assigned with `REF=` to a concrete FB instance.
- Method calls through the interface reference dispatch
  dynamically: the runtime picks the concrete FB's method
  body. This is the IEC 61131-3 equivalent of a C++ virtual
  call or a Java interface method.
- Interface extension is **subtype-compatible**: a reference
  typed as the base interface can hold an instance whose FB
  implements the derived interface (Liskov substitution).
- Empty interfaces (no methods) are legal — they serve as
  **marker interfaces** that flag a capability without
  prescribing a call shape. Pattern is rare in PLC code.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.5.4** —
"Interfaces". The keywords `INTERFACE`, `END_INTERFACE` are
reserved. `EXTENDS` is documented under the same clause when
used between interfaces; the single-inheritance variant for
FUNCTION_BLOCKs is clause 6.5.5.

## matiec conformance

❌ **Not supported.** No INTERFACE production exists in
matiec's grammar; the parser stops at the first INTERFACE
token. As with [METHOD](../method/), the only matiec-compatible
path is to refactor away from interface-based polymorphism
entirely. Switching to the C++-codegen target (roadmap) is
the supported upgrade path.

## ForgeIEC notes

- **Reference types in interfaces:** the IEC 61131-3 reference
  syntax `REFERENCE TO IAccount` plus `REF=` for assignment
  is its own sub-feature (see the `REFERENCE` / `REF_TO` /
  `REF=` / `NULL` future page). The tree-sitter-st parser
  needs both INTERFACE and REFERENCE tokens before
  end-to-end interface usage compiles.
- **C++ codegen mapping:** the roadmap maps an INTERFACE to a
  C++ abstract base class with pure virtual methods (`virtual
  bool Withdraw(LREAL amount) = 0;`). `IMPLEMENTS` becomes
  public inheritance. Multiple-interface extension uses
  C++ multiple inheritance with abstract bases — which is
  safe because interfaces carry no state.
- **Editor display:** the planned Library-Help-Panel will
  surface interfaces under their own tree-node so that an FB
  picker can show "FBs that implement IAccount" alongside
  the FB itself.

## See also

- [METHOD](../method/) — method declarations inside an
  interface vs inside an implementing FB.
- [EXTENDS](../extends/) — FUNCTION_BLOCK inheritance, which
  is the other half of OO polymorphism.
- [IMPLEMENTS](../implements/) — the FB-side keyword that
  signs the contract.
