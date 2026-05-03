---
title: "المساعدة"
summary: "وثائق وموارد ForgeIEC"
---

## المساعدة والموارد

مرحباً بكم في قسم المساعدة في ForgeIEC. ستجدون هنا معلومات
حول أساسيات مشروعنا وفلسفتنا.

---

## المواضيع

### [المساعدة عبر الإنترنت](/help/online/)

نقطة الدخول للمساعدة السياقية للمحرر. يفتح F1 في المحرر بالضبط الصفحة
المقابلة على هذا الموقع. مخطط الـ URL ومعرفات الموضوعات موصوفة هناك.

### [تكوين الباص](/help/bus-config/)

مخطط PLCopen XML لتكوين الباص الميداني الصناعي في مشاريع `.forge`.
المقاطع والأجهزة وربط المتغيرات وتعيين عناوين IEC.

### [تغطية الاختبارات](/help/tests/)

117 اختبارا آليا يتحقق من مجموعة ميزات لغة IEC 61131-3 الكاملة
وجميع كتل المكتبة القياسية البالغ عددها 132 ونظام تعدد المهام.

### [فلسفة المصدر المفتوح](/help/open-source/)

الفكرة وراء المصدر المفتوح تتجاوز البرمجيات بكثير — إنها حركة
تحرر المعرفة وتُديمقرط الابتكار.

---

## البداية

يتكون ForgeIEC من مكونين:

1. **محرر ForgeIEC** (`forgeiec`) — بيئة التطوير على محطة العمل
2. **خادم ForgeIEC** (`anvild`) — نظام التشغيل على PLC الهدف

### التثبيت من مستودع ForgeIEC APT

يتم توفير ForgeIEC كمستودع Debian موقّع على
`apt.forgeiec.io`. يتم الإعداد مرة واحدة فقط على كل
محطة عمل أو PLC هدف:

```bash
# استيراد مفتاح التوقيع
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# إضافة مصدر المستودع
# (Debian 12 "bookworm" أو Debian 13 "trixie" — حسب نظامك)
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

sudo apt update
```

ثم قم بتثبيت أي حزمة ForgeIEC باستخدام مدير الحزم القياسي:

```bash
# المحرر (محطة العمل)
sudo apt install forgeiec

# الخادم (PLC الهدف)
sudo apt install anvild
```

تتبع التحديثات دورة `apt update && apt upgrade` العادية —
لا حاجة لملفات `.deb` يدوية.

### المنصات المدعومة

| المكون  | المعماريات    | إصدارات Debian   |
|---------|---------------|------------------|
| المحرر  | amd64, arm64  | bookworm, trixie |
| الخادم  | amd64, arm64  | bookworm, trixie |
| Bridges | amd64, arm64  | bookworm, trixie |
| Hearth  | amd64, arm64  | bookworm, trixie |

### اتصل بنا

للاستفسارات: blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**الوثائق تنمو مع المشروع.**

blacksmith@forgeiec.io

</div>
