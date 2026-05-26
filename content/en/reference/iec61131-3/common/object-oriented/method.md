---
title: "METHOD / END_METHOD"
summary: "Declare a named operation on a FUNCTION_BLOCK class. Methods carry their own VAR-block, signature, and body — they are called with dot syntax on an FB instance."
weight: 10
iec_chapter: "6.5.3"
construct_kind: "object-oriented"
keywords: ["METHOD", "END_METHOD", "THIS", "ABSTRACT", "FINAL", "OVERRIDE", "PUBLIC", "PRIVATE", "PROTECTED", "INTERNAL"]
llm_signals:
  - error_pattern: "Unexpected token: 'METHOD'"
    where: "FStCompiler"
    diagnosis: "FStCompiler does not yet implement the IEC 61131-3 third-edition OOP layer. METHOD declarations are rejected at parse time."
    fix_strategy: "Until OOP support lands in FStCompiler, refactor the method body into a separate FUNCTION or FUNCTION_BLOCK that takes the would-be `THIS` data as an explicit VAR_IN_OUT parameter. Track the OOP roadmap on the section landing page."
    fix_example: |
      (* before — fails: Unexpected token: 'METHOD' *)
      FUNCTION_BLOCK Counter
      VAR
          count : INT := 0;
      END_VAR
      METHOD PUBLIC Increment : BOOL
          count := count + 1;
          Increment := TRUE;
      END_METHOD
      END_FUNCTION_BLOCK
      (* after — compiles today *)
      FUNCTION_BLOCK Counter
      VAR
          count : INT := 0;
      END_VAR
      END_FUNCTION_BLOCK

      FUNCTION CounterIncrement : BOOL
      VAR_IN_OUT
          c : Counter;
      END_VAR
          c.count := c.count + 1;
          CounterIncrement := TRUE;
      END_FUNCTION
  - error_pattern: "matiec: error: missing 'END_METHOD'"
    where: "matiec"
    diagnosis: "matiec's grammar (iec_bison.yy) does not include METHOD productions at all. The above error is the closest matiec gets — it parses tokens individually but never accepts a METHOD body."
    fix_strategy: "matiec cannot compile OOP. Switch the codegen target to `cxx` once the C++-codegen pipeline supports METHOD (roadmap item, not yet emitted). For matiec-compatible workarounds, see the FUNCTION refactor above."
  - error_pattern: "ForgeIEC: method '...' has no body but is not marked ABSTRACT"
    where: "FStAstCxxEmitter (roadmap)"
    diagnosis: "Once OOP emission lands, a METHOD declared without a body must carry the ABSTRACT modifier — otherwise the C++ emitter cannot resolve which class implements the call."
    fix_strategy: "Either add ABSTRACT to the method header, or add a body — even an empty one is legal as long as the return-variable assignment is satisfied for a value-returning method."
---

## Definition

A `METHOD` is a named operation that belongs to a
`FUNCTION_BLOCK` class. It declares its own input/output/inout
variables, optional local `VAR` block, and a body. Inside the
body, the surrounding FB's members are reachable directly (and
explicitly via `THIS.<member>`). Callers invoke a method with
**dot syntax** on an FB instance: `myFb.MyMethod(in := 1)`.

Methods generalize the single implicit "cycle" call of a plain
FUNCTION_BLOCK: an FB with methods can carry multiple named
operations without each one needing its own FB instance.

## Syntax

```text
METHOD [<access_modifier>] [<class_modifier>] <method_name> [: <return_type>]
    <var_blocks>
    <statement_list>
END_METHOD
```

- `<access_modifier>` — `PUBLIC` (default) / `PRIVATE` /
  `PROTECTED` / `INTERNAL`. Controls visibility for callers
  outside the FB / a derived FB / the namespace.
- `<class_modifier>` — `ABSTRACT` (no body, derived FB must
  override) / `FINAL` (derived FB cannot override) /
  `OVERRIDE` (explicit override of a base-class method).
- `<return_type>` — optional. Without it, the method has no
  return value (analogous to a `void` C function); with it,
  the body must assign `<method_name> := <expr>` before
  `END_METHOD`.
- `<var_blocks>` — any of `VAR_INPUT`, `VAR_OUTPUT`,
  `VAR_IN_OUT`, `VAR`, `VAR_TEMP`. No `VAR_GLOBAL` /
  `VAR_EXTERNAL` inside a method.

### Example (roadmap — not yet compilable)

