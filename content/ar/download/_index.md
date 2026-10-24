---
title: "التنزيل"
summary: "جميع مكونات ForgeIEC — مستودعات APT وRPM، والتنزيلات المباشرة، والشيفرة المصدرية"
---

## مكونات ForgeIEC في لمحة

يتكون ForgeIEC من عدة مكونات، وتتوقف المكونات التي تحتاجها على دورك:

| الدور | المكوّن | مكان التثبيت |
|---|---|---|
| **مبرمج / مستخدم PLC** | `forgeiec-studio` | محطة العمل |
| **مهندس التشغيل والإعداد** | `forgeiec-anvil-server` (يتضمن `anvild`) | وحدة PLC المستهدفة |
| **جسر HMI / OPC-UA** | `forgeiec-bellows-server` (يتضمن `bellowsd`) | وحدة PLC المستهدفة أو مضيف منفصل |
| **Modbus TCP** | مضمَّن في `forgeiec-anvil-server` | وحدة PLC المستهدفة |
| **Profibus / EtherCAT / EthernetIP** | مضمَّن كذلك في `forgeiec-anvil-server` | وحدة PLC المستهدفة |
| **لوحة المشغّل** | `forgeiec-screen-wayland` أو `-xorg` | عتاد اللوحة |

---

## التثبيت من مستودع الحزم

يُوفَّر ForgeIEC كمستودع Debian موقَّع على `apt.forgeiec.io` وكمستودع
RPM موقَّع على `rpm.forgeiec.io`. يتم الإعداد مرة واحدة لكل محطة عمل
أو وحدة PLC مستهدفة — اختر توزيعتك:

{{< distro-install >}}

ثم ثبّت المكونات كلًّا على حدة:

```bash
# محطة العمل
sudo apt install forgeiec-studio          # ForgeIEC Studio
sudo apt install forgeiec-fdd-data        # أوصاف الأجهزة (موصى به)

# وحدة PLC المستهدفة
sudo apt install forgeiec-anvil-server    # بيئة تشغيل PLC (anvild + جميع tongs-*)
sudo apt install forgeiec-bellows-server  # بوابة HMI (bellowsd)

# لوحة المشغّل
sudo apt install forgeiec-screen-wayland  # وضع الكشك على Wayland
sudo apt install forgeiec-screen-xorg     # وضع الكشك على X11
```

على أنظمة RPM تصبح الأوامر `sudo dnf install …` مع أسماء الحزم نفسها.

جسور الناقل (`tongs-modbustcp` و`tongs-ethercat` و`tongs-profibus`
و`tongs-ethernetip`) **ليست** حزمًا منفصلة — فهي موجودة داخل
`forgeiec-anvil-server` ويشغّلها `anvild`.

تتبع التحديثات دورة `apt update && apt upgrade` المعتادة —
دون الحاجة إلى ملفات `.deb` يدوية.

---

## المنصات المدعومة

### Debian / Ubuntu (`apt.forgeiec.io`)

| الحزمة | المعماريات | الإصدارات (Suites) |
|---|---|---|
| `forgeiec-studio` | amd64, arm64 | bookworm, trixie, noble |
| `forgeiec-fdd-data` | مستقلة عن المعمارية | bookworm, trixie, noble |
| `forgeiec-anvil-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-bellows-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-screen-wayland` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `forgeiec-screen-xorg` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `hearth-server` | amd64, arm64 | bookworm, trixie, jammy, noble |

مطابقة الإصدارات: `bullseye` = Debian 11، `bookworm` = Debian 12،
`trixie` = Debian 13، `jammy` = Ubuntu 22.04، `noble` = Ubuntu 24.04.

### Enterprise Linux / Fedora (`rpm.forgeiec.io`)

| الحزمة | المعمارية | التوزيعات |
|---|---|---|
| `forgeiec-screen-wayland` | x86_64 | AlmaLinux 9 (`el9`)، Fedora 44 |
| `forgeiec-screen-xorg` | x86_64 | AlmaLinux 9 (`el9`)، Fedora 44 |

توزيع RPM جديد ويغطي حاليًا لوحة المشغّل فقط. سيتبعه ForgeIEC Studio
وبيئة التشغيل بمجرد استقرار حزم RPM الخاصة بهما.

هناك **مفتاحا توقيع مختلفان**: `forgeiec.gpg` (ed25519) لـ apt
و`forgeiec-rpm.asc` (RSA-4096) لـ rpm. والفرق ليس شكليًا — إذ يأتي
RHEL 9 مع `rpm` 4.16 الذي لا يستطيع محلّل PGP الداخلي فيه التحقق من
ed25519.

غياب arm64 عن جانب RPM مقصود: مسار الترجمة المتقاطعة في CI يعتمد على
حزم Debian غير موجودة في Enterprise Linux.

**إصدار Windows** من ForgeIEC Studio: قيد الإعداد. وحتى ذلك الحين يعمل
Studio أصليًا على Linux أو عبر WSL2 على محطات عمل Windows.

---

## التنزيلات المباشرة (أرشيفات الإصدارات)

إذا لم تستطع أو لم ترغب في استخدام مستودع الحزم — مثلًا لمحطات عمل
معزولة عن الشبكة (air gap) — يمكنك الحصول على إصدارات منفردة من
Forgejo. **المستودعات غير متاحة للتصفح العام**: أرسل إلينا مفتاح SSH
العام الخاص بك على blacksmith@forgeiec.io وسنقوم بتفعيله. بعد ذلك تصبح
المستودعات التالية متاحة لك:

- **الشيفرة المصدرية لـ ForgeIEC Studio**: `ForgeIEC/forgeiec-studio`
- **anvild + الجسور**: `ForgeIEC/anvil`
- **bellowsd**: `ForgeIEC/bellows`
- **الشيفرة المصدرية للموقع**: `ForgeIEC/forgeiec-website`

مع كل إصدار تُرفق حزم `.deb` موقَّعة وأرشيفات المصدر بوسم الإصدار على
Forgejo.

---

## البناء من المصدر

```bash
# استنساخ المستودع (مع الوحدات الفرعية) — عبر SSH فقط، بعد تفعيل
# مفتاح SSH العام الخاص بك
git clone --recurse-submodules ssh://git@git.forgeiec.io/ForgeIEC/forgeiec-studio.git
cd forgeiec-studio

# بناء Studio + جميع الخدمات (daemons)
cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(nproc)

# النشر على النظام المحلي
./deploy.sh all
```

المتطلبات المسبقة:

- Debian 12/13 أو Ubuntu 24.04+
- `build-essential cmake qt6-base-dev qt6-declarative-dev libtomlplusplus-dev`
- Rust 1.85+ (عبر rustup)

---

## مشاريع تجريبية

مشاريع أمثلة مرفقة مع ForgeIEC Studio:

| المشروع | الغرض |
|---|---|
| `knight_rider.forge` | اختبار الأضواء المتتابعة الكلاسيكي لمصابيح LED في Bellows |
| المزيد قادم | … |

تجدها في Studio تحت `File → Open Example`.

---

## الخطوات التالية

- [الخطوات الأولى مع ForgeIEC Studio](/help/)
- [إعداد مساعد الذكاء الاصطناعي](/en/help/ai/) (بالإنجليزية)
- [إعداد الناقل](/help/bus-config/)
- [الأخبار + ملاحظات الإصدار](/en/news/) (بالإنجليزية)
