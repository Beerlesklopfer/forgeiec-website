---
title: "تغطية الاختبارات"
summary: "ضمان الجودة الآلي: 117 اختبارًا يتحقق من مفردات IEC 61131-3 الكاملة وجميع الكتل القياسية ونظام المهام المتعددة"
---

يتم حماية ForgeIEC من خلال مجموعة اختبارات آلية شاملة.
يتم التحقق من كل commit قبل الدمج مقابل **117 اختبار وحدة** تغطي
مفردات IEC 61131-3 Structured Text الكاملة وجميع الكتل الوظيفية
القياسية ونظام المهام المتعددة.

## نظرة عامة على مجموعات الاختبار

| المجموعة | الاختبارات | يتحقق من |
|----------|----------:|----------|
| **FStCompilerTest** | 101 | مفردات ST الكاملة |
| **FStLibraryTest** | 8 | جميع الكتل القياسية الـ 132 (FBs + FCs) |
| **FCodeGeneratorThreadingTest** | 8 | جدولة المهام المتعددة + المزامنة بدون أقفال |
| **الإجمالي** | **117** | **0 أخطاء** |

---

## 1. مفردات ST (FStCompilerTest)

101 اختبار يتحقق من كل بنية لغوية مدعومة في IEC 61131-3 Structured Text.
كل اختبار يجمّع جزءًا من كود ST عبر FStCompiler ويتحقق من كود C++ المُولَّد.

### 1.1 التعيينات

| الاختبار | كود ST | يتحقق من |
|----------|--------|----------|
| `assignSimple` | `a := 42;` | تعيين بسيط |
| `assignExpression` | `a := b + 1;` | تعيين بتعبير |
| `assignExternal` | `ExtVar := 10;` | وصول VAR_EXTERNAL |
| `assignGvlQualified` | `GVL.ExtVar := 5;` | مسار GVL مؤهل |

### 1.2 العوامل الحسابية

| الاختبار | كود ST | عامل C |
|----------|--------|--------|
| `arithmeticAdd` | `a := b + 1;` | `+` |
| `arithmeticSub` | `a := b - 1;` | `-` |
| `arithmeticMul` | `a := b * 2;` | `*` |
| `arithmeticDiv` | `a := b / 2;` | `/` |
| `arithmeticMod` | `a := b MOD 3;` | `%` |
| `arithmeticPower` | `c := x ** 2.0;` | `EXPT()` |
| `arithmeticNegate` | `a := -b;` | `-(...)` |
| `arithmeticParentheses` | `a := (b + 1) * 2;` | الأقواس |

### 1.3 عوامل المقارنة

| الاختبار | كود ST | عامل C |
|----------|--------|--------|
| `compareEqual` | `flag := a = b;` | `==` |
| `compareNotEqual` | `flag := a <> b;` | `!=` |
| `compareLess` | `flag := a < b;` | `<` |
| `compareGreater` | `flag := a > b;` | `>` |
| `compareLessEqual` | `flag := a <= b;` | `<=` |
| `compareGreaterEqual` | `flag := a >= b;` | `>=` |

### 1.4 العوامل المنطقية

| الاختبار | كود ST | عامل C |
|----------|--------|--------|
| `boolAnd` | `flag := flag AND flag;` | `&&` |
| `boolOr` | `flag := flag OR flag;` | `\|\|` |
| `boolXor` | `flag := flag XOR flag;` | `^` |
| `boolNot` | `flag := NOT flag;` | `!` |

### 1.5 القيم الحرفية

| الاختبار | كود ST | يتحقق من |
|----------|--------|----------|
| `literalInteger` | `a := 12345;` | عدد صحيح |
| `literalReal` | `c := 3.14;` | فاصلة عائمة |
| `literalBoolTrue` | `flag := TRUE;` | قيمة منطقية |
| `literalBoolFalse` | `flag := FALSE;` | قيمة منطقية |
| `literalString` | `text := 'hello';` | سلسلة نصية |
| `literalTime` | `counter := T#500ms;` | ثابت زمني |

### 1.6 هياكل التحكم

**IF / ELSIF / ELSE / END_IF**

| الاختبار | يتحقق من |
|----------|----------|
| `ifSimple` | شرط بسيط |
| `ifElse` | تفرع If-Else |
| `ifElsif` | تفرع متعدد مع ELSIF |
| `ifNested` | كتل IF متداخلة |

**FOR / WHILE / REPEAT**

| الاختبار | يتحقق من |
|----------|----------|
| `forSimple` | FOR idx := 0 TO 10 DO |
| `forWithBy` | FOR مع خطوة BY |
| `whileLoop` | حلقة WHILE |
| `repeatUntil` | حلقة REPEAT/UNTIL |

**CASE**

| الاختبار | يتحقق من |
|----------|----------|
| `caseStatement` | CASE/OF مع عدة تسميات + switch/case/break |

**RETURN / EXIT**

| الاختبار | يتحقق من |
|----------|----------|
| `returnStatement` | RETURN → goto __end |
| `exitStatement` | EXIT داخل FOR → break |