```iec-st
FUNCTION_BLOCK BankAccount
VAR
    balance : LREAL := 0.0;
    overdraftLimit : LREAL := 0.0;
END_VAR

METHOD PUBLIC Deposit
VAR_INPUT
    amount : LREAL;
END_VAR
    balance := balance + amount;
END_METHOD

METHOD PUBLIC Withdraw : BOOL
VAR_INPUT
    amount : LREAL;
END_VAR
    IF balance - amount < -overdraftLimit THEN
        Withdraw := FALSE;
    ELSE
        balance := balance - amount;
        Withdraw := TRUE;
    END_IF;
END_METHOD

METHOD PUBLIC GetBalance : LREAL
    GetBalance := balance;
END_METHOD
END_FUNCTION_BLOCK

(* Caller: *)
VAR
    acc : BankAccount;
    ok  : BOOL;
END_VAR
acc.Deposit(amount := 100.0);
ok := acc.Withdraw(amount := 30.0);
```

## Semantics

- Each method call binds to **the FB instance the caller
  named** — `myFb.MyMethod(...)` operates on `myFb`'s data;
  `otherFb.MyMethod(...)` operates on `otherFb`'s data. There
  is no shared state between instances unless the FB declares
  it via static members (not part of IEC 61131-3).
- Methods see all of the enclosing FB's `VAR` / `VAR_INPUT` /
  `VAR_OUTPUT` / `VAR_IN_OUT` members. `THIS` is the explicit
  reference to the current instance; bare member names resolve
  to `THIS.<member>` implicitly.
- A method's `VAR` block is **per-call local storage**, not
  per-instance. Two consecutive calls to `myFb.MyMethod()` do
  not see each other's `VAR` values.
- Method dispatch is **static** when the variable holding the
  FB instance has the concrete FB type (the compiler resolves
  the call at compile time). Dispatch becomes **dynamic
  (virtual)** when the variable has an interface type or a
  base-class type from which the actual instance derives — see
  [INTERFACE](../interface/) and [EXTENDS](../extends/).
- `ABSTRACT` methods have no body. The enclosing FB must
  itself be abstract or implement an interface that declares
  the method; either way no instance of the abstract FB can
  be created directly. A derived FB must provide a body
  before instantiation becomes legal.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.5.3** — "Methods".
The keywords `METHOD`, `END_METHOD`, `THIS` are reserved.
Access modifiers `PUBLIC`, `PRIVATE`, `PROTECTED`, `INTERNAL`
and class modifiers `ABSTRACT`, `FINAL`, `OVERRIDE` are
reserved (clauses 6.5.3.2 / 6.5.3.3).

## matiec conformance

❌ **Not supported.** matiec's grammar (`utils/matiec_src/lib/
iec_bison.yy`) does not include any METHOD production. Source
files that contain `METHOD … END_METHOD` blocks fail at
parse-time with an "unexpected token" error.

ForgeIEC's older codegen pipeline (`codegen.target = "c"`,
deprecated since Phase 6 of the ST→C++-Codegen-Sprint) routes
through matiec and therefore inherits this limitation.

## ForgeIEC notes

- **tree-sitter-st parser:** the METHOD/END_METHOD tokens are
  on the TS-ST-Cleanup Phase 2 sprint queue together with
  PROPERTY / NAMESPACE / REFERENCE. Until that lands, the
  ForgeIEC editor highlights `METHOD` as an unknown identifier
  and the AST walker treats the block as an ERROR node — which
  surfaces in `codegen.lint`'s `parse_diagnostics[]` array
  (see the [Parser-Error-Reporting Sprint](
  /reference/iec61131-3/_index.md#error-reporting) for the
  diagnostic format).
- **FStAstCxxEmitter (C++ codegen):** the roadmap maps METHOD
  declarations to C++ member functions on the generated
  POU class (`class GenBankAccount { … bool Withdraw(LREAL
  amount); }`). Visibility modifiers map directly (`public:`,
  `private:`, `protected:`). `ABSTRACT` maps to `= 0` pure
  virtual; `FINAL` to `final`; `OVERRIDE` to `override`.
- **Workaround today** — see the first `llm_signals` entry.
  Refactor methods to free-standing functions or function
  blocks that take the data they operate on as a
  `VAR_IN_OUT` parameter. The call site `acc.Withdraw(amount
  := 30.0)` becomes `WithdrawFromAccount(c := acc, amount :=
  30.0)`. Slightly less ergonomic, fully matiec-compatible.

## See also

- [INTERFACE](../interface/) — methods declared on an
  interface set the contract that implementing FBs satisfy.
- [EXTENDS](../extends/) — inherited methods, `SUPER` calls,
  `OVERRIDE` modifier.
- [variable declarations](../../variable-declarations/) — the
  `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP` /
  `VAR` blocks used inside a method header.
