---
title: "محرر Structured Text"
summary: "محرر ST + أساسيات اللغة: عبارات IEC 61131-3، الوصول البتي، المراجع المؤهلة للمجمّع"
---

## نظرة عامة

**Structured Text (ST)** هي لغة عالية المستوى شبيهة بـ Pascal من
IEC 61131-3 والمحرر الافتراضي لـ POUs من نوع PROGRAM وFUNCTION_BLOCK
وFUNCTION في ForgeIEC. المحرر هو تركيبة قائمة على `QWidget`
من جدول متغيرات ومنطقة كود، مرتبطين عبر مقسّم رأسي.

```
+----------------------------------------+
| Variable table                         |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT/VAR_INST)    |
+========================================+  <- QSplitter (vertical)
| Code area                              |  <- FStCodeEdit
| (Tree-sitter highlighting + folding +  |
|  Ctrl-Space completion)                |
+----------------------------------------+
```

## تخطيط المحرر

| المنطقة | المحتوى |
|---|---|
| **جدول المتغيرات** (أعلى) | الإعلانات بأعمدة الاسم، النوع، القيمة الأولية، العنوان، التعليق. التحريرات تتزامن حية في كتلة `VAR ... END_VAR` للكود. |
| **منطقة الكود** (أسفل) | مصدر ST بين أقسام المتغيرات. طي السطور مدفوع بشجرة AST لـ tree-sitter، أرقام السطور، إبراز سطر المؤشر. |
| **شريط البحث** (Ctrl-F / Ctrl-H) | يُعرض فوق منطقة الكود، مع وضع الاستبدال للبحث والاستبدال. |

يتذكر المقسّم موضعه لكل POU في حالة التخطيط.

## إبراز بناء الجملة بـ Tree-sitter

بدلاً من `QSyntaxHighlighter` قائم على التعابير النمطية، يحلل ForgeIEC
مصدر ST بـ **Tree-sitter** إلى AST ويلوّن عبر استعلامات الالتقاط:

  - **الكلمات المفتاحية** (`IF`، `THEN`، `FOR`، `FUNCTION_BLOCK`، ...): أرجواني
  - **أنواع البيانات** (`BOOL`، `INT`، `REAL`، `TIME`، ...): سماوي
  - **النصوص + حرفيات الزمن** (`'abc'`، `T#20ms`): أخضر
  - **التعليقات** (`(* ... *)`، `// ...`): رمادي، مائل
  - **PUBLISH / SUBSCRIBE**: كلمات Anvil المفتاحية الممتدة، نمط مخصص

الفائدة: يبقى الإبراز صحيحاً في البنى المعقدة (التعليقات المتداخلة،
حرفيات الزمن، المراجع المؤهلة)، ونفس AST يقود النطاقات القابلة للطي
لطي الكود.

## إكمال الكود (Ctrl-Space)

الضغط على **Ctrl-Space** أو كتابة حرفين متطابقين يفتح نافذة الإكمال
المنبثقة. يعرف المكمّل:

  - **الكلمات المفتاحية لـ IEC** (`IF`، `CASE`، `FOR`، `WHILE`، `RETURN`، ...)
  - **أنواع البيانات** (`BOOL`، `INT`، `DINT`، `REAL`، `STRING`، `TIME`، ...)
  - **المتغيرات المحلية** لـ POU الحالي
  - **أسماء POU** في المشروع (PROGRAM، FUNCTION_BLOCK، FUNCTION)
  - **كتل المكتبة** (`TON`، `R_TRIG`، `JK_FF`، `DEBOUNCE`، ...)
  - **الوظائف القياسية** (`ABS`، `SQRT`، `LIMIT`، `LEN`، ...)

التغييرات في مجمّع المتغيرات (إشارة `poolChanged`) تنتشر في نموذج
الإكمال بتأخير 100 ms — تصبح مدخلات المجمّع الجديدة متاحة فوراً
تقريباً، دون أن تطلق كل ضغطة مفتاح إعادة فحص كامل.

## أساسيات اللغة (IEC 61131-3)

### العبارات

