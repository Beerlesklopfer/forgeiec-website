---
title: "ForgeIEC"
---

<div style="text-align:center; padding: 3rem 1rem;">

# مصنوع للصناعة.

**بيئة تطوير IEC 61131-3 بجودة صناعية. مفتوح المصدر.**

[اتصل بنا](mailto:blacksmith@forgeiec.io)

</div>

---

## ما الذي نبنيه

ForgeIEC هي بيئة تطوير IEC 61131-3 كاملة للأتمتة الصناعية —
خمس لغات IEC، أنظمة حافلات صناعية، تصحيح أخطاء في الوقت الفعلي.

تم تطويرها بطموح منافسة الأنظمة التجارية الراسخة على قدم المساواة.
كل ميزة مدعومة باختبارات موثقة قبل الإصدار.

---

## لماذا المصدر المفتوح

الأتمتة الصناعية تقنية أساسية. لكن الوصول إلى الأدوات المهنية
مقيد بتكاليف الترخيص والأنظمة المملوكة. ForgeIEC يجعل قيمة
الأتمتة في متناول الجميع — بدون تقييد من المورد، بدون رسوم ترخيص.

كمشروع مفتوح المصدر، ForgeIEC ملك للمجتمع.

---

## البدء

```bash
# إضافة مفتاح التوقيع (مرة واحدة)
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# إضافة مصدر المستودع
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

# تثبيت المحرر وبيئة التشغيل
sudo apt update
sudo apt install forgeiec-studio forgeiec-anvil-server
```

المثال لـ Debian 13 (trixie). في Debian 12 (bookworm) أو Ubuntu 24.04 (noble) استبدل كلا الموضعين لـ `trixie`. جميع التوزيعات وRPM والحزم الأخرى: [التنزيل](/download/).

---

<div style="text-align:center; padding: 2rem;">

**سننشر معلومات تفصيلية عندما يكون إصدار بجودة صناعية جاهزاً.**

blacksmith@forgeiec.io

</div>