### 1.7 الكتل الوظيفية (استدعاءات FB)

| الاختبار | يتحقق من |
|----------|----------|
| `fbCallWithInputs` | `MyTon(IN := flag, PT := T#500ms);` |
| `fbCallWithOutputAssign` | `MyTimer(IN := flag, Q => flag);` — تعيين OUT => |

### 1.8 الوصول إلى المصفوفات

| الاختبار | يتحقق من |
|----------|----------|
| `arrayReadSubscript` | `a := arr[3];` |
| `arrayWriteSubscript` | `arr[5] := 42;` |
| `arrayComputedIndex` | `a := arr[idx + 1];` |
| `arrayInForLoop` | وصول مصفوفة في حلقة FOR |

### 1.9 تحويلات الأنواع

يتعرف المترجم على نمط `XXX_TO_YYY` ويولّد
تحويلات بأسلوب C (`(TYPE)value`)، وفقًا لمعيار IEC.

| الاختبار | كود ST | يولّد |
|----------|--------|-------|
| `typeConvIntToReal` | `INT_TO_REAL(a)` | `(REAL)a` |
| `convRealToInt` | `REAL_TO_INT(c)` | `(INT)c` |
| `convBoolToInt` | `BOOL_TO_INT(flag)` | `(INT)flag` |
| `convIntToBool` | `INT_TO_BOOL(a)` | `(BOOL)a` |
| `convDintToReal` | `DINT_TO_REAL(counter)` | `(REAL)counter` |
| `convIntToDint` | `INT_TO_DINT(a)` | `(DINT)a` |

### 1.10 الوصول إلى أعضاء الهيكل

| الاختبار | يتحقق من |
|----------|----------|
| `structMemberAccess` | `pos.x := 42;` → `data__->pos.value.x` |

### 1.11 متغيرات عبر المهام (متعددة المهام)

| الاختبار | يتحقق من |
|----------|----------|
| `crossPrimitiveGet` | `__GET_EXTERNAL_ATOMIC` للقراءة بدون أقفال |
| `crossPrimitiveSet` | `__SET_EXTERNAL_ATOMIC` للكتابة بدون أقفال |
| `crossStructuredGet` | `__snap_` وصول لقطة محلية للخيط |
| `crossStructuredMemberAccess` | `__snap_Struct.field` وصول |

### 1.12 الكتل الوظيفية القياسية

يتم إنشاء نسخة من كل FB قياسي واستدعاؤها:

| الاختبار | نوع FB | يتحقق من |
|----------|--------|----------|
| `fbTon` | TON | تأخير التشغيل |
| `fbTof` | TOF | تأخير الإيقاف |
| `fbTp` | TP | مؤقت نبضي |
| `fbCtu` | CTU | عداد تصاعدي |
| `fbCtd` | CTD | عداد تنازلي |
| `fbRtrig` | R_TRIG | حافة صاعدة |
| `fbFtrig` | F_TRIG | حافة هابطة |
| `fbRs` | RS | إعادة تعيين مهيمنة |
| `fbSr` | SR | ضبط مهيمن |

### 1.13 الدوال القياسية

| الفئة | الاختبارات | الدوال |
|-------|----------:|--------|
| الرياضيات | 12 | ABS, SQRT, SIN, COS, TAN, ASIN, ACOS, ATAN, EXP, LN, LOG, TRUNC |
| الاختيار | 4 | SEL, LIMIT, MIN, MAX |
| السلاسل النصية | 6 | LEN, LEFT, RIGHT, MID, CONCAT, FIND |
| إزاحة البتات | 4 | SHL, SHR, ROL, ROR |
| تحويل الأنواع | 6 | INT_TO_REAL, REAL_TO_INT, BOOL_TO_INT, ... |

### 1.14 الحالات الحدية

| الاختبار | يتحقق من |
|----------|----------|
| `complexNestedExpression` | تعبيرات متداخلة |
| `multipleStatementsOnSeparateLines` | برامج متعددة الأسطر |
| `emptyBody` | جسم POU فارغ |
| `commentOnlyBody` | تعليقات فقط |
| `caseInsensitiveKeywords` | IF/if/If |
| `caseInsensitiveVariables` | حساسية الأحرف الكبيرة/الصغيرة |

---

## 2. المكتبة القياسية (FStLibraryTest)

8 اختبارات مبنية على البيانات تتحقق من **جميع الكتل الـ 132** في
المكتبة القياسية (`standard_library.sql`) تلقائيًا.

### 2.1 الكتل الوظيفية (13 FB)

| الاختبار | يتحقق من |
|----------|----------|
| `fbSingleInstance` | كل FB قابل للإنشاء والاستدعاء بشكل فردي |
| `fbDoubleInstance` | نسختان من نفس نوع FB في وقت واحد |
| `fbOutputRead` | جميع المخرجات قابلة للقراءة بعد الاستدعاء |