| العبارة | الصيغة |
|---|---|
| **التعيين** | `var := expression;` |
| **IF / ELSIF / ELSE** | `IF cond THEN ... ELSIF cond THEN ... ELSE ... END_IF;` |
| **CASE** | `CASE x OF 1: ... ; 2,3: ... ; ELSE ... END_CASE;` |
| **FOR** | `FOR i := 1 TO 10 BY 1 DO ... END_FOR;` |
| **WHILE** | `WHILE cond DO ... END_WHILE;` |
| **REPEAT** | `REPEAT ... UNTIL cond END_REPEAT;` |
| **EXIT / RETURN** | الخروج من الحلقة / مغادرة POU |

### التعابير

العوامل القياسية بأسبقية IEC: `**`، أحادي `+/-/NOT`، `* / MOD`،
`+ -`، المقارنات، `AND / &`، `XOR`، `OR`. الأقواس كما في Pascal.
لا يُسمح بالتحويلات العددية الضمنية — يجب استدعاء `INT_TO_DINT`،
`REAL_TO_INT` إلخ صراحة.

### الوصول البتي على أنواع ANY_BIT

`var.<bit>` يستخرج أو يضبط بتاً واحداً، مباشرة على متغيرات
`BYTE`/`WORD`/`DWORD`/`LWORD`:

```text
status.0 := TRUE;             (* set bit 0 *)
alarm := flags.7 OR flags.3;  (* read bits *)
```

يترجم المترجم هذا إلى تقنيع بتي نظيف مع `AND`/`OR`/الإزاحة،
بدون متغيرات مساعدة.

### المراجع المؤهلة بثلاثة مستويات

`<Category>.<Group>.<Variable>` يصل إلى مدخلات المجمّع مباشرة، دون
الحاجة لإعلان GVLs صراحة:

| البادئة | المصدر |
|---|---|
| `Anvil.X.Y`   | مدخل مجمّع بـ `anvilGroup="X"` |
| `Bellows.X.Y` | مدخل مجمّع بـ `hmiGroup="X"` |
| `GVL.X.Y`     | مدخل مجمّع بـ `gvlNamespace="X"` |
| `HMI.X.Y`     | مرادف لـ `Bellows.X.Y` |

`Anvil.X.Y` و`Bellows.X.Y` يمكن أن يشيرا بشكل مستقل إلى مدخلات
مجمّع مختلفة — يصدر المترجم رموز C منفصلة بمجرد اختلاف عناوين IEC.

### المتغيرات الموضّعة (`AT %...`)

تربط المتغيرات الموضّعة الإعلان بعنوان IEC:

```text
button_raw    AT %IX0.0  : BOOL;
motor_speed   AT %QW1    : INT;
flag_persist  AT %MX10.3 : BOOL;
```

العنوان هو المفتاح الأساسي في المجمّع — انظر
[تنسيق ملف المشروع](../file-format/).

## أمثلة على الكود

### مثال 1 — استدعاء TON بكتلة مكتبة

```text
PROGRAM PLC_PRG
VAR
    start_button   AT %IX0.0  : BOOL;
    motor_run      AT %QX0.0  : BOOL;
    fbDelay        : TON;
END_VAR

fbDelay(IN := start_button, PT := T#3s);
motor_run := fbDelay.Q;
END_PROGRAM
```

`fbDelay` نسخة من FB المكتبة `TON`. بعد 3 ثوانٍ من الضغط
على `start_button`، يتحول `motor_run` إلى TRUE.

### مثال 2 — قراءة Bellows تقود إخراجاً

```text
PROGRAM Lampen
VAR
    relay_lamp  AT %QX0.1 : BOOL;
END_VAR

(* HMI panel can write Bellows.Pfirsich.T_1 *)
relay_lamp := Bellows.Pfirsich.T_1 OR Anvil.Sensors.contact_door;
END_PROGRAM
```

`Bellows.Pfirsich.T_1` و `Anvil.Sensors.contact_door` هي مراجع
بثلاثة مستويات يحلها المترجم دون إعلان GVL — بشرط أن تبقى
كلا العلامتين في مجمّع العناوين وأن يكون تصدير HMI للمجموعة
`Pfirsich` نشطاً.

## مواضيع ذات صلة

- [المكتبة](../library/) — كتل الوظائف + الوظائف المتاحة
- [Instruction List](../il/) — محرر نص بديل (قائم على المراكم)
- [تنسيق ملف المشروع](../file-format/) — كيف يُحفظ كود ST في `.forge`
