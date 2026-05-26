---
title: "Object-oriented extensions"
summary: "METHOD, INTERFACE, EXTENDS, IMPLEMENTS and the rest of the IEC 61131-3 third-edition OOP layer. ForgeIEC parses these constructs, matiec does not."
weight: 70
---

## Object-oriented extensions

IEC 61131-3 **third edition** (2013) introduced an object-oriented
layer on top of the FUNCTION_BLOCK POU: classes can declare
**methods**, **interfaces** describe contracts, and FBs can
**extend** a base FB or **implement** an interface. The third
edition also defined access-modifier visibility (`PUBLIC` /
`PRIVATE` / `PROTECTED` / `INTERNAL`), the `THIS` / `SUPER`
self-references, properties with `GET` / `SET` accessors, the
`ABSTRACT` / `FINAL` / `OVERRIDE` modifiers, namespaces, and
reference types.

ForgeIEC's parser (tree-sitter-st) is being extended to cover
the OOP layer ahead of the codegen pipeline that emits it.
**matiec does not implement any of these constructs** — when
ForgeIEC's codegen target is `c` (matiec/iec2c, deprecated since
Phase 6 of the ST→C++-Codegen-Sprint), POUs using OOP fail to
compile. With the C++-codegen pipeline (`target = "cxx"`,
default since Phase 5), OOP support is **on the roadmap** but
not yet emitted.

Refer to the individual pages for the current status of each
construct.

## Pages

- [METHOD / END_METHOD](method/) — declare a method on a
  FUNCTION_BLOCK. Methods carry their own VAR-block and
  signature; they are called with `<fb_instance>.<method>(...)`
  syntax.
- [INTERFACE / END_INTERFACE](interface/) — declare a contract
  of method signatures that conforming FBs must implement.
  Interfaces enable polymorphic dispatch via interface-typed
  variables.
- [EXTENDS](extends/) — single inheritance between
  FUNCTION_BLOCKs. The derived FB inherits the base's members
  and methods, may override methods, and gains access to the
  base via `SUPER`.
- [IMPLEMENTS](implements/) — declare that a FUNCTION_BLOCK
  conforms to one or more interfaces. Compiler enforces that
  every interface method is implemented with a matching
  signature.

## Out-of-section but related

The following OOP-adjacent constructs live on other pages:

- `THIS` / `SUPER` — implicit references inside methods.
  Documented on the [METHOD](method/) page.
- `ABSTRACT` / `FINAL` / `OVERRIDE` — method/class modifiers.
  Documented on the [METHOD](method/) and [EXTENDS](extends/)
  pages.
- `PUBLIC` / `PRIVATE` / `PROTECTED` / `INTERNAL` — visibility
  modifiers. Documented in
  [variable-declarations/](../variable-declarations/) (TBD —
  separate page once tree-sitter-st emits the tokens).
- `PROPERTY` / `GET` / `SET` — property accessors. Future
  page, currently a stub in the chapter-map.
- `NAMESPACE` / `END_NAMESPACE` / `USING` / `::` — namespace
  declarations and the scope-resolution operator. Future page.
- `REFERENCE` / `REF_TO` / `REF=` / `NULL` — reference types
  for OOP polymorphism. Future page.

## IEC reference

IEC 61131-3 third edition (2013), clauses **6.5.3** (METHOD),
**6.5.4** (INTERFACE), **6.5.5** (EXTENDS / IMPLEMENTS),
**6.5.6** (THIS / SUPER), **6.5.7** (Properties), **6.5.8**
(visibility / modifiers).

## ForgeIEC roadmap

| Construct | tree-sitter-st | FStCompiler | FStAstCxxEmitter | matiec |
|---|---|---|---|---|
| `METHOD` | 🔜 planned | ❌ | 🔜 planned | ❌ |
| `INTERFACE` | 🔜 planned | ❌ | 🔜 planned | ❌ |
| `EXTENDS` | 🔜 planned | ❌ | 🔜 planned | ❌ |
| `IMPLEMENTS` | 🔜 planned | ❌ | 🔜 planned | ❌ |
| `THIS` / `SUPER` | 🔜 planned | ❌ | 🔜 planned | ❌ |
| `ABSTRACT` / `FINAL` / `OVERRIDE` | 🔜 planned | ❌ | 🔜 planned | ❌ |
| `PUBLIC` / `PRIVATE` / `PROTECTED` / `INTERNAL` | 🔜 planned | ❌ | 🔜 planned | ❌ |
| `PROPERTY` / `GET` / `SET` | 🔜 planned | ❌ | 🔜 planned | ❌ |
| `NAMESPACE` / `USING` / `::` | 🔜 planned | ❌ | 🔜 planned | ❌ |
| `REFERENCE` / `REF_TO` / `REF=` / `NULL` | 🔜 planned | ❌ | 🔜 planned | ❌ |

The TS-ST-Cleanup Phase 2 sprint adds the OOP tokens to the
parser. Once the parser sees them, the AST-walker is extended
with OO-aware IR nodes, the emitter learns to map them to C++
classes/inheritance/virtual-dispatch, and these pages become
implementation reference instead of roadmap pages.
