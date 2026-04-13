---
title: "تكوين الباص"
summary: "مخطط PLCopen XML لتكوين الباص الميداني الصناعي"
---

## مساحة الاسم

```
https://forgeiec.io/v2/bus-config
```

يصف هذا المخطط امتداد ForgeIEC لتنسيق PLCopen XML
لتخزين تكوين الباص الميداني داخل ملفات مشروع `.forge`.
يستخدم آلية `<addData>` المتوافقة مع معيار PLCopen TC6.

## نظرة عامة

يحدد تكوين الباص الطوبولوجيا الفيزيائية للمنشأة:
تحتوي **المقاطع** (شبكات الباص الميداني) على **أجهزة**،
وكل جهاز مرتبط بمتغيرات المدخلات/المخرجات في المشروع
عبر ربط الباص.

```
مشروع .forge
  +-- المقاطع (شبكات الباص الميداني)
  |     +-- الأجهزة
  |           +-- المتغيرات (عبر ربط الباص في مجمع العناوين)
  +-- مجمع العناوين (FAddressPool)
        +-- متغير: DI_1, %IX0.0, busBinding -> Maibeere
        +-- متغير: DO_1, %QX0.0, busBinding -> Maibeere
```

## هيكل XML

يتم تخزين تكوين الباص كـ `<addData>` على مستوى المشروع:

```xml
<project>
  <!-- محتوى PLCopen القياسي -->
  <types>...</types>
  <instances>...</instances>

  <!-- تكوين باص ForgeIEC -->
  <addData>
    <data name="https://forgeiec.io/v2/bus-config"
          handleUnknown="discard">
      <fi:busConfig xmlns:fi="https://forgeiec.io/v2">

        <fi:segment id="a3f7c2e1-..."
                    protocol="modbustcp"
                    name="باص ميداني صالة 1"
                    enabled="true"
                    interface="eth0"
                    bindAddress="192.168.24.100/24"
                    gateway=""
                    pollIntervalMs="0">

          <fi:device hostname="Maibeere"
                     ipAddress="192.168.24.25"
                     port="502"
                     slaveId="1"
                     anvilGroup="Maibeere"/>

          <fi:device hostname="Stachelbeere"
                     ipAddress="192.168.24.26"
                     port="502"
                     slaveId="1"
                     anvilGroup="Stachelbeere"/>

        </fi:segment>

      </fi:busConfig>
    </data>
  </addData>
</project>
```

## العناصر

### `fi:busConfig`

العنصر الجذر. يحتوي على عنصر `fi:segment` واحد أو أكثر.

| الخاصية | مطلوب | الوصف |
|---------|-------|-------|
| `xmlns:fi` | نعم | مساحة الاسم: `https://forgeiec.io/v2` |

### `fi:segment`

مقطع باص ميداني (شبكة فيزيائية).

| الخاصية | مطلوب | النوع | الوصف |
|---------|-------|-------|-------|
| `id` | نعم | UUID | معرف المقطع الفريد |
| `protocol` | نعم | String | البروتوكول: `modbustcp`، `modbusrtu`، `ethercat`، `profibus` |
| `name` | نعم | String | اسم العرض (حر) |
| `enabled` | لا | Bool | المقطع نشط (`true`) أو معطل (`false`). الافتراضي: `true` |
| `interface` | لا | String | واجهة الشبكة (مثل `eth0`، `/dev/ttyUSB0`) |
| `bindAddress` | لا | String | IP/CIDR للواجهة (مثل `192.168.24.100/24`) |
| `gateway` | لا | String | عنوان البوابة (فارغ = بدون بوابة) |
| `pollIntervalMs` | لا | Int | فترة الاستقصاء بالميلي ثانية (`0` = بأسرع ما يمكن) |

### `fi:device`

جهاز داخل مقطع.

| الخاصية | مطلوب | النوع | الوصف |
|---------|-------|-------|-------|
| `hostname` | نعم | String | اسم الجهاز (يستخدم كمعرف) |
| `ipAddress` | لا | String | عنوان IP (Modbus TCP) |
| `port` | لا | Int | منفذ TCP (الافتراضي: `502`) |
| `slaveId` | لا | Int | معرف العبد Modbus |
| `anvilGroup` | لا | String | مجموعة Anvil IPC للنقل بدون نسخ |

## ربط المتغير بالجهاز

لا يتم إدراج متغيرات المدخلات/المخرجات **داخل** عنصر `fi:device`.
بدلاً من ذلك، يحمل كل متغير في مجمع العناوين خاصية `busBinding`
تشير إلى `hostname` الجهاز:

```
FLocatedVariable
  name: "DI_1"
  address: "%IX0.0"
  anvilGroup: "Maibeere"
  busBinding:
    deviceId: "Maibeere"
    modbusAddress: 0
    count: 1
```

## تعيين عناوين IEC

يتم اشتقاق عنوان IEC للمتغير المرتبط من الطوبولوجيا الفيزيائية:

```
قاعدة المقطع + إزاحة الجهاز + موضع السجل
```

| نطاق العناوين | المعنى | المصدر |
|---------------|--------|--------|
| `%IX` / `%IW` / `%ID` | مدخل فيزيائي | ربط الباص |
| `%QX` / `%QW` / `%QD` | مخرج فيزيائي | ربط الباص |
| `%MX` / `%MW` / `%MD` | علامة (بدون مدخلات/مخرجات فيزيائية) | مخصص المجمع |

## البروتوكولات المدعومة

| البروتوكول | قيمة `protocol` | الوسط | عفريت الجسر |
|-----------|----------------|-------|-------------|
| Modbus TCP | `modbustcp` | إيثرنت | `tongs-modbustcp` |
| Modbus RTU | `modbusrtu` | RS-485 (تسلسلي) | `tongs-modbusrtu` |
| EtherCAT | `ethercat` | إيثرنت (الوقت الحقيقي) | `tongs-ethercat` |
| Profibus DP | `profibus` | تسلسلي (باص ميداني) | `tongs-profibus` |

## التوافق

تضمن خاصية `handleUnknown="discard"` أن أدوات PLCopen
التي لا تعرف ForgeIEC يمكنها تجاهل تكوين الباص بأمان
دون توليد أخطاء. وبالعكس، يقرأ ForgeIEC كتل `<addData>`
غير المعروفة من موردين آخرين ويحافظ عليها عند الحفظ.

---

<div style="text-align:center; padding: 2rem;">

**تكوين باص ForgeIEC — يعمل بدون اتصال، متوافق مع PLCopen، بدون تكرار.**

blacksmith@forgeiec.io

</div>