**الكتل الوظيفية المغطاة:** SR, RS, R_TRIG, F_TRIG, CTU, CTD, CTUD, TON, TOF, TP,
RTC, SEMA, RampGen

### 2.2 الدوال (119 FC)

| الاختبار | يتحقق من |
|----------|----------|
| `fcCall` | كل FC قابلة للاستدعاء مع المعاملات الصحيحة (104 تم اختبارها) |
| `fcInExpression` | قيمة إرجاع FC قابلة للاستخدام في التعبيرات |

**الفئات المغطاة:**

- **الحساب:** ADD, SUB, MUL, DIV, MOD, EXPT, ABS
- **المقارنة:** EQ, NE, LT, GT, LE, GE
- **حساب المثلثات:** SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2
- **اللوغاريتمات:** EXP, LN, LOG, SQRT
- **الاختيار:** SEL, MUX, LIMIT, MIN, MAX, MOVE, CLAMP
- **السلاسل النصية:** LEN, LEFT, RIGHT, MID, CONCAT, INSERT, DELETE, REPLACE, FIND
- **إزاحة البتات:** SHL, SHR, ROL, ROR
- **تحويل الأنواع:** 60+ دالة تحويل (BOOL_TO_INT, INT_TO_REAL, ...)
- **إضافات ForgeIEC:** LERP, MAP_RANGE, HYPOT, DEG, RAD, IK_2Link,
  CABS, CADD, CMUL, CSUB, CARG, CCONJ, CPOLAR, CRECT

---

## 3. المهام المتعددة (FCodeGeneratorThreadingTest)

8 اختبارات تتحقق من نظام جدولة المهام المتعددة الكامل وفقًا
لمواصفات التصميم (MT-spec, docs/design/multi-task-scheduler.md).

| الاختبار | يتحقق من |
|----------|----------|
| `singleProgramDefaultTask` | برنامج واحد بدون مهمة صريحة → تركيب DefaultTask، بدون خيوط |
| `twoProgramsTwoTasks` | مهمتان → RESOURCE0_start__، Legacy-Shim config_run__، كلا خيطي المهمة |
| `crossPrimitiveAtomicEmission` | متغير INT مشترك → تخزين Location بـ `std::atomic<>`، `__GET_EXTERNAL_ATOMIC` في الجسم |
| `crossStructuredDoubleBuffer` | STRUCT مشترك → `__DBUF_[2]` + `thread_local __snap_` + نسخ Double-Buffer دخول/خروج |
| `localVarNoSync` | متغير في مهمة واحدة فقط → `__SET_EXTERNAL` عادي، بدون Atomic |
| `conflictTwoWriters` | مهمتان تكتبان نفس المتغير → تحذير ترجمة |
| `singleProgramDefaultTask` | التوافق مع الإصدارات السابقة: المشاريع الحالية تعمل بدون تغيير |

### بنية المهام المتعددة

```
Primary Task (Task 0)          Secondary Tasks (1..N)
    |                               |
    | config_run__()                | RESOURCE0_task_thread__()
    |   ├─ sync_in                  |   ├─ dbuf_rd (copy-in)
    |   ├─ TASK0_body__()           |   ├─ TASKn_body__()
    |   └─ sync_out                 |   └─ dbuf_wr (copy-out)
    |                               |
    | [تحت bufferLock]              | [lock-free]
```

**آليات المزامنة:**
- **CrossPrimitive** (BOOL, INT, REAL, ...): `std::atomic<T>` على متغير الموقع، `__GET_EXTERNAL_ATOMIC` / `__SET_EXTERNAL_ATOMIC` في كود الجسم
- **CrossStructured** (STRUCT, ARRAY, STRING): Double-Buffer `__DBUF_[2]` مع مؤشر كتابة ذري، لقطات `thread_local` `__snap_` لاتساق المجموعة

---

## ضمان الجودة

### التحقق الآلي

تُنفَّذ الاختبارات مع كل بناء باستخدام `-DBUILD_TESTS=ON`.
التكامل مع خط أنابيب CI (Forgejo Actions) جاهز.

### الاختبارات المبنية على البيانات

تقرأ اختبارات المكتبة (`FStLibraryTest`) تعريفات الكتل
مباشرة من `standard_library.sql`. عند إضافة كتل جديدة،
يتم اختبارها تلقائيًا — لا حاجة لإنشاء حالات اختبار يدويًا.

### الاكتمال

تغطي مجموعة الاختبارات مفردات IEC 61131-3 Structured Text الكاملة
كما يدعمها ForgeIEC:

- جميع العوامل (حسابية، مقارنة، منطقية، إزاحة بتات)
- جميع هياكل التحكم (IF, FOR, WHILE, REPEAT, CASE)
- جميع أنواع القيم الحرفية (Integer, Real, Bool, String, Time)
- جميع الكتل الوظيفية والدوال القياسية (132 كتلة)
- الوصول إلى المصفوفات والهياكل
- متغيرات GVL المؤهلة
- المزامنة عبر المهام (Atomics + Double-Buffer)
- تحويلات الأنواع (توليد تحويلات C)
